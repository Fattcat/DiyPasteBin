from flask import Flask, render_template, request, redirect, url_for, send_from_directory
import os

os.chdir(os.path.dirname(os.path.abspath(__file__)))  # Zabezpečí správne relatívne cesty
app = Flask(__name__)

PASTE_FOLDER = 'ulozene_subory'
UPLOAD_FOLDER = 'uploady'
os.makedirs(PASTE_FOLDER, exist_ok=True)
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route('/')
def index():
    paste_files = os.listdir(PASTE_FOLDER)
    upload_files = os.listdir(UPLOAD_FOLDER)
    return render_template('index.html', files=paste_files, upload_files=upload_files)

@app.route('/save', methods=['POST'])
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
def upload_file():
    file = request.files.get('file')
    if file and file.filename != '':
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], file.filename))
    return redirect(url_for('index'))

@app.route('/uploads/<filename>')
def download_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename, as_attachment=True)

if __name__ == '__main__':
    app.run(host="192.168.x.xxx",port=5001, debug=True)
