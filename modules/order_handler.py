import psycopg2
import datetime
from modules.helpers.data_getter import GetInfo


class HandleOrder:

    conn = psycopg2.connect(database="pushkina_restraunt", user="postgres", password="228", host="localhost", port=5432)
    cursor = conn.cursor()

    @staticmethod
    def create_order(table, waiter, food, qtn=1):
        """
        Создание заказа
        :param table: номер стола
        :param waiter: айди официанта
        :param food: название позиции
        :param qtn: количество в заказе
        :return:
        """
        HandleOrder.cursor.execute(f"SELECT food_title FROM food WHERE food_id = {food}")
        food_data = list(HandleOrder.cursor.fetchone())[0]
        HandleOrder.cursor.execute(
            "INSERT INTO orders (order_table, order_waiter, order_pstatus, order_food, order_total) "
            f"VALUES ({table}, {waiter}, 'Не оплачен', "
            " '{\"Состав\": [{"
            f"\"Позиция\": \"{food_data}\", \"Кол-во\": {qtn}"
            "}]}', "
            f" (SELECT food_price FROM food WHERE food_title = '{food_data}') * {qtn} )")
        HandleOrder.conn.commit()
        HandleOrder.cursor.execute(f"SELECT order_id, order_food FROM orders WHERE order_table='{table}' "
                                   f"AND order_waiter='{waiter}' AND order_pstatus='Не оплачен'")
        answer = list(HandleOrder.cursor.fetchone())
        if len(answer) > 0:
            HandleOrder.cursor.execute("UPDATE tables SET table_daily_usage=table_daily_usage + 1, table_in_use='true' "
                                       f"WHERE table_id={table}")
            HandleOrder.conn.commit()
            return True
        else:
            return False

    @staticmethod
    def cancel_order(table_id):
        """
        Отмена заказа по столу
        """
        order_id = GetInfo.table_order(table_id)
        if order_id is not None:
            HandleOrder.cursor.execute(f"UPDATE orders SET order_pstatus='Отменен', "
                                       f"order_etime='{datetime.datetime.now()}' "
                                       f"WHERE order_id={order_id}")
            HandleOrder.conn.commit()
            HandleOrder.cursor.execute("UPDATE tables SET table_in_use='false' WHERE table_id= "
                                       f"(SELECT order_table FROM orders WHERE order_id={order_id} "
                                       "AND order_pstatus='Отменен')")
            HandleOrder.conn.commit()
            return order_id

