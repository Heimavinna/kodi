from flask import Flask, render_template, request, redirect, url_for, session
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
from flask_bcrypt import Bcrypt

app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

app.config['SECRET_KEY'] = 'baraeinhvad'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///appdb.db'
#app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

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
    
    todo = db.relationship('Todo')   
    

class Todo(db.Model):
    __tablename__ = 'todo'
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100))
    complete = db.Column(db.Boolean)
    
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    user = db.relationship("User", backref='user')


@app.route('/')
def index():

    if 'username' in session:
        u_id = current_user.id
        return render_template('base.html', todo_list=Todo.query.filter_by(user_id=u_id))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    session.pop('username', None)
    if request.method == 'POST':
        form_data = request.form.to_dict()
        print(form_data)
        currentUsername = form_data['username']
        currentPassword = form_data['password']
        notendur = User.query.filter_by(username=currentUsername).first()
        if notendur:
            if bcrypt.check_password_hash(notendur.password, currentPassword):
                session['username'] = currentUsername
                login_user(notendur)
                return redirect(url_for('index'))
            
    return render_template('login.html')

@app.route('/logout', methods=['GET','POST'])
def logout():
    logout_user()
    return redirect(url_for('login'))

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

# Login og register route

@app.route('/')
def index():
    return redirect('login')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        form_data = request.form.to_dict()
        print(form_data)

        currentUsername = form_data['username']
        currentPassword = form_data['password']
    return render_template('login.html')


@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        form_data = request.form.to_dict()
        print(form_data)
    return render_template('register.html')




@app.route("/add", methods=["POST"])
def add():
    # adda new item
    u_id = current_user.id
    title = request.form.get("title")
    new_todo = Todo(title=title, complete = False, user_id=u_id)
    db.session.add(new_todo)
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/update/<int:todo_id>")
def update(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    todo.complete = not todo.complete
    db.session.commit()
    return redirect(url_for("index"))

@app.route("/delete/<int:todo_id>")
def delete(todo_id):
    todo = Todo.query.filter_by(id=todo_id).first()
    db.session.delete(todo)
    db.session.commit()
    return redirect(url_for("index"))


@app.errorhandler(404)
def page_not_found(e):
    return render_template('404.html'), 404


if __name__ == '__main__':
    db.create_all()



    app.run(debug=True, use_reloader=True)