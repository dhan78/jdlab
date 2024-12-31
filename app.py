from flask import Flask, render_template, request, redirect, url_for, session
from werkzeug.utils import secure_filename
import os
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'your-secret-key-here'  # Required for session

# Default admin credentials
ADMIN_EMAIL = "admin@jdlab.com"
ADMIN_PASSWORD = "Simba2025"

# Configure upload folder
UPLOAD_FOLDER = 'uploads'

# Create uploads directory if it doesn't exist
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        if email == ADMIN_EMAIL and password == ADMIN_PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('upload_file'))
        else:
            return render_template('login.html', error="Invalid credentials")
    
    return render_template('login.html')

@app.route('/upload', methods=['GET', 'POST'])
def upload_file():
    if not session.get('logged_in'):
        return redirect(url_for('login'))
        
    if request.method == 'POST':
        if 'files[]' not in request.files:
            return 'No file part', 400
        
        files = request.files.getlist('files[]')
        
        for file in files:
            if file and file.filename:
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        
        return redirect(url_for('upload_file'))
    
    # List uploaded files with their timestamps
    files = []
    for file in os.listdir(app.config['UPLOAD_FOLDER']):
        timestamp = os.path.getmtime(os.path.join(app.config['UPLOAD_FOLDER'], file))
        date_str = datetime.fromtimestamp(timestamp).strftime('%Y-%m-%d %H:%M:%S')
        files.append({'name': file, 'date': date_str})
    
    return render_template('upload.html', files=files)

@app.route('/logout')
def logout():
    session.pop('logged_in', None)
    return redirect(url_for('login'))

if __name__ == '__main__':
    app.run(debug=True) 