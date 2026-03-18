# 🏥 FastAPI Medical Appointment System

🚀 A complete backend application built using **FastAPI** as part of the **Feb Internship 2026 Final Project** at Innomatics Research Labs.

This project demonstrates real-world backend development concepts including API design, validation, CRUD operations, workflows, and advanced querying.

---

## 📌 Project Objective

To build a fully functional FastAPI backend system implementing:

- GET APIs
- POST APIs with Pydantic validation
- Helper functions
- CRUD operations
- Multi-step workflows
- Search, Sorting, and Pagination

---

## 🧠 Features Implemented

✅ RESTful API Design (GET, POST, PUT, DELETE)  
✅ Pydantic Data Validation  
✅ Helper Functions for Business Logic  
✅ Full CRUD Operations  
✅ Multi-step Appointment Workflow  
✅ Search Functionality  
✅ Sorting (Ascending/Descending)  
✅ Pagination Support  
✅ Swagger UI Testing  

---

## 🔄 Workflow Implemented

Appointment Lifecycle:

1. **Create Appointment** → status = scheduled  
2. **Confirm Appointment** → status = confirmed  
3. **Complete Appointment** → status = completed  
4. **Cancel Appointment** → status = cancelled  

---

## 📡 API Endpoints Overview

### 🔹 GET APIs
- `/` → Home route  
- `/doctors` → List all doctors  
- `/doctors/{id}` → Get doctor by ID  
- `/appointments` → List appointments  
- `/appointments/count` → Total appointments  

---

### 🔹 POST APIs
- `/appointments` → Create appointment  
- `/doctors` → Add new doctor  

---

### 🔹 PUT APIs
- `/doctors/{id}` → Update doctor  

---

### 🔹 DELETE APIs
- `/doctors/{id}` → Delete doctor  

---

### 🔹 Workflow APIs
- `/appointments/{id}/confirm`  
- `/appointments/{id}/cancel`  
- `/appointments/{id}/complete`  

---

### 🔹 Advanced APIs
- `/doctors/search` → Search by specialization  
- `/doctors/sort` → Sort doctors  
- `/doctors/page` → Pagination  
- `/appointments/search`  
- `/appointments/sort`  
- `/appointments/page`  
- `/doctors/browse` → Combined search + sort + pagination  

---

## 🛠️ Technologies Used

- Python 3.x  
- FastAPI  
- Pydantic  
- Uvicorn  

---

## ⚙️ Installation & Setup

### 1️⃣ Clone Repository
```bash
git clone https://github.com/your-username/fastapi-medical-appointment-system.git
cd fastapi-medical-appointment-system
2️⃣ Install Dependencies
pip install -r requirements.txt
3️⃣ Run the Application
uvicorn main:app --reload
4️⃣ Open Swagger UI

👉 http://127.0.0.1:8000/docs

📸 Screenshots

All API endpoints are tested in Swagger UI.

Screenshots are available in the screenshots/ folder:

Q1_home_route.png

Q2_get_doctors.png

...

Q20_browse.png

## 📂 Project Structure
fastapi-medical-appointment-system/
│
├── main.py
├── requirements.txt
├── README.md
└── screenshots/
⚠️ Important Notes

All 20 endpoints are implemented and tested

Route order is maintained correctly

Proper error handling included

Uses in-memory storage (no database)

📢 Acknowledgement

Grateful to Innomatics Research Labs for providing this opportunity to learn and build real-world backend applications.

🔗 Author

Atharv Atmaram Jadhav
📧 atharvjadhav1112@gmail.com

🔗 LinkedIn: https://www.linkedin.com/in/atharv-jadhav-6044032b2

📌 Tags

#FastAPI #Python #BackendDevelopment #APIs #Internship #WebDevelopment