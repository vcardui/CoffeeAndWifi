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
# | WhatIs.......: Form - Class
# +----------------------------------------------------------------------------+

# ------------ Resources / Documentation involved -------------
# Flask-WTF Basic fields: https://wtforms.readthedocs.io/en/3.0.x/fields/#basic-fields
# Flask-WTF Validators: https://wtforms.readthedocs.io/en/3.0.x/validators/#module-wtforms.validators
# Dynamic Forms with Flask: https://blog.miguelgrinberg.com/post/dynamic-forms-with-flask

# Flaskform class pass arguments for constructor:
# Struggling to understand FlaskForm with concurrent use of a constructor with super() function: https://www.reddit.com/r/flask/comments/pag4yl/struggling_to_understand_flaskform_with/
# (It inheritances)
# What Does Super().__Init__(*Args, **Kwargs) Do in Python?: https://www.geeksforgeeks.org/what-does-super-__init__args-kwargs-do-in-python/

# ------------------------- Libraries -------------------------
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, URLField, TimeField, SelectField
from wtforms.validators import InputRequired, Regexp

# ------------------------- Classes -------------------------
class CafeForm(FlaskForm):
    name = StringField('Name', [
        InputRequired("Enter cafe's name"),
        Regexp(
            regex="^[A-Za-z0-9 áéíóúüñÁÉÍÓÚÜÑàâäæçèéêëîïôœùûüÿÀÂÆÇÈÉÊËÎÏÔŒÙÛÜŸß .&'@#-]+$",
            message="Remove any not alphabetical characters or emoji"
        )
    ])

    url = URLField('Cafe Location on google maps', [
        InputRequired("Add location")
    ])

    openingTime = TimeField('Opening time', format='%H:%M')

    closingTime = TimeField('Closing time', format='%H:%M')

    coffeeRating = SelectField('Coffee Rating', coerce=str)
    wifiRating = SelectField('Wifi Rating', coerce=str)
    powerRating = SelectField('Power Rating', coerce=str)

    submit = SubmitField(label="Add")

    def __init__(self, ratings: dict = None, *args, **kwargs):
        super(CafeForm, self).__init__(*args, **kwargs)
        self.coffeeRating.choices = ratings['Coffe']
        self.wifiRating.choices = ratings['Wifi']
        self.powerRating.choices = ratings['Power']