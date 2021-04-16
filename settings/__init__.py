from flask import Blueprint

settings = Blueprint(
    'settings',
    __name__,
    url_prefix='/settings',
    template_folder='templates',
    static_folder='static'
)
