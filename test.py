"""
Edge case test cases for the Clinic Management System.
Covers every edge case listed in Section 14 of the assignment.
Run this file directly: python test.py
"""

from validation import validate_patient, validate_doctor, validate_tests, validate_appointment
from billing import apply_senior_discount, cancel_appointment
from reports import generate_patient_report, generate_doctor_report
from models import create_patients, create_appointment, create_doctors, Doctor, Appointment
import json

with open("input_data.json", "r") as file:
    data = json.load(file)
    patients = create_patients(data["patients"])
    doctors = create_doctors(data["doctors"])
    appointments = create_appointment(data["appointments"])
    test_prices = data["test_prices"]

print("=" * 50)
print("EDGE CASE TESTS")
print("=" * 50)

# 1. Invalid patient ID
print("\n[1] Invalid patient ID:")
print(validate_patient("P999", patients))

# 2. Invalid doctor ID
print("\n[2] Invalid doctor ID:")
print(validate_doctor("D999", doctors))

# 3. Doctor unavailable
print("\n[3] Doctor unavailable:")
doctors["D001"].available = False
test_appt = Appointment(appointment_id="T1", patient_id="P001", doctor_id="D001",
                         status="pending", tests=[])
print(validate_appointment(test_appt, patients, doctors, test_prices))
doctors["D001"].available = True  # restore

# 4. Invalid test name
print("\n[4] Invalid test name:")
print(validate_tests(["XYZ"], test_prices))

# 5. Duplicate test
print("\n[5] Duplicate test:")
print(validate_tests(["ECG", "ECG"], test_prices))

# 6. Empty test list (should be VALID, not an error)
print("\n[6] Empty test list (should be valid):")
print(validate_tests([], test_prices))

# 7. Negative / invalid age
print("\n[7] Negative age (should not crash, no discount applied):")
print(apply_senior_discount(-5, 1000))

# 8. Invalid appointment status
print("\n[8] Invalid/unknown appointment status:")
test_appt_bad_status = Appointment(appointment_id="T2", patient_id="P001", doctor_id="D001",
                                    status="unknown_status", tests=[])
print(validate_appointment(test_appt_bad_status, patients, doctors, test_prices))

# 9. Cancel a completed appointment (should be rejected)
print("\n[9] Cancel a completed appointment (A001):")
print(cancel_appointment(appointments[0]))

# 10. Process a cancelled appointment (should be rejected by validate_appointment)
print("\n[10] Process an already-cancelled appointment (A003):")
print(validate_appointment(appointments[2], patients, doctors, test_prices))

# 11. Cancel the same appointment twice
print("\n[11] Cancel same appointment twice:")
test_pending = Appointment(appointment_id="T3", patient_id="P001", doctor_id="D001",
                            status="pending", tests=[])
print("First cancel:", cancel_appointment(test_pending))
print("Second cancel:", cancel_appointment(test_pending))

# 12. Doctor with no appointments
print("\n[12] Doctor with no appointments:")
doctors["D999"] = Doctor(doctor_id="D999", name="Dr. Test", specialization="Test",
                          fee=1000, available=True)
report = generate_doctor_report(appointments, patients, doctors, test_prices)
print(report["per_doctor"]["D999"])
del doctors["D999"]  # clean up

# 13. Empty appointments list
print("\n[13] Empty appointments list (report should not crash):")
empty_report = generate_doctor_report([], patients, doctors, test_prices)
print("Per-doctor stats all zero:", all(v["appointment"] == 0 for v in empty_report["per_doctor"].values()))

# 14. Empty patients dict
print("\n[14] Empty patients dict (report should not crash):")
empty_patient_report = generate_patient_report(appointments, {}, doctors, test_prices)
print(empty_patient_report["per_patient"])

print("\n" + "=" * 50)
print("ALL EDGE CASE TESTS COMPLETED")
print("=" * 50)