from pathlib import Path
import shutil
import zipfile


RAW_DIR = Path("data/submissions/raw")
EXTRACT_DIR = Path("data/submissions/extracted")


def get_zip_files():
    return sorted(RAW_DIR.glob("*.zip"))


def extract_submission(zip_path):
    if EXTRACT_DIR.exists():
        shutil.rmtree(EXTRACT_DIR)

    EXTRACT_DIR.mkdir(parents=True)

    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(EXTRACT_DIR)

    macos_folder = EXTRACT_DIR / "__MACOSX"

    if macos_folder.exists():
        shutil.rmtree(macos_folder)

    for ds_store in EXTRACT_DIR.rglob(".DS_Store"):
        ds_store.unlink(missing_ok=True)

    folders = [item for item in EXTRACT_DIR.iterdir() if item.is_dir()]
    files = [item for item in EXTRACT_DIR.iterdir() if item.is_file()]

    if len(folders) == 1 and not files:
        student_folder = folders[0]

        for item in student_folder.iterdir():
            shutil.move(
                str(item),
                str(EXTRACT_DIR / item.name),
            )

        student_folder.rmdir()

    docx_files = [
        path
        for path in EXTRACT_DIR.rglob("*.docx")
        if not path.name.startswith("~$")
    ]

    if len(docx_files) != 1:
        raise ValueError(
            f"Expected exactly one DOCX file in {zip_path.name}, "
            f"but found {len(docx_files)}."
        )

    print(f"Extraction completed for {zip_path.name}.")

    return docx_files[0]