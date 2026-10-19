import pandas as pd

from app import app, db, User, UserProfile




# ==========================================================
# LOAD DATASET
# ==========================================================

df = pd.read_csv(
    "dataset/skill_exchange_dataset_1000.csv"
)

print("Dataset loaded successfully.")

print("Number of users:", len(df))


# ==========================================================
# IMPORT INTO MYSQL
# ==========================================================

with app.app_context():

    imported_count = 0
    skipped_count = 0

    for index, row in df.iterrows():

        # --------------------------------------------------
        # GET NAME
        # --------------------------------------------------

        name = str(row["name"]).strip()

        if not name:
            print("Skipping row because name is empty.")
            skipped_count += 1
            continue


        # --------------------------------------------------
        # CREATE EMAIL
        # --------------------------------------------------

        base_email = (
            name
            .lower()
            .replace(" ", "")
            + "@gmail.com"
        )

        email = base_email

        counter = 1

        while User.query.filter_by(email=email).first():

            email = (
                name
                .lower()
                .replace(" ", "")
                + str(counter)
                + "@gmail.com"
            )

            counter += 1


        # --------------------------------------------------
        # PASSWORD
        # --------------------------------------------------

        password = name.lower()



        # --------------------------------------------------
        # CREATE USER
        # --------------------------------------------------

        new_user = User(

            name=name,

            email=email,

            password=password

        )

        db.session.add(new_user)

        db.session.flush()


        # --------------------------------------------------
        # CREATE USER PROFILE
        # --------------------------------------------------

        profile = UserProfile(

            user_id=new_user.id,

            age=int(row["age"]),

            gender=str(row["gender"]),

            city=str(row["city"]),

            teach_skill=str(row["teach_skill"]),

            learn_skill=str(row["learn_skill"]),

            proficiency_level=str(
                row["proficiency_level"]
            ),

            preferred_language=str(
                row["preferred_language"]
            ),

            learning_mode=str(
                row["learning_mode"]
            ),

            availability=str(
                row["availability"]
            ),

            rating=float(row["rating"]),

            completed_exchanges=int(
                row["completed_exchanges"]
            )

        )

        db.session.add(profile)


        imported_count += 1


        # --------------------------------------------------
        # DISPLAY PROGRESS
        # --------------------------------------------------

        print(
            f"Imported {imported_count}: "
            f"{name} → {email}"
        )


    # ======================================================
    # SAVE EVERYTHING
    # ======================================================

    db.session.commit()


    print()
    print("=" * 50)

    print(
        "IMPORT COMPLETED SUCCESSFULLY"
    )

    print(
        "Imported users:",
        imported_count
    )

    print(
        "Skipped users:",
        skipped_count
    )

    print("=" * 50)