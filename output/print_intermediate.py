import json
from pathlib import Path


EXTRACTED_ANSWERS_FILE = Path(
    "data/temporary/extracted_answers.json"
)


def print_extracted_answers():
    if not EXTRACTED_ANSWERS_FILE.exists():
        print("No extracted answers file found.")
        return

    with EXTRACTED_ANSWERS_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:
        extracted_answers = json.load(file)

    print("\n" + "=" * 100)
    print("STUDENT EXTRACTED ANSWERS")
    print("=" * 100)

    for question_id, answer in extracted_answers.items():

        has_typed = bool(answer.get("typed_text", "").strip())
        has_vision = bool(answer.get("vision_text", "").strip())

        if has_typed and has_vision:
            source = "Typed Text + Vision OCR"

        elif has_typed:
            source = "Typed Text"

        elif has_vision:
            source = "Vision OCR"

        else:
            source = "No Answer"

        print(f"\nQUESTION {question_id}")
        print(f"Source : {source}")
        print("-" * 100)
        print(answer.get("combined_text") or "No answer found")