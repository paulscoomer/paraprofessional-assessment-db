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
                WHERE submission_uuid = %s;
                """,
                (
                    data.get('nonacceptance', 0), data.get('goals', 0), data.get('impulse', 0), data.get('awareness', 0),
                    data.get('strategies', 0), data.get('clarity', 0), data.get('total', 0), uuid
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
                WHERE submission_uuid = %s;
                """,
                (
                    data.get('self_disclosure', 0), data.get('empathy', 0), data.get('social_relaxation', 0),
                    data.get('assertiveness', 0), data.get('altercentrism', 0), data.get('interaction_management', 0),
                    data.get('expressiveness', 0), data.get('supportiveness', 0), data.get('immediacy', 0),
                    data.get('environmental_control', 0), data.get('total', 0), uuid
                )
            )
        elif form_type == 'literacy_numeracy':
            cur.execute(
                """
                UPDATE participants
                SET literacy_comprehension = %s, literacy_grammar = %s, literacy_critical_thinking = %s, literacy_total = %s,
                    math_numerical_operations = %s, math_problem_solving = %s, math_data_interpretation = %s, math_total = %s
                WHERE submission_uuid = %s;
                """,
                (
                    data.get('literacy_comprehension', 0), data.get('literacy_grammar', 0), data.get('literacy_critical_thinking', 0), data.get('literacy_total', 0),
                    data.get('math_numerical_operations', 0), data.get('math_problem_solving', 0), data.get('math_data_interpretation', 0), data.get('math_total', 0), uuid
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
        form_data = request.get_json()
        print("Received form data:", form_data)  # Debug logging

        # Safely access required keys from the payload
        form_type = form_data.get('form_type')
        uuid_value = form_data.get('uuid')
        data = form_data.get('data')
        role = form_data.get('role')

        # Validate required keys are present
        if not form_type or not data or not role:
            raise ValueError("Missing one or more required keys: form_type, data, or role")

        # If UUID doesn't exist, generate a new one
        if not uuid_value:
            uuid_value = str(uuid.uuid4())

        # Insert data for the appropriate form using safe key access
        insert_data(uuid_value, data, role, form_type)

        return jsonify({"status": "success", "uuid": uuid_value}), 200

    except Exception as e:
        print(f"Error processing webhook: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500

if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port, debug=True)
