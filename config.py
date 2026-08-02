from pathlib import Path

BASE_DIR = Path(__file__).resolve().parent

RAW_SUBMISSIONS_DIR = BASE_DIR / "data" / "submissions" / "raw"
EXTRACTED_SUBMISSIONS_DIR = BASE_DIR / "data" / "submissions" / "extracted"

TEMPLATE_FILE =  Path("data/templates/CS579_fall2024_Written_Assignment_01.docx")

RESULTS_FILE = (
    BASE_DIR
    / "data"
    / "results"
    / "grades.xlsx"
)

TEMP_DIR = BASE_DIR / "data" / "temporary"

VISION_MODEL = "gpt-5-mini"
ANSWER_EXTRACTION_MODEL = "gpt-5-mini"