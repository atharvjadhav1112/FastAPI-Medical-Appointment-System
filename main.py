from fastapi import FastAPI, HTTPException, Query
from pydantic import BaseModel, Field
from typing import Optional

app = FastAPI(title="Medical Appointment System")

# ------------------------------
# DATA STORAGE
# ------------------------------
doctors = [
    {"id": 1, "name": "Dr. Hathi", "specialization": "Cardiologist", "fee": 500, "experience_years": 10, "is_available": True},
    {"id": 2, "name": "Dr. Mehta", "specialization": "Dermatologist", "fee": 400, "experience_years": 8, "is_available": True},
    {"id": 3, "name": "Dr. Sodi", "specialization": "Pediatrician", "fee": 300, "experience_years": 5, "is_available": True},
    {"id": 4, "name": "Dr. Bhide", "specialization": "General", "fee": 200, "experience_years": 4, "is_available": True},
    {"id": 5, "name": "Dr. Gada", "specialization": "Dentist", "fee": 600, "experience_years": 8, "is_available": True},
    {"id": 6, "name": "Dr. Iyer", "specialization": "Neurologist", "fee": 350, "experience_years": 9, "is_available": True},
]

appointments = []
appt_counter = 1
doctor_counter = 7  

# ------------------------------
# HELPERS
# ------------------------------
def find_doctor(doctor_id):
    return next((d for d in doctors if d["id"] == doctor_id), None)

def find_appointment(appt_id):
    return next((a for a in appointments if a["id"] == appt_id), None)

def calculate_fee(base_fee, appointment_type):
    if appointment_type == "video":
        return base_fee * 0.8
    elif appointment_type == "emergency":
        return base_fee * 1.5
    return base_fee

def filter_doctors_logic(specialization, max_fee, min_exp, is_available):
    result = doctors
    if specialization is not None:
        result = [d for d in result if d["specialization"].lower() == specialization.lower()]
    if max_fee is not None:
        result = [d for d in result if d["fee"] <= max_fee]
    if min_exp is not None:
        result = [d for d in result if d["experience_years"] >= min_exp]
    if is_available is not None:
        result = [d for d in result if d["is_available"] == is_available]
    return result

# ------------------------------
# MODELS
# ------------------------------
class AppointmentRequest(BaseModel):
    patient_name: str = Field(min_length=2)
    doctor_id: int = Field(gt=0)
    date: str
    reason: str = Field(min_length=5)
    appointment_type: str = "in-person"

class DoctorModel(BaseModel):
    name: str = Field(min_length=2)
    specialization: str
    fee: int = Field(gt=0)
    experience_years: int = Field(gt=0)
    is_available: bool = True

# ------------------------------
# DAY 1 — GET APIs
# ------------------------------

@app.get("/")
def home():
    return {"message": "Medical Appointment System API"}

@app.get("/doctors")
def get_doctors():
    return {
        "total": len(doctors),
        "available": len([d for d in doctors if d["is_available"]]),
        "data": doctors
    }

@app.get("/appointments")
def get_appointments():
    return appointments

@app.get("/appointments/count")
def get_appointment_count():
    return {"total_appointments": len(appointments)}

# ------------------------------
# DAY 2 — POST
# ------------------------------

@app.post("/appointments", status_code=201)
def create_appointment(data: AppointmentRequest):
    global appt_counter

    doctor = find_doctor(data.doctor_id)
    if not doctor:
        raise HTTPException(404, "Doctor not found")

    if not doctor["is_available"]:
        raise HTTPException(400, "Doctor not available")

    fee = calculate_fee(doctor["fee"], data.appointment_type)

    appointment = {
        "id": appt_counter,
        "patient_name": data.patient_name,
        "doctor_id": data.doctor_id,
        "date": data.date,
        "reason": data.reason,
        "type": data.appointment_type,
        "fee": fee,
        "status": "scheduled"
    }

    appointments.append(appointment)
    appt_counter += 1

    return appointment

