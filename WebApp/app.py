from flask import Flask, render_template, url_for, redirect, flash
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

@app.route('/login' , methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@admin.com' and form.password.data == 'admin':
            flash('You have been logged in!', 'success')
            return redirect(url_for('home'))
        else:
            flash('Login Unsuccessful. Please check username and password', 'danger')
    return render_template('login.html' , footer=False, form=form)

@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegistrationForm()
    if form.validate_on_submit():
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))
    return render_template('signup.html' , footer=False, form=form)


if __name__ == '__main__':
    app.run(debug=True)
