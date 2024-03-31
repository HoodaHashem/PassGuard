from flask import Flask, render_template, url_for
from forms import RegistrationForm, LoginForm

app = Flask(__name__)
app.config['SECRET_KEY'] = '2a67f7d6ba6bb5c0e829e3a4f99237f7'


@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html' , footer=True)

@app.route('/Getintouch')
def Getintouch():
    return render_template('Getintouch.html' , footer=False)

@app.route('/about')
def about():
    return render_template('About.html' , footer=True)

@app.route('/login')
def login():
    form = LoginForm()
    return render_template('login.html' , footer=False, form=form)

@app.route('/signup')
def signup():
    form = RegistrationForm()
    return render_template('signup.html' , footer=False, form=form)


if __name__ == '__main__':
    app.run(debug=True)
