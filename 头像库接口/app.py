import os
from flask import Flask, render_template

app = Flask(__name__)

# Debug: Print the current working directory and template folder path
print("Current working directory:", os.getcwd())
print("Template folder:", os.path.join(os.getcwd(), 'templates'))

@app.route('/')
def index():
    return render_template('index.html')

if __name__ == '__main__':
    app.run(debug=True)
