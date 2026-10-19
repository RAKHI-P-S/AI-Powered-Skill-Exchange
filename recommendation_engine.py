import pandas as pd
import joblib

from sklearn.neighbors import NearestNeighbors

from models import db, User, UserProfile


# ==========================================================
# LOAD ENCODERS
# ==========================================================

encoders = joblib.load(
    "models/encoders.pkl"
)


# ==========================================================
# FEATURES USED BY KNN
# ==========================================================

features = [
    "age",
    "gender",
    "city",
    "teach_skill",
    "learn_skill",
    "proficiency_level",
    "preferred_language",
    "learning_mode",
    "availability",
    "rating",
    "completed_exchanges"
]


# ==========================================================
# GET CANDIDATES FROM MYSQL
# ==========================================================

def find_candidate(
    user_teach_skill,
    user_learn_skill,
    current_user_id=None
):

        candidates = UserProfile.query.filter(
            UserProfile.teach_skill == user_learn_skill,
            UserProfile.learn_skill == user_teach_skill
        ).all()
        data = []

        for profile in candidates:

            # Don't recommend the logged-in user
            if (
                current_user_id is not None
                and profile.user_id == current_user_id
            ):
                continue

            user = User.query.get(
                profile.user_id
            )

            if user is None:
                continue

            data.append({

                "user_id": profile.user_id,

                "name": user.name,

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

            })

        return pd.DataFrame(data)


# ==========================================================
# ENCODE DATA
# ==========================================================

def encode_data(data):

    encoded = data.copy()

    categorical_columns = [
        "gender",
        "city",
        "teach_skill",
        "learn_skill",
        "proficiency_level",
        "preferred_language",
        "learning_mode",
        "availability"
    ]

    for column in categorical_columns:

        encoder = encoders[column]

        values = encoded[column].astype(str)

        encoded[column] = values.apply(

            lambda value:
            encoder.transform([value])[0]
            if value in encoder.classes_
            else -1

        )

    return encoded


# ==========================================================
# RECOMMEND USERS
# ==========================================================

def recommended_user(
    current_user,
    current_user_id=None
):

    # ------------------------------------------------------
    # FIND CANDIDATES FROM MYSQL
    # ------------------------------------------------------

    candidates = find_candidate(

        current_user["teach_skill"],

        current_user["learn_skill"],

        current_user_id

    )


    # ------------------------------------------------------
    # NO MATCH
    # ------------------------------------------------------

    if candidates.empty:

        return pd.DataFrame()


    print("\nCandidates from MySQL:")
    print(candidates)


    # ------------------------------------------------------
    # ENCODE CANDIDATES
    # ------------------------------------------------------

    candidate_encoded = encode_data(
        candidates
    )


    x = candidate_encoded[features]


    # ------------------------------------------------------
    # ENCODE CURRENT USER
    # ------------------------------------------------------

    current_user_encoded = {

        "age":
            current_user["age"],

        "gender":
            encoders["gender"].transform(
                [current_user["gender"]]
            )[0],

        "city":
            encoders["city"].transform(
                [current_user["city"]]
            )[0],

        "teach_skill":
            encoders["teach_skill"].transform(
                [current_user["teach_skill"]]
            )[0],

        "learn_skill":
            encoders["learn_skill"].transform(
                [current_user["learn_skill"]]
            )[0],

        "proficiency_level":
            encoders["proficiency_level"].transform(
                [current_user["proficiency_level"]]
            )[0],

        "preferred_language":
            encoders["preferred_language"].transform(
                [current_user["preferred_language"]]
            )[0],

        "learning_mode":
            encoders["learning_mode"].transform(
                [current_user["learning_mode"]]
            )[0],

        "availability":
            encoders["availability"].transform(
                [current_user["availability"]]
            )[0],

        "rating":
            current_user["rating"],

        "completed_exchanges":
            current_user["completed_exchanges"]

    }


    user_vector = pd.DataFrame(
        [current_user_encoded]
    )

    user_vector = user_vector[features]


    # ------------------------------------------------------
    # KNN
    # ------------------------------------------------------

    knn = NearestNeighbors(

        n_neighbors=min(
            5,
            len(x)
        ),

        metric="euclidean"

    )

    knn.fit(x)


    distances, indices = knn.kneighbors(
        user_vector
    )


    # ------------------------------------------------------
    # GET RECOMMENDATIONS
    # ------------------------------------------------------

    recommendations = candidates.iloc[
        indices[0]
    ].copy()


    recommendations["distance"] = distances[0]


    # Smaller distance = better match
    recommendations = recommendations.sort_values(
        by="distance"
    )


    return recommendations