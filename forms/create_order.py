from flask_wtf import FlaskForm
from wtforms import SubmitField, SelectField
from wtforms.validators import DataRequired, InputRequired
from modules.helpers.data_getter import GetInfo


class CreateOrder(FlaskForm):
    table = SelectField('Стол: ', choices=GetInfo.free_tables(), validators=[InputRequired()])
    waiter = SelectField('Официант: ', choices=GetInfo.waiters(), validators=[DataRequired()])
    food = SelectField('Состав заказа: ', choices=GetInfo.food_list(), validators=[DataRequired()])
    quantity = SelectField('Количество: ', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], validators=[DataRequired()])
    submit = SubmitField('Создать заказ')
