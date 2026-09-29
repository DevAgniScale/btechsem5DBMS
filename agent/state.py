from typing import TypedDict, Optional


class AgentState(TypedDict, total=False):
    question: str
    route: Optional[str]
    unit_no: Optional[int]
    unit_name: Optional[str]
    topic: Optional[str]
    related_pyqs: list[dict]
    answer: str


if __name__ == "__main__":
    # Local self-test. Run from the project root with:
    #     python -m agent.state
    # No API keys needed - this just checks the AgentState shape.
    print("=== agent/state.py self-test ===\n")

    sample: AgentState = {
        "question": "Explain paging.",
        "route": "specific",
        "unit_no": 4,
        "unit_name": "Memory Management",
        "topic": "Paging and Segmentation",
        "related_pyqs": [{"question": "Explain paging with a diagram.", "year": "2022"}],
        "answer": "Paging splits memory into fixed-size blocks called pages.",
    }
    print("Sample AgentState:")
    for k, v in sample.items():
        print(f"   {k}: {v}")

    expected_keys = {"question", "route", "unit_no", "unit_name", "topic", "related_pyqs", "answer"}
    actual_keys = set(AgentState.__annotations__)
    print(f"\nExpected fields: {sorted(expected_keys)}")
    print(f"Actual fields:   {sorted(actual_keys)}")

    if actual_keys == expected_keys:
        print("\nSUCCESS: AgentState fields match the expected schema.")
    else:
        print(f"\nFAILED: mismatch - missing {expected_keys - actual_keys}, extra {actual_keys - expected_keys}")
