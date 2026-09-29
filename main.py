import json
from models import validate_data, create_patients, create_doctors, create_appointment, save_results
from processing import process_appointment
from reports import generate_clinic_report

"""Hospital Appointment and Billing System"""

if __name__ == "__main__":

    try:
        with open("input_data.json", "r") as file:
            data=json.load(file)
            validate_data(data)

        # Creating patient objects
        patient_objects = create_patients(data["patients"])

        # Creating doctor objects
        doctor_objects = create_doctors(data["doctors"])

        # creating appointment objects
        appointment_objects = create_appointment(data["appointments"])

        test_prices=data["test_prices"]

        results=[]

        for appointment in appointment_objects:
            result = process_appointment(appointment, patient_objects, doctor_objects, test_prices)
            results.append(result)

        save_results(results, "output_data.json")

        generate_clinic_report(appointment_objects, patient_objects, doctor_objects, test_prices)
    except FileNotFoundError:
        print("Error: input_data.json file not found")

    except json.JSONDecodeError:
        print("Error: Invalid JSON format in data.json")

    except ValueError as e:
        print(f"Error: {e}")



