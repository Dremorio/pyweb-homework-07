from models import Group, Lector, Student, Subject, StudentMark
from db import session

from sqlalchemy import func, desc

"""

Знайти 5 студентів із найбільшим середнім балом з усіх предметів.
Знайти студента із найвищим середнім балом з певного предмета.
Знайти середній бал у групах з певного предмета.
Знайти середній бал на потоці (по всій таблиці оцінок).
Знайти які курси читає певний викладач.
Знайти список студентів у певній групі.
Знайти оцінки студентів у окремій групі з певного предмета.
Знайти середній бал, який ставить певний викладач зі своїх предметів.
Знайти список курсів, які відвідує певний студент.
Список курсів, які певному студенту читає певний викладач.
Середній бал, який певний викладач ставить певному студентові.
Оцінки студентів у певній групі з певного предмета на останньому занятті.

"""


def select_1():
    return session.query(Student.name, func.round(func.avg(StudentMark.mark), 2).label('avg_mark')) \
        .select_from(StudentMark).join(Student).group_by(Student.id).order_by(desc('avg_mark')).limit(5).all()


def select_2(id_subject):
    return session.query(Student.name, Subject.subject, func.round(func.avg(StudentMark.mark), 2).label('avg_mark')) \
        .select_from(StudentMark).join(Student).join(Subject).filter(Subject.id == id_subject) \
        .group_by(Student.id, Subject.subject) \
        .order_by(desc('avg_mark')).first()


def select_3(id_subject):
    return session.query(Group.group_char, Subject.subject,
                         func.round(func.avg(StudentMark.mark), 2).label('avg_mark')). \
        select_from(Student).join(StudentMark, Student.id == StudentMark.student_id). \
        join(Subject, Subject.id == StudentMark.subject_id). \
        join(Group, Group.group_char == Student.group_char).filter(Subject.id == id_subject). \
        group_by(Group.group_char, Subject.subject). \
        order_by(Group.group_char).all()


def select_4():
    return session.query(func.round(func.avg(StudentMark.mark), 2).label('avg_mark')).select_from(StudentMark).first()


def select_5(id_lector):
    return session.query(Lector.name, Subject.subject).select_from(Subject). \
        join(Lector, Subject.lectors_id == Lector.id).filter(Lector.id == id_lector).all()


def select_6(gr_chr):
    return session.query(Group.group_char, Student.name).select_from(Group). \
        join(Student, Group.group_char == Student.group_char).filter(Group.group_char == gr_chr).all()


def select_7(gr_chr, id_subject):
    return session.query(Student.name, StudentMark.mark, Group.group_char, Subject.subject). \
        select_from(Student).join(StudentMark, Student.id == StudentMark.student_id). \
        join(Group, Student.group_char == Group.group_char). \
        join(Subject, Subject.id == StudentMark.subject_id). \
        filter(Group.group_char == gr_chr, Subject.id == id_subject). \
        order_by(desc(StudentMark.mark)).all()


def select_8(id_lector):
    return session.query(Subject.subject, Lector.name, func.round(func.avg(StudentMark.mark), 2).label('avg_mark')). \
        select_from(StudentMark).join(Subject, Subject.id == StudentMark.subject_id). \
        join(Lector, Lector.id == Subject.lectors_id).filter(Lector.id == id_lector). \
        group_by(Subject.subject, Lector.name).all()


def select_9(id_student):
    return session.query(Student.name, Subject.subject).select_from(Student). \
        join(StudentMark, Student.id == StudentMark.student_id). \
        join(Subject, Subject.id == StudentMark.subject_id).filter(Student.id == id_student). \
        group_by(Student.name, Subject.subject).all()


def select_10(id_student, id_lector):
    return session.query(Subject.subject, Student.name, Lector.name).select_from(Subject). \
        join(StudentMark, StudentMark.subject_id == Subject.id). \
        join(Lector, Lector.id == Subject.lectors_id). \
        join(Student, Student.id == StudentMark.student_id). \
        filter(Student.id == id_student, Lector.id == id_lector). \
        group_by(Subject.subject, Student.name, Lector.name).all()


def select_11(id_student, id_lector):
    return session.query(Student.name, Lector.name, func.round(func.avg(StudentMark.mark), 2).label('avg_mark')). \
        select_from(Student).join(StudentMark, StudentMark.student_id == Student.id). \
        join(Subject, Subject.id == StudentMark.subject_id). \
        join(Lector, Lector.id == Subject.lectors_id). \
        filter(Student.id == id_student, Lector.id == id_lector).\
        group_by(Student.name, Lector.name). \
        order_by(Lector.name, Student.name).first()


def select_12(gr_ch, id_subject):
    subquery = session.query(func.max(StudentMark.date).label('max_date')) \
        .join(Student, Student.id == StudentMark.student_id) \
        .join(Group, Group.group_char == Student.group_char) \
        .join(Subject, Subject.id == StudentMark.subject_id) \
        .filter(Group.group_char == gr_ch, Subject.id == id_subject) \
        .scalar()

    return session.query(Student.name, StudentMark.mark, StudentMark.date) \
        .join(StudentMark, Student.id == StudentMark.student_id) \
        .join(Group, Group.group_char == Student.group_char) \
        .join(Subject, Subject.id == StudentMark.subject_id) \
        .filter(Group.group_char == gr_ch, Subject.id == id_subject, StudentMark.date == subquery) \
        .all()
