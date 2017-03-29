from flask import Flask, redirect, url_for, render_template, flash, g, request
from flask_wtf import Form
from wtforms import StringField
from wtforms.validators import DataRequired
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from flask_login import LoginManager, UserMixin, login_user, logout_user,\
    current_user, login_required
from oauth import OAuthSignIn
import unirest

app = Flask(__name__)

app.config['SECRET_KEY'] = 'top secret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['OAUTH_CREDENTIALS'] = {
    'facebook': {
        'id': '626512050883314',
        'secret': 'aa702c47c08575595ccaf0c8cd55c8c0'
    },
    'twitter': {
        'id': 'ilEOnavzVmc7rXH9j72puWReT',
        'secret': 'PTde262dJtAbNqeESNXa97ZR5sQFWR33Uvw5LUZlzsimCWMDFq'
    }
}

db = SQLAlchemy(app)
lm = LoginManager(app)
lm.login_view = 'index'

POSTS_PER_PAGE = 10

class PostForm(Form):
    post = StringField('post', validators=[DataRequired()])

followers = db.Table('followers',
    db.Column('follower_id', db.Integer, db.ForeignKey('user.id')),
    db.Column('followed_id', db.Integer, db.ForeignKey('user.id'))
)

class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    social_id = db.Column(db.String(64), nullable=False, unique=True)
    nickname = db.Column(db.String(64), nullable=False)
    email = db.Column(db.String(64), nullable=True)
    posts = db.relationship('Post', backref='author', lazy='dynamic')
    followed = db.relationship('User', 
                               secondary=followers, 
                               primaryjoin=(followers.c.follower_id == id), 
                               secondaryjoin=(followers.c.followed_id == id), 
                               backref=db.backref('followers', lazy='dynamic'), 
                               lazy='dynamic')
    def follow(self, user):
        if not self.is_following(user):
            self.followed.append(user)
            return self

    def unfollow(self, user):
        if self.is_following(user):
            self.followed.remove(user)
            return self

    def is_following(self, user):
        return self.followed.filter(followers.c.followed_id == user.id).count() > 0

    def followed_posts(self):
        return Post.query.join(followers, (followers.c.followed_id == Post.user_id)).filter(followers.c.follower_id == self.id).order_by(Post.timestamp.desc())

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    body = db.Column(db.String(140))
    timestamp = db.Column(db.DateTime)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))

    def __repr__(self):
        return '<Post %r>' % (self.body)

@app.before_request
def before_request():
    g.user = current_user

@lm.user_loader
def load_user(id):
    return User.query.get(int(id))


@app.route('/', methods=['GET', 'POST'])
@app.route('/index', methods=['GET', 'POST'])
def index():
    #if g.user is not None and g.user.is_authenticated:
     #   recipes = "I have made a terrible mistake."
      #  print recipes
       # post = Post(body=recipes, timestamp=datetime.utcnow(),author=g.user)
        #db.session.add(post)
        #db.session.commit()
    return render_template('index.html')

@app.route("/submit", methods=['POST'])
def submit():
    form_data = request.form
    ingredients = form_data['totallist']
    print ingredients
    # These code snippets use an open-source library. http://unirest.io/python
    url = "https://spoonacular-recipe-food-nutrition-v1.p.mashape.com/recipes/findByIngredients?fillIngredients=true&ingredients=" + ingredients + "&limitLicense=false&number=5&ranking=1"
    response = unirest.get(url,
      headers={
        "X-Mashape-Key": "Ns3zcSqSBRmshNRLntIW4o1vPHyMp1vBQ72jsnR4qCtZpKfAXW",
        "Accept": "application/json"
      }
    )
    print response.code
    print response.headers
    print response.body
    data = response.body
    image1=data[0]["image"]
    image2=data[1]["image"]
    image3=data[2]["image"]
    image4=data[3]["image"]
    ending1=image1.rsplit('/', 1)[-1]
    ending2=image2.rsplit('/', 1)[-1]
    ending3=image3.rsplit('/', 1)[-1]
    ending4=image4.rsplit('/', 1)[-1]
    sep='.'
    end1=ending1.split(sep, 1)[0]
    end2=ending2.split(sep, 1)[0]
    end3=ending3.split(sep, 1)[0]
    end4=ending4.split(sep, 1)[0]
    title1=data[0]["title"]
    title2=data[1]["title"]
    title3=data[2]["title"]
    title4=data[3]["title"]
    link1="https://spoonacular.com/recipes/" + end1
    link2="https://spoonacular.com/recipes/" + end2
    link3="https://spoonacular.com/recipes/" + end3
    link4="https://spoonacular.com/recipes/" + end4
    save1='<h1>' + title1 + '</h1>' + '<a href="' + link1 + '"><img src="' + image1 + '"></a>'
    save2='<h1>' + title2 + '</h1>' + '<a href="' + link2 + '"><img src="' + image2 + '"></a>'
    save3='<h1>' + title3 + '</h1>' + '<a href="' + link3 + '"><img src="' + image3 + '"></a>'
    save4='<h1>' + title4 + '</h1>' + '<a href="' + link4 + '"><img src="' + image4 + '"></a>'

    return render_template("recipes.html", ingredients=ingredients, 
        link1=link1, link2=link2, link3=link3, link4=link4, 
        image1=image1, image2=image2, image3=image3, image4=image4,
        title1=title1, title2=title2, title3=title3, title4=title4,
        save1=save1, save2=save2, save3=save3, save4=save4)

