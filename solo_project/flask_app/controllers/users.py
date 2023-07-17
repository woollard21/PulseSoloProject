from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import user, post
from flask_bootstrap import Bootstrap
from flask_bcrypt import Bcrypt
bcrypt = Bcrypt(app)

@app.route('/')
def index():
    return render_template('/pulse_home.html')

@app.route('/register_page.html')
def register_page():
    return render_template('/register_page.html')

@app.route('/register/user', methods=['POST'])
def create():
    if not user.User.validate_user(request.form):
        return redirect('/register_page.html')
    hashed_pw= bcrypt.generate_password_hash(request.form['password'])
    data = {
        'first_name': request.form['first_name'],
        'last_name': request.form['last_name'],
        'email': request.form['email'],
        'password': hashed_pw,
        'subscribe': request.form['subscribe'],
        'new_student': request.form['new_student'],
    }
    one_user_id = user.User.create_user(data)
    session['logged_in_id'] = one_user_id
    return redirect ('/successful/creation/')

@app.route('/successful/creation/')
def logged_in_user():
    if 'logged_in_id' not in session:
        return redirect('/')
    data={
        'id': session['logged_in_id']
    }
    return render_template ('pulse_social.html', all_posts=post.Post.all_posts())

@app.route('/login/user', methods=["POST"])
def log_in_user():
    one_user=user.User.user_with_email(request.form)
    if not one_user:
        flash('User not found', 'login')
        return redirect('/')
    if not bcrypt.check_password_hash(one_user.password, request.form['password']):
        flash('Password not found', 'login')
        return redirect ('/')
    session['logged_in_id'] = one_user.id
    print(one_user.id)
    return redirect ('/successful/creation/')

@app.route('/create')
def create_post():
    if 'logged_in_id' not in session:
        return redirect('/')
    print('logged_in_id')
    return render_template('/create_post.html')

@app.route('/store')
def storefront():
    if 'logged_in_id' not in session:
        return redirect('/')
    return render_template('/pulse_merch.html')

@app.route('/logout', methods=["POST"])
def logout():
    session.clear()
    return redirect('/')