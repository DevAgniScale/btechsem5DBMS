from langgraph.graph import StateGraph, START, END

from .state import AgentState
from .nodes import identify_unit, analyze_unit, generate_answer, not_found


def _after_unit(state: AgentState) -> str:
    return "analyze_unit" if state.get("unit_no") else "not_found"


def _after_analysis(state: AgentState) -> str:
    return "generate_answer" if state.get("topic") else "not_found"


def build_graph():
    g = StateGraph(AgentState)

    g.add_node("identify_unit", identify_unit)
    g.add_node("analyze_unit", analyze_unit)
    g.add_node("generate_answer", generate_answer)
    g.add_node("not_found", not_found)

    g.add_edge(START, "identify_unit")
    g.add_conditional_edges("identify_unit", _after_unit, ["analyze_unit", "not_found"])
    g.add_conditional_edges("analyze_unit", _after_analysis, ["generate_answer", "not_found"])
    g.add_edge("generate_answer", END)
    g.add_edge("not_found", END)

    return g.compile()


if __name__ == "__main__":
    # Run custom prompt or self-test from terminal:
    #     python -m agent.graph "What is ACID property?"
    #     python -m agent.graph
    import sys
    import asyncio

    # Ensure Windows console supports unicode characters
    if sys.stdout.encoding and sys.stdout.encoding.lower() != "utf-8":
        try:
            sys.stdout.reconfigure(encoding="utf-8", errors="replace")
        except Exception:
            pass

    from config import GOOGLE_API_KEY
    from .nodes import UNITS

    async def _run_prompt(q: str):
        graph = build_graph()
        print(f"\n> Question: {q}\n" + "-" * 50)
        result = await graph.ainvoke({"question": q})
        if result.get("topic"):
            print(f"**Unit {result['unit_no']}: {result['unit_name']}**")
            print(f"**Topic:** {result['topic']}\n")
            print(result["answer"])
            if result.get("related_pyqs"):
                print("\n**Related PYQs on this topic:**")
                for i, p in enumerate(result["related_pyqs"], 1):
                    year = f" ({p['year']})" if p.get("year") else ""
                    print(f"{i}. {p['question']}{year}")
        else:
            print(f"[Not matched] -> {result['answer']}")
        print("-" * 50 + "\n")

    async def _self_test():
        print("=== agent/graph.py test run ===\n")
        
        # If user passed custom prompt via CLI argument
        if len(sys.argv) > 1:
            custom_question = " ".join(sys.argv[1:])
            await _run_prompt(custom_question)
            return

        # Default sample questions
        test_questions = []
        if UNITS:
            first_unit_no = next(iter(UNITS))
            first_topic = next(iter(UNITS[first_unit_no]["topics"]))
            if UNITS[first_unit_no]["topics"][first_topic]:
                test_questions.append(UNITS[first_unit_no]["topics"][first_topic][0]["question"])
            else:
                test_questions.append("What is DBMS?")
        test_questions.append("What is the capital of France?")  # out of syllabus test

        for q in test_questions:
            await _run_prompt(q)

        print("SUCCESS: graph ran end-to-end.")

    if not GOOGLE_API_KEY:
        print("SKIPPED: GOOGLE_API_KEY is not set in your .env file.")
        print("Add it, then re-run: python -m agent.graph")
    else:
        asyncio.run(_self_test())
