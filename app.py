from flask import Flask
from flask_pymongo import PyMongo
from config import Config

app = Flask(__name__)
app.config.from_object(Config)

# MongoDB Setup
mongo = PyMongo(app)

# Importing Blueprints
from routes.auth import auth_bp
from routes.diary import diary_bp

# Registering Blueprints
app.register_blueprint(auth_bp, url_prefix='/auth')
app.register_blueprint(diary_bp, url_prefix='/diary')

if __name__ == '__main__':
    app.run(debug=True, host= "0.0.0.0")
