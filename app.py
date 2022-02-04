from flask import Flask, render_template, request

app = Flask(__name__)   

@app.route("/", methods=['POST','GET'])
def index():
    if request.method =='POST':
        content = request.form
        return render_template("index.html", content=content)
    else:
        return render_template('index.html')

@app.route("/add")
def add():
    return render_template('add.html')


if __name__ == '__main__':
    app.run()
    