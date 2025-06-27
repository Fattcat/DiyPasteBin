# pastebin
from flask import Flask, request, render_template, redirect, url_for
import os

app = Flask(__name__)
PASTE_DIR = "pastes"
os.makedirs(PASTE_DIR, exist_ok=True)

@app.route("/", methods=["GET", "POST"])
def index():
    paste_content = ""
    filename = ""

    if request.method == "POST":
        filename = request.form.get("filename", "").strip()
        paste_content = request.form.get("paste", "")
        filename = filename if filename else "default.txt"
        filename = secure_filename(filename)

        with open(os.path.join(PASTE_DIR, filename), "w", encoding="utf-8", newline="\n") as f:
            f.write(paste_content)
        return redirect(url_for("index", file=filename))

    # Načítaj zoznam súborov
    files = sorted(os.listdir(PASTE_DIR))

    # Ak je v URL file, načítaj jeho obsah
    file_to_open = request.args.get("file")
    if file_to_open and file_to_open in files:
        filepath = os.path.join(PASTE_DIR, file_to_open)
        with open(filepath, "r", encoding="utf-8") as f:
            paste_content = f.read()
        filename = file_to_open

    return render_template("index.html", paste=paste_content, files=files, filename=filename)


def secure_filename(name):
    # Odstráň nebezpečné znaky pre názov súboru
    return "".join(c for c in name if c.isalnum() or c in (' ', '.', '_', '-')).strip()

if __name__ == "__main__":
#    app.run(host="0.0.0.0", port=5000, debug=True)
