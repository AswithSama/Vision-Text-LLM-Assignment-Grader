grading_item_1 = {
    "question_id": "1",
    "points": 10,

    "description": """
We are given a Bayesian network over the variables
A, B, C, D, E, G, H, J, K, L, X, Y, Z.
""",

    "task": """
Write the Bayesian network factorization of the joint probability

P(A, B, C, D, E, G, H, J, K, L, X, Y, Z).
""",

    "reference_answer": """
P(A) * P(B|A) * P(C|D) * P(D|X) * P(E) *
P(G|C,D) * P(H) * P(J|B,E,G) * P(K|G,H,L) *
P(L|Z) * P(X) * P(Y) * P(Z|Y)
""",

    "grading_instructions": """
You are given a student response to a Bayesian-network factorization question.

Your primary responsibility is to identify and extract the student's intended final answer from the complete student response.

Focus on identifying what the student is submitting as their final answer, regardless of whether it is correct or incorrect.

The student may:
- provide the final answer directly;
- perform calculations and then provide a final answer;
- revise their work before presenting a final answer.

Your job is to identify the final answer that the student intended to submit.

Ignore intermediate calculations, rough work, scratch work, or derivations when a clear final answer is present.

Do not assign points.
Do not award partial credit.
Do not determine whether the answer is correct.
Do not compare the answer with the reference answer.
Do not modify, correct, or complete the student's answer.
Do not rewrite the student's answer to match the reference answer.

Return the student's intended final answer as faithfully as possible. Preserve the mathematical notation and wording used by the student. You may normalize insignificant formatting such as whitespace and line breaks, but do not change the mathematical meaning or notation.

If:
- a clear final factorization can be identified, then return:

{
    "decision": 1,
    "candidate_final_answer": "the student's intended final factorization",
    "reason": "A clear final answer was identified."
}

--------------------

If:
- no final answer can be identified;
- the response contains only incomplete calculations;
- the transcription is unreadable or corrupted;
- multiple conflicting final answers are present;
- the student's intended final answer is ambiguous.

then return:

{
    "decision": 0,
    "candidate_final_answer": null,
    "reason": "Brief explanation of why manual review is required."
}

Return valid JSON only.
"""
}

grading_item_2a = {
    "question_id": "2.A",
    "points": 2,

    "task": """
Complete the conditional probability tables for each chance node.
""",

    "reference_answer": """
Solution — Part A: Conditional Probability Tables

Node A has no parents, so its CPT is its prior:

P(A=T) = 0.7
P(A=F) = 1 - P(A=T) = 1 - 0.7 = 0.3

Node B's CPT is conditioned on A:

P(B=T|A=T) = 1 - P(B=F|A=T) = 1 - 0.2 = 0.8
P(B=F|A=T) = 0.2

P(B=T|A=F) = 1 - P(B=F|A=F) = 1 - 0.9 = 0.1
P(B=F|A=F) = 0.9

The marginal probabilities may also be shown:

P(B=T) = 0.59
P(B=F) = 0.41

However, these marginal values are not required when the conditional
probability tables are complete.
""",

    "grading_instructions": """
You are given a student's response to a conditional-probability-table question.

Your task is not to decide whether the entire response is correct. Instead,
extract the probability values that the student explicitly provides or
clearly derives.

Extract the following six values:

1. P(A=T)
2. P(A=F)
3. P(B=T | A=T)
4. P(B=F | A=T)
5. P(B=T | A=F)
6. P(B=F | A=F)

For every requested value:

- Return the student's final stated or clearly derived numeric value.
- Return null when the student does not provide or clearly derive that value.
- Do not infer a missing value merely because it could be computed from another
  value.
- Do not silently correct an incorrect value.
- Preserve the student's intended numeric answer even when it differs from the
  reference answer.
- Equivalent decimal, fraction, or percentage forms are acceptable.

Also determine whether the response contains relevant calculation work.

Set "calculations" to true when the student shows at least one relevant
probability calculation, complement operation, substitution, or equivalent
mathematical step used to complete the CPT.

Examples that count as calculations include:

- 1 - 0.7 = 0.3
- 1 - 0.2 = 0.8
- P(A=F) = 1 - P(A=T)
- P(B=T|A=T) = 1 - P(B=F|A=T)
- Writing "1 - 0.8" as part of an attempt, even if the referenced number or
  final result is incorrect
- Showing that two corresponding probabilities sum to 1
- Substituting probabilities into a marginalization equation

Set "calculations" to false when:

- the response contains only final numbers without any visible calculation,
  complement reasoning, formula, or mathematical step;
- the work is unrelated to the chance-node CPTs;
- no meaningful mathematical work is identifiable.

The calculation does not need to be fully correct. A minor arithmetic,
notation, transcription, or labeling mistake may still count as calculation
work when the student's method is recognizable and relevant.

When comparing the student's calculation method with the reference solution,
treat the method as sufficiently relevant when approximately 70-80% or more
of the identifiable calculation approach follows the same probability-
complement or CPT-completion reasoning. This percentage concerns the
student's calculation method and way of solving, not the number of final
probability values that are correct.

The marginal probabilities P(B=T)=0.59 and P(B=F)=0.41 may appear in the
student's response, but they are not required and should not replace any of
the six requested CPT values.

Return valid JSON only in exactly this structure:

{
    "p_a_true": <number or null>,
    "p_a_false": <number or null>,
    "p_b_true_given_a_true": <number or null>,
    "p_b_false_given_a_true": <number or null>,
    "p_b_true_given_a_false": <number or null>,
    "p_b_false_given_a_false": <number or null>,
    "calculations": <true or false>
}

Rules:
- the student's extracted final value if explicitly provided or clearly derived, or
- null if the student does not provide or clearly derive that value.
- The "calculations" field must be either true or false.
- Do not include a correctness decision, score, explanation, markdown, or any
additional keys.
"""
}

grading_item_2b = {
    "question_id": "2.B",
    "points": 9,

    "task": """
Which decision, x, y, or z, is best given evidence B=T?
Justify the answer.
""",

    "reference_answer": """
First calculate the posterior probabilities:

P(B=T) =
P(B=T | A=T)P(A=T) + P(B=T | A=F)P(A=F)

= (0.8)(0.7) + (0.1)(0.3)
= 0.59

P(A=T | B=T) =
P(B=T | A=T)P(A=T) / P(B=T)

= (0.8)(0.7) / 0.59
≈ 0.9492

P(A=F | B=T) ≈ 0.0508

Then calculate expected utility for every decision:

EU(x | B=T) =
(0.9492)(100) + (0.0508)(0)
≈ 94.92

EU(y | B=T) =
(0.9492)(20) + (0.0508)(70)
≈ 22.54

EU(z | B=T) =
(0.9492)(30) + (0.0508)(80)
≈ 32.54

The best decision is x because it has the highest expected utility.
""",

"grading_instructions": """
You are given a student's response to a Bayesian decision-network problem.

Your task is NOT to determine whether the student's answer is correct.
Instead, extract the values that the student explicitly provides or clearly
derives.

Extract the following values when present:

1. The expected utility for decision x.
2. The expected utility for decision y.
3. The expected utility for decision z.
4. The student's selected best decision (x, y, or z).

For every requested numeric value:

- Return the student's final stated or clearly derived value.
- Return null if the student does not explicitly provide or clearly derive
  that value.
- Do not infer missing values from other values.
- Do not silently correct incorrect values.
- Preserve the student's intended answer even if it differs from the
  reference answer.
- Equivalent decimal, fraction, or percentage forms are acceptable.

The student may use any reasonable notation for expected utility, including
but not limited to:

- EU(x), EU(y), EU(z)
- EU(x | B=T)
- U(x), U(y), U(z)
- E(U(x))
- Expected Utility
- Expected Payoff
- Expected Value
- Tables listing values for x, y, and z
- Any equivalent notation that clearly associates a utility value with a
  particular decision.

For the selected decision:

- Return exactly "x", "y", or "z" if the student explicitly chooses one.
- Return null if no final decision can be identified.

Also determine whether the response contains relevant calculations.

Set "calculations" to true when the student demonstrates a substantially
similar Bayesian or expected-utility solution process as shown in the
reference solution.

Students may omit the posterior-probability calculations if they were
computed previously. This is acceptable.

To put calculations=true, the response should contain recognizable
mathematical work showing how the expected utilities are obtained or
compared. This may include formulas, substitutions, arithmetic,
intermediate steps, expected-utility computations, or mathematical
comparisons such as max(U(x), U(y), U(z)), EU(x) > EU(y), argmax, or other
equivalent notation.

Minor arithmetic, notation, transcription, or rounding mistakes are
acceptable as long as the student's reasoning is recognizable and follows
approximately 70-80% of the calculation approach demonstrated in the
reference solution.

Put calculations=false  if the response only states the final decision or
lists unsupported final values without any recognizable mathematical
reasoning.

Return valid JSON only in exactly this structure:

{
    "eu_x": <number or null>,
    "eu_y": <number or null>,
    "eu_z": <number or null>,
    "best_decision": <"x", "y", "z", or null>,
    "calculations": <true or false>
}

Each numeric field must contain:
- the student's extracted final value if explicitly provided or clearly
  derived, or
- null otherwise.

Do not include explanations, scores, decisions, markdown, or any additional
keys.
"""
}


