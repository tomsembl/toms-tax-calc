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

def comma_number(number): return ("{:,}".format(number))

def austax(gross, hecs):
    #Error Handling
    if type(gross) not in (int, float): raise TypeError(f"type {type(gross)} is not int or float")
    if gross < 0 or gross > 10**20: raise ValueError("outside of bounds 0 - 10²⁰")

    #Tax
    if gross >= 180001: tax = 51667 + 0.45 * (gross - 180000)
    elif gross >= 120001: tax = 29467 + 0.37 * (gross - 120000)
    elif gross >= 45001: tax = 5092 + 0.325 * (gross - 45000)
    elif gross >= 18201: tax = 0.19 * (gross - 18200)
    else: tax = 0
    tax_percent = round(100*tax/(gross+0.01), 2)

    #HECS
    if hecs:
        hecs_brackets = [0, 47014, 54283, 57539, 60992, 64652, 68530, 72642, 77002, 81621, 86519, 91710, 97213, 103046, 109228, 115782, 122729, 130093, 137898, 10**20]
        hecs_percents = [0, 0.01, 0.02, 0.025, 0.03, 0.035, 0.04, 0.045, 0.05, 0.055, 0.06, 0.065, 0.07, 0.075, 0.08, 0.085, 0.09, 0.095, 0.1]
        for i, hecs_bracket in enumerate(hecs_brackets):
            if i == len(hecs_brackets)-1: break #error handling
            if hecs_bracket <= gross < hecs_brackets[i+1]: hecs_percent = hecs_percents[i]
        hecs = gross * hecs_percent
        hecs_percent = round(100*hecs_percent, 2)
    
    net = gross - tax - hecs if hecs else gross - tax
    net_percent = round(100-hecs_percent-tax_percent if hecs else 100-tax_percent, 2)
    
    #Output
    return f"Gross:${gross}: , Net:${int(net)}:({net_percent}%), Tax:${int(tax)}:({tax_percent}%)" + (f", HECS:${int(hecs)}:({hecs_percent}%)" if hecs else "")


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