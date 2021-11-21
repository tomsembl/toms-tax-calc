# cd /d c:\users\tom.mcelhinney/python/tax-calc/
# pipenv shell
# set FLASK_ENV=development (CMD), $env:FLASK_ENV = "development" (powershell)
# flask run --host=0.0.0.0 --port=5000

import os
try: from flask import Flask
except: 
    os.system('cmd /c "pip install --trusted-host pypi.org --trusted-host files.pythonhosted.org flask"')
    from flask import Flask
from flask import render_template, request, flash, redirect, url_for
from austax import austax

app = Flask(__name__)
app.secret_key = 'UAHFufaue9f9afae73BBB8FB32qF9'

@app.route('/')
def root():
    return redirect(url_for('home'))

@app.route('/home', methods=["GET", "POST"])
def home():
    if request.method == "GET":
        return render_template("tax-calc.html")
    else:
        gross = request.form['amount']
        is_hecs = request.form.get('hecs')
        print("Gross:", gross+", Hecs:", is_hecs)
        if gross.isnumeric():
            for item in austax(int(gross),bool(is_hecs)).split(", "):
                flash(item)
        else:
            flash("error: only number characters allowed")
        return render_template("tax-calc.html")

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=80)