import json
import shutil
from pathlib import Path

from dotenv import load_dotenv

load_dotenv()

from config import TEMPLATE_FILE
from engine.submission_handler import (
    extract_submission,
    get_zip_files,
)
from engine.docx_extractor import extract_docx_contents
from engine.answer_segmenter import segment_answers
from engine.answer_extractor import extract_answers
from engine.llm_extractor import extract_evaluation_results
from engine.deterministic_grader import deterministic_grader
from engine.manual_review import (
    manual_review,
    needs_manual_review_before_grading,
)
from engine.excel_writer import save_results_to_excel
from prompts.grading_items import grading_items
from prompts.schema import evaluation_schemas


EXTRACTED_ANSWERS_FILE = Path(
    "data/temporary/extracted_answers.json"
)

EVALUATION_RESULTS_FILE = Path(
    "data/temporary/evaluation_results.json"
)

EXTRACTED_DIRECTORY = Path(
    "data/submissions/extracted"
)


def get_student_name(submission_path):
    parts = submission_path.stem.split("_")

    assignment_index = next(
        (
            index
            for index, value in enumerate(parts)
            if value.upper().startswith("CS")
        ),
        len(parts),
    )

    name_parts = parts[:assignment_index]

    if len(name_parts) < 2:
        return submission_path.stem

    last_name = name_parts[0]
    given_names = name_parts[1:]

    return " ".join(given_names + [last_name])


zip_files = get_zip_files()

if not zip_files:
    raise FileNotFoundError(
        "No ZIP submissions found in data/submissions/raw."
    )


for zip_number, zip_path in enumerate(zip_files, start=1):
    print("\n" + "=" * 100)
    print(
        f"PROCESSING SUBMISSION {zip_number}/{len(zip_files)}: "
        f"{zip_path.name}"
    )
    print("=" * 100)

    try:
        submission_path = extract_submission(zip_path)

        student_name = get_student_name(submission_path)

        print(f"Student: {student_name}")

        submission_contents = extract_docx_contents(
            submission_path
        )

        answers = segment_answers(
            submission_contents
        )

        extracted_answers = extract_answers(
            answers
        )

        evaluation_results = extract_evaluation_results(
            extracted_answers,
            grading_items,
            evaluation_schemas,
        )

        grading_results = {}

        for question_id, student_result in evaluation_results.items():
            student_answer = extracted_answers[
                question_id
            ]["combined_text"]

            reference_answer = grading_items[
                question_id
            ]["reference_answer"]

            if needs_manual_review_before_grading(
                student_result
            ):
                grading_result = {
                    "question_id": question_id,
                    "grade": None,
                    "max_points": grading_items[
                        question_id
                    ]["points"],
                    "requires_manual_review": True,
                    "grading_method": "manual_review",
                    "reason": (
                        "The LLM extraction contains a missing "
                        "value or calculations was marked false."
                    ),
                }

                grading_result = manual_review(
                    question_id=question_id,
                    grading_result=grading_result,
                    student_answer=student_answer,
                    reference_answer=reference_answer,
                )

            else:
                grading_result = deterministic_grader(
                    question_id,
                    student_result,
                )

                if grading_result["requires_manual_review"]:
                    grading_result = manual_review(
                        question_id=question_id,
                        grading_result=grading_result,
                        student_answer=student_answer,
                        reference_answer=reference_answer,
                    )

            grading_results[question_id] = grading_result

        print(f"\nFINAL GRADING RESULTS FOR {student_name}")
        print(json.dumps(grading_results, indent=4))
        
        save_results_to_excel(
            student_name=student_name,
            grading_results=grading_results,
            extracted_answers=extracted_answers,
        )

        print(f"Completed grading for {student_name}.")

    except Exception as error:
        print(
            f"Failed to process {zip_path.name}: {error}"
        )

    finally:
        EXTRACTED_ANSWERS_FILE.unlink(
            missing_ok=True
        )

        EVALUATION_RESULTS_FILE.unlink(
            missing_ok=True
        )

        if EXTRACTED_DIRECTORY.exists():
            shutil.rmtree(
                EXTRACTED_DIRECTORY
            )

        EXTRACTED_DIRECTORY.mkdir(
            parents=True,
            exist_ok=True,
        )

        print("Temporary student files cleared.")