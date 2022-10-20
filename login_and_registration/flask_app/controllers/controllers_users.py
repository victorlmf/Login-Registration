from flask_app import app
from flask import request, render_template, redirect, session, flash
from flask_app.models.models_user import User
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('/index.html')

# Register User
@app.route('/register_user', methods=['POST'])
def register_user():
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'dob': request.form['dob'],
        'password': request.form['password'],
        'confirm_pw': request.form['confirm_pw'],
        'fav_language': request.form.getlist('fav_language')
    }
    valid = User.user_validator(data)
    if valid:
        pw_hash = bcrypt.generate_password_hash(data['password'])
        data['pw_hash'] = pw_hash
        user = User.create_user(data)
        session['user'] = user
        print('You got it, you are a new user')
        user_id = User.get_by_email(request.form).id
        return redirect(f'/success/{user_id}')
    return redirect('/')

# Login User
@app.route('/login_user', methods=['POST'])
def login_user():
    user = User.get_by_email(request.form)
    if not user:
        flash('Invalid email or password, or please select at least 2 hobbies!', 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(user.password, request.form['password']):
        flash('Invalid password!', 'login')
        return redirect('/')
    session['user'] = user.id
    hobbies = len(request.form.getlist('hobby'))
    if hobbies < 2:
        flash('Please select at least 2 hobbies!', 'login')
        return redirect('/')
    session['hobbies'] = request.form.getlist('hobby')
    return redirect(f'/success/{user.id}')

# Success Route
@app.route('/success/<int:id>')
def success(id):
    if 'user' not in session: 
        return redirect('/')
    data = {
        "id": id
    }
    user = User.get_by_id(data)
    return render_template('/success.html', user = user[0])

# Logout User
@app.route('/logout')
def logout():
    session.clear()
    return redirect('/')