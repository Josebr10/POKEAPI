from flask import Flask
from templates import render_template

app = Flask(__name__)

@app.route('/')
def hello():
    return render_template('index.html')


app.run(host='localhost', port=5000, debug=True)
