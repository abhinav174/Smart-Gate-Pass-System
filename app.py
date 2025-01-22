from flask import Flask, render_template, request, redirect, url_for, session,send_file
import qrcode
import datetime
import io

app = Flask(__name__)
app.secret_key = '8688252160'  # Replace with a strong secret key

# Sample user data (replace with actual database)
users = {
    "teacher1": {"username": "teacher1", "password": "password1"},
    "student1": {"username": "student1", "password": "password1"},
}

class GatePassSystem:
    def __init__(self):
        self.pending_requests = [] 

    def create_gate_pass_request(self, student_name, student_id, reason):
        """
        Creates a gate pass request.

        Args:
            student_name: Name of the student.
            student_id: Student ID.
            reason: Reason for leaving/entering the college.

        Returns:
            A dictionary containing the gate pass request details.
        """
        request_id = f"GPR_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"
        request_data = {
            "request_id": request_id,
            "student_name": student_name,
            "student_id": student_id,
            "reason": reason,
            "status": "Pending"
        }
        self.pending_requests.append(request_data)
        return request_data

    def get_pending_requests(self):
        """
        Returns a list of pending gate pass requests.
        """
        return self.pending_requests

    def approve_request(self, request_id):
        """
        Approves a gate pass request.

        Args:
            request_id: ID of the request to approve.
        """
        for i, request in enumerate(self.pending_requests):
            if request["request_id"] == request_id:
                self.pending_requests[i]["status"] = "Approved"
                break

    def reject_request(self, request_id):
        """
        Rejects a gate pass request.

        Args:
            request_id: ID of the request to reject.
        """
        for i, request in enumerate(self.pending_requests):
            if request["request_id"] == request_id:
                self.pending_requests[i]["status"] = "Rejected"
                break

    def generate_gate_pass(self, request_data):
        """
        Generates a gate pass with a QR code.

        Args:
            request_data: Approved gate pass request data.

        Returns:
            A dictionary containing the gate pass details and the QR code data.
        """
        pass_id = f"GP_{datetime.datetime.now().strftime('%Y%m%d%H%M%S')}"

        gate_pass_data = {
            "pass_id": pass_id,
            "student_name": request_data["student_name"],
            "student_id": request_data["student_id"],
            "reason": request_data["reason"],
            "time_in": datetime.datetime.now().strftime("%H:%M:%S"),
            "time_out": None,
            "date": datetime.datetime.now().strftime("%Y-%m-%d"),
            "status": "Active" 
        }

        qr_data = str(gate_pass_data)

        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(qr_data)
        qr.make(fit=True)
        img = qr.make_image(fill_color="black", back_color="white")

        return {
            "pass_id": pass_id,
            "gate_pass_data": gate_pass_data,
            "qr_code": img
        }

gate_pass_system = GatePassSystem()

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']

        if username in users and users[username]['password'] == password:
            session['username'] = username
            session['user_type'] = 'teacher' if username in ['teacher1'] else 'student'  # Simplified user type check
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid username or password')

    return render_template('login.html')

@app.route('/logout')
def logout():
    session.pop('username', None)
    session.pop('user_type', None)
    return redirect(url_for('index'))


@app.route('/dashboard')
def dashboard():
    if 'username' in session:
        if session['user_type'] == 'teacher':
            pending_requests = gate_pass_system.get_pending_requests() 
            return render_template('teacher_dashboard.html', pending_requests=pending_requests)
        elif session['user_type'] == 'student':
            student_name = session.get('username')
            student_requests = [request for request in gate_pass_system.pending_requests if 
                                request['student_name'] == student_name]
            return render_template('student_dashboard.html', requests=student_requests)
    else:
        return redirect(url_for('login'))

@app.route('/student/request_gate_pass', methods=['GET', 'POST'])
def student_request_gate_pass():
    if 'username' in session and session['user_type'] == 'student':
        if request.method == 'POST':
            student_name = session.get('username')  # Get student name from session
            student_id = request.form['student_id']  # Get student ID from form
            reason = request.form['reason']
            gate_pass_system.create_gate_pass_request(student_name, student_id, reason)
            return redirect(url_for('student_dashboard'))
        return render_template('student_request_gate_pass.html')
    else:
        return redirect(url_for('login'))

@app.route('/teacher/approve_request/<request_id>')
def teacher_approve_request(request_id):
    if 'username' in session and session['user_type'] == 'teacher':
        gate_pass_system.approve_request(request_id)
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))

@app.route('/teacher/reject_request/<request_id>')
def teacher_reject_request(request_id):
    if 'username' in session and session['user_type'] == 'teacher':
        gate_pass_system.reject_request(request_id)
        return redirect(url_for('dashboard'))
    else:
        return redirect(url_for('login'))

@app.route('/student/dashboard') 
def student_dashboard():
    if 'username' in session and session['user_type'] == 'student':
        return render_template('student_dashboard.html') 
    else:
        return redirect(url_for('login'))
    
# ... (Add routes for generating and displaying QR codes)
@app.route('/student/generate_qr_code')
def student_generate_qr_code():
    if 'username' in session and session['user_type'] == 'student':
        # Find the latest approved request for the student
        student_name = session.get('username')
        approved_requests = [request for request in gate_pass_system.pending_requests if 
                            request['student_name'] == student_name and request['status'] == 'Approved']
        if approved_requests:
            latest_request = approved_requests[-1]  # Get the most recent approved request
            gate_pass = gate_pass_system.generate_gate_pass(latest_request)

            # Create an in-memory file for the QR code image
            img_io = io.BytesIO()
            gate_pass["qr_code"].save(img_io, format='PNG')
            img_io.seek(0)

            # Return the QR code image as a response
            return send_file(img_io, mimetype='image/png')
        else:
            return render_template('student_dashboard.html', error="No approved gate pass found.")
    else:
        return redirect(url_for('login'))

# Adjust student_dashboard.html to include a link to generate the QR code

if __name__ == '__main__':
    app.run(debug=True)