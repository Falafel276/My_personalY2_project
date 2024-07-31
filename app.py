from flask import Flask, render_template, request, redirect, url_for, session, flash
import pyrebase
import random
import string
# Initialize the Flask app
app = Flask(__name__, template_folder = 'Templates',static_folder = 'Static')
app.secret_key = ''.join(random.choices(string.ascii_letters + string.digits, k=16))

# Firebase configuration

firebaseConfig = {
  'apiKey': "AIzaSyBuya-ZTjlYHd5Gc7mMhdomWJnmeesJYVA",
  'authDomain': "myfirsty2project.firebaseapp.com",
  'databaseURL': "https://myfirsty2project-default-rtdb.europe-west1.firebasedatabase.app",
  'projectId': "myfirsty2project",
  'storageBucket': "myfirsty2project.appspot.com",
  'messagingSenderId': "808540316383",
  'appId': "1:808540316383:web:20c3b1d18cfc6db0807f6a",
  "databaseURL": "https://myfirsty2project-default-rtdb.europe-west1.firebasedatabase.app/"
}

# Initialize Pyrebase
firebase = pyrebase.initialize_app(firebaseConfig)
auth = firebase.auth()
db = firebase.database()

@app.route('/', methods=['GET', 'POST'])
def home():
    return render_template('home.html')

@app.route('/signin', methods=['GET', 'POST'])
def signin():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']

        try:
            session['user'] = auth.sign_in_with_email_and_password(email, password)
            return redirect(url_for('interests'))
        except Exception as e:
            print(e)
            return render_template('signin.html', error='Invalid email or password')
    return render_template('signin.html')



@app.route('/signup', methods=['GET', 'POST'])
def signup():
    error = ""
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        username = request.form['Username']
        full_name=request.form['full_name']
        try:

            session['user'] = auth.create_user_with_email_and_password(email, password)
            UID=session['user']['localId']
            our_user={
                "email":email,
                "password":password,
                "username": username,
                "full name": full_name

            }
            db.child('Users').child(UID).set(our_user)
            return redirect(url_for('signin'))
        except :
            error = "Authentication failed"
            print(error)
    else:
        return render_template("signup.html")
    return render_template("signup.html")



@app.route('/interests', methods=['GET','POST'])
def interests():
    if request.method == 'POST':
        instrument = request.form('instrument')
        hobbies = request.form('Hobbies')

        interests = {'Instrument' : instrument,'hobbies': hobbies}
        
        db.child("Iterests").push(interests)
        
        return render_template('Interest.html')
    return render_template('Interest.html')

@app.route('/results', methods=['GET','POST'])
def interests():
    if request.method == 'POST':
        instrument = request.form('instrument')
        hobbies = request.form('Hobbies')

        interests = {'Instrument' : instrument,'hobbies': hobbies}
        
        return render_template('Interest.html')
    return render_template('Interest.html')


if __name__ == '__main__':
    app.run(debug=True)


# @app.route('/', methods=['GET', 'POST'])
# def home():
# if request.method == 'POST':
#     # Extract email and password from the form
#     email = request.form.get('email')
#     password = request.form.get('password')

#     try:
#         # Authenticate user with Firebase
#         user = auth.sign_in_with_email_and_password(email, password)

#         # Store the idToken in the session to manage user login state
#         session['user'] = user['idToken']

#         # Optionally store user information in the database
#         user_info = auth.get_account_info(user['idToken'])['users'][0]
#         db.child("users").child(user_info['localId']).update({
#             'email': email,
#             'lastLogin': user_info['lastLoginAt']
#         })

#         # Flash a success message
#         flash('Login successful!', 'success')

#         # Redirect to the interests page after successful login
#         return redirect(url_for('interests'))
#     except Exception as e:
#         # Flash an error message if login fails
#         flash('Invalid login credentials. Please try again.', 'danger')

# return render_template('home.html')


# # Signup Route
# @app.route('/signup', methods=['GET', 'POST'])
# def signup():
# if request.method == 'POST':
#     email = request.form.get('email')
#     password = request.form.get('password')

#     try:
#         # Create a new user with Firebase
#         user = auth.create_user_with_email_and_password(email, password)

#         # Store user information in the database
#         db.child("users").child(user['localId']).set({
#             'email': email,
#             'signupDate': user['createdAt']
#         })

#         flash('Account created successfully! You can now log in.', 'success')
#         return redirect(url_for('home'))  # Redirect to home for login
#     except Exception as e:
#         flash('Error creating account. Please try again.')
#         return render_template('signup.html')

# return render_template('signup.html')

# @app.route('/interests')
# def interests():
# return render_template('interests.html')

# @app.route('/results')
# def results():
# return render_template('results.html')

# if __name__ == '__main__':
# app.run(debug=True)



# Home Route with Login Logic