grading_item_2c = {
    "question_id": "2.C",
    "points": 9,

    "task": """
What is the value of information for B?
Justify the answer.
""",

    "reference_answer": """
Without observing B:

EU(x) = (0.7)(100) + (0.3)(0) = 70
EU(y) = (0.7)(20) + (0.3)(70) = 35
EU(z) = (0.7)(30) + (0.3)(80) = 45

Therefore:

MEU without B = 70, using decision x.

When B=T:

P(B=T) = 0.59

The best decision is x, with:

MEU(B=T) ≈ 94.92

When B=F:

P(B=F) = 0.41

P(A=T | B=F) =
P(B=F | A=T)P(A=T) / P(B=F)

= (0.2)(0.7) / 0.41
≈ 0.3415

P(A=F | B=F) ≈ 0.6585

EU(x | B=F) ≈ 34.15
EU(y | B=F) ≈ 52.93
EU(z | B=F) ≈ 62.93

Therefore the best decision when B=F is z.

Expected maximum utility with information B:

MEU with B =
P(B=T)MEU(B=T) + P(B=F)MEU(B=F)

≈ (0.59)(94.92) + (0.41)(62.93)
≈ 81.8

Value of information:

VOI(B) =
MEU with B - MEU without B

≈ 81.8 - 70
≈ 11.8
""",

    "grading_instructions": """
Your primary responsibility is to inspect the complete student response and
extract the specific values and evidence requested in the output JSON.

This is mainly an information-extraction task, not a grading task.

Identify only what the student actually wrote or clearly calculated.
Do not fill in missing values using the reference answer.
Do not silently correct arithmetic.
Do not replace the student's values with the expected values.
Do not infer a value unless it is directly and unambiguously supported by the
student's written work.

Students may use different mathematical notation, abbreviations, variable names, or formatting to represent the same quantity. Be flexible when identifying these values, but do not assume or infer a value that is not explicitly stated or unambiguously derived from the student's work.
Extract the following quantities from the student's response whenever they can be clearly identified:

- EU(x) without observing B
- EU(y) without observing B
- EU(z) without observing B
- MEU without observing B
- MEU with information B
- VOI(B)

For each numeric field:

- Return the student's numeric value when it is clearly present.
- Return null when the value is missing, unreadable, ambiguous, or cannot be
  reliably identified.
- Preserve the student's value even when it appears incorrect.
- Minor formatting differences, such as commas, extra spaces, or approximate
  symbols, may be normalized.
- Do not recalculate a value from other values unless the student explicitly
  shows that calculation and the result can be clearly identified.

For the "calculations" field:

- Return true when the student shows relevant calculations or derivations for
  the value-of-information problem.
- Return false when the response contains only final values, unrelated work,
  or no meaningful calculations.

For the "reason" field:

Provide only a brief summary of extraction quality and relevance. You may note
whether the response contains relevant work, missing values, unreadable parts,
or clearly irrelevant calculations.

Do not make a full grading judgment.
Do not assign points.
Do not decide pass or fail.
Do not compare every value against the reference answer.

A limited evaluation is allowed only for the "reason" field, such as:

- "Relevant calculations were present and all requested values were readable."
- "Some values were missing or unclear."
- "The response contained calculations, but they were not clearly related to
  the requested quantities."
- "Only a final VOI value was present; supporting values were not identified."

Return valid JSON in this exact format:

{
    "eu_x_without_b": <number or null>,
    "eu_y_without_b": <number or null>,
    "eu_z_without_b": <number or null>,
    "meu_without_b": <number or null>,
    "meu_with_b": <number or null>,
    "voi_b": <number or null>,
    "reason": "Brief extraction-focused explanation.",
    "calculations": <true or false>
}

Use JSON numbers, not numeric strings.

Return valid JSON only.
"""
}


grading_items = {
    "1": grading_item_1,
    "2.A": grading_item_2a,
    "2.B": grading_item_2b,
    "2.C": grading_item_2c,
}