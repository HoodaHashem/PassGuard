from flask import Flask, render_template, url_for


app = Flask(__name__)

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
    return render_template('login.html' , footer=True)

@app.route('/signup')
def signup():
    return render_template('signup.html' , footer=True)


if __name__ == '__main__':
    app.run(debug=True)
