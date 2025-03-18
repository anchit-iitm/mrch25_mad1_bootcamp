from flask import Flask, render_template, request, redirect, url_for
from models import db

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite3'

db.init_app(app)

@app.route('/')
def hello_world():
    print('Hello, World!')
    return 'Hello, World!'

@app.route('/html')
def hello_html():
    return render_template('index.html')

@app.route('/page1', methods=['GET', 'POST'])
def page01():
    if request.method == 'GET':
        return render_template('page1.html')
    if request.method == 'POST':
        print(request.form) 
        return redirect(url_for('page01'))


if __name__ == '__main__':
    app.run(port=1508)