from flask import Flask, request, url_for, redirect, render_template
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt


# Create app, that hosts the application. Don't worry about that __name__ object, it's just a convention.
app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

app.config['SECRET_KEY'] = 'timabundinn'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

class User(db.Model, UserMixin):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), nullable=False, unique=True)
    password = db.Column(db.String(80), nullable=False)


@app.route('/')
def index():
    return render_template("index3.html")
     


@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form_data = request.form.to_dict()
        print(form_data)
        currentUsername = form_data['username']
        currentPassword = form_data['password']
        notendur = User.query.filter_by(username=currentUsername).first()
        if notendur:
            if bcrypt.check_password_hash(notendur.password, currentPassword):
                login_user(notendur)
                return redirect(url_for('index'))
            
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        form_data = request.form.to_dict()
        password = form_data['password']
        username = form_data['username']
        rugald_passw = bcrypt.generate_password_hash(password)
        nyr_notandi = User(username=username, password=rugald_passw)
        db.session.add(nyr_notandi)
        db.session.commit()
        print(form_data)
        return redirect(url_for('login'))
    return render_template('register.html')


@app.route('/sida2', methods=['GET', 'POST'])
def sida2():
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return "redirect(url_for('index'))"

    # show the form, it wasn't submitted
    return render_template('index2.html')


@app.route('/sida3', methods=['GET', 'POST'])
def sida3():
    if request.method == 'POST':
        # do stuff when the form is submitted

        # redirect to end the POST handling
        # the redirect can be to the same route or somewhere else
        return "redirect(url_for('index'))"

    # show the form, it wasn't submitted
    return render_template('index.html')




@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


# This starts the web app 
if __name__ == '__main__':
    app.run(debug=True, use_reloader=True)