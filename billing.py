def calculate_test_charges(requested_tests, test_prices):
    total_test_charges=0
    for test in requested_tests:
        price=test_prices[test]
        total_test_charges+=price

    return total_test_charges


def apply_insurance_coverage(consultation_fee, test_charges, insurance_enabled):
    if insurance_enabled:
        total_covered=(consultation_fee*0.20)+(test_charges*0.50)
        return total_covered
    else:
        return 0

def apply_senior_discount(age, amount_after_insurance):
    if age>=60:
        return amount_after_insurance*0.10
    else:
        return 0

def calculate_bill(appointment, patients, doctors, test_prices):
    doctor_id=appointment.doctor_id
    patient_id=appointment.patient_id
    tests=appointment.tests
    consultation_fee=doctors[doctor_id].fee
    age=patients[patient_id].age
    insurance_enabled=patients[patient_id].insurance
    test_charges=calculate_test_charges(tests, test_prices)
    subtotal=consultation_fee + test_charges
    insurance_covered=apply_insurance_coverage(consultation_fee, test_charges, insurance_enabled)
    amount_after_insurance=subtotal - insurance_covered
    discount = apply_senior_discount(age, amount_after_insurance)
    final_amount=amount_after_insurance - discount

    return {
        "consultation_fee": consultation_fee,
        "test_charges":test_charges,
        "subtotal":subtotal,
        "insurance_covered": insurance_covered,
        "discount": discount,
        "final_amount": final_amount
    }

def cancel_appointment(appointment):
    status=appointment.status
    if status=="completed":
        return False, "Cannot cancel a compeleted appointment"
    elif status=="cancelled":
        return False, "Already cancelled"
    elif status=="pending":
        appointment.status="cancelled"
        return True,None
