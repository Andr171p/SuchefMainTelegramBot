import pymysql

from backend.database.db_config import RailwayAccessDB, AccessDB


class SuchefStockDB:
    def __init__(self):
        self.access_db = AccessDB()
        self.connection = None

    def db_connect(self):
        try:
            self.connection = pymysql.connect(
                host=self.access_db.host,
                port=self.access_db.port,
                user=self.access_db.user,
                password=self.access_db.password,
                database=self.access_db.database,
                cursorclass=pymysql.cursors.DictCursor
            )
            print("[SuchefStockDB : db_connect] :\n"
                  "connection successfully..")
        except Exception as _ex:
            print(f"[SuchefOrdersDB : db_connect] :\n"
                  f"{_ex}")

    def create_stock_table(self):
        self.db_connect()
        with self.connection.cursor() as cursor:
            create_table_query = "CREATE TABLE `stocks`(id int AUTO_INCREMENT," \
                                 "  url longtext," \
                                 "  title longtext," \
                                 "  info longtext, PRIMARY KEY (id));"
            cursor.execute(create_table_query)
            print("[SuchefStockDB : create_stock_table] :\n"
                  "Table created successfully")

    def drop_stock_table(self):
        self.db_connect()
        with self.connection.cursor() as cursor:
            drop_table_query = "DROP TABLE `stocks`"
            cursor.execute(drop_table_query)
            print("[SuchefStockDB : drop_stock_table] :\n"
                  "Table drop successfully")

    def clear_db(self):
        self.db_connect()
        try:
            with self.connection.cursor() as cursor:
                query = "TRUNCATE TABLE `stocks`"
                cursor.execute(query)
        except Exception as _ex:
            print(_ex)
        finally:
            self.connection.commit()
            self.connection.close()

    def db_all_data(self):
        self.db_connect()
        try:
            with self.connection.cursor() as cursor:
                sql_query = "SELECT * FROM `stocks`"
                cursor.execute(sql_query)
                data = cursor.fetchall()
                result = []
                for values in data:
                    result.append(list(values.values()))
        except Exception as _ex:
            print(f"def db_all_data: {_ex}")
        finally:
            cursor.close()
            self.connection.close()
            return result

    def db_insert_stock_data(self, stock_data):
        self.db_connect()
        length = len(stock_data)
        try:
            with self.connection.cursor() as cursor:
                for i in range(length):
                    url = stock_data[i][0]
                    title = stock_data[i][1]
                    info = stock_data[i][2]

                    sql_query = "INSERT INTO `stocks`" \
                                "(url, title, info)" \
                                "VALUES (%s, %s, %s)"
                    parameters = (
                        url, title, info
                    )
                    cursor.execute(sql_query, parameters)
        except Exception as _ex:
            print(f"def db_insert_stock_data: {_ex}")
        finally:
            self.connection.commit()
            self.connection.close()