# ------------------------------
# DAY 3 — FILTER (FIXED ROUTE ORDER)
# ------------------------------

@app.get("/doctors/filter")
def filter_doctors(
    specialization: Optional[str] = None,
    max_fee: Optional[int] = None,
    min_exp: Optional[int] = None,
    is_available: Optional[bool] = None
):
    return filter_doctors_logic(specialization, max_fee, min_exp, is_available)

@app.get("/doctors/search")
def search_doctors(keyword: str):
    return [d for d in doctors if keyword.lower() in d["specialization"].lower()]

@app.get("/doctors/sort")
def sort_doctors(sort_by: str = "fee", order: str = "asc"):
    reverse = order == "desc"
    return sorted(doctors, key=lambda x: x.get(sort_by, 0), reverse=reverse)

@app.get("/doctors/page")
def paginate_doctors(page: int = 1, limit: int = 2):
    start = (page - 1) * limit
    return doctors[start:start + limit]

@app.get("/doctors/browse")
def browse_doctors(
    keyword: Optional[str] = None,
    sort_by: Optional[str] = None,
    order: str = "asc",
    page: int = 1,
    limit: int = 2
):
    result = doctors

    if keyword:
        result = [d for d in result if keyword.lower() in d["specialization"].lower()]

    if sort_by:
        reverse = order == "desc"
        result = sorted(result, key=lambda x: x.get(sort_by, 0), reverse=reverse)

    start = (page - 1) * limit
    return result[start:start + limit]

# ------------------------------
# DAY 4 — CRUD
# ------------------------------

@app.post("/doctors", status_code=201)
def add_doctor(doc: DoctorModel):
    global doctor_counter

    new_doc = doc.dict()
    new_doc["id"] = doctor_counter
    doctors.append(new_doc)

    doctor_counter += 1
    return new_doc

@app.put("/doctors/{doctor_id}")
def update_doctor(doctor_id: int, doc: DoctorModel):
    doctor = find_doctor(doctor_id)
    if not doctor:
        raise HTTPException(404, "Doctor not found")

    doctor.update(doc.dict())
    return doctor

@app.delete("/doctors/{doctor_id}")
def delete_doctor(doctor_id: int):
    doctor = find_doctor(doctor_id)
    if not doctor:
        raise HTTPException(404, "Doctor not found")

    doctors.remove(doctor)
    return {"message": "Doctor deleted"}

# ------------------------------
# DAY 5 — WORKFLOW
# ------------------------------

@app.post("/appointments/{id}/confirm")
def confirm_appointment(id: int):
    appt = find_appointment(id)
    if not appt:
        raise HTTPException(404, "Appointment not found")

    appt["status"] = "confirmed"
    return appt

@app.post("/appointments/{id}/cancel")
def cancel_appointment(id: int):
    appt = find_appointment(id)
    if not appt:
        raise HTTPException(404, "Appointment not found")

    appt["status"] = "cancelled"
    return appt

@app.post("/appointments/{id}/complete")
def complete_appointment(id: int):
    appt = find_appointment(id)
    if not appt:
        raise HTTPException(404, "Appointment not found")

    appt["status"] = "completed"
    return appt

# ------------------------------
# DAY 6 — APPOINTMENT ADVANCED
# ------------------------------

@app.get("/appointments/search")
def search_appointments(status: Optional[str] = None):
    if status:
        return [a for a in appointments if a["status"] == status]
    return appointments

@app.get("/appointments/sort")
def sort_appointments(order: str = "asc"):
    reverse = order == "desc"
    return sorted(appointments, key=lambda x: x["fee"], reverse=reverse)

@app.get("/appointments/page")
def paginate_appointments(page: int = 1, limit: int = 2):
    start = (page - 1) * limit
    return appointments[start:start + limit]


@app.get("/doctors/{doctor_id}")
def get_doctor(doctor_id: int):
    doctor = find_doctor(doctor_id)
    if not doctor:
        raise HTTPException(404, "Doctor not found")
    return doctor