import json
from openai import OpenAI
from pathlib import Path

EVALUATION_RESULTS_FILE = Path("data/temporary/evaluation_results.json")

client = OpenAI()


def answer_evaluation(
    question_id,
    student_answer,
    grading_item,
    schema,
):
    if not student_answer or not student_answer.strip():
        raise ValueError(
            f"No student answer was provided for question {question_id}"
        )

    prompt = f"""
QUESTION ID:
{grading_item["question_id"]}

TASK:
{grading_item["task"]}

REFERENCE ANSWER:
{grading_item["reference_answer"]}

INSTRUCTIONS:
{grading_item["grading_instructions"]}

STUDENT RESPONSE:
{student_answer}
"""

    response = client.responses.create(
        model="gpt-5-mini",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": prompt,
                    }
                ],
            }
        ],
        text={
            "format": {
                "type": "json_schema",
                "name": (
                    f"question_"
                    f"{question_id.replace('.', '_')}_result"
                ),
                "strict": True,
                "schema": schema,
            }
        },
    )

    return json.loads(response.output_text)


def extract_evaluation_results(
    extracted_answers,
    grading_items,
    evaluation_schemas,
):
    if EVALUATION_RESULTS_FILE.exists():
        with EVALUATION_RESULTS_FILE.open(
            "r",
            encoding="utf-8",
        ) as file:
            print("Loaded evaluation results from JSON.")
            return json.load(file)

    evaluation_results = {}

    for question_id, grading_item in grading_items.items():

        student_answer = extracted_answers[
            question_id
        ]["combined_text"]

        evaluation_results[question_id] = answer_evaluation(
            question_id=question_id,
            student_answer=student_answer,
            grading_item=grading_item,
            schema=evaluation_schemas[question_id],
        )

    EVALUATION_RESULTS_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with EVALUATION_RESULTS_FILE.open(
        "w",
        encoding="utf-8",
    ) as file:
        json.dump(
            evaluation_results,
            file,
            indent=4,
        )

    print(
        "Successfully extracted and stored evaluation results."
    )

    return evaluation_results