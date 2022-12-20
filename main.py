from flask import Flask
from order_handler import HandleOrder

app = Flask(__name__)


@app.route("/add_order/<int:table_number>/<int:waiter_id>/<string:food>/<int:quantity>")
def make_order(table_number, waiter_id, food, quantity):
    order = HandleOrder.add_order(table=table_number, waiter=waiter_id, food=food, qtn=quantity)
    return order


if __name__ == "__main__":
    app.run(debug=True, port=8999)
