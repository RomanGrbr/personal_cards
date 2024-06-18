# Не вносить изменения !

NUMBER = 'number'
TEXT = 'text'
STRING = 'string'
DATE_TIME = 'datetime-local'
DATE = 'date'
TIME = 'time'
WEEK = 'week'
EMAIL = 'email'
FILE = 'file'
IMAGE = 'image'
MOVE = 'video'
AUDIO = 'audio'
CHECKBOX = 'checkbox'
RADIO = 'radio'
TEL = 'tel'
URL = 'url'


CREATE, READ, UPDATE, DELETE = "Создание", "Чтение", "Редактирование", "Удаление"
LOGIN, LOGOUT, LOGIN_FAILED = "Вход", "Выход", "Ошибка входа"
ACTION_TYPES = [
    (CREATE, CREATE),
    (READ, READ),
    (UPDATE, UPDATE),
    (DELETE, DELETE),
    (LOGIN, LOGIN),
    (LOGOUT, LOGOUT),
    (LOGIN_FAILED, LOGIN_FAILED),
]

SUCCESS, FAILED = "Успешный", "Неудачный"
ACTION_STATUS = [(SUCCESS, SUCCESS), (FAILED, FAILED)]