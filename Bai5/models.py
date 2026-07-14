from sqlalchemy import Column, Integer, String, ForeignKey, DateTime
from sqlalchemy.orm import relationship
from datetime import datetime
from database import Base

class Registration(Base):
    """
    Model Registration: Bảng trung gian liên kết (N-N)
    Chứa các ràng buộc khóa ngoại chặt chẽ cấp độ Database để tránh dữ liệu rác.
    """
    __tablename__ = "registrations"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    workshop_id = Column(Integer, ForeignKey("workshops.id", ondelete="CASCADE"), nullable=False)
    registered_at = Column(DateTime, default=datetime.utcnow, nullable=False)


class Student(Base):
    """Model Student: Thực thể Sinh viên"""
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_code = Column(String(20), unique=True, nullable=False, index=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), unique=True, nullable=False)

    workshops = relationship("Workshop", secondary="registrations", back_populates="students")


class Workshop(Base):
    """Model Workshop: Thực thể Buổi hội thảo ngắn hạn"""
    __tablename__ = "workshops"

    id = Column(Integer, primary_key=True, autoincrement=True)
    title = Column(String(150), nullable=False)
    maximum_participants = Column(Integer, nullable=False)

    students = relationship("Student", secondary="registrations", back_populates="workshops")