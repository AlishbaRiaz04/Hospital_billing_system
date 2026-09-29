from dataclasses import dataclass
import json

from dataclasses import dataclass
#Data Classes
@dataclass
class Patient:
    patient_id:str
    name:str
    age: int
    city: str
    insurance: bool

@dataclass
class Doctor:
    doctor_id:str
    name:str
    specialization: str
    fee: int
    available: bool

@dataclass
class Appointment:
    appointment_id:str
    patient_id:str
    doctor_id:str
    status:str
    tests: list

def validate_data(data):
    if not isinstance(data, dict):
        raise ValueError("Data must be a dicitonary")

    if not isinstance(data.get("patients"), dict):
        raise ValueError("Patients must be a dictionary")

    if not isinstance(data.get("doctors"), dict):
        raise ValueError("Doctors must be a dicitonary")

    if not isinstance(data.get("appointments"),list):
        raise ValueError("Appointment must be a List")

    if not isinstance(data.get("test_prices"), dict):
        raise ValueError("Test prices must be a dictionary")


def create_patients(patients):
    patient_objects={}
    for patient_id,info in patients.items():
        patient=Patient(patient_id, **info)
        patient_objects[patient_id]=patient
    return patient_objects

def create_doctors(doctors):
    doctor_objects={}
    for doctor_id,info in doctors.items():
        doctor=Doctor(doctor_id, **info)
        doctor_objects[doctor_id]=doctor
    return doctor_objects

def create_appointment(appointments):
    appointment_objects=[]
    for appointment in appointments:
        appt=Appointment(**appointment)
        appointment_objects.append(appt)
    return appointment_objects

def save_results(results, filename):
    with open(filename, "w")as file:
        json.dump(results, file, indent=4)


