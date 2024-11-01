# app.py
from flask import Flask, jsonify, request, make_response
import json
from database import get_db_connection
from io import StringIO
import csv

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

# Endpoint to update a guest's preferences and allergies
@app.route('/guests/<int:guest_id>', methods=['PATCH'])
def update_guest(guest_id):
    data = request.json
    conn = get_db_connection()
    cursor = conn.cursor()
    
    # Check if the guest exists
    cursor.execute('SELECT * FROM guests WHERE id = ?', (guest_id,))
    guest = cursor.fetchone()
    if not guest:
        conn.close()
        return jsonify({"error": "Guest not found"}), 404
    
    # Build the update statement dynamically based on provided fields
    fields = []
    values = []
    
    if 'preferences' in data:
        preferences = json.dumps(data['preferences'])
        fields.append('preferences = ?')
        values.append(preferences)
        
    if 'allergy' in data:
        fields.append('allergy = ?')
        values.append(data['allergy'])
    
    if not fields:
        conn.close()
        return jsonify({"error": "No fields to update"}), 400
    
    # Prepare the SQL query
    values.append(guest_id)
    sql = 'UPDATE guests SET ' + ', '.join(fields) + ' WHERE id = ?'
    
    cursor.execute(sql, values)
    conn.commit()
    conn.close()
    
    return jsonify({"message": "Guest updated successfully"}), 200

# Endpoint to export guests data as CSV
@app.route('/guests/csv', methods=['GET'])
def export_guests_csv():
    conn = get_db_connection()
    cursor = conn.cursor()
    cursor.execute('SELECT * FROM guests')
    guests = cursor.fetchall()
    conn.close()
    
    si = StringIO()
    writer = csv.writer(si)
    
    # Write CSV header
    writer.writerow(['ID', 'Name', 'Email', 'Preferences', 'Allergy'])
    
    # Write guest data
    for guest in guests:
        writer.writerow([
            guest['id'],
            guest['name'],
            guest['email'],
            guest['preferences'],
            guest['allergy']
        ])
    
    # Create a response with the CSV data
    output = make_response(si.getvalue())
    output.headers["Content-Disposition"] = "attachment; filename=guests.csv"
    output.headers["Content-type"] = "text/csv"
    return output

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5004)