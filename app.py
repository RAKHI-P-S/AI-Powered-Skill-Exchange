from flask import Flask, render_template, request, redirect, session

from flask_sqlalchemy import SQLAlchemy

from models import db, User, UserProfile, ConnectionRequest

from recommendation_engine import recommended_user

app=Flask(__name__)
app.config["SECRET_KEY"] = "my_super_secret_key_12345"
app.config["SQLALCHEMY_DATABASE_URI"] = \
"mysql+pymysql://root:@localhost/skillmatch"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

   

@app.route("/")
def home():
    return render_template("home.html")


@app.route("/login",methods=["GET","POST"])
def login():
    if request.method=="POST":

        email=request.form["email"]
        password=request.form["password"]

        user=User.query.filter_by(email=email,password=password).first()

        if user:

            session["user_id"]=user.id
            session["user_name"]=user.name

            return redirect("/dashboard")

        else:

            return "Invalid Email or Password"

    return render_template("login.html")

@app.route("/register",methods=["GET","POST"])
def register():

     if request.method=="POST":
         print("Register button clicked")

         name=request.form["name"]
         email=request.form["email"]
         password=request.form["password"]
         confirm_password = request.form["confirm_password"]
         print(name)
         print(email)

         if password!=confirm_password:
             return "password do not match"
         
         existing_user=User.query.filter_by(email=email).first()

         if existing_user:
             return "email already regesterd"

         new_user=User(name=name,email=email,password=password)
         db.session.add(new_user)
         db.session.commit()
         print("Inserted Successfully")

         return redirect("/login")

     return render_template("register.html")

@app.route("/dashboard")
def dashboard():
    
    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(session["user_id"])

    return render_template(
        "dashboard.html",
        username=user.name)


@app.route("/form")
def form():
   return render_template("recommndation.html")


@app.route("/recommend")
def recommend():

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    user = User.query.get(user_id)

    if user is None:
        session.clear()
        return redirect("/login")

    profile = UserProfile.query.filter_by(
        user_id=user_id
    ).first()


    if profile is None:

        return render_template(
            "no_profile.html",
            username=user.name
        )
    current_user = {

        "age": profile.age,

        "gender": profile.gender,

        "city": profile.city,

        "teach_skill": profile.teach_skill,

        "learn_skill": profile.learn_skill,

        "proficiency_level":
            profile.proficiency_level,

        "preferred_language":
            profile.preferred_language,

        "learning_mode":
            profile.learning_mode,

        "availability":
            profile.availability,

        "rating":
            profile.rating,

        "completed_exchanges":
            profile.completed_exchanges
    }
    recommendations = recommended_user(
        current_user,
        current_user_id=user_id
    )

    if recommendations.empty:

        return render_template(
            "no_match.html",
            username=user.name
        )

    return render_template(

        "result.html",

        recommendations=
            recommendations.to_dict(
                orient="records"
            )

    )
@app.route("/profile")
def profile():

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    user = User.query.get(user_id)

    profile = UserProfile.query.filter_by(
        user_id=user_id
    ).first()

    return render_template(
        "profile.html",
        user=user,
        profile=profile
    )

@app.route("/profile/edit", methods=["GET", "POST"])
def edit_profile():

    if "user_id" not in session:
        return redirect("/login")

    user_id = session["user_id"]

    profile = UserProfile.query.filter_by(
        user_id=user_id
    ).first()

    if request.method == "POST":

        if profile is None:

            profile = UserProfile(
                user_id=user_id
            )

            db.session.add(profile)

        profile.age = int(request.form["age"])
        profile.gender = request.form["gender"]
        profile.city = request.form["city"]
        profile.teach_skill = request.form["teach_skill"]
        profile.learn_skill = request.form["learn_skill"]
        profile.proficiency_level = request.form["proficiency_level"]
        profile.preferred_language = request.form["preferred_language"]
        profile.learning_mode = request.form["learning_mode"]
        profile.availability = request.form["availability"]

        db.session.commit()

        return redirect("/profile")

    user = User.query.get(user_id)

    return render_template(
        "edit_profile.html",
        user=user,
        profile=profile
    )

@app.route("/send_request", methods=["POST"])
def send_request():

    sender_id = session["user_id"]

    receiver_id = request.form["receiver_id"]

    request_data = ConnectionRequest(

        sender_id=sender_id,

        receiver_id=receiver_id,

        status="Pending")

    db.session.add(request_data)
    db.session.commit()
    return redirect("/dashboard")

@app.route("/profile/<int:user_id>")
def view_profile(user_id):

    if "user_id" not in session:
        return redirect("/login")

    user = User.query.get(user_id)

    if user is None:
        return "User not found"

    profile = UserProfile.query.filter_by(
        user_id=user_id
    ).first()

    if profile is None:
        return "Profile not found"

    return render_template(
        "view_profile.html",
        user=user,
        profile=profile
    )






@app.route("/logout")
def logout():

    session.clear()

    return redirect("/")




with app.app_context():
    db.create_all()
    print("User Saved Successfully")

if __name__=="__main__":
    app.run(debug=True)