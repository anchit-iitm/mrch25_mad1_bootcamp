from flask import Flask, render_template, request, redirect, url_for
from models import db, user

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite3'

db.init_app(app)

with app.app_context():
    db.create_all()

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
        name_var = request.form['username']
        new_user = user(name=name_var)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('page01'))
    
@app.route('/page2/<int:id>')
def page02(id):
    data = user.query.filter_by(user_id=id).first()
    print(data)
    if data:
        backend_name = data.name
        ID = data.user_id
    else:
        backend_name = 'No entry found'
        ID = 'No entry found'
    return render_template('page2.html', frontend_name=backend_name, id=ID)

@app.route('/page3')
def page03():
    all_data = user.query.all()
    print(all_data)
    return render_template('page3.html', data=all_data)

if __name__ == '__main__':
    app.run(port=1508)