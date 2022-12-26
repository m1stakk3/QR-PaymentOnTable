from flask import Flask, render_template, request
from modules.order_handler import HandleOrder
from modules.add_order import AddOrderForm
from modules.data_getter import DataGetter
import os


app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route("/add_order/", methods=['GET', 'POST'])
def make_order():
    if request.method == 'GET':
        form = AddOrderForm()
        return render_template('create_order.html', form=form)
    if request.method == 'POST':
        table = request.form.get('table')
        waiter = request.form.get('waiter')
        food = request.form.get('food')
        quantity = request.form.get('quantity')
        if HandleOrder.add_order(table=table, waiter=waiter, food=food, qtn=quantity):
            return f'Заказ обработан! Стол: {table}, Официант: {waiter}, Состав заказа: {food} в количестве {quantity}'
        else:
            return 'Ошибка при создании заказа!'


@app.route("/payment/<int:table_id>/", methods=['GET', 'POST'])
def pay_order(table_id):
    if request.method == 'GET':
        debt = DataGetter.get_payment_info(table_id)
        order_id = DataGetter.current_order_for_table(table_id)
        return render_template('payment_page.html', debt=debt, order_id=order_id)
    if request.method == 'POST':
        return 'Позже сделаю'


@app.route("/cancel_order/<int:table_id>/", methods=['GET'])
def cancel_order(table_id):
    if request.method == 'GET':
        answer = HandleOrder.cancel_order(table_id)
        if answer is not None:
            return render_template('order_cancel.html', order_id=answer[1], order_table=table_id)
        else:
            return f'Заказов на столе {table_id} нет'


if __name__ == "__main__":
    app.run(debug=True, port=8999)
