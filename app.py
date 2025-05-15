from flask import Flask, request, jsonify
from flask_cors import CORS
import json, uuid, os

app = Flask(__name__)
CORS(app)

API_KEY = "123456"

def load_data():
    try:
        with open('students.json', 'r') as f:
            return json.load(f)
    except:
        return []

def save_data(data):
    with open('students.json', 'w') as f:
        json.dump(data, f, indent=4)

@app.before_request
def check_api_key():
    if request.headers.get("x-api-key") != API_KEY:
        return jsonify({"error": "Missing or invalid API Key"}), 403

@app.route('/students', methods=['GET'])
def get_students():
    return jsonify(load_data())

@app.route('/students/<id>', methods=['GET'])
def get_student(id):
    students = load_data()
    student = next((s for s in students if s['id'] == id), None)
    return jsonify(student or {"error": "Not found"}), 404 if not student else 200

@app.route('/students', methods=['POST'])
def create_student():
    students = load_data()
    data = request.get_json()
    data['id'] = str(uuid.uuid4())
    students.append(data)
    save_data(students)
    return jsonify(data), 201

@app.route('/students/<id>', methods=['PUT'])
def update_student(id):
    students = load_data()
    for student in students:
        if student['id'] == id:
            student.update(request.get_json())
            save_data(students)
            return jsonify(student)
    return jsonify({"error": "Not found"}), 404

@app.route('/students/<id>', methods=['DELETE'])
def delete_student(id):
    students = load_data()
    students = [s for s in students if s['id'] != id]
    save_data(students)
    return jsonify({"message": "Deleted"}), 200

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 5000))
    app.run(debug=True, host='0.0.0.0', port=port)
