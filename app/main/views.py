from flask import render_template, redirect, url_for, request
from flask_login import login_required, current_user
from . import main
from .forms import PostForm, CommentForm, UpdateProfile, Sport
from ..models import Post, Comment, User, Upvote, Downvote
from .. import db, photos


@main.route('/')
@login_required
def index():
    '''
    View root page function that returns the index page and its data
    '''
    posts = Post.query.all()
    interview = Post.query.filter_by(category='interview').all()
    sport = Post.query.filter_by(category='sport').all()
    motivation = Post.query.filter_by(category='motivation').all()

    return render_template('index.html', interview=interview, sport=sport, motivation=motivation, posts=posts)


@main.route('/posts')
@login_required
def posts():
    '''
    View post function that returns the post page and data
    '''

    posts = Post.query.all()
    likes = Upvote.query.all()
    user = current_user
    return render_template('pitch_details.html', posts=posts, likes=likes, user=user)


@main.route('/new_post', methods=['GET', 'POST'])
@login_required
def new_post():
    '''
    View post function that returns the new post page and data
    '''
    form = PostForm()
    if form.validate_on_submit():
        title = form.title.data
        post = form.post.data
        category = form.category.data
        user_id = current_user._get_current_object().id
        new_post = Post(post=post, title=title, category=category, user_id=user_id)
        new_post.save()
        return redirect(url_for('.index'))
    return render_template('pitch.html', form=form)


@main.route('/comment/<int:post_id>', methods=['GET', 'POST'])
@login_required
def comment(post_id):
    '''
    View post function that returns the comment page and data
    '''

    form = CommentForm()
    post = Post.query.get(post_id)
    user = User.query.all()
    comments = Comment.query.filter_by(post_id=post_id).all()
    if form.validate_on_submit():
        comment = form.comment.data
        post_id = post_id
        user_id = current_user._get_current_object().id
        new_comment = Comment(
            comment=comment,
            post_id=post_id,
            user_id=user_id
        )
        new_comment.save()
        new_comments = [new_comment]
        print(new_comments)
        return redirect(url_for('.comment', post_id=post_id))
    return render_template('comment.html', form=form, post=post, comments=comments, user=user)


@main.route('/user/<name>')
def profile(name):
    user = User.query.filter_by(username = name).first()
    user_id = current_user._get_current_object().id
    posts = Post.query.filter_by(user_id = user_id).all()
    if user is None:
        (404)

    return render_template("profile/profile.html", user = user,posts=posts)


@main.route('/user/<name>/updateprofile', methods = ['POST','GET'])
@login_required
def updateprofile(name):
    form = UpdateProfile()
    user = User.query.filter_by(username = name).first()
    if user == None:
        (404)
    if form.validate_on_submit():
        user.bio = form.bio.data
        user.save_u()
        return redirect(url_for('.profile',name = name))
    return render_template('profile/update.html',form =form)    


@main.route('/user/<name>/update/pic',methods= ['POST'])
@login_required
def update_pic(name):
    user = User.query.filter_by(username = name).first()
    if 'photo' in request.files:
        filename = photos.save(request.files['photo'])
        path = f'photos/{filename}'
        user.profile_pic_path = path
        db.session.commit()
    return redirect(url_for('main.profile',name=name))


@main.route('/like/<int:id>', methods=['POST', 'GET'])
@login_required
def upvote(id):
    '''
    View like function that returns likes
    '''

    post = Post.query.get(id)
    new_vote = Upvote(post=post, upvote=1)
    new_vote.save()
    return redirect(url_for('main.posts'))


@main.route('/dislike/<int:id>', methods=['GET', 'POST'])
@login_required
def downvote(id):
    '''
    View dislike function that returns dislikes
    '''

    post = Post.query.get(id)
    vm = Downvote(post=post, downvote=1)
    vm.save()
    return redirect(url_for('main.posts'))

@main.route('/user/category/sport', methods=['GET', 'POST'])
@login_required
def sport():
    form = Sport()
    title = 'Post a pitch'
    if form.validate_on_submit():
        post = form.post.data
        body = form.body.data
        new_sport = Sport(post=post, user=current_user, body=body)
        new_sport.save_sport()
        return redirect(url_for('.sport'))
    return render_template("sport.html", sport_form=form, title=title)

