import os
import psycopg2
import uuid
from flask import Flask, request, jsonify
from psycopg2.extras import Json

# Database connection setup
DATABASE_URL = os.environ.get('DATABASE_URL', 'your_database_url')

app = Flask(__name__)

@app.route('/')
def home():
    return "Flask is running, and the webhook is available at /webhook."

# Helper function to insert form data into the database
def insert_data(uuid, data, role, form_type):
    try:
        # Connect to the database
        conn = psycopg2.connect(DATABASE_URL)
        cur = conn.cursor()

        # Depending on the form type (DERS, ICCS, Literacy, Math), insert data
        if form_type == 'ders':
            cur.execute(
                """
                UPDATE participants
                SET ders_nonacceptance = %s, ders_goals = %s, ders_impulse = %s, ders_awareness = %s, 
                    ders_strategies = %s, ders_clarity = %s, ders_total = %s
                WHERE uuid = %s;
                """,
                (
                    data['nonacceptance'], data['goals'], data['impulse'], data['awareness'],
                    data['strategies'], data['clarity'], data['total'], uuid
                )
            )
        elif form_type == 'iccs':
            cur.execute(
                """
                UPDATE participants
                SET iccs_self_disclosure = %s, iccs_empathy = %s, iccs_social_relaxation = %s, 
                    iccs_assertiveness = %s, iccs_altercentrism = %s, iccs_interaction_management = %s, 
                    iccs_expressiveness = %s, iccs_supportiveness = %s, iccs_immediacy = %s, 
                    iccs_environmental_control = %s, iccs_total = %s
                WHERE uuid = %s;
                """,
                (
                    data['self_disclosure'], data['empathy'], data['social_relaxation'], data['assertiveness'], 
                    data['altercentrism'], data['interaction_management'], data['expressiveness'],
                    data['supportiveness'], data['immediacy'], data['environmental_control'], data['total'], uuid
                )
            )
        elif form_type == 'literacy_numeracy':
            cur.execute(
                """
                UPDATE participants
                SET literacy_comprehension = %s, literacy_grammar = %s, literacy_critical_thinking = %s, literacy_total = %s,
                    math_numerical_operations = %s, math_problem_solving = %s, math_data_interpretation = %s, math_total = %s
                WHERE uuid = %s;
                """,
                (
                    data['literacy_comprehension'], data['literacy_grammar'], data['literacy_critical_thinking'], data['literacy_total'],
                    data['math_numerical_operations'], data['math_problem_solving'], data['math_data_interpretation'], data['math_total'], uuid
                )
            )

        conn.commit()

    except Exception as e:
        print(f"Error inserting data for {form_type}: {e}")
    finally:
        cur.close()
        conn.close()

# Webhook endpoint to receive data
@app.route('/webhook', methods=['POST'])
def webhook():
    try:
        # Get the form data
        form_data = request.json
        print("Received form data:", form_data)  # Debug logging

        form_type = form_data.get('form_type')  # 'ders', 'iccs', 'literacy_numeracy', etc.
        uuid_value = form_data.get('uuid')  # The UUID to link forms

        if not uuid_value:
            # If UUID doesn't exist, generate a new one
            uuid_value = str(uuid.uuid4())

        # Insert data for the appropriate form
        insert_data(uuid_value, form_data['data'], form_data['role'], form_type)

        return jsonify({"status": "success", "uuid": uuid_value}), 200

    except Exception as e:
        print(f"Error processing webhook: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
