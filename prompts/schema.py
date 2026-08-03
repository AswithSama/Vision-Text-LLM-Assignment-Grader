evaluation_schemas = {
    "1": {
        "type": "object",
        "properties": {
            "decision": {
                "type": "integer",
                "enum": [0, 1]
            },
            "candidate_final_answer": {
                "type": ["string", "null"]
            },
            "reason": {
                "type": "string"
            }
        },
        "required": [
            "decision",
            "candidate_final_answer",
            "reason"
        ],
        "additionalProperties": False
    },

    "2.A": {
        "type": "object",
        "properties": {
            "p_a_true": {"type": ["number", "null"]},
            "p_a_false": {"type": ["number", "null"]},
            "p_b_true_given_a_true": {
                "type": ["number", "null"]
            },
            "p_b_false_given_a_true": {
                "type": ["number", "null"]
            },
            "p_b_true_given_a_false": {
                "type": ["number", "null"]
            },
            "p_b_false_given_a_false": {
                "type": ["number", "null"]
            },
            "calculations": {"type": "boolean"}
        },
        "required": [
            "p_a_true",
            "p_a_false",
            "p_b_true_given_a_true",
            "p_b_false_given_a_true",
            "p_b_true_given_a_false",
            "p_b_false_given_a_false",
            "calculations"
        ],
        "additionalProperties": False
    },

    "2.B": {
        "type": "object",
        "properties": {
            "eu_x": {"type": ["number", "null"]},
            "eu_y": {"type": ["number", "null"]},
            "eu_z": {"type": ["number", "null"]},
            "best_decision": {
                "type": ["string", "null"],
                "enum": ["x", "y", "z", None]
            },
            "calculations": {"type": "boolean"}
        },
        "required": [
            "eu_x",
            "eu_y",
            "eu_z",
            "best_decision",
            "calculations"
        ],
        "additionalProperties": False
    },

    "2.C": {
        "type": "object",
        "properties": {
            "eu_x_without_b": {"type": ["number", "null"]},
            "eu_y_without_b": {"type": ["number", "null"]},
            "eu_z_without_b": {"type": ["number", "null"]},
            "meu_without_b": {"type": ["number", "null"]},
            "meu_with_b": {"type": ["number", "null"]},
            "voi_b": {"type": ["number", "null"]},
            "reason": {"type": "string"},
            "calculations": {"type": "boolean"}
        },
        "required": [
            "eu_x_without_b",
            "eu_y_without_b",
            "eu_z_without_b",
            "meu_without_b",
            "meu_with_b",
            "voi_b",
            "reason",
            "calculations"
        ],
        "additionalProperties": False
    }
}