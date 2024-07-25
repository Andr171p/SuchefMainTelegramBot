from backend.parser.stock_parser import ParseSuchefStock

from backend.database.stock_db.db_stock_manage import SuchefStockDB


class ActualStock:
    def __init__(self):
        self.actual_stock = None

    @staticmethod
    def update_stock():
        # init stock parser:
        suchef_stock_parser = ParseSuchefStock()
        # init stock database:
        suchef_stock_db = SuchefStockDB()
        # parse actual stock:
        actual_stock = suchef_stock_parser.parse_stock()
        # insert stock in db:
        suchef_stock_db.db_insert_stock_data(
            stock_data=actual_stock
        )

    def get_actual_stock(self):
        suchef_stock_db = SuchefStockDB()
        self.actual_stock = suchef_stock_db.db_all_data()
        return self.actual_stock
