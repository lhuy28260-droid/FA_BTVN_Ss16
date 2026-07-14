
from pydantic import BaseModel, Field
from typing import List


class RegistrationInputSchema(BaseModel):
    student_id: int = Field(..., description="ID của sinh viên thực hiện đăng ký")
    workshop_id: int = Field(..., description="ID của buổi hội thảo muốn tham gia")


class SubWorkshopResponse(BaseModel):
    id: int
    title: str

    model_config = {"from_attributes": True}


class StudentWorkshopsOutputSchema(BaseModel):
    student_id: int = Field(..., alias="id") 
    full_name: str
    workshops: List[SubWorkshopResponse]

    model_config = {
        "from_attributes": True,
        "populate_by_name": True 
    }

class SubStudentResponse(BaseModel):
    id: int
    full_name: str

    model_config = {"from_attributes": True}

class WorkshopStudentsOutputSchema(BaseModel):
    workshop_id: int = Field(..., alias="id")
    title: str
    students: List[SubStudentResponse]

    model_config = {
        "from_attributes": True,
        "populate_by_name": True
    }