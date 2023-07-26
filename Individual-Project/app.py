from flask import Flask, render_template, request, redirect, url_for, flash
from flask import session as login_session
import pyrebase

config = {
  "apiKey": "AIzaSyBgYZ3voLU1FNbM8J05bUvTFnbHyx7zMrs",
  "authDomain": "cs-firebase-y2.firebaseapp.com",
  "projectId": "cs-firebase-y2",
  "storageBucket": "cs-firebase-y2.appspot.com",
  "messagingSenderId": "996495197683",
 " appId": "1:996495197683:web:b77b737703ed5cce637e86",
  "measurementId": "G-91TMB3J5QK",
  "databaseURL": "https://cs-firebase-y2-default-rtdb.europe-west1.firebasedatabase.app/"
}

firebase = pyrebase.initialize_app(config)
auth = firebase.auth()
db = firebase.database()
app = Flask(__name__, template_folder='templates', static_folder='static')
app.config['SECRET_KEY'] = 'super-secret-key'

#Code goes below here___________________________________________________________________________________________________________________________________

@app.route('/', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'GET':
       return render_template("signup.html")
    else:   
        full_name = request.form['full_name']
        email = request.form['email']
        username = request.form['username']
        password = request.form['password']
        try:
          login_session['user'] = auth.create_user_with_email_and_password(email, password)
          UID = login_session['user']['localId']
          user = {"full_name": "", "email": "","username": ""}
          db.child("Users").child(UID).set(user)
          return render_template('home.html')
        except:
          return render_template("signup.html")


@app.route('/login', methods=['GET', 'POST'])
def login():
    error = ""
    if request.method == 'POST':
      try:
        email = request.form['email']
        password = request.form['password']
        #try:
        login_session['user'] = auth.sign_in_with_email_and_password(email, password)
        return render_template("home.html")
      except:
        return render_template("signup.html")
    else:
      return render_template('login.html')


@app.route('/home', methods =['GET', 'POST'])
def home():  
 if request.method == 'GET':
    images = db.child("Imgs").get().val()
    return render_template('home.html', imgs=images)
 else:
    return render_template("home.html")


@app.route('/imgs', methods =['GET', 'POST'])
def imgs():
 if request.method == 'POST':
     try:
         imgs = {"title": request.form['title'], "artist": request.form['artist'], "style": request.form['style'], "description": request.form['description'],"image": request.form['image']}
         db.child("Imgs").push(imgs)
         images= db.child("Imgs").get().val()
         return render_template("home.html", imgs = images)
     except:
         print("Couldn't add img")
         return render_template("home.html")
 else:
    return render_template("imgs.html")


#@app.route('/all_posts', methods=['GET', 'POST'])
#def all_posts():
 # if 'user' in login_session and 'localId' in login_session['user']:
#      UID = login_session['user']['localId']
     # if request.method == 'POST':
    #    posts = {"posts"[post1,post2,post3,post4,post5,post6]}
   #     db.child("Users").child(UID).push(posts)
  #      all_posts = db.child("Users").get().val()
 #       return render_template("all_posts.html", posts=posts)
  #    else:
 #       return render_template("all_posts.html")
 # else:      
#    return redirect(url_for('signin'))

  #all_posts = db.child("Users").get().val()
  #users = db.child("Users").get().val()
  
  #return render_template("all_posts.html",posts = all_posts, users = users)

    
#Code goes above here____________________________________________________________________________________________________________________________________
if __name__ == '__main__':
    app.run(debug=True)

# @app.route('/img2', methods =['GET', 'POST'])
# def img2():
#   if request.method=="POST":
#       post2 = request.form['post2']
#       return render_template('img3.html')
#   return render_template("img2.html")

# @app.route('/img3', methods =['GET', 'POST'])
# def img3():
#   if request.method=="POST":
#     post3 = request.form['post3']
#     return render_template('img4.html')
#   else:
#     return render_template('img3.html')

# @app.route('/img4', methods =['GET', 'POST'])
# def img4():
#   if request.method=="POST":
#     post4 = request.form['post4']
#     return render_template('img5.html')
#   else:
#     return render_template('img4.html')

# @app.route('/img5', methods =['GET', 'POST'])
# def img5():
#   if request.method=="POST":
#     post5 = request.form['post5']
#     return render_template('img6.html')
#   else:
#     return render_template('img5.html')

# @app.route('/img6', methods =['GET', 'POST'])
# def img6():
#     if request.method=="POST":
#       post6 = request.form['post6']
#       #return render_template("img6.html")
#       return render_template('all_posts.html')
#     else:
#       return render_template("img6.html")