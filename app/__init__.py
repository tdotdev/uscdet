from flask import Flask

app = Flask('USC-DET', template_folder='app/templates')

from app import routes