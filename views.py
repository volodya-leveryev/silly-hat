""" Функции представления """
from functools import wraps
from typing import Callable

from authlib.integrations.flask_client import OAuth
from flask import (Response, redirect, render_template, request, session,
                   url_for)

import models

oauth = OAuth()


def admin_required(func: Callable) -> Callable:
    @wraps(func)
    def wrapper(*args, **kwargs) -> Response:
        if 'user' in session:
            return func(*args, **kwargs)
        return redirect(url_for('home'))
    return wrapper


def home():
    """
    Главная страница
    Содержит ссылки на страницу аутентификации и страницы просмотра расписаний.
    """
    context = {
        'groups': [],
        'teachers': [],
        'rooms': [],
    }
    return render_template('home.html', **context)


def auth_init():
    """ Начало аутентификации """
    redirect_uri = url_for('auth_done', _external=True)
    # return oauth.google.authorize_redirect(redirect_uri)
    return oauth.azure.authorize_redirect(redirect_uri)


def auth_done():
    """ Завершение аутентификации """
    # token = oauth.google.authorize_access_token()
    token = oauth.azure.authorize_access_token()
    if userinfo := oauth.azure.parse_id_token(token):
        session['user'] = userinfo
    return redirect(url_for('home'))


def logout():
    """ Выйти из системы """
    session.clear()
    return redirect(url_for('home'))


def schedule_group():
    """
    Просмотр расписания учебной группы
    Расписание учебной группы на текущую неделю с возможностью выбора другой
    группы и перехода к другой неделе.
    """
    return render_template('group_schedule.html')


def schedule_teacher():
    """
    Просмотр расписания преподавателя
    Расписание преподавателя на текущую неделю с возможностью выбора другого
    преподавателя и перехода к другой неделе.
    """
    return render_template('teacher_schedule.html')


def schedule_room():
    """
    Просмотр расписания аудитории
    Расписание аудитории на текущую неделю с возможностью выбора другой
    аудитории и перехода к другой неделе.
    """
    return render_template('room_schedule.html')


@admin_required
def edit_persons():
    """
    Редактирование людей
    Список людей с возможностью наложить фильтры и редактирования во
    всплывающем окне.
    Доступно только авторизированному пользователю.
    """
    page = request.args.get('p', 1)
    context = {
        'persons': models.Person.objects.all()
    }
    return render_template('edit_persons.html', **context)


@admin_required
def edit_edu_groups():
    """
    Редактирование учебных групп
    Список учебных групп с возможностью наложить фильтры и редактирования во
    всплывающем окне.
    Доступно только авторизированному пользователю.
    """
    return render_template('edit_edu_groups.html')


@admin_required
def edit_rooms():
    """
    Редактирование аудиторий
    Список аудиторий с возможностью наложить фильтры и редактирования во
    всплывающем окне.
    Доступно только авторизированному пользователю.
    """
    return render_template('edit_rooms.html')


@admin_required
def edit_courses():
    """
    Редактирование учебных курсов
    Список учебных курсов с возможностью наложить фильтры и редактирования во
    всплывающем окне.
    Доступно только авторизированному пользователю.
    """
    return render_template('edit_courses.html')


def event():
    """
    Редактирование событий
    Открывается из расписания.
    Перед записью проверяет корректность и дает возможность выбрать другой
    вариант аудитории или времени.
    Доступно только авторизованному пользователю
    """
    return render_template('event.html')
