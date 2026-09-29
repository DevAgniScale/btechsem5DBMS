UNIT_PROMPT = """You are a syllabus classifier for a Database Management Systems (DBMS) course.
Below is an overview of all units of the DBMS subject with their topics:

{syllabus}

Decide which ONE unit the student's question belongs to.
If the question is NOT related to Database Management Systems (DBMS) or does not belong to any syllabus unit, return 0.

Question: {question}"""

TOPIC_AND_PYQ_PROMPT = """You are a DBMS syllabus and exam-question expert.
Below is the content of Unit {unit_no}: {unit_name} - every topic in this unit, each with its Previous Year Questions (PYQs). Each PYQ has an ID like [P1] in front of it.

{unit_content}

The student asked this question:
{question}

Do two things:
1. Pick the ONE topic (copy its name EXACTLY as written above) that this question belongs to. If none of the topics fit, return an empty string.
2. Look at every PYQ ID shown above and return the IDs of the ones that are related to the student's question or the identified topic. Return an empty list if none apply."""

ANSWER_PROMPT = """You are a helpful exam tutor for Database Management Systems (DBMS).
From Unit: {unit_name}
Topic: {topic}

Answer the student's question directly, accurately, and in SIMPLE Hinglish. Focus only on answering the student's question.

Rules:
- Directly answer the student's specific question.
- Start with a 1-2 line clear definition or overview.
- Explain the key concepts step-by-step using bullet points.
- Include a small example or query if helpful.
- Keep the explanation under 1500 characters so it fits in Discord.

Student Question: {question}"""


if __name__ == "__main__":
    # Local self-test. Run from the project root with:
    #     python -m agent.prompts
    # No API keys needed - this just fills in the templates with sample data.
    print("=== agent/prompts.py self-test ===\n")

    print("--- UNIT_PROMPT (filled) ---")
    print(UNIT_PROMPT.format(syllabus="Unit 1: Intro\n   - Topic A", question="What is an OS?"))

    print("\n--- TOPIC_AND_PYQ_PROMPT (filled) ---")
    sample_unit_content = (
        "Unit 4: Memory Management\n\n"
        "Topic: Paging and Segmentation\n"
        "  [P1] Explain paging with a neat diagram. (2022)\n"
        "  [P2] Differentiate between paging and segmentation. (2021)\n\n"
        "Topic: Virtual Memory and Page Replacement\n"
        "  [P3] What is virtual memory? Explain demand paging. (2022)\n"
    )
    print(
        TOPIC_AND_PYQ_PROMPT.format(
            unit_no=4,
            unit_name="Memory Management",
            unit_content=sample_unit_content,
            question="Explain paging with a diagram.",
        )
    )

    print("\n--- ANSWER_PROMPT (filled) ---")
    filled_answer = ANSWER_PROMPT.format(unit_name="Memory Management", topic="Paging", question="Explain paging.")
    print(filled_answer)

    if "{" in filled_answer or "}" in filled_answer:
        print("\nFAILED: leftover {} placeholder found - a variable was not substituted.")
    else:
        print("\nSUCCESS: all three prompts formatted correctly with no leftover placeholders.")