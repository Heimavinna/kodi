from flask import Flask, render_template, redirect, session, url_for, request
import json
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import create_engine
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import InputRequired, Length, ValidationError
from flask_bcrypt import Bcrypt

app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
app.config['SECRET_KEY'] = 'leynilykill'
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
    test_store = db.relationship('TestStore')    
class TestStore(db.Model):
    __tablename__ = 'test_store'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(40), nullable=False)
    todo = db.Column(db.String(200))
    done = db.Column(db.Integer, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", backref='user')
 
    
class RegisterForm(FlaskForm):
    username = StringField(validators={InputRequired(), 
                                       Length(min=5, max=20)}, 
                                       render_kw={"placeholder": "Notandanafn"})   
    password = PasswordField(validators={InputRequired(), 
                                         Length(min=8, max=20)}, 
                                        render_kw={'placeholder': 'Lykilorð'})
    
    submit = SubmitField('Register')
    
    def validate_username(self, username):
        nuverandi_notandi= User.query.filter_by(username=username.data).first()
        if nuverandi_notandi:
            raise ValidationError(
                'Þessi notandi er nú þegar til. Viltu vinsamlegast breyta nafninu'

            )
class LoginForm(FlaskForm):
    username = StringField(validators={InputRequired(), 
                                       Length(min=5, max=20)}, 
                                       render_kw={"placeholder": "Notandanafn"})   
    password = PasswordField(validators={InputRequired(), 
                                         Length(min=8, max=20)}, 
                                        render_kw={'placeholder': 'Lykilorð'})
    
    submit = SubmitField('Login')
class TodoForm(FlaskForm):
    name = StringField(validators={InputRequired(),
                                   Length(min=1, max=40)},
                                   render_kw={"placeholder": "Nafn á Toddo"})
    todo = StringField(validators={InputRequired(),
                                   Length(min=0, max=200)},
                                   render_kw={"placeholder": "Skrifaðu einhvað um todo'ið"})
    done = StringField(validators={InputRequired(),
                                   Length(min=0, max=10)},
                                   render_kw={"placeholder": "Hvenær eru skil?"})
    submit = SubmitField('Bæta við')



@app.route('/')
def home():
    return render_template('base.html')

@app.route('/error')
def error():
    return "Það var einhvað sem fór úrskeiðis, mjög líklegst lengd notandanafns"

@app.route('/addtodo', methods=['GET', 'POST'])
def addtodo():
    form = TodoForm()
    u_id = current_user.id
    if form.validate_on_submit():
        todo = TestStore(name=form.name.data, todo=form.todo.data, done=form.done.data, user_id=u_id)
        db.session.add(todo)
        db.session.commit()
        return redirect(url_for('dashboard'))
        
    return render_template("todo.html", form = form)

@app.route('/dashboard', methods=['GET','POST'])
def dashboard():
    u_id = current_user.id
    return render_template('dashboard.html', todo=TestStore.query.filter_by(user_id=u_id))

@app.route('/login', methods=['GET','POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        notandi = User.query.filter_by(username=form.username.data).first()
        if notandi:
            if bcrypt.check_password_hash(notandi.password, form.password.data):
                login_user(notandi)
                return redirect(url_for('dashboard'))
            
    return render_template('login.html', form=form)

@app.route('/logout', methods=['GET','POST'])
def logout():
    logout_user()
    return redirect(url_for('login'))

@app.route('/register', methods=['GET','POST'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        ruglad_password = bcrypt.generate_password_hash(form.password.data)
        nyr_notandi = User(username=form.username.data, password=ruglad_password)
        db.session.add(nyr_notandi)
        db.session.commit()
        return redirect(url_for('login'))

    return render_template('register.html', form=form)

if __name__ == '__main__':
    app.run(debug=True)