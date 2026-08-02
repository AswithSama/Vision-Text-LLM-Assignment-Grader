from pathlib import Path
import shutil
import zipfile


def extract_submission():
    raw_dir = Path("data/submissions/raw")
    extract_dir = Path("data/submissions/extracted")

    # Make sure extracted exists
    extract_dir.mkdir(parents=True, exist_ok=True)

    # Find the single ZIP file
    zip_path = next(raw_dir.glob("*.zip"))

    # Empty extracted folder
    if extract_dir.exists():
        shutil.rmtree(extract_dir)

    extract_dir.mkdir(parents=True)

    # Extract ZIP
    with zipfile.ZipFile(zip_path, "r") as zip_ref:
        zip_ref.extractall(extract_dir)

    # Remove macOS metadata folder if present
    macos_folder = extract_dir / "__MACOSX"

    if macos_folder.exists():
        shutil.rmtree(macos_folder)

    # Flatten the extracted folder if needed
    folders = [f for f in extract_dir.iterdir() if f.is_dir()]

    if len(folders) == 1:
        student_folder = folders[0]

        for item in student_folder.iterdir():
            shutil.move(str(item), extract_dir)

        student_folder.rmdir()

    # Return the extracted DOCX file
    docx_file = next(extract_dir.glob("*.docx"))

    print("Extraction completed successfully.")

    return docx_file