def normalize_text(text):
    return " ".join(text.lower().split())


def find_block_by_text(contents, text):
    target = normalize_text(text)

    for index, item in enumerate(contents):
        if item["type"] == "paragraph":
            if target in normalize_text(item["text"]):
                return index

        elif item["type"] == "table_row":
            for cell in item["cells"]:
                if target in normalize_text(cell["text"]):
                    return index

    return None


def clean_section(section):
    cleaned = {
        "text": [],
        "images": [],
    }

    for item in section:
        if item["type"] == "paragraph":
            text = item["text"].strip()

            if text:
                cleaned["text"].append(text)

        elif item["type"] == "table_row":
            for cell in item["cells"]:
                text = cell["text"].strip()

                if text and text.lower() != "your solution:":
                    cleaned["text"].append(text)

        elif item["type"] == "image":
            cleaned["images"].append(
                {
                    "filename": item["filename"],
                    "bytes": item["bytes"],
                    "width": item["width"],
                    "height": item["height"],
                    "sha256": item["sha256"],
                }
            )

    return cleaned


def segment_answers(submission_contents):
    problem_1_start = find_block_by_text(
        submission_contents,
        "What is the Bayesian network factorization",
    )

    problem_2_start = find_block_by_text(
        submission_contents,
        "Problem 2",
    )

    part_a_start = find_block_by_text(
        submission_contents,
        "Complete conditional probability tables",
    )

    part_b_start = find_block_by_text(
        submission_contents,
        "Which decision",
    )

    part_c_start = find_block_by_text(
        submission_contents,
        "What is the value of information",
    )

    boundaries = {
        "problem_1_start": problem_1_start,
        "problem_2_start": problem_2_start,
        "part_a_start": part_a_start,
        "part_b_start": part_b_start,
        "part_c_start": part_c_start,
    }

    missing_boundaries = [
        name
        for name, value in boundaries.items()
        if value is None
    ]

    if missing_boundaries:
        raise ValueError(
            "Could not locate the following question boundaries: "
            + ", ".join(missing_boundaries)
        )

    problem_1_section = submission_contents[
        problem_1_start + 1 : problem_2_start
    ]

    problem_2a_section = submission_contents[
        part_a_start + 1 : part_b_start
    ]

    problem_2b_section = submission_contents[
        part_b_start + 1 : part_c_start
    ]

    problem_2c_section = submission_contents[
        part_c_start + 1 :
    ]

    answers = {
        "1": clean_section(problem_1_section),
        "2.A": clean_section(problem_2a_section),
        "2.B": clean_section(problem_2b_section),
        "2.C": clean_section(problem_2c_section),
    }

    print("Successfully segmented answers.")

    return answers