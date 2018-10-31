from flask_wtf import Form
from wtforms import StringField,ValidationError, SelectField, TextAreaField, FloatField
from wtforms.validators import InputRequired, Optional

class AddCategory(Form):
    categoryName = StringField('', validators=[Optional()])
    categoryAmount = FloatField('', validators=[Optional()])