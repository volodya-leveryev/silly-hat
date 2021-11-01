""" Модели данных """
from enum import Enum

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


class Person(db.Model):
    """ Человек """
    # обязательные поля
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)  # имя
    surname = db.Column(db.String(50), nullable=False)  # фамилия
    # ссылки на пользователя
    users = db.relationship('User', backref='person', lazy=True)
    # ссылки на курсы обучения
    courses = db.relationship('Course', backref='person', lazy=True)
    # опциональные поля
    patronymic = db.Column(db.String(50), default='')  # отчество
    maiden = db.Column(db.String(50), default='')  # девичья фамилия
    phones = db.Column(db.String(50), default='')  # телефоны
    notes = db.Column(db.Text, default='')  # примечания


class User(db.Model):
    """ Пользователь """
    # обязательные поля
    id = db.Column(db.Integer, primary_key=True)
    logins = db.Column(db.String(50), nullable=False)  # логины
    permissions = db.Column(db.Integer, nullable=False)  # права доступа
    # ссылка на человека
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'),
                          nullable=False)
    # опциональные поля
    notes = db.Column(db.Text, default='')  # примечания

    def is_admin(self) -> bool:
        mask = 2 ** 1
        return bool(self.permissions % mask)


class Degree(Enum):
    """ Квалификации """
    BACHELOR = 1  # бакалавр
    MASTER = 2  # магистр
    PHD = 3  # кандидит наук


class EduGroup(db.Model):
    """ Учебная группа """
    # обязательные поля
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)  # название
    year = db.Column(db.Integer, nullable=False)  # год поступления
    degree = db.Column(db.Enum(Degree), nullable=False)  # квалификация
    students = db.Column(db.Integer, nullable=False)  # количество студентов
    # ссылки на курсы обучения
    courses = db.relationship('Course', backref='edu_group', lazy=True)
    # опциональные поля
    notes = db.Column(db.Text, default='')  # примечания


class Room(db.Model):
    """ Аудитория """
    # обязательные поля
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)  # название
    building = db.Column(db.String(50), nullable=False)  # корпус
    # ссылки на занятия
    events = db.relationship('Event', backref='room', lazy=True)
    # опциональные поля
    capacity = db.Column(db.Integer)  # количество мест
    notes = db.Column(db.Text, default='')  # примечания


class Control(Enum):
    credit = 1  # зачет
    credit_grade = 2  # зачет с оценкой
    exam = 3  # экзамен


class Course(db.Model):
    """ Учебный курс """
    # обязательные поля
    id = db.Column(db.Integer, primary_key=True)
    code = db.Column(db.String(15), nullable=False)  # шифр
    name = db.Column(db.String(50), nullable=False)  # название
    elective = db.Column(db.Boolean, nullable=False)  # выборная
    credits = db.Column(db.Integer, nullable=False)  # зачетные единицы
    controls = db.Column(db.Integer, nullable=False)  # формы контроля (список)
    begin = db.Column(db.Date, nullable=False)  # дата начала
    end = db.Column(db.Date, nullable=False)  # дата окончания
    # ссылка на преподавателя
    person_id = db.Column(db.Integer, db.ForeignKey('person.id'), nullable=True)
    # ссылка на учебную группу
    edu_group_id = db.Column(db.Integer, db.ForeignKey('edu_group.id'),
                             nullable=False)
    # ссылки на занятия
    events = db.relationship('Event', backref='course', lazy=True)
    # опциональные поля
    notes = db.Column(db.Text, default='')  # примечания

    def has_control(self, control: Control) -> bool:
        mask = 2 ** control.value
        return bool(self.controls % mask)


class Event(db.Model):
    """ Событие """

    class Forms(Enum):
        lecture = 1  # лекция
        practice = 2  # практическое занятие
        lab_work = 3  # лабораторная работа
        exam = 4  # экзамен

    # обязательные поля
    id = db.Column(db.Integer, primary_key=True)
    begin = db.Column(db.DateTime, nullable=False)  # дата и время начала
    end = db.Column(db.DateTime, nullable=False)  # дата и время окончания
    name = db.Column(db.String(50), nullable=False)  # название
    # ссылка на учебный курс
    course_id = db.Column(db.Integer, db.ForeignKey('course.id'), nullable=True)
    # ссылка на аудиторию
    room_id = db.Column(db.Integer, db.ForeignKey('room.id'), nullable=False)
    # опциональные поля
    type = db.Column(db.Enum(Forms))  # тип занятия
    notes = db.Column(db.Text, default='')  # примечания
