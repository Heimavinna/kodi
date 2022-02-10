from flask import Flask, request, url_for, redirect, render_template



# Create app, that hosts the application. Don't worry about that __name__ object, it's just a convention.
app = Flask(__name__)

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
    return render_template('login.html')



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