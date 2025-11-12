import os
import time
import subprocess
import sys
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
UPLOAD_FOLDER = 'uploads'
PASSWORD = "MIXO"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

ALLOWED_EXTENSIONS = {'py'}

# إنشاء مجلد uploads إذا ما كانش موجود
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/Api-hosting-python-by-xzanja-py/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        password = request.form.get('password')
        if password == PASSWORD:
            return redirect('/how-to-use')
    return render_template('login.html')

@app.route('/how-to-use', methods=['GET', 'POST'])
def how_to_use():
    if request.method == 'POST':
        return redirect('/dashboard')
    return render_template('how_to_use.html')

@app.route('/dashboard', methods=['GET', 'POST'])
def dashboard():
    files = os.listdir(app.config['UPLOAD_FOLDER'])
    message = ""
    if request.method == "POST":
        package_name = request.form.get('package_name')
        message = install_package(package_name)
    return render_template('dashboard.html', files=files, message=message)

def install_package(package_name):
    try:
        subprocess.check_call([sys.executable, "-m", "pip", "install", package_name])
        return f"تم تثبيت المكتبة {package_name} بنجاح!"
    except subprocess.CalledProcessError:
        return f"فشل في تثبيت المكتبة {package_name}."

@app.route('/upload', methods=['POST'])
def upload():
    file = request.files['file']
    if file and allowed_file(file.filename):
        filepath = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(filepath)
    return redirect('/dashboard')

@app.route('/run/<filename>')
def run_script(filename):
    filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if not os.path.exists(filepath):
        return f"<h3>File <b>{filename}</b> not found.</h3><br><a href='/dashboard'>Back to Dashboard</a>"
    try:
        subprocess.Popen(['python3', filepath])
        return f"<h3>Script <b>{filename}</b> is running in the background.</h3><br><a href='/dashboard'>Back to Dashboard</a>"
    except Exception as e:
        return f"<h3>Error running script:</h3><pre>{str(e)}</pre>"

@app.route('/speed')
def speed():
    start = time.time()
    for _ in range(1000000): pass
    end = time.time()
    return f"<h2>Speed Test Done in {end - start:.4f} seconds</h2>"

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000, debug=True)
