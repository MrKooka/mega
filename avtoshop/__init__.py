from flask import Blueprint

avtoshop = Blueprint(
    'avtoshop',
    __name__,
    url_prefix='/avtoshop',
    template_folder='templates',
    static_folder='static'
)
