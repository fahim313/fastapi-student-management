import json
from fastapi import FastAPI,Path,HTTPException,Query,Body 
from pydantic import BaseModel,Field
from typing import Annotated 
app = FastAPI()

class Student(BaseModel):
    id: Annotated[str, Field(..., description="Unique ID of the student", examples=["S012"])]
    name: Annotated[str, Field(..., description="Full name of the student", examples=["Nayeem Hasan"])]
    age: Annotated[int, Field(..., gt=5, lt=19, description="Student age", examples=[15])]
    student_class: Annotated[int, Field(..., gt=0, lt=13, description="Student class", examples=[9])]
    roll: Annotated[int, Field(..., gt=0, description="Roll number", examples=[5])]
    Math_marks: Annotated[int, Field(..., gt=-1, lt=101, description="Math marks", examples=[80])]
    English_marks: Annotated[int, Field(..., gt=-1, lt=101, description="English marks", examples=[85])]
    Science_marks: Annotated[int, Field(..., gt=-1, lt=101, description="Science marks", examples=[87])]
    phone: Annotated[
        str,
        Field(
            ...,
            pattern=r"^01[3-9]\d{8}$",
            description="Bangladesh mobile phone number",
            examples=["01710000012"]
        )
    ]
    


#load data

def load_data():
    with open("students_db.json", "r") as file:
        data= json.load(file)
    return data

# save data 

def save_data(data):
    with open("students_db.json", "w") as file:
        json.dump(data, file)
        
        
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
    
# Sort students 

@app.get("/sort_students")
def view_sorted_students(sorted_by:str = Query(...,
description="sort on the basis of student_class,age, roll,marks"),order:str = Query("asc",description="Choose order:asc or desc")):
    valid_fields = ["age","student_class","rool","Math_marks","English_marks","Science_marks"]
    
    if sorted_by not in valid_fields:
        raise HTTPException(status_code=404, detail=f"Invalid field. select from{valid_fields}")
    
    if order not in ['asc','desc']:
        raise HTTPException(status_code=404,detail="choose between asc or desc")
    data = load_data()
    
    if order == 'asc':
        sorted_data = list(data.values())
        sorted_data.sort(key=lambda x: x[sorted_by]) 
        return sorted_data
     
    else:
        sorted_data = list(data.values())
        sorted_data.sort(key=lambda x: x[sorted_by],reverse=True) 
        return sorted_data 

# create student 

@app.post("/create")
def create_student(student: Student):

    data = load_data()

    if student.id in data:
        raise HTTPException(
            status_code=400,
            detail="Student already exists"
        )

    data[student.id] = student.model_dump(exclude=["id"])

    save_data(data)

    return {
        "message": "Student created successfully",
        "student_id": student.id
    }