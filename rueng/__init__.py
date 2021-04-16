from flask import Blueprint

rueng = Blueprint(
    'rueng',
    __name__,
    url_prefix='/rueng',
    template_folder='templates',
    static_folder='static'
)
