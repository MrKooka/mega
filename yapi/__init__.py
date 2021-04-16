from flask import Blueprint

yapi = Blueprint(
    'yapi',
    __name__,
    url_prefix='/yapi',
    template_folder='templates',
    static_folder='static'
)
