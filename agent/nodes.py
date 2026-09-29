from typing import Literal
from pydantic import BaseModel, Field
from langchain_google_genai import ChatGoogleGenerativeAI

import config
from .loader import load_units, load_helper
from .prompts import ROUTER_PROMPT, HELPER_PROMPT, UNIT_PROMPT, TOPIC_AND_PYQ_PROMPT, ANSWER_PROMPT
from .state import AgentState

UNITS = load_units()
HELPER_TEXT = load_helper()


def _get_llm():
    return ChatGoogleGenerativeAI(
        model=config.GEMINI_MODEL,
        google_api_key=config.GOOGLE_API_KEY,
        temperature=0.2,
    )


class RouteDecision(BaseModel):
    route: Literal["generic", "specific", "unrelated"] = Field(
        description="Classify as 'generic' for broad DBMS advice/strategies/important topics/timeframes, 'specific' for specific syllabus questions/concepts, or 'unrelated' for non-DBMS queries"
    )


class UnitDecision(BaseModel):
    unit_no: int = Field(description="The unit number (1, 2, 3, 4, 5) that best fits the question, or -1 if none fit")


class TopicAndPyqDecision(BaseModel):
    topic: str = Field(description="The exact topic name as listed in the unit content, or empty string if none")
    pyq_ids: list[str] = Field(default_factory=list, description="List of PYQ IDs (e.g. ['P1', 'P2']) relevant to the question")


def route_question(state: AgentState) -> dict:
    """Classifies the question as generic advice, specific syllabus concept, or unrelated."""
    syllabus_lines = []
    for u_no, u_data in sorted(UNITS.items()):
        syllabus_lines.append(f"Unit {u_no}: {u_data['name']}")
        for t in u_data["topics"]:
            syllabus_lines.append(f"   - {t}")
        syllabus_lines.append("")
    syllabus_text = "\n".join(syllabus_lines)

    prompt = ROUTER_PROMPT.format(syllabus=syllabus_text, question=state["question"])
    llm = _get_llm()
    structured_llm = llm.with_structured_output(RouteDecision)
    decision: RouteDecision = structured_llm.invoke(prompt)

    return {"route": decision.route}


def handle_helper(state: AgentState) -> dict:
    """Answers broad preparation, study strategy, and important topic questions using helper.md."""
    helper_content = load_helper() or HELPER_TEXT
    prompt = HELPER_PROMPT.format(
        helper_content=helper_content,
        question=state["question"],
    )
    llm = _get_llm()
    res = llm.invoke(prompt)
    if isinstance(res.content, str):
        answer = res.content
    elif isinstance(res.content, list):
        text_parts = [
            item if isinstance(item, str) else item.get("text", str(item)) if isinstance(item, dict) else str(item)
            for item in res.content
        ]
        answer = "".join(text_parts)
    else:
        answer = str(res.content)

    return {
        "unit_no": 0,
        "unit_name": "General DBMS Exam Guide & Strategy",
        "topic": "Important Topics & Strategic Preparation",
        "related_pyqs": [],
        "answer": answer,
    }


def identify_unit(state: AgentState) -> dict:
    """Classifies the student question into one of the syllabus units."""
    if not UNITS:
        return {"unit_no": None, "unit_name": None}

    # Format syllabus summary
    syllabus_lines = []
    for u_no, u_data in sorted(UNITS.items()):
        syllabus_lines.append(f"Unit {u_no}: {u_data['name']}")
        for t in u_data["topics"]:
            syllabus_lines.append(f"   - {t}")
        syllabus_lines.append("")
    syllabus_text = "\n".join(syllabus_lines)

    prompt = UNIT_PROMPT.format(syllabus=syllabus_text, question=state["question"])
    llm = _get_llm()
    structured_llm = llm.with_structured_output(UnitDecision)
    decision: UnitDecision = structured_llm.invoke(prompt)

    unit_no = decision.unit_no
    if unit_no in UNITS:
        return {"unit_no": unit_no, "unit_name": UNITS[unit_no]["name"]}
    return {"unit_no": None, "unit_name": None}


def analyze_unit(state: AgentState) -> dict:
    """Picks the matching topic and finds related PYQs from the identified unit."""
    unit_no = state.get("unit_no")
    if unit_no is None or unit_no not in UNITS:
        return {"topic": None, "related_pyqs": []}

    unit_data = UNITS[unit_no]
    pyq_map = {}
    content_lines = [f"Unit {unit_no}: {unit_data['name']}\n"]

    counter = 1
    for topic_name, pyqs in unit_data["topics"].items():
        content_lines.append(f"Topic: {topic_name}")
        if not pyqs:
            content_lines.append("  (No PYQs for this topic)")
        for p in pyqs:
            pid = f"P{counter}"
            pyq_map[pid] = p
            year_str = f" ({p['year']})" if p.get("year") else ""
            content_lines.append(f"  [{pid}] {p['question']}{year_str}")
            counter += 1
        content_lines.append("")

    unit_content = "\n".join(content_lines)
    prompt = TOPIC_AND_PYQ_PROMPT.format(
        unit_no=unit_no,
        unit_name=unit_data["name"],
        unit_content=unit_content,
        question=state["question"],
    )

    llm = _get_llm()
    structured_llm = llm.with_structured_output(TopicAndPyqDecision)
    decision: TopicAndPyqDecision = structured_llm.invoke(prompt)

    # Match topic name (exact or case-insensitive)
    matched_topic = None
    if decision.topic:
        for t in unit_data["topics"]:
            if t.strip().lower() == decision.topic.strip().lower():
                matched_topic = t
                break

    # Collect matched PYQs
    related_pyqs = []
    for pid in decision.pyq_ids:
        clean_id = pid.strip().upper().replace("[", "").replace("]", "")
        if clean_id in pyq_map and pyq_map[clean_id] not in related_pyqs:
            related_pyqs.append(pyq_map[clean_id])

    return {"topic": matched_topic, "related_pyqs": related_pyqs}


def generate_answer(state: AgentState) -> dict:
    """Generates a student-friendly explanation of the concept."""
    prompt = ANSWER_PROMPT.format(
        unit_name=state.get("unit_name", ""),
        topic=state.get("topic", ""),
        question=state["question"],
    )
    llm = _get_llm()
    res = llm.invoke(prompt)
    if isinstance(res.content, str):
        answer = res.content
    elif isinstance(res.content, list):
        text_parts = [
            item if isinstance(item, str) else item.get("text", str(item)) if isinstance(item, dict) else str(item)
            for item in res.content
        ]
        answer = "".join(text_parts)
    else:
        answer = str(res.content)

    return {"answer": answer}


def not_found(state: AgentState) -> dict:
    """Fallback handler when question is not related to DBMS or cannot be matched."""
    return {
        "answer": "This question does not appear to be related to Database Management Systems (DBMS) or the syllabus. Please ask a DBMS-related question!",
        "topic": None,
        "related_pyqs": [],
    }


if __name__ == "__main__":
    # Local self-test. Run from the project root with:
    #     python -m agent.nodes
    print("=== agent/nodes.py self-test ===\n")
    print(f"Loaded {len(UNITS)} units for nodes.")
    for u_no, u in UNITS.items():
        print(f"  - Unit {u_no}: {u['name']} ({len(u['topics'])} topics)")
    print(f"\nLoaded helper.md content length: {len(HELPER_TEXT)} chars.")
    print("\nSUCCESS: agent/nodes.py loaded successfully.")