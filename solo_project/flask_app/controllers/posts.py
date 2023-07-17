from flask_app import app
from flask import render_template, redirect, request, session, flash
from flask_app.models import user, post

@app.route('/submit/post', methods=["POST"])
def new_post():
    if 'logged_in_id' not in session:
        return redirect('/')
    if not post.Post.validate_post(request.form):
        return redirect('/create')
    post.Post.create_post(request.form)
    return redirect('/posted/successfully')

@app.route('/posted/successfully')
def social_page():
    if 'logged_in_id' not in session:
        return redirect('/')
    return render_template('/pulse_social.html', all_posts=post.Post.all_posts())

@app.route('/post/delete', methods=['POST'])
def delete_post():
    post.Post.delete_post(request.form)
    return redirect('/posted/successfully')