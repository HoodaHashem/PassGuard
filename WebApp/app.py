from flask import Flask, render_template, url_for


app = Flask(__name__)

@app.route('/')
@app.route('/home')
def home():
    return render_template('home.html' , footer=True)

@app.route('/Getintouch')
def Getintouch():
    return render_template('Getintouch.html' , footer=False, title='Get in touch')

if __name__ == '__main__':
    app.run(debug=True)
