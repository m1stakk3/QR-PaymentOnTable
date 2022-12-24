from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, ValidationError, InputRequired, Length
from modules.data_getter import DataGetter


class DataValidators:
    @staticmethod
    def table_checker(form, field):
        if (field.data < 1) and (field.data > 10):
            raise ValidationError('Диапазон столов от 1 до 10!')


class AddOrderForm(FlaskForm):
    table = SelectField('Стол: ', choices=DataGetter.get_free_tables(), validators=[InputRequired()])
    waiter = SelectField('Официант: ', choices=DataGetter.get_waiters(), validators=[DataRequired()])
    food = SelectField('Состав заказа: ', choices=DataGetter.get_food(), validators=[DataRequired()])
    quantity = SelectField('Количество: ', choices=[(1, '1'), (2, '2'), (3, '3'), (4, '4'), (5, '5')], validators=[DataRequired()])
    submit = SubmitField('Создать заказ')