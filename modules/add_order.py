from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, IntegerField, SelectField
from wtforms.validators import DataRequired, ValidationError, InputRequired, Length


class DataValidators:
    @staticmethod
    def table_checker(form, field):
        if (field.data < 1) and (field.data > 10):
            raise ValidationError('Диапазон столов от 1 до 10!')


class AddOrderForm(FlaskForm):
    table = IntegerField('Стол: ', validators=[InputRequired(), Length(min=1, max=2)])
    waiter = SelectField('Официант: ', choices=[(1, 'Сильный'), (2, 'Тестер')], validators=[DataRequired()])
    order_info = StringField('Состав заказа: ', validators=[DataRequired()])
    submit = SubmitField('Создать заказ')