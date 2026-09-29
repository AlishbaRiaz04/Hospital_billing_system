from validation import validate_appointment
from billing import calculate_bill

def process_appointment(appointment, patients, doctors, test_prices):
    is_valid, reason=validate_appointment(appointment, patients, doctors, test_prices)
    if not is_valid:
        return {
            "appointment_id": appointment.appointment_id,
            "status": "rejected",
            "reason": reason,
            "bill": None
        }
    else:
        bill=calculate_bill(appointment, patients, doctors, test_prices)
        return {
            "appointment_id": appointment.appointment_id,
            "status": "accepted",
            "reason": reason,
            "bill": bill
        }

