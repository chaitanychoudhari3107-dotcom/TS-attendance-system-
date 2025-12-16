from flask import Flask, jsonify, request
import secrets, time

app = Flask(__name__)

CURRENT_TOKEN = None
TOKEN_EXPIRY = 0

def mark_attendance(name):
    print("TEST MARKED:", name)

@app.route("/")
def home():
    return jsonify({"message": "Backend is running!"})

@app.route("/generate_token", methods=["POST"])
def generate_token():
    global CURRENT_TOKEN, TOKEN_EXPIRY
    CURRENT_TOKEN = secrets.token_hex(4)
    TOKEN_EXPIRY = time.time() + 120
    return jsonify({
        "token": CURRENT_TOKEN,
        "expires_in": 120
    })

@app.route("/mark_attendance", methods=["POST"])
def attendance():
    data = request.get_json()
    token = data.get("token")
    student_name = data.get("student_name")

    if token != CURRENT_TOKEN:
        return jsonify({"status": "error", "message": "Invalid token!"})

    if time.time() > TOKEN_EXPIRY:
        return jsonify({"status": "error", "message": "Token expired!"})

    mark_attendance(student_name)
    return jsonify({
        "status": "success",
        "message": f"Attendance marked for {student_name}"
    })

if __name__ == "__main__":
    app.run(debug=True)
