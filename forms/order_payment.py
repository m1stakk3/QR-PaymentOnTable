from flask_wtf import FlaskForm
from wtforms import SubmitField, IntegerField
from wtforms.validators import DataRequired, InputRequired


class OrderPayment(FlaskForm):
    """ форма оплаты для приема данных """
    money = IntegerField(label=None, validators=[InputRequired(), DataRequired()])
    submit = SubmitField('Оплатить')
