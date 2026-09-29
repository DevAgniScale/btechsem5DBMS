"""Parses data/unit_N.md files into a dict.

Expected file format:

# Unit 1: <Unit Name>

## Topic: <Topic Name>
- PYQ: <question text> (Year)
"""
import re
import config

ROMAN_MAP = {"I": 1, "II": 2, "III": 3, "IV": 4, "V": 5, "VI": 6, "VII": 7, "VIII": 8, "IX": 9, "X": 10}

UNIT_RE = re.compile(r"^#\s*Unit\s*([0-9]+|[IVXLCDM]+)\s*[:\u2014\-–]\s*(.+)$", re.I)
TOPIC_RE = re.compile(r"^##\s*Topic\s*:\s*(.+)$", re.I)
PYQ_FORMAT1_RE = re.compile(r"^-\s*\*\*\[([^\]]+)\]\*\*\s*(.+)$")
PYQ_FORMAT2_RE = re.compile(r"^-\s*PYQ\s*:\s*(.+?)(?:\s*\((\d{4}[^)]*)\))?\s*$", re.I)


def _parse_unit_no(raw: str) -> int:
    raw_upper = raw.upper()
    if raw_upper in ROMAN_MAP:
        return ROMAN_MAP[raw_upper]
    return int(raw)


def load_units() -> dict:
    """Returns {unit_no: {"name": str, "topics": {topic: [{"question", "year"}]}}} for unit_*.md files."""
    units = {}
    for path in sorted(config.DATA_DIR.glob("unit_*.md")):
        unit_no, topic = None, None
        for line in path.read_text(encoding="utf-8").splitlines():
            line = line.strip()
            if m := UNIT_RE.match(line):
                unit_no = _parse_unit_no(m.group(1))
                units[unit_no] = {"name": m.group(2).strip(), "topics": {}}
            elif (m := TOPIC_RE.match(line)) and unit_no is not None:
                topic = m.group(1).strip()
                units[unit_no]["topics"][topic] = []
            elif unit_no is not None and topic:
                if m := PYQ_FORMAT1_RE.match(line):
                    year = m.group(1).strip()
                    question = m.group(2).strip()
                    units[unit_no]["topics"][topic].append({"question": question, "year": year})
                elif m := PYQ_FORMAT2_RE.match(line):
                    question = m.group(1).strip()
                    year = (m.group(2) or "").strip()
                    units[unit_no]["topics"][topic].append({"question": question, "year": year})
    return units


def load_helper() -> str:
    """Returns the text content of data/helper.md."""
    helper_path = config.DATA_DIR / "helper.md"
    if helper_path.exists():
        return helper_path.read_text(encoding="utf-8")
    return ""


if __name__ == "__main__":
    # Local self-test. Run from the project root with:
    #     python -m agent.loader
    # No API keys needed - this only reads your data/*.md files.
    print("=== agent/loader.py self-test ===\n")
    print(f"Reading from: {config.DATA_DIR}\n")

    units = load_units()

    if not units:
        print("FAILED: no units found. Check that data/unit_*.md files exist and follow the format:")
        print("  # Unit 1: <name>")
        print("  ## Topic: <name>")
        print("  - PYQ: <question text> (Year)")
    else:
        total_topics = sum(len(u["topics"]) for u in units.values())
        total_pyqs = sum(len(qs) for u in units.values() for qs in u["topics"].values())
        print(f"Loaded {len(units)} unit(s), {total_topics} topic(s), {total_pyqs} PYQ(s) total.\n")

        for no, u in sorted(units.items()):
            topic_count = len(u["topics"])
            pyq_count = sum(len(qs) for qs in u["topics"].values())
            print(f"Unit {no}: {u['name']}  ({topic_count} topics, {pyq_count} PYQs)")
            for t, qs in u["topics"].items():
                print(f"   - {t}  [{len(qs)} PYQs]")

        first_unit_no = next(iter(units))
        first_topic = next(iter(units[first_unit_no]["topics"]))
        print(f"\nSample - Unit {first_unit_no} -> '{first_topic}':")
        for p in units[first_unit_no]["topics"][first_topic]:
            year = f" ({p['year']})" if p["year"] else ""
            print(f"   * {p['question']}{year}")

        print("\nSUCCESS: loader.py parsed all unit files correctly.")
