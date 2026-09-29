#Validate patient
def validate_patient(patient_id, patients):
    if patient_id in patients:
        return True,None
    else:
        return False,"Patient does not exists in data"

def validate_doctor(doctor_id, doctors):
    if doctor_id in doctors:
        return True,None
    else:
        return False,"Doctor does not exists in data"

def validate_tests(requested_tests, test_prices):
    if len(requested_tests)==0:
        return True,None
    seen=set()
    for test in requested_tests:
        if test not in test_prices:
            return False, "Invalid Test"
        if test in seen:
            return False, "Duplicate"
        else:
            seen.add(test)
    return True, None

def validate_appointment(appointment, patients, doctors, test_prices):
    patient_id=appointment.patient_id
    doctor_id=appointment.doctor_id
    status=appointment.status
    tests=appointment.tests
    is_valid, reason=validate_patient(patient_id, patients)
    if not is_valid:
        return False, reason
    is_valid, reason=validate_doctor(doctor_id, doctors)
    if not is_valid:
        return False, reason
    if not doctors[doctor_id].available:
        return False, "Not available"
    if status=="cancelled":
        return False, "Rejected"
    is_valid, reason=validate_tests(tests, test_prices)
    if not is_valid:
        return False,reason
    return True,None