**Smart Gate Pass System**

This Flask application implements a basic gate pass system for a school. It allows students to request gate passes, teachers to approve or reject requests, and students to generate QR codes for approved gate passes.

**Features**

User authentication (teachers and students)
Student gate pass request creation with reason
Teacher dashboard to view pending requests
Teacher functionalities to approve or reject requests
Student dashboard to view their gate pass requests
QR code generation for approved gate passes (students only)
**Requirements**

Python 3.x
Flask (pip install Flask)
Flask-Session (pip install Flask-Session)
QRCode library (pip install qrcode)
Running the Application

Save the code as a Python file (e.g., gate_pass_system.py).
Replace the sample user data in the users dictionary with a connection to your actual user database.
Install the required libraries (pip install ...).
Run the script using python gate_pass_system.py.
This will launch the development server, typically accessible at [invalid URL removed] (assuming you run the app from your local machine).
**Deployment**

For deployment on a production server, you can configure a web server like Heroku or AWS to run the Python script.

**Security Considerations**

This is a basic implementation and does not include robust security measures.
In production, consider using a more secure user authentication mechanism and data storage.
Implement proper authorization checks to restrict access based on user roles.
**Further Enhancements**

Integrate with a database for persistent storage of user data and gate pass requests.
Implement email notifications for gate pass approvals/rejections.
Add functionalities for logging gate pass usage (entry/exit times).
Enhance the UI with better styling and user experience elements.

**Home Screen/Login Screen**
![image](https://github.com/user-attachments/assets/6a2a495a-13c5-4b08-a4b5-71a0892cf300)

**Student Dashboard**
![image](https://github.com/user-attachments/assets/f96b0b79-cb8e-4d2b-bf3d-b654ade15d18)

**Student Request Form** 
![image](https://github.com/user-attachments/assets/a7915caa-15b0-4b76-9010-6811a789c817)

**Teacher Dashboard**
![image](https://github.com/user-attachments/assets/105987f7-97df-4786-aaee-c212b5db8abb)

**Student QR Code Generation**
![image](https://github.com/user-attachments/assets/397af076-e5f9-448e-8847-4f0b1f8ccd85)



