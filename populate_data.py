import random
import psycopg2
from faker import Faker

# Database connection setup
DATABASE_URL = "postgres://u4gn2oc4sl89kl:pab7eeb42fcd87eabdaf527f38bd38ec839730ee50c4c30160a0fd620d6951f79@cd1goc44htrmfn.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/dedbcjon211l4f"

# Initialize Faker
fake = Faker()

# Constants for gender distribution
total_women = 260
total_men = 97
total_participants = total_women + total_men

# Role distribution
roles = ["Administrator", "Therapist/Teacher", "Paraprofessional", "Other"]
role_counts = {"Administrator": 10, "Therapist/Teacher": 36, "Paraprofessional": 27, "Other": total_participants - (10 + 36 + 27)}

# Education distribution
education_levels = [
    "No Degree", "Diploma/GED", "Associates/Some College", "Bachelor's Degree", "Master's Degree", "Post Graduate Degree"
]

# Age categories
age_range_categories = ["Under 18", "18-24", "25-34", "35-44", "45-54", "55+"]


# Helper function to generate valid education level
def get_education(role):
    if role == "Administrator":
        return random.choice(["Master's Degree", "Post Graduate Degree"])
    elif role == "Therapist/Teacher":
        return random.choices(["Bachelor's Degree", "Master's Degree"], weights=[0.4, 0.6])[0]
    elif role == "Paraprofessional":
        return random.choices(["Diploma/GED", "Bachelor's Degree"], weights=[0.8, 0.2])[0]
    else:  # "Other"
        return random.choices(education_levels, weights=[0.1, 0.5, 0.2, 0.15, 0.04, 0.01])[0]


# Generate age based on role constraints
def get_age_range(role, education):
    if role == "Administrator":
        return random.choice(["35-44", "45-54", "55+"])
    if role == "Therapist/Teacher":
        return random.choices(["18-24", "25-34", "35-44", "45-54", "55+"], weights=[0.1, 0.35, 0.3, 0.15, 0.1])[0]
    if role == "Paraprofessional":
        return random.choice(age_range_categories)
    if role == "Other" and education in ["Bachelor's Degree", "Master's Degree", "Post Graduate Degree"]:
        return random.choice(["25-34", "35-44", "45-54", "55+"])
    return random.choice(age_range_categories)


# Generate assessment scores
def generate_ders():
    ders_scores = {
        "nonacceptance": random.randint(6, 30),
        "goals": random.randint(5, 25),
        "impulse": random.randint(6, 30),
        "awareness": random.randint(6, 30),
        "strategies": random.randint(8, 40),
        "clarity": random.randint(5, 25),
    }
    ders_total = sum(ders_scores.values())
    return ders_scores, ders_total

def generate_iccs():
    subscores = {
        "self_disclosure": random.randint(3, 15),
        "empathy": random.randint(3, 15),
        "social_relaxation": random.randint(3, 15),
        "assertiveness": random.randint(3, 15),
        "altercentrism": random.randint(3, 15),
        "interaction_management": random.randint(3, 15),
        "expressiveness": random.randint(3, 15),
        "immediacy": random.randint(3, 15),
        "environmental_control": random.randint(3, 15),
        "supportiveness": random.randint(3, 15),
    }

    total_score = sum(subscores.values())
    return subscores, total_score


def generate_literacy():
    return {
        "comprehension": random.choice([0, 25, 50, 75, 100]),
        "grammar_syntax": random.choice([0, 33, 66, 100]),
        "critical_thinking": random.choice([0, 33, 66, 100]),
    }


def generate_math():
    return {
        "numerical_operations": random.choice([0, 25, 50, 75, 100]),
        "problem_solving": random.choice([0, 33, 66, 100]),
        "data_interpretation": random.choice([0, 33, 66, 100]),
    }


# Connect to the database
try:
    conn = psycopg2.connect("postgres://u4gn2oc4sl89kl:pab7eeb42fcd87eabdaf527f38bd38ec839730ee50c4c30160a0fd620d6951f79@cd1goc44htrmfn.cluster-czrs8kj4isg7.us-east-1.rds.amazonaws.com:5432/dedbcjon211l4f"
)
    cur = conn.cursor()

    # Clear table before inserting new data
    cur.execute("DELETE FROM participants;")
    cur.execute("ALTER SEQUENCE participants_id_seq RESTART WITH 1;")

    # Insert new participants
    for _ in range(total_participants):
        gender = "Female" if _ < total_women else "Male"
        role = random.choices(roles, weights=[10, 36, 27, total_participants - 73])[0]
        education = get_education(role)
        age_range = get_age_range(role, education)
        ders_scores, ders_total = generate_ders() 
        iccs_subscores, iccs_total_score = generate_iccs()
        literacy_scores = generate_literacy()
        math_scores = generate_math()

        # Insert into database
        cur.execute(
    """
    INSERT INTO participants 
    (gender, role, education_level, age_range, 
     ders_nonacceptance, ders_goals, ders_impulse, ders_awareness, ders_strategies, ders_clarity, ders_total, 
     iccs_self_disclosure, iccs_empathy, iccs_social_relaxation, iccs_assertiveness, iccs_altercentrism, 
     iccs_interaction_management, iccs_expressiveness, iccs_supportiveness, iccs_immediacy, iccs_environmental_control, iccs_total, 
     literacy_comprehension, literacy_grammar, literacy_critical_thinking, 
     math_numerical_operations, math_problem_solving, math_data_interpretation)
    VALUES (%s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, %s, %s, %s, %s, %s, %s, %s, 
            %s, %s, %s, 
            %s, %s, %s);
    """,
    (
        gender, role, education, age_range, 
        ders_scores["nonacceptance"], ders_scores["goals"], ders_scores["impulse"], 
        ders_scores["awareness"], ders_scores["strategies"], ders_scores["clarity"], ders_total,  
        iccs_subscores["self_disclosure"], iccs_subscores["empathy"], iccs_subscores["social_relaxation"],
        iccs_subscores["assertiveness"], iccs_subscores["altercentrism"], iccs_subscores["interaction_management"],
        iccs_subscores["expressiveness"], iccs_subscores["supportiveness"], iccs_subscores["immediacy"], 
        iccs_subscores["environmental_control"], iccs_total_score,  
        literacy_scores["comprehension"], literacy_scores["grammar_syntax"], literacy_scores["critical_thinking"],
        math_scores["numerical_operations"], math_scores["problem_solving"], math_scores["data_interpretation"]
    )
)


    conn.commit()
    print("Dummy data inserted successfully! Total records:", total_participants)

except Exception as e:
    print("Error:", e)

finally:
    cur.close()
    conn.close()
