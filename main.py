from flask import Flask, render_template, request
from modules.order_handler import HandleOrder
from modules.add_order import AddOrderForm
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
        order_info = request.form.get('order_info')
        return f'Заказ обработан! Стол: {table}, Официант: {waiter}, Состав заказа: {order_info}'


if __name__ == "__main__":
    app.run(debug=True, port=8999)
