from blog import app, db, bcrypt
from flask import render_template, redirect, url_for, flash, request, abort
from blog.forms import RegisterForm, LoginForm, EditProfileForm, CreatePostForm
from blog.models import User, Post
from flask_login import login_user, logout_user, current_user, login_required
from sqlalchemy import desc


@app.route('/')
def home():
    return render_template('home.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        hashed_pass = bcrypt.generate_password_hash(form.password.data).decode('utf-8')
        user = User(username=form.username.data, email=form.email.data, password=hashed_pass)
        db.session.add(user)
        db.session.commit()
        login_user(user)
        flash('Yor register successful.', 'success')
        return redirect(url_for('home'))
    return render_template('register.html', form=form)

@app.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user and bcrypt.check_password_hash(user.password, form.password.data):
            login_user(user, remember=form.remember.data)                        
            flash('You log in successfully', 'success')
            next_url = request.args.get('next')
            return redirect(next_url if next_url else url_for('home'))
        else:
            flash('Wrong username or password', 'danger')
    return render_template('login.html', form=form)


@app.route('/logout')
@login_required
def logout():
    logout_user()
    flash('Yot log out successfull', 'success')
    return redirect(url_for('home'))


@app.route('/profile', methods=['GET', "POST"])
@login_required
def profile():
    form = EditProfileForm()
    if request.method == 'GET':
        form.username.data = current_user.username
        form.email.data = current_user.email
    else:
        if form.validate_on_submit():
            current_user.username = form.username.data
            current_user.email = form.email.data
            db.session.commit()
            flash('Profile edited successfully.', 'success')
    return render_template('profile.html', form=form)


@app.route('/posts', defaults={'user_id': None})
@app.route('/posts/<int:user_id>')
def posts(user_id):
    posts = Post.query.order_by(desc(Post.date)).all()
    if user_id:
        posts = Post.query.filter_by(user_id=user_id)
    return render_template('all_posts.html', posts=posts)

@app.route('/post_details/<int:post_id>')
def post_details(post_id):
    post = db.get_or_404(Post, post_id)
    return render_template('post_details.html', post=post)

@app.route('/create_post', methods=['GET', "POST"])
@login_required
def create_post():
    form = CreatePostForm()
    if request.method == 'POST':
        if form.validate_on_submit():
            post = Post(title=form.title.data, body=form.body.data, user_id=current_user.id)
            db.session.add(post)
            db.session.commit()
            flash('Post created successfully', 'success')
            return redirect(url_for('posts'))
    return render_template('create_post.html', form=form, name='Create')

@app.route('/delete_post/<int:post_id>')
@login_required
def delete_post(post_id):
    post = db.get_or_404(Post, post_id)
    if current_user != post.author:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Post deleted', 'success')
    return redirect(url_for('posts'))

@app.route('/update_post/<int:post_id>', methods=['GET', "POST"])
@login_required
def update_post(post_id):
    post = db.get_or_404(Post, post_id)
    form = CreatePostForm()
    if current_user != post.author:
        abort(403)
    if request.method == "GET":
        form.title.data = post.title
        form.body.data = post.body
    else:
        if form.validate_on_submit():
            post.title = form.title.data
            post.body = form.body.data
            db.session.commit()
            flash('Post edited successfully', 'success')
            return redirect(url_for('post_details', post_id=post.id))
    
    return render_template('create_post.html', form=form, name='Update')



    