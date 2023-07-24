from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {
    "apiKey": "AIzaSyAxDSAy5K1YKIoDekm_7LOF1OLsRNmhE7o",

  "authDomain": "test-1-de4ba.firebaseapp.com",

  "projectId": "test-1-de4ba",

  "storageBucket": "test-1-de4ba.appspot.com",

  "messagingSenderId": "186347406573",

  "appId": "1:186347406573:web:dbcafd482deaa060e3b8e4", 
  "databaseURL":"https://test-1-de4ba-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase=pyrebase.initialize_app(config)
db=firebase.database()
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'
auth= firebase.auth()

@app.route('/', methods=['GET', 'POST'])
def signin():
    if request.method=="POST":
        user=request.form["email"]
        password= request.form["password"]
        try:
            login_session['user']=auth.sign_in_with_email_and_password(user, password)
            return (redirect(url_for('add_tweet')))
        except Exception as e:
            error=e
            print(f"ERROR: {e}")
    return render_template("signin.html")


@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method=="POST":
        user=request.form["email"]
        password= request.form["password"]
        bio= request.form['bio']
        try:
            login_session['user']=auth.create_user_with_email_and_password(user, password)
            user= {'email': user, 'bio':bio}
            UID= login_session['user']['localId']
            db.child('users').child(UID).set(user)
            return (redirect(url_for('add_tweet')))
        except Exception as e:
            error='authentication error'
            print(f"ERROR: {e}")
            return render_template("signup.html")


@app.route('/add_tweet', methods=['GET', 'POST'])
def add_tweet():
    if request.method=='POST':
        title=request.form['title']
        text= request.form['text']
        tweet= {'title':title, 'text':text, 'UID':login_session['user']['localId']}
        db.child('tweets').push(tweet)
        return render_template("add_tweet.html")
    else:
        return render_template("add_tweet.html")

@app.route("/signout")
def signout():
    auth.current_user=None
    login_session['user']=None
    return (redirect(url_for('signin')))

@app.route('/all_tweets', methods=['GET', 'POST'])
def tweets():
    return render_template('tweets.html', tweets= db.child('tweets').get().val())
if __name__ == '__main__':
    app.run(debug=True)