from flask import Flask, render_template, request, redirect, url_for
from flask_security import Security, login_user, logout_user, current_user, auth_required, roles_accepted

from models import db, user, user_datastore

app = Flask(__name__)
app.config['DEBUG'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///test.sqlite3'
app.config['SECRET_KEY'] = 'super-secret'
app.config['SECURITY_LOGIN_URL'] = '/ijghjsvef67832r'
app.config['SECURITY_UNAUTHORIZED_VIEW'] = '/login'

db.init_app(app)
Security(app, user_datastore)

with app.app_context():
    db.create_all()
    user_datastore.find_or_create_role(name='admin')
    user_datastore.find_or_create_role(name='user')
    if not user_datastore.find_user(email="admin@a.com"):
        user_datastore.create_user(email="admin@a.com", password="admin", name="admin", roles=['admin'])
    db.session.commit()

@app.route('/')
def hello_world():
    print('Hello, World!')
    return 'Hello, World!'

@app.route('/html')
def hello_html():
    return render_template('index.html')

@app.route('/page1', methods=['GET', 'POST'])
@auth_required('session')
@roles_accepted('admin')
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

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'GET':
        return render_template('login.html')
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        user = user_datastore.find_user(email=email)
        if user and user.password == password:
            login_user(user)
            return redirect(url_for('page01'))
        else:
            return 'Invalid credentials'
        
@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('login'))
    
@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'GET':
        return render_template('register.html')
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        name = request.form['name']
        # print(email, password, name)
        # new_user = user(email=email, password=password, name=name)
        # db.session.add(new_user)
        if not user_datastore.find_user(email=email):
            user_datastore.create_user(email=email, password=password, name=name, roles=['user'])
            db.session.commit()
            return redirect(url_for('login'))
        else:
            return 'User already exists, go back and try again'

if __name__ == '__main__':
    app.run(port=1508)