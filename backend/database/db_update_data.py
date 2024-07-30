import asyncio

from backend.client.order_status import OrdersAtTheMoment

from backend.database.today_orders_db.db_orders_manage import OrdersEngineDB
from backend.database.db_loader import create_event_loop


'''async def db_update_orders_data(timeout=60):
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
            await asyncio.sleep(timeout)'''


async def db_loop_update_orders_data(timeout=70):
    # init orders database engine class:
    orders_engine_db = OrdersEngineDB()
    # init orders at the moment class:
    orders_at_the_moment = OrdersAtTheMoment()
    # first orders transaction:
    orders = await orders_at_the_moment.orders_at_the_moment()
    await orders_engine_db.db_insert_orders_data(orders=orders)
    # start update database:
    while True:
        new_orders = await OrdersAtTheMoment().orders_at_the_moment()
        await orders_engine_db.db_update_orders_data(orders=new_orders)
        # wait timeout:
        await asyncio.sleep(timeout)


loop = create_event_loop()
loop.run_until_complete(db_loop_update_orders_data())