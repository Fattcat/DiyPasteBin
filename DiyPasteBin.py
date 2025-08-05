from flask import Flask, render_template, request, redirect, url_for, send_from_directory, session
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))
app = Flask(__name__)
app.secret_key = 'tajny_kluc_sem_daj_silny'  # Zmeň si to na silný tajný kľúč

USERNAME = 'admin'
PASSWORD = 'dONKo'  # môžeš si neskôr spraviť hashovanie

PASTE_FOLDER = 'ulozene_subory'
UPLOAD_FOLDER = 'uploady'
os.makedirs(PASTE_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

def login_required(f):
    from functools import wraps
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if not session.get('logged_in'):
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

@app.route('/login', methods=['GET', 'POST'])
def login():
    error = None
    if request.method == 'POST':
        if request.form['username'] == USERNAME and request.form['password'] == PASSWORD:
            session['logged_in'] = True
            return redirect(url_for('index'))
        else:
            error = 'Nesprávne meno alebo heslo.'
    return render_template('login.html', error=error)

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

@app.route('/')
@login_required
def index():
    paste_files = os.listdir(PASTE_FOLDER)
    upload_files = os.listdir(UPLOAD_FOLDER)
    return render_template('index.html', files=paste_files, upload_files=upload_files)

@app.route('/save', methods=['POST'])
@login_required
def save_file():
    nazov = request.form.get('nazov', '').strip()
    obsah = request.form.get('obsah', '').replace('\r\n', '\n')
    if not nazov:
        return render_template('index.html', chyba="Musíte zadať názov súboru.", obsah=obsah, nazov=nazov,
                               files=os.listdir(PASTE_FOLDER),
                               upload_files=os.listdir(UPLOAD_FOLDER))
    filepath = os.path.join(PASTE_FOLDER, nazov)
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(obsah)
    return redirect(url_for('index'))

@app.route('/open/<filename>')
@login_required
def open_file(filename):
    filepath = os.path.join(PASTE_FOLDER, filename)
    if os.path.exists(filepath):
        with open(filepath, 'r', encoding='utf-8') as f:
            obsah = f.read()
        return render_template('index.html', obsah=obsah, nazov=filename,
                               files=os.listdir(PASTE_FOLDER),
                               upload_files=os.listdir(UPLOAD_FOLDER))
    else:
        return render_template('index.html', chyba="Súbor neexistuje.",
                               files=os.listdir(PASTE_FOLDER),
                               upload_files=os.listdir(UPLOAD_FOLDER))

@app.route('/upload', methods=['POST'])
@login_required
def upload_file():
    file = request.files.get('file')
    if file and file.filename != '':
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
@login_required
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5001, debug=True)