@app.route("/save1", methods=['POST'])
def save1():
    if g.user is not None and g.user.is_authenticated:
        formdata = request.form
        recipe1 = formdata['save1']
        print recipe1
        rec1 = 'Here is a new recipe:"' + recipe1 + '"Saved from search'  
        print rec1
        post = Post(body=rec1, timestamp=datetime.utcnow(),author=g.user)
        db.session.add(post)
        db.session.commit()
    return redirect(url_for('user', nickname=g.user))

@app.route("/save2", methods=['POST'])
def save2():
    if g.user is not None and g.user.is_authenticated:
        formdata = request.form
        recipe2 = formdata['save2']
        print recipe2    
        post = Post(body=recipe2, timestamp=datetime.utcnow(),author=g.user)
        db.session.add(post)
        db.session.commit()
    return redirect(url_for('user', nickname=g.user))

@app.route("/save3", methods=['POST'])
def save3():
    if g.user is not None and g.user.is_authenticated:
        formdata = request.form
        recipe3 = formdata['save3']
        print recipe3  
        post = Post(body=recipe3, timestamp=datetime.utcnow(),author=g.user)
        db.session.add(post)
        db.session.commit()
    return redirect(url_for('user', nickname=g.user))

@app.route("/save4", methods=['POST'])
def save4():
    if g.user is not None and g.user.is_authenticated:
        formdata = request.form
        recipe4 = formdata['save4']
        print recipe4   
        post = Post(body=recipe4, timestamp=datetime.utcnow(),author=g.user)
        db.session.add(post)
        db.session.commit()
    return redirect(url_for('user', nickname=g.user))

@app.route('/logout')
def logout():
    logout_user()
    return redirect(url_for('index'))

@app.route('/user/<nickname>')
@app.route('/user/<nickname>/<int:page>')
@login_required
def user(nickname, page=1):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))
    posts = user.posts.paginate(page, POSTS_PER_PAGE, False)
    return render_template('user.html',
                           user=user,
                           posts=posts)

@app.route('/authorize/<provider>')
def oauth_authorize(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    return oauth.authorize()


@app.route('/callback/<provider>')
def oauth_callback(provider):
    if not current_user.is_anonymous:
        return redirect(url_for('index'))
    oauth = OAuthSignIn.get_provider(provider)
    social_id, username, email = oauth.callback()
    if social_id is None:
        flash('Authentication failed.')
        return redirect(url_for('index'))
    user = User.query.filter_by(social_id=social_id).first()
    if not user:
        user = User(social_id=social_id, nickname=username, email=email)
        db.session.add(user)
        db.session.commit()
    login_user(user, True)
    return redirect(url_for('index'))

@app.route('/follow/<nickname>')
@login_required
def follow(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))
    if user == g.user:
        flash('You can\'t follow yourself!')
        return redirect(url_for('user', nickname=nickname))
    u = g.user.follow(user)
    if u is None:
        flash('Cannot follow ' + nickname + '.')
        return redirect(url_for('user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash('You are now following ' + nickname + '!')
    return redirect(url_for('user', nickname=nickname))

@app.route('/unfollow/<nickname>')
@login_required
def unfollow(nickname):
    user = User.query.filter_by(nickname=nickname).first()
    if user is None:
        flash('User %s not found.' % nickname)
        return redirect(url_for('index'))
    if user == g.user:
        flash('You can\'t unfollow yourself!')
        return redirect(url_for('user', nickname=nickname))
    u = g.user.unfollow(user)
    if u is None:
        flash('Cannot unfollow ' + nickname + '.')
        return redirect(url_for('user', nickname=nickname))
    db.session.add(u)
    db.session.commit()
    flash('You have stopped following ' + nickname + '.')
    return redirect(url_for('user', nickname=nickname))
if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)
