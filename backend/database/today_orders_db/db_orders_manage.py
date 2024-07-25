from aiomysql import Pool, DictCursor

from backend.database.db_connect import db_connect

from backend.database.today_orders_db.db_orders_sql import OrdersSQL

from misc.row_wrapper import RowWrapper


class OrdersEngineDB:
    pool: Pool = db_connect

    async def db_create_orders_table(self):
        async with self.pool.acquire() as connection:
            async with connection.cursor(DictCursor) as cursor:
                await cursor.execute(OrdersSQL.create_table_query)
        self.pool.close()
        await self.pool.wait_closed()

    async def db_drop_orders_table(self):
        async with self.pool.acquire() as connection:
            async with connection.cursor(DictCursor) as cursor:
                await cursor.execute(OrdersSQL.drop_table_query)
        self.pool.close()
        await self.pool.wait_closed()

    async def db_clear_table(self):
        async with self.pool.acquire() as connection:
            async with connection.cursor(DictCursor) as cursor:
                await cursor.execute(OrdersSQL.clear_table_query)
        self.pool.close()
        await self.pool.wait_closed()

    async def db_select_all_data(self):
        async with self.pool.acquire() as connection:
            async with connection.cursor(DictCursor) as cursor:
                await cursor.execute(OrdersSQL.select_all_data_query)
                result = await cursor.fetchall()
        self.pool.close()
        await self.pool.wait_closed()
        return result

    async def db_insert_orders_data(self, orders):
        values = RowWrapper(
            data=orders
        ).create_matrix()
        async with self.pool.acquire() as connection:
            async with connection.cursor(DictCursor) as cursor:
                await cursor.executemany(
                    OrdersSQL.insert_data_query,
                    values
                )
        self.pool.close()
        await self.pool.wait_closed()

    async def db_order_data_from_phone_number(self, phone_number):
        values = (
            phone_number,
        )
        async with self.pool.acquire() as connection:
            async with connection.cursor(DictCursor) as cursor:
                await cursor.execute(
                    OrdersSQL.data_from_phone_number_query,
                    values
                )
                result = await cursor.fetchall()
        self.pool.close()
        await self.pool.wait_closed()
        return result


from backend.client.order_status import OrdersAtTheMoment
from backend.database.db_loader import loop
async def main():
    db = OrdersEngineDB()
    '''o = OrdersAtTheMoment()
    await db.db_insert_orders_data(orders=await o.orders_at_the_moment())'''
    res =  await db.db_order_data_from_phone_number(phone_number='9088777711')
    print(res)

loop.run_until_complete(main())