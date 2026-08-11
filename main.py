import json
from fastapi import FastAPI,Path,HTTPException 

app = FastAPI()

def load_data():
    with open("students_db.json", "r") as file:
        data= json.load(file)
    return data

@app.get("/")
def home():
    return {"message": "Student Management System API"}

@app.get("/about")
def about():
    return {"message": "This API is designed to manage student information and related data."} 

# GET all students

@app.get("/students")
def get_all_students():
    data = load_data()
    return data 

# GET specific student 

@app.get("/students/{student_id}")
def get_student(student_id:str = Path(...,description="The ID of the student to retrieve",example ="S001")):
    data = load_data() 
    if student_id in data:
        return data[student_id]
    else:
        raise HTTPException(status_code = 404, detail = f"Student ID {student_id} not found.")