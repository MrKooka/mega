from flask import Blueprint

dashroute = Blueprint(
    'dashroute',
    __name__,
    url_prefix='/DashExample',
    template_folder='templates',
    static_folder='static'
)
