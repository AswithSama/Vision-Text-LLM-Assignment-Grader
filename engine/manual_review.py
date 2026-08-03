def manual_review(question_id, grading_result, student_answer, reference_answer):

    print("\n" + "=" * 100)
    print(f"MANUAL REVIEW REQUIRED: QUESTION {question_id}")
    print("=" * 100)
    
    print("\nREFERENCE SOLUTION")
    print("-" * 100)
    print(reference_answer)

    print("\nSTUDENT ANSWER:")
    print(student_answer or "No answer available.")

    print("\nAUTOMATIC GRADING RESULT:")
    print("Reason:", grading_result["reason"])
    print("Maximum points:", grading_result["max_points"])

    while True:
        try:
            grade = float(input(f"\nEnter grade for Question {question_id} " f"out of {grading_result['max_points']}: "))

            if 0 <= grade <= grading_result["max_points"]:
                break

            print(f"Grade must be between 0 and "f"{grading_result['max_points']}.")

        except ValueError:
            print("Please enter a valid numeric grade.")

    note = input("Enter a short manual review note: ").strip()

    grading_result["grade"] = grade
    grading_result["requires_manual_review"] = False
    grading_result["grading_method"] = "manual"
    grading_result["reason"] = (note or grading_result["reason"])

    return grading_result


def needs_manual_review_before_grading(student_result):
    ignored_fields = {"reason"}

    for field, value in student_result.items():
        if field in ignored_fields:
            continue

        if value is None:
            return True

    return student_result.get("calculations") is False