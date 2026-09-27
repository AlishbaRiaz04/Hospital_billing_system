"""Hospital Appointment and Billing System"""



patients = {
    "P001": {"name": "Ali Khan", "age": 32, "city": "Lahore", "insurance": True},
    "P002": {"name": "Ahmed Raza", "age": 45, "city": "Multan", "insurance": False},
    "P003": {"name": "Sara Ahmed", "age": 28, "city": "Lahore", "insurance": True},
    "P004": {"name": "Usman Ali", "age": 67, "city": "Islamabad", "insurance": False}
}

doctors = {
    "D001": {"name": "Dr. Hassan", "specialization": "Cardiology", "fee": 5000, "available": True},
    "D002": {"name": "Dr. Sara", "specialization": "Dermatology", "fee": 3000, "available": True},
    "D003": {"name": "Dr. Ahmed", "specialization": "General", "fee": 2000, "available": True}
}

appointments = [
    {"appointment_id": "A001", "patient_id": "P001", "doctor_id": "D001",
     "status": "completed", "tests": ["ECG", "Blood Test"]},
    {"appointment_id": "A002", "patient_id": "P002", "doctor_id": "D003",
     "status": "completed", "tests": []},
    {"appointment_id": "A003", "patient_id": "P003", "doctor_id": "D002",
     "status": "cancelled", "tests": []},
    {"appointment_id": "A004", "patient_id": "P004", "doctor_id": "D001",
     "status": "completed", "tests": ["ECG"]}
]

test_prices = {
    "ECG": 1500,
    "Blood Test": 1000,
    "X-Ray": 2500,
    "MRI": 8000
}

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
    patient_id=appointment["patient_id"]
    doctor_id=appointment["doctor_id"]
    status=appointment["status"]
    tests=appointment["tests"]
    is_valid, reason=validate_patient(patient_id, patients)
    if not is_valid:
        return False, reason
    is_valid, reason=validate_doctor(doctor_id, doctors)
    if not is_valid:
        return False, reason
    if not doctors[doctor_id]["available"]:
        return False, "Not available"
    if status=="cancelled":
        return False, "Rejected"
    is_valid, reason=validate_tests(tests, test_prices)
    if not is_valid:
        return False,reason
    return True,None

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
    doctor_id=appointment["doctor_id"]
    patient_id=appointment["patient_id"]
    tests=appointment["tests"]
    consultation_fee=doctors[doctor_id]["fee"]
    age=patients[patient_id]["age"]
    insurance_enabled=patients[patient_id]["insurance"]
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
    status=appointment["status"]
    if status=="completed":
        return False, "Cannot cancel a compeleted appointment"
    elif status=="cancelled":
        return False, "Already cancelled"
    elif status=="pending":
        appointment["status"]="cancelled"
        return True,None

def generate_doctor_report(appointments, patients, doctors, test_prices):
    doctor_stats={}
    for doctor_id in doctors:
        doctor_stats[doctor_id]={
            "name": doctors[doctor_id]["name"],
            "appointment": 0,
            "completed": 0,
            "cancelled": 0,
            "revenue": 0,
            "consultation_fee": 0,
            "test_charges": 0
        }
    for appointment in appointments:
        doctor_id=appointment["doctor_id"]
        if doctor_id in doctor_stats:
            doctor_stats[doctor_id]["appointment"]+=1
            if appointment["status"]=="completed":
                doctor_stats[doctor_id]["completed"]+=1
                bill = calculate_bill(appointment, patients, doctors, test_prices)
                subtotal = bill["subtotal"]
                doctor_stats[doctor_id]["revenue"] += subtotal
                doctor_stats[doctor_id]["consultation_fee"] += bill["consultation_fee"]
                doctor_stats[doctor_id]["test_charges"] += bill["test_charges"]
            elif appointment["status"]=="cancelled":
                doctor_stats[doctor_id]["cancelled"] += 1
    specialization_count={}
    for doctor_id in doctor_stats:
        specialization=doctors[doctor_id]["specialization"]
        if specialization in specialization_count:
            specialization_count[specialization]+=doctor_stats[doctor_id]["appointment"]
        else:
            specialization_count[specialization]=doctor_stats[doctor_id]["appointment"]
        revenue=doctor_stats[doctor_id]["revenue"]
        completed_count=doctor_stats[doctor_id]["completed"]
        if doctor_stats[doctor_id]["completed"]>0:
            doctor_stats[doctor_id]["average_bill"]=revenue/completed_count
        else:
            doctor_stats[doctor_id]["average_bill"]=0
    most_requested_doctor = max(doctor_stats, key=lambda doctor_id: doctor_stats[doctor_id]["appointment"])
    most_requested_specialization = max(specialization_count, key=lambda specialization: specialization_count[specialization])
    return {
        "per_doctor": doctor_stats,
        "most_requested_doctor": most_requested_doctor,
        "most_requested_specialization": most_requested_specialization
    }

def generate_patient_report(appointments, patients, doctors, test_prices):
    patient_stats={}
    insured_patients=[]
    senior_citizen_patients=[]
    for pid in patients:
        patient_stats[pid]={
            "name": patients[pid]["name"],
            "appointment": 0,
            "completed": 0,
            "cancelled": 0,
            "total_medical_charges": 0,
            "insurance_covered": 0,
            "patient_paid": 0,
            "consultation_fee": 0,
            "test_charges": 0
        }
        if patients[pid]["insurance"]:
            insured_patients.append(pid)
        if patients[pid]["age"]>=60:
            senior_citizen_patients.append(pid)
    for appointment in appointments:
        pid=appointment["patient_id"]
        if pid in patient_stats:
            patient_stats[pid]["appointment"]+=1
            if appointment["status"]=="completed":
                patient_stats[pid]["completed"]+=1
                bill=calculate_bill(appointment,patients, doctors, test_prices)
                patient_stats[pid]["insurance_covered"] += bill["insurance_covered"]
                patient_stats[pid]["consultation_fee"]+=bill["consultation_fee"]
                patient_stats[pid]["test_charges"]+=bill["test_charges"]
                patient_stats[pid]["patient_paid"]+=bill["final_amount"]
                patient_stats[pid]["total_medical_charges"]+=bill["subtotal"]
            elif appointment["status"]=="cancelled":
                patient_stats[pid]["cancelled"]+=1
    if len(patient_stats)>0:
        highest_spending_patient=max(patient_stats, key=lambda pid: patient_stats[pid]["patient_paid"])
        patient_with_most_appointments=max(patient_stats, key=lambda pid: patient_stats[pid]["appointment"])
        patients_with_no_completed_appointment=[pid for pid in patient_stats if patient_stats[pid]["completed"]==0]
    else:
        highest_spending_patient=None
        patient_with_most_appointments=None
        patients_with_no_completed_appointment=None
    return {
        "per_patient": patient_stats,
        "highest_spending_patient": highest_spending_patient,
        "patients_with_most_appointments": patient_with_most_appointments,
        "patients_with_no_completed_appointment": patients_with_no_completed_appointment,
        "insured_patients": insured_patients,
        "senior_citizen_patients": senior_citizen_patients
    }

def process_appointment(appointment, patients, doctors, test_prices):
    is_valid, reason=validate_appointment(appointment, patients, doctors, test_prices)
    if not is_valid:
        return {
            "appointment_id": appointment["appointment_id"],
            "status": "rejected",
            "reason": reason,
            "bill": None
        }
    else:
        bill=calculate_bill(appointment, patients, doctors, test_prices)
        return {
            "appointment_id": appointment["appointment_id"],
            "status": "accepted",
            "reason": reason,
            "bill": bill
        }

def generate_clinic_report(appointments, patients, doctors, test_prices):
    total_patients=len(patients)
    total_doctors=len(doctors)
    total_appointments=len(appointments)
    completed=0
    cancelled=0
    pending=0
    for appointment in appointments:
        if appointment["status"]=="completed":
            completed+=1
        elif appointment["status"]=="cancelled":
            cancelled+=1
        elif appointment["status"]=="pending":
            pending+=1
    patient_report=generate_patient_report(appointments, patients, doctors, test_prices)
    doctor_report=generate_doctor_report(appointments, patients, doctors, test_prices)
    highest_spending_patient=patients[patient_report["highest_spending_patient"]]["name"]
    total_consultation_revenue=0
    total_insurance_covered=0
    total_patient_revenue=0
    total_test_revenue=0
    for patient in patient_report["per_patient"].values():
        total_consultation_revenue+=patient["consultation_fee"]
        total_insurance_covered+=patient["insurance_covered"]
        total_patient_revenue+=patient["patient_paid"]
    for doctor in doctor_report["per_doctor"].values():
        total_test_revenue+=doctor["test_charges"]

    print("=" * 50)
    print(f"CLINIC DASHBOARD".center(50))
    print("="*50)
    print(f"Total Patients: {total_patients}")
    print(f"Total Doctors: {total_doctors}")
    print(f"Total Appointments: {total_appointments}")
    print(f"Completed: {completed}")
    print(f"Cancelled: {cancelled}")
    print(f"Pending: {pending}")
    print(f"Total Consultation Revenue: ${total_consultation_revenue}")
    print(f"Total Test Revenue: ${total_test_revenue}")
    print(f"Total Insurance Coverage: ${total_insurance_covered}")
    print(f"Total Patient Revenue: ${total_patient_revenue}")
    print(f"Most Requested Specialization: {doctor_report['most_requested_specialization']}")
    print(f"Highest Spending Patient: {highest_spending_patient}")
    print("="*50)



if __name__ == "__main__":
    print("Processing all appointments...\n")
    results = []
    for appointment in appointments:
        result = process_appointment(appointment, patients, doctors, test_prices)
        results.append(result)
        print(result)

    print()
    generate_clinic_report(appointments, patients, doctors, test_prices)


