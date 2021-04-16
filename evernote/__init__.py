from flask import Blueprint

evernote = Blueprint(
    'evernote',
    __name__,
    url_prefix='/evernote',
    template_folder='templates',
    static_folder='static'
)
