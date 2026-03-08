from flask_wtf import FlaskForm
from flask_wtf.file import FileField, FileAllowed, FileRequired
from wtforms import StringField, TextAreaField, IntegerField, FloatField, SelectField
from wtforms.validators import DataRequired, NumberRange, Optional

class PropertyForm(FlaskForm):
    title = StringField('Property Title', validators=[DataRequired()])
    description = TextAreaField('Description', validators=[DataRequired()])
    bedrooms = IntegerField('Number of Bedrooms', validators=[DataRequired(), NumberRange(min=0)])
    bathrooms = FloatField('Number of Bathrooms', validators=[DataRequired(), NumberRange(min=0)])
    location = StringField('Location', validators=[DataRequired()])
    price = FloatField('Price', validators=[DataRequired(), NumberRange(min=0)])
    currency = SelectField('Currency', choices=[('JMD', 'JMD'), ('USD', 'USD')], validators=[DataRequired()], default='JMD')
    property_type = SelectField('Property Type', choices=[('House', 'House'), ('Apartment', 'Apartment')], validators=[DataRequired()])
    photo = FileField('Photo', validators=[
        FileRequired(),
        FileAllowed(['jpg', 'jpeg', 'png', 'gif'], 'Images only!')
    ])