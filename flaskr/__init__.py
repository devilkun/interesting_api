from flask import Flask
from flaskr import router

app = Flask(__name__)
app.register_blueprint(router.api, url_prefix='/api')

