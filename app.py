from flask import Flask, render_template

from neighborhoods.neighborhoods import neighborhoods_bp

app = Flask(__name__)

app.register_blueprint(neighborhoods_bp, url_prefix='/neighborhoods')

@app.route("/")
def home():
    return render_template('home.html')
