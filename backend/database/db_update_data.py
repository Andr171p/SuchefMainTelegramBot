import asyncio

from backend.client.order_status import TodayOrders

from backend.database.today_orders_db.db_orders_manage import SuchefOrdersDB


async def db_update_orders_data(timeout=60):
    # init db with today orders data:
    suchef_orders_db = SuchefOrdersDB()
    # init today orders class:
    today_orders = TodayOrders()
    while True:
        try:
            orders_at_the_time = today_orders.orders_at_the_time()

            suchef_orders_db.db_update_and_clear_data(
                orders_at_the_time=orders_at_the_time
            )

            await asyncio.sleep(timeout)

        except Exception as _ex:
            print(f"[async def db_update_orders_data] : {_ex}")
            await asyncio.sleep(timeout)