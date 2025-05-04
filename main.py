# +----------------------------------------------------------------------------+
# | CARDUI WORKS v1.0.0
# +----------------------------------------------------------------------------+
# | Copyright (c) 2024 - 2025, CARDUI.COM (www.cardui.com)
# | Vanessa Reteguín <vanessa@reteguin.com>
# | Released under the MIT license
# | www.cardui.com/carduiframework/license/license.txt
# +----------------------------------------------------------------------------+
# | Author.......: Vanessa Reteguín <vanessa@reteguin.com>
# | First release: May 2nd, 2025
# | Last update..: May 4th, 2025
# | WhatIs.......: CoffeAndWifi - Main
# +----------------------------------------------------------------------------+

# ------------ Resources / Documentation involved -------------
# Jinja Expressions: https://jinja.palletsprojects.com/en/stable/templates/#jinja-filters.length
# SweetAlert Js with Flask: https://github.com/elijahondiek/SweetAlert-Js-with-Flask

# ------------------------- Libraries -------------------------
from flask import Flask, render_template, flash, redirect, url_for
from flask_bootstrap import Bootstrap5
from csv import reader, writer

from Form import CafeForm

# ------------------------- Variables -------------------------
app = Flask(__name__)
app.config['SECRET_KEY'] = '8BYkEfBA6O6donzWlSihBXox7C0sKR6b'
Bootstrap5(app)



# Cafe's Database rating options
ratings = {
  "Coffe": [],
  "Wifi": [],
  "Power": []
}

icons = {"Coffe": "☕️", "Wifi": "💪", "Power": "🔌"}

for category in ratings:
    rate = ""
    for i in range(0, 5):
        if i == 0 and category != "Coffe":
            ratings[category].append((i, "✘"))
        rate += icons[category]
        ratings[category].append((i+1, rate))

# print(ratings)
# {'Coffe': [(1, '☕️'), (2, '☕️☕️'), (3, '☕️☕️☕️'), (4, '☕️☕️☕️☕️'), (5, '☕️☕️☕️☕️☕️')], 'Wifi': [(0, '✘'), (1, '💪'), (2, '💪💪'), (3, '💪💪💪'), (4, '💪💪💪💪'), (5, '💪💪💪💪💪')], 'Power': [(0, '✘'), (1, '🔌'), (2, '🔌🔌'), (3, '🔌🔌🔌'), (4, '🔌🔌🔌🔌'), (5, '🔌🔌🔌🔌🔌')]}

# ----------------------- Flask routes ------------------------
@app.route("/")
def home():
    return render_template("index.html")


@app.route('/add', methods=["GET", "POST"])
def add_cafe():
    form = CafeForm(ratings)
    if form.validate_on_submit():

        newCafe = []
        for i in form.data:
            newCafe.append(form.data[i])

        newCafe = newCafe[:-2]

        newCafe[2] = newCafe[2].strftime("%H.%M %p")
        newCafe[3] = newCafe[3].strftime("%H.%M %p")

        newCafe[4] = ratings["Coffe"][int(newCafe[4]) - 1][1]
        newCafe[5] = ratings["Wifi"][int(newCafe[5]) - 1][1]
        newCafe[6] = ratings["Power"][int(newCafe[6]) - 1][1]

        # print(newCafe)

        with open('cafe-data.csv', mode='a', newline='') as cafeData_csv:
            write = writer(cafeData_csv)
            write.writerow(newCafe)

        print("newCaffe added")
        flash(f"Record Saved!", "success")
        return redirect( url_for('cafes') )
    return render_template('add.html', form=form)


@app.route('/cafes')
def cafes():
    # Cafe's Data
    with open('cafe-data.csv', newline='', encoding='utf-8') as cafe_csv:
        cafe_data = reader(cafe_csv, delimiter=',')
        cafe_list = []
        for row in cafe_data:
            cafe_list.append(row)
    return render_template('cafes.html', cafes=cafe_list)


if __name__ == '__main__':
    app.run(debug=True)
