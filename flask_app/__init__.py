from flask import Flask, session
from flask_session import Session

app = Flask(__name__)
app.secret_key = "Xhuljano" 

# Configure Session to Use the Filesystem
app.config["SESSION_PERMANENT"] = True
app.config["SESSION_TYPE"] = "filesystem"
Session(app)
