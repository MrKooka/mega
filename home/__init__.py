from flask import Blueprint

home = Blueprint(
    'home',
    __name__,
    url_prefix='/',
    template_folder='templates',
    static_folder='static'
)
