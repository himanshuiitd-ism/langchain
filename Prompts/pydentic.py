from pydantic import BaseModel,EmailStr,Field
from typing import Optional

class Student(BaseModel):
  name: str = 'Himanshu'
  age: Optional[int] = None
  email : EmailStr # validates the email (builtin)
  cgpa: float = Field(gt = 0, lt = 10, default=5, description='A decimal value representing the cgpa of the student')


new_student= {'age':'32','cgpa' : 7.909090, 'email':'hi@gmail.com'}

student = Student(**new_student)
print(student)
print(type(student))

# We can also convert this python object into dict or json

student_dict = dict(student)
print(student_dict['age'])
student_json = student.model_dump_json()
print(student_json)