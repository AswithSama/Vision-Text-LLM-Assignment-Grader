import re


EXPECTED_ANSWERS = {
    "1": {
        "candidate_final_answer": (
            "P(A) * P(B|A) * P(C|D) * P(D|X) * P(E) * "
            "P(G|C,D) * P(H) * P(J|B,E,G) * P(K|G,H,L) * "
            "P(L|Z) * P(X) * P(Y) * P(Z|Y)"
        ),
        "points": 10,
    },

    "2.A": {
        "values": {
            "p_a_true": 0.7,
            "p_a_false": 0.3,
            "p_b_true_given_a_true": 0.8,
            "p_b_false_given_a_true": 0.2,
            "p_b_true_given_a_false": 0.1,
            "p_b_false_given_a_false": 0.9,
        },
        "tolerance": 0,
        "points": 2,
    },

    "2.B": {
        "values": {
            "eu_x": 94.9,
            "eu_y": 22.48,
            "eu_z": 32.47,
        },
        "tolerance": 2,
        "best_decision": "x",
        "points": 9,
    },

    "2.C": {
        "values": {
            "eu_x_without_b": 70,
            "eu_y_without_b": 35,
            "eu_z_without_b": 45,
            "meu_without_b": 70,
            "meu_with_b": 81.8005,
            "voi_b": 11.8005,
        },
        "tolerance": 1.5,
        "points": 9,
    },
}

def deterministic_grader(question_id, student_result):
    expected = EXPECTED_ANSWERS[question_id]
    failed_fields = []

    if question_id == "1":
        student_answer = re.sub(r"\s+", "", student_result["candidate_final_answer"],).lower()
        reference_answer = re.sub(r"\s+", "", expected["candidate_final_answer"]).lower()

        if student_answer != reference_answer:
            failed_fields.append("candidate_final_answer")

    else:
        tolerance = expected.get("tolerance", 0)

        for field, expected_value in expected["values"].items():
            student_value = student_result[field]

            if abs(float(student_value) - expected_value) > tolerance:
                failed_fields.append(field)

        if "best_decision" in expected:
            student_decision = str(student_result["best_decision"]).strip().lower()

            if student_decision != expected["best_decision"]:
                failed_fields.append("best_decision")

    if failed_fields:
        return {
            "question_id": question_id,
            "grade": None,
            "max_points": expected["points"],
            "requires_manual_review": True,
            "grading_method": "manual_review",
            "reason": (
                "The following fields did not satisfy the "
                "automatic grading rules: "
                + ", ".join(failed_fields)
            ),
        }

    return {
        "question_id": question_id,
        "grade": expected["points"],
        "max_points": expected["points"],
        "requires_manual_review": False,
        "grading_method": "automatic",
        "reason": "All required values satisfied the grading rules.",
    }