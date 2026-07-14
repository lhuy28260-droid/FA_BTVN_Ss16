from fastapi import FastAPI, HTTPException, status
from sqlalchemy import Column, Integer, String, ForeignKey, Table, create_engine, select
from sqlalchemy.orm import declarative_base, sessionmaker, relationship, Session

app = FastAPI(title="SQLAlchemy Many-to-Many Relationship Framework")

Base = declarative_base()


class Enrollment(Base):
    """
    Model Enrollment: Bảng trung gian liên kết (N-N)
    Chứa các khóa ngoại ràng buộc chặt chẽ tham chiếu vật lý.
    """
    __tablename__ = "enrollments"

    id = Column(Integer, primary_key=True, autoincrement=True)
    student_id = Column(Integer, ForeignKey("students.id", ondelete="CASCADE"), nullable=False)
    course_id = Column(Integer, ForeignKey("courses.id", ondelete="CASCADE"), nullable=False)


class Student(Base):
    """Model Student: Thực thể Học viên"""
    __tablename__ = "students"

    id = Column(Integer, primary_key=True, autoincrement=True)
    full_name = Column(String(100), nullable=False)
    email = Column(String(100), nullable=False, unique=True)

    courses = relationship("Course", secondary="enrollments", back_populates="students")


class Course(Base):
    """Model Course: Thực thể Khóa học"""
    __tablename__ = "courses"

    id = Column(Integer, primary_key=True, autoincrement=True)
    name = Column(String(100), nullable=False)

    students = relationship("Student", secondary="enrollments", back_populates="courses")


DATABASE_URL = "sqlite:///:memory:"
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)


Base.metadata.create_all(bind=engine)


db = SessionLocal()
try:
    
    student_1 = Student(full_name="Nguyen Van A", email="vana@gmail.com")
    student_2 = Student(full_name="Tran Thi B", email="thib@gmail.com")
    
    
    course_fastapi = Course(name="FastAPI Advanced Framework")
    course_react = Course(name="ReactJS SPA Development")
    
    
    course_fastapi.students.append(student_1)
    course_fastapi.students.append(student_2)
    course_react.students.append(student_1)
    
    db.add_all([student_1, student_2, course_fastapi, course_react])
    db.commit()
finally:
    db.close()


@app.get("/courses/{course_id}/students")
def get_students_by_course(course_id: int):
    """
    API lấy danh sách toàn bộ sinh viên đã đăng ký của một khóa học cụ thể.
    """
    session = SessionLocal()
    try:
        # Tìm kiếm khóa học theo ID
        course = session.query(Course).filter(Course.id == course_id).first()
        
        if course is None:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail=f"Không tìm thấy dữ liệu khóa học mang mã số {course_id}!"
            )
            
        result_students = []
        for s in course.students:
            result_students.append({
                "id": s.id,
                "full_name": s.full_name,
                "email": s.email
            })
            
        return {
            "status_code": 200,
            "course_name": course.name,
            "total_registered_students": len(result_students),
            "data": result_students
        }
    finally:
        session.close()