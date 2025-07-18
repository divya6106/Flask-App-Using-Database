from flask import Flask, render_template, request, url_for, flash, redirect
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///mydb.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.secret_key = 'sk'

db = SQLAlchemy(app)

# User Model
class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    fname = db.Column(db.String(100), nullable=False)
    lname = db.Column(db.String(100), nullable=False)
    password = db.Column(db.String(100), nullable=False)

# Home Page
@app.route("/")
def index():
    return render_template("index.html")

# Main Page (after login)
@app.route("/main")
def main():
    return render_template("main.html")

# Register Page
@app.route("/register", methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        if User.query.filter_by(email=request.form['email']).first():
            flash("Email already registered.", "error")
            return redirect(url_for('register'))

        new_user = User(
            username=request.form['username'],
            email=request.form['email'],
            fname=request.form['fname'],
            lname=request.form['lname'],
            password=request.form['password']  # plain text password
        )
        db.session.add(new_user)
        db.session.commit()
        flash("User registered successfully!", "success")
        return redirect(url_for('login'))

    return render_template("register.html")

# Login Page
@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        user = User.query.filter_by(username=request.form['username']).first()
        if user and user.password == request.form['password']:
            flash("Login successful!", "success")
            return redirect(url_for("main"))
        else:
            flash("Invalid username or password.", "error")
            return redirect(url_for("login"))

    return render_template("login.html")

# Show All Users (for testing only)
@app.route("/users")
def list_users():
    users = User.query.all()
    return render_template("users.html", users=users)



if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)
