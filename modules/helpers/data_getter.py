import psycopg2


class Connect:
    conn = psycopg2.connect(database="pushkina_restraunt", user="postgres", password="228", host="localhost", port=5432)
    cursor = conn.cursor()


class GetInfo:
    @staticmethod
    def free_tables():
        """ Список свободных столов """
        Connect.cursor.execute("SELECT table_id FROM tables WHERE table_in_use='false' ORDER BY table_id ASC")
        tables = Connect.cursor.fetchall()
        result = []
        for _ in tables:
            temp = (*_, str(*_))
            result.append(temp)
        return result

    @staticmethod
    def waiters():
        """ Список всех офиков """
        Connect.cursor.execute("SELECT e.emp_id, e.emp_name, e.emp_surname FROM employees e JOIN posts p ON e.emp_post=p.post_id WHERE p.post_name='Официант' ORDER BY e.emp_surname")
        waiters = Connect.cursor.fetchall()
        result = []
        for _ in waiters:
            temp = (_[0], _[1][:1] + '. ' + _[-1])
            result.append(temp)
        return result

    @staticmethod
    def food_list():
        """ Список всей еды """
        Connect.cursor.execute("SELECT food_id, food_title FROM food ORDER BY food_category ASC")
        food = Connect.cursor.fetchall()
        return food

    @staticmethod
    def bill_info(table_id):
        """ Инфа по сумме в чеке """
        Connect.cursor.execute("SELECT order_table FROM orders ORDER BY order_table ASC")
        tables = list(Connect.cursor.fetchall())
        result = []
        for _ in tables:
            result.append(*_)
        if table_id in result:
            Connect.cursor.execute("SELECT o.order_total FROM orders o JOIN tables t ON t.table_id=o.order_table "
                                   f"WHERE o.order_pstatus='Не оплачен' AND o.order_etime is Null AND t.table_id={table_id}")
            total = list(Connect.cursor.fetchone())
            return total[0]
        else:
            return "Стол свободен"

    @staticmethod
    def payment_info(table_id):
        """ Проверка доступности стола и информации оплаты по столу """
        Connect.cursor.execute("SELECT order_table FROM orders ORDER BY order_table ASC")
        tables = list(Connect.cursor.fetchall())
        result = []
        for _ in tables:
            result.append(*_)
        if table_id in result:
            Connect.cursor.execute("SELECT o.order_payment FROM orders o JOIN tables t ON t.table_id=o.order_table "
                                   f"WHERE o.order_etime is Null AND t.table_id={table_id}")
            total = list(Connect.cursor.fetchone())
            return total[0]
        else:
            return "Стол свободен"

    @staticmethod
    def current_orders():
        """ Все неоплаченные заказы """
        Connect.cursor.execute("SELECT order_id FROM orders WHERE order_pstatus='Не оплачен'")
        orders = list(Connect.cursor.fetchall())
        result = []
        for _ in orders:
            result.append(*_)
        return result

    @staticmethod
    def table_order(table_id):
        """ Получение заказа для текущего стола """
        Connect.cursor.execute(f"SELECT order_id FROM orders WHERE order_table={table_id} AND order_pstatus='Не оплачен'")
        result = Connect.cursor.fetchone()
        if result is None:
            return result
        else:
            return result[0]

    @staticmethod
    def debt(table_id):
        """ Разница между суммой долга стола и внесенной оплатой """
        Connect.cursor.execute(f"SELECT order_id FROM orders WHERE order_table={table_id} AND order_pstatus='Не оплачен'")
        result = Connect.cursor.fetchone()
        if result is None:
            return False
        Connect.cursor.execute(f"SELECT order_payment, order_total FROM orders WHERE order_id={list(result)[0]}")
        money = list(Connect.cursor.fetchone())
        if money[0] >= money[-1]:
            return 0
        else:
            return money[-1] - money[0]
