from flask import Flask, render_template, request, session, redirect

app = Flask(__name__)

app.secret_key = "Xhuljano"