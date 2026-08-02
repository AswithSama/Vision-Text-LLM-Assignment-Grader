import json
from pathlib import Path
from dotenv import load_dotenv
load_dotenv()

from config import TEMPLATE_FILE
from engine.submission_handler import extract_submission
from engine.docx_extractor import extract_docx_contents
from engine.answer_segmenter import segment_answers
from engine.answer_extractor import extract_answers
from output.print_intermediate import print_extracted_answers


EXTRACTED_ANSWERS_FILE = Path(
    "data/temporary/extracted_answers.json"
)


submission_path = extract_submission()

template_contents = extract_docx_contents(TEMPLATE_FILE)
submission_contents = extract_docx_contents(submission_path)

answers = segment_answers(submission_contents)


if EXTRACTED_ANSWERS_FILE.exists():
    with EXTRACTED_ANSWERS_FILE.open(
        "r",
        encoding="utf-8",
    ) as file:
        extracted_answers = json.load(file)

    print("Loaded previously extracted answers from JSON.")

else:
    extracted_answers = extract_answers(answers)
    print("Vision model ran once and stored the extracted answers.")


print(print_extracted_answers())