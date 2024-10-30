# app.py
from flask import Flask, jsonify, request
import json
from database import get_db_connection

app = Flask(__name__)

# Endpoint to create a new guest profile
@app.route('/guests', methods=['POST'])
def create_guest():
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Convert preferences to a JSON string if it's provided as a dictionary
    preferences = json.dumps(data.get('preferences', {}))
    
    cursor.execute('INSERT INTO guests (name, email, preferences, allergy) VALUES (?, ?, ?, ?)',
                   (data['name'], data['email'], preferences, data.get('allergy', '')))
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Guest created successfully"}), 201

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
