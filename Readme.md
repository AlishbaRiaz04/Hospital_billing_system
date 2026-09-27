# Hospital Appointment & Billing Management System

## Approach

The program is built as a set of small, single-purpose functions organized in layers, where each layer only depends on the layer below it:

1. **Validation** — checks whether a patient, doctor, or appointment is legitimate to process
2. **Billing** — calculates charges, insurance coverage, senior discounts, and the final bill
3. **Cancellation** — handles status transitions for cancelling an appointment
4. **Reporting** — aggregates per-doctor and per-patient statistics
5. **Dashboard** — a clinic-wide summary that reuses the two reports above
6. **Orchestrator** (`process_appointment`) — ties validation and billing together for one appointment
7. A short `main` block runs all appointments through the pipeline and prints results

No classes are used, per the assignment's restrictions — all data is kept in plain dictionaries and lists.

## Files

- `main.py` — all function definitions, starter data, and the program's execution loop
- `test_cases.py` — edge case tests (imports functions from `main.py`)
- `sample_output.txt` — example output from running `main.py`

## Design Decisions

**Validation is split into small functions, not one big one.** `validate_patient`, `validate_doctor`, and `validate_tests` each answer one narrow question. `validate_appointment` calls all three internally rather than duplicating their checks — this way, if any of these checks are ever needed on their own elsewhere, they don't need to be rewritten.

**Doctor existence and doctor availability are two separate checks.** "Does this doctor exist" is a data-integrity question; "is this doctor currently available" is a state question. Keeping them apart in `validate_doctor` (existence only) vs. `validate_appointment` (availability check) keeps each function's responsibility narrow.

**`calculate_bill` returns a full breakdown dictionary, not just a final number.** The patient and doctor reports both need to display insurance coverage, consultation fees, and test charges as separate figures — returning the whole breakdown once avoids recalculating the same numbers repeatedly in different functions.

**`apply_insurance_coverage` and `apply_senior_discount` each return one combined number**, not separate consultation/test breakdowns, since nothing downstream needs the two rates split apart — only the total.

**`cancel_appointment` doesn't call `validate_appointment`.** Cancellation only cares about the appointment's current status (a state-transition question), not whether the patient/doctor IDs are valid (a data-integrity question) — these are different concerns, so they're kept in separate functions with different responsibilities.

**Reports and the dashboard avoid recalculating shared work.** `generate_doctor_report` and `generate_patient_report` both call `calculate_bill` once per completed appointment. `generate_clinic_report` doesn't repeat any of that work — it calls both reports and sums the numbers they already computed.

**`generate_clinic_report` is the one function that both prints and returns data.** Every other reporting function only returns data (since other functions consume their output), but nothing calls `generate_clinic_report`'s result afterward — it's the end of the chain, so it both displays the formatted dashboard and returns the dictionary (useful for testing the numbers without reading printed text).

**`process_appointment` always returns the same four keys** (`appointment_id`, `status`, `reason`, `bill`), regardless of whether the appointment was accepted or rejected — using `None` for whichever field doesn't apply. This keeps the return shape consistent instead of branching into two different formats.

## Known Limitation

`generate_patient_report`'s `highest_spending_patient` and `patient_with_most_appointments` use `max()` over the `patients` dictionary. If `patients` is completely empty, `max()` will raise a `ValueError` since there's nothing to compare. A production version should guard this case explicitly (e.g. return `None` when `patients` is empty) rather than letting it raise.

## *args / **kwargs (Sections 9 & 10)

- `calculate_total(*charges)` — accepts any number of charge amounts and returns their sum
- `calculate_bill_flexible(base_amount, **options)` — a configurable billing function supporting `insurance=True` and `senior_discount=True` as options

## Lambda & Comprehensions (Sections 11 & 12)

- `lambda` is used with `max()` to find `most_requested_doctor`, `most_requested_specialization`, `highest_spending_patient`, and `patient_with_most_appointments`
- List comprehensions are used to build `insured_patients`, `senior_citizen_patients`, and `patients_with_no_completed_appointment`

## Config / LEGB (Section 13)

A `CLINIC_CONFIG` dictionary holds `tax`, `currency`, and `senior_discount_rate`. `get_config_value()` reads from this global dictionary without ever reassigning it inside a function — this only requires the *Global* scope to be read, not written to, so no `global` keyword is needed anywhere in the program.