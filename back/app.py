from flask import Flask, render_template
from flask_cors import CORS
from flask_restful import Api
from routes.config import connection
from routes.sc import sc
from routes.s import s
from routes.c import c

app = Flask(__name__, template_folder='./templates', static_folder='./templates/static')
CORS(app)


if connection.ping() is None:
    print("Oracle database connection successful!")
else:
    print("Failed to connect to Oracle database")

app.register_blueprint(sc)
app.register_blueprint(s)
app.register_blueprint(c)
@app.route('/')
def index():
    return render_template('index.html')
if __name__ == "__main__":
    app.run(host='127.0.0.1', port=8010)
