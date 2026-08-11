import json
from fastapi import FastAPI,Path,HTTPException,Query

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
    
# Sort students 

@app.get("/sort_students")
def view_sorted_students(sorted_by:str = Query(...,
description="sort on the basis of class,age, roll,marks"),order:str = Query("asc",description="Choose order:asc or desc")):
    valid_fields = ["age","class","rool","Math marks","English marks","Science marks"]
    
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
