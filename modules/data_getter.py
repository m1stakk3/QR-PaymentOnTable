import psycopg2


class DataGetter:
    conn = psycopg2.connect(database="pushkina_restraunt", user="postgres", password="228", host="localhost", port=5432)
    cursor = conn.cursor()

    @staticmethod
    def get_free_tables():
        DataGetter.cursor.execute("SELECT table_id FROM tables WHERE table_in_use = 'false' ORDER BY table_id ASC")
        tables = DataGetter.cursor.fetchall()
        result = []
        for _ in tables:
            temp = (*_, str(*_))
            result.append(temp)
        return result

    @staticmethod
    def get_waiters():
        DataGetter.cursor.execute("SELECT e.emp_id, e.emp_name, e.emp_surname FROM employees e JOIN posts p "
                                  "ON e.emp_post=p.post_id WHERE p.post_name='Официант' ORDER BY e.emp_surname")
        waiters = DataGetter.cursor.fetchall()
        result = []
        for _ in waiters:
            temp = (_[0], _[1][:1] + '. ' + _[-1])
            result.append(temp)
        return result

    @staticmethod
    def get_food():
        DataGetter.cursor.execute("SELECT food_id, food_title FROM food ORDER BY food_category ASC")
        food = DataGetter.cursor.fetchall()
        return food

    @staticmethod
    def get_payment_info(table_id):
        DataGetter.cursor.execute("SELECT order_table FROM orders ORDER BY order_table ASC")
        tables = list(DataGetter.cursor.fetchall())
        temp = []
        for _ in tables:
            temp.append(*_)
        if table_id in temp:
            DataGetter.cursor.execute("SELECT o.order_total-o.order_payment FROM orders o "
                                      "JOIN tables t ON t.table_id=o.order_table "
                                      "WHERE o.order_pstatus='Не оплачен' AND o.order_etime is Null "
                                      f"AND t.table_id={table_id}")
            total = list(DataGetter.cursor.fetchone())
            if total[0] is not None:
                return total[0]
            else:
                return "Текущий стол забронирован!"
        else:
            return "На текущем столе нет задолженности!"
