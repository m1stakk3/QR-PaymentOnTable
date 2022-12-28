import psycopg2
import datetime
from modules.helpers.data_getter import GetInfo


class Connect:
    conn = psycopg2.connect(database="pushkina_restraunt", user="postgres", password="228", host="localhost", port=5432)
    cursor = conn.cursor()


class Payment:
    @staticmethod
    def pay(order_id, money):
        """
        оплата с проверкой на корректность
        :param order_id:
        :param money:
        :return:
        """

        Connect.cursor.execute(f"SELECT order_table FROM orders WHERE order_id={order_id}")
        table_id = list(Connect.cursor.fetchone())[0]

        if GetInfo.debt(table_id) > 0:
            print(GetInfo.debt(table_id))
            Connect.cursor.execute(f"UPDATE orders SET order_payment=order_payment+{money} WHERE order_id={order_id}")
            Connect.conn.commit()
            Connect.cursor.execute(f"UPDATE orders SET order_etime='{datetime.datetime.now()}', order_pstatus='Оплачен' WHERE order_id={order_id}")
            Connect.conn.commit()
            return True
        else:
            return False


