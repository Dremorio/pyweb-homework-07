from sqlalchemy import Column, Integer, String, ForeignKey, Date
from sqlalchemy.orm import relationship
from db import Base


class Group(Base):
    __tablename__ = 'groups'
    group_char = Column(String(1), primary_key=True)
    students = relationship('Student', back_populates='group')


class Lector(Base):
    __tablename__ = 'lectors'
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    subjects = relationship('Subject', back_populates='lector')


class Student(Base):
    __tablename__ = 'students'
    id = Column(Integer, primary_key=True)
    name = Column(String(30))
    group_char = Column(String(1), ForeignKey('groups.group_char'))
    group = relationship('Group', back_populates='students')
    marks = relationship('StudentMark', back_populates='student')


class Subject(Base):
    __tablename__ = 'subjects'
    id = Column(Integer, primary_key=True)
    subject = Column(String(30))
    lectors_id = Column(Integer, ForeignKey('lectors.id'))
    lector = relationship('Lector', back_populates='subjects')
    marks = relationship('StudentMark', back_populates='subject')


class StudentMark(Base):
    __tablename__ = 'student_marks'
    id = Column(Integer, primary_key=True)
    student_id = Column(Integer, ForeignKey('students.id'))
    subject_id = Column(Integer, ForeignKey('subjects.id'))
    mark = Column(Integer)
    date = Column(Date)
    student = relationship('Student', back_populates='marks')
    subject = relationship('Subject', back_populates='marks')

