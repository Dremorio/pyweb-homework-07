from models import Group, Lector, Student, Subject, StudentMark
from db import session
from random import randint, sample, choice
from faker import Faker

fake = Faker()

GROUPS = 3
STUDENTS = randint(30, 50)
SUBJECTS_NUM = randint(5, 8)
LECTORS = randint(3, 5)
MARKS = randint(0, 20)

GROUPS_LST = ['A', 'B', 'C']
SUBJECTS_LST = ["Physics", "Chemistry", "Biology", "Mathematics",
                "Computer Science", "History", "Literature", "Economy"]
SUBJECTS = sample(SUBJECTS_LST, SUBJECTS_NUM)


def create_groups(num):
    groups = [Group(group_char=GROUPS_LST[i]) for i in range(num)]
    session.add_all(groups)
    session.commit()


def create_lectors(num):
    lectors = [Lector(name=fake.name()) for _ in range(num)]
    session.add_all(lectors)
    session.commit()


def create_students(num):
    groups = session.query(Group).all()
    students = [Student(name=fake.name(), group_char=choice(groups).group_char) for _ in range(num)]
    session.add_all(students)
    session.commit()


def create_subjects(num):
    lectors = session.query(Lector).all()
    subjects = [Subject(subject=SUBJECTS[i], lectors_id=choice(lectors).id) for i in range(num)]
    session.add_all(subjects)
    session.commit()


def create_student_marks(num):
    subjects = session.query(Subject).all()
    for student in session.query(Student).all():
        for i in range(num):
            mark = StudentMark(
                student_id=student.id,
                subject_id=choice(subjects).id,
                mark=fake.random_int(min=1, max=100),
                date=fake.date_between(start_date='-1y', end_date='today')
            )
            session.add(mark)
    session.commit()


if __name__ == '__main__':
    create_groups(GROUPS)
    create_lectors(LECTORS)
    create_students(STUDENTS)
    create_subjects(SUBJECTS_NUM)
    create_student_marks(MARKS)
