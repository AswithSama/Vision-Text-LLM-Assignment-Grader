import base64
import json
from pathlib import Path

from config import VISION_MODEL
from openai import OpenAI

client = OpenAI()

EXTRACTED_ANSWERS_FILE = Path("data/temporary/extracted_answers.json")

def image_to_data_url(image_data):
    image_bytes = image_data["bytes"]
    image_format = image_data.get("format") or "PNG"

    mime_type = f"image/{image_format.lower()}"

    encoded_image = base64.b64encode(
        image_bytes
    ).decode("utf-8")

    return f"data:{mime_type};base64,{encoded_image}"

def transcribe_image(image_data):
    image_url = image_to_data_url(image_data)

    response = client.responses.create(
        model="gpt-5-mini",
        input=[
            {
                "role": "user",
                "content": [
                    {
                        "type": "input_text",
                        "text": (
                            "Transcribe this handwritten student answer exactly. "
                            "Preserve equations, probability notation, variables, "
                            "subscripts, arithmetic, line order, and conclusions. "
                            "Do not solve, correct, or explain the work. "
                            "If a symbol is unclear, write [unclear]."
                        ),
                    },
                    {
                        "type": "input_image",
                        "image_url": image_url,
                    },
                ],
            }
        ],
    )
    return response.output_text.strip()


def extract_answers(answers):
    extracted_answers = {}

    for question_id, answer in answers.items():
        typed_text = "\n".join(
            answer["text"]
        ).strip()

        image_transcriptions = []

        for image_number, image_data in enumerate(
            answer["images"],
            start=1,
        ):
            transcription = transcribe_image(
                image_data
            )

            image_transcriptions.append(
                {
                    "image_number": image_number,
                    "filename": image_data["filename"],
                    "text": transcription,
                }
            )

        vision_text = "\n\n".join(
            item["text"]
            for item in image_transcriptions
            if item["text"]
        )

        combined_parts = []

        if typed_text:
            combined_parts.append(typed_text)

        if vision_text:
            combined_parts.append(vision_text)

        extracted_answers[question_id] = {
            "typed_text": typed_text,
            "image_transcriptions": image_transcriptions,
            "vision_text": vision_text,
            "combined_text": "\n\n".join(combined_parts),
        }

    EXTRACTED_ANSWERS_FILE.parent.mkdir(
        parents=True,
        exist_ok=True,
    )

    with EXTRACTED_ANSWERS_FILE.open("w", encoding="utf-8",) as file:
        json.dump(
            extracted_answers,
            file,
            indent=4,
        )

    print("Successfully extracted and stored answers.")

    return extracted_answers
