import psycopg2
import qrcode
import os


class HandleOrder:

    conn = psycopg2.connect(database="pushkina_restraunt", user="postgres", password="228", host="localhost", port=5432)
    cursor = conn.cursor()

    @staticmethod
    def add_order(table, waiter, food, qtn=1):      # {'Заказ': 0, 'Состав': {'Позиция': '', 'Кол-во': 0}}):
        HandleOrder.cursor.execute(f"SELECT table_in_use FROM tables WHERE table_id = {table}")
        table_status = list(HandleOrder.cursor.fetchone())[0]
        HandleOrder.cursor.execute(f"SELECT food_title FROM food")

        if table_status == 'false':
            HandleOrder.cursor.execute("UPDATE tables SET table_daily_usage = table_daily_usage + 1 "
                                       f"WHERE table_id = {table};"
                                       "UPDATE tables SET table_in_use = 'true' "
                                       f"WHERE table_id = {table}")

            HandleOrder.cursor.execute(
                "INSERT INTO orders (order_table, order_waiter, order_payment, order_food, order_total) "
                f"VALUES ({table}, {waiter}, 'Не оплачен', "
                " '{\"Состав\": {"
                f"\"Позиция\": \"{food}\", \"Кол-во\": {qtn}"
                "}}', "
                f" (SELECT food_price FROM food WHERE food_title = '{food}') * {qtn} )")

            HandleOrder.conn.commit()

            HandleOrder.cursor.execute(f"SELECT order_id, order_food FROM orders WHERE order_table = '{table}' "
                                       f"AND order_waiter = '{waiter}' AND order_payment = 'Не оплачен'")
            answer = list(HandleOrder.cursor.fetchone())

            QRgen(order_id=answer[0], waiter=waiter, food=answer[-1])
            return 'Заказ размещен!'
        else:
            return 'Стол занят, либо заказ не оплачен!'


class QRgen:

    def __init__(self, order_id, waiter, food):
        path = rf'X:\QR-tables\QR\{order_id}.png'
        HandleOrder.cursor.execute(f"SELECT order_stime, order_total FROM orders WHERE order_id = {order_id}")
        result = HandleOrder.cursor.fetchone()
        img = qrcode.make(data={'Дата создания заказа': result[0], 'Состав заказа': food, 'Сумма заказа': result[-1]})
        img.save(path)
        if os.path.exists(path):
            HandleOrder.cursor.execute(f"UPDATE orders SET order_qr = '{path}' WHERE order_id = {order_id}")
