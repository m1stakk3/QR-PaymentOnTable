from flask import Flask, render_template, request
from modules.order_handler import HandleOrder
from forms.create_order import CreateOrder
from forms.order_payment import OrderPayment
from modules.helpers.data_getter import GetInfo
from modules.payment_handler import Payment
import os


app = Flask(__name__)
SECRET_KEY = os.urandom(32)
app.config['SECRET_KEY'] = SECRET_KEY


@app.route("/create_order/", methods=['GET', 'POST'])
def create():
    """ страница создания заказа """
    if request.method == 'GET':
        form = CreateOrder()
        return render_template('create_order.html', form=form)
    if request.method == 'POST':
        table = request.form.get('table')
        waiter = request.form.get('waiter')
        food = request.form.get('food')
        quantity = request.form.get('quantity')
        if HandleOrder.create_order(table=table, waiter=waiter, food=food, qtn=quantity):
            return f'Заказ обработан! Стол: {table}, Официант: {waiter}, Состав заказа: {food} в количестве {quantity}'
        else:
            return 'Ошибка при создании заказа!'


@app.route("/update_order/<int:table_id>", methods=['GET', 'POST'])
def update(table_id):
    """ страница дополнения заказа """
    if request.method == 'GET':
        pass
    if request.method == 'POST':
        pass


@app.route("/cancel_order/<int:table_id>/", methods=['GET'])
def cancel(table_id):
    """ страница отмены заказа """
    if request.method == 'GET':
        answer = HandleOrder.cancel_order(table_id)
        if answer is not None:
            return render_template('order_cancel.html', order_id=answer[1], order_table=table_id)
        else:
            return f'Заказов на столе {table_id} нет'


@app.route("/payment/<int:table_id>/", methods=['GET', 'POST'])
def payment(table_id):
    """ страница оплаты заказа """
    order_id = GetInfo.table_order(table_id)
    if request.method == 'GET':
        debt = GetInfo.debt(table_id)
        if debt is False:
            return render_template('payment_page1.html', order_id=order_id)
        else:
            form = OrderPayment()
            debt = GetInfo.debt(table_id)
            return render_template('payment_page.html', form=form, order_id=order_id, debt=debt)
    if request.method == 'POST':
        money = request.form.get('money')
        if Payment.pay(order_id, money):
            return 'Оплата внесена'
        else:
            return render_template('payment_page1.html', order_id=order_id)


if __name__ == "__main__":
    app.run(debug=True, port=8999)
