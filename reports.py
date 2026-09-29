from billing import calculate_bill


def generate_doctor_report(appointments, patients, doctors, test_prices):
    doctor_stats={}
    for doctor_id in doctors:
        doctor_stats[doctor_id]={
            "name": doctors[doctor_id].name,
            "appointment": 0,
            "completed": 0,
            "cancelled": 0,
            "revenue": 0,
            "consultation_fee": 0,
            "test_charges": 0
        }
    for appointment in appointments:
        doctor_id=appointment.doctor_id
        if doctor_id in doctor_stats:
            doctor_stats[doctor_id]["appointment"]+=1
            if appointment.status=="completed":
                doctor_stats[doctor_id]["completed"]+=1
                bill = calculate_bill(appointment, patients, doctors, test_prices)
                subtotal = bill["subtotal"]
                doctor_stats[doctor_id]["revenue"] += subtotal
                doctor_stats[doctor_id]["consultation_fee"] += bill["consultation_fee"]
                doctor_stats[doctor_id]["test_charges"] += bill["test_charges"]
            elif appointment.status=="cancelled":
                doctor_stats[doctor_id]["cancelled"] += 1
    specialization_count={}
    for doctor_id in doctor_stats:
        specialization=doctors[doctor_id].specialization
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
            "name": patients[pid].name,
            "appointment": 0,
            "completed": 0,
            "cancelled": 0,
            "total_medical_charges": 0,
            "insurance_covered": 0,
            "patient_paid": 0,
            "consultation_fee": 0,
            "test_charges": 0
        }
        if patients[pid].insurance:
            insured_patients.append(pid)
        if patients[pid].age>=60:
            senior_citizen_patients.append(pid)
    for appointment in appointments:
        pid=appointment.patient_id
        if pid in patient_stats:
            patient_stats[pid]["appointment"]+=1
            if appointment.status=="completed":
                patient_stats[pid]["completed"]+=1
                bill=calculate_bill(appointment,patients, doctors, test_prices)
                patient_stats[pid]["insurance_covered"] += bill["insurance_covered"]
                patient_stats[pid]["consultation_fee"]+=bill["consultation_fee"]
                patient_stats[pid]["test_charges"]+=bill["test_charges"]
                patient_stats[pid]["patient_paid"]+=bill["final_amount"]
                patient_stats[pid]["total_medical_charges"]+=bill["subtotal"]
            elif appointment.status=="cancelled":
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

def generate_clinic_report(appointments, patients, doctors, test_prices):
    total_patients=len(patients)
    total_doctors=len(doctors)
    total_appointments=len(appointments)
    completed=0
    cancelled=0
    pending=0
    for appointment in appointments:
        if appointment.status=="completed":
            completed+=1
        elif appointment.status=="cancelled":
            cancelled+=1
        elif appointment.status=="pending":
            pending+=1
    patient_report=generate_patient_report(appointments, patients, doctors, test_prices)
    doctor_report=generate_doctor_report(appointments, patients, doctors, test_prices)
    highest_spending_patient=patients[patient_report["highest_spending_patient"]].name
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

