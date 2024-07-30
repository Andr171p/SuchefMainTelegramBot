from aiomysql import Pool, DictCursor

from backend.database.db_connect import db_connect

from backend.database.today_orders_db.db_orders_sql import OrdersSQL

from misc.row_wrapper import RowWrapper, RowWrapperFromKeys
from misc.row_wrapper import InsertValues, ValuesFromKeys

from misc.utils import DataUtils


class OrdersEngineDB:
    pool: Pool = db_connect

    async def db_create_orders_table(self):
        async with self.pool.acquire() as connection:
            async with connection.cursor(DictCursor) as cursor:
                await cursor.execute(OrdersSQL.create_table_query)
        '''self.pool.close()
        await self.pool.wait_closed()'''

    async def db_drop_orders_table(self):
        async with self.pool.acquire() as connection:
            async with connection.cursor(DictCursor) as cursor:
                await cursor.execute(OrdersSQL.drop_table_query)
        '''self.pool.close()
        await self.pool.wait_closed()'''

    async def db_clear_table(self):
        async with self.pool.acquire() as connection:
            async with connection.cursor(DictCursor) as cursor:
                await cursor.execute(OrdersSQL.clear_table_query)
        '''self.pool.close()
        await self.pool.wait_closed()'''

    async def db_select_all_data(self):
        async with self.pool.acquire() as connection:
            async with connection.cursor(DictCursor) as cursor:
                await cursor.execute(OrdersSQL.select_all_data_query)
                result = await cursor.fetchall()
        '''self.pool.close()
        await self.pool.wait_closed()'''
        return result

    async def db_insert_orders_data(self, orders):
        values = RowWrapper(data=orders).create_matrix()
        print(values)
        async with self.pool.acquire() as connection:
            async with connection.cursor(DictCursor) as cursor:
                await cursor.executemany(
                    OrdersSQL.insert_data_query,
                    values
                )
        '''self.pool.close()
        await self.pool.wait_closed()'''

    async def db_insert_order_data(self, order_from_db):
        values = InsertValues(db_row_data=order_from_db)
        async with self.pool.acquire() as connection:
            async with connection.cursor(DictCursor) as cursor:
                await cursor.execute(
                    OrdersSQL.insert_data_query,
                    values
                )
        '''self.pool.close()
        await self.pool.wait_closed()'''

    async def db_order_data_from_phone_number(self, phone_number):
        values = (phone_number,)
        async with self.pool.acquire() as connection:
            async with connection.cursor(DictCursor) as cursor:
                await cursor.execute(
                    OrdersSQL.data_from_phone_number_query,
                    values
                )
                result = await cursor.fetchall()
        '''self.pool.close()
        await self.pool.wait_closed()'''
        return result

    async def db_check_trigger_status(self, phone_number, triggers):
        triggers_status = "', '".join(triggers)
        value = (phone_number,)
        async with self.pool.acquire() as connection:
            async with connection.cursor(DictCursor) as cursor:
                await cursor.execute(
                    f"{OrdersSQL.check_trigger_status}('{triggers_status}')",
                    value
                )
                result = await cursor.fetchall()
        '''self.pool.close()
        await self.pool.wait_closed()'''
        return result

    async def db_update_sent(self, phone_number, triggers):
        triggers_status = "', '".join(triggers)
        value = (phone_number,)
        async with self.pool.acquire() as connection:
            async with connection.cursor(DictCursor) as cursor:
                await cursor.execute(
                    f"{OrdersSQL.update_sent_query}('{triggers_status}')",
                    value
                )
        '''self.pool.close()
        await self.pool.wait_closed()'''

    async def db_check_sent(self, phone_number):
        values = (phone_number,)
        async with self.pool.acquire() as connection:
            async with connection.cursor(DictCursor) as cursor:
                await cursor.execute(
                    OrdersSQL.check_sent_query,
                    values
                )
                result = await cursor.fetchall()
        '''self.pool.close()
        await self.pool.wait_closed()'''
        return bool(result)

    async def db_update_orders_data(self, orders):
        data_utils = DataUtils()
        async with self.pool.acquire() as connection:
            async with connection.cursor(DictCursor) as cursor:
                # get all table data:
                await cursor.execute(
                    OrdersSQL.select_all_data_query
                )
                orders_from_db = await cursor.fetchall()

                for order in orders_from_db:
                    order.pop('id')

                update_orders = data_utils.intersection_list(
                    data=orders_from_db,
                    new_data=orders,
                    key='phone_number'
                )
                insert_orders = data_utils.subtract_list(
                    data=orders_from_db,
                    new_data=orders,
                    key='phone_number'
                )
                print(insert_orders)
                delete_orders = data_utils.subtract_list(
                    data=orders,
                    new_data=orders_from_db,
                    key='phone_number'
                )
                if len(orders_from_db) != 0:
                    for order in delete_orders:
                        value = (order['phone_number'],)
                        await cursor.execute(
                            OrdersSQL.delete_data_query,
                            value
                        )
                for order in update_orders:
                    values = (order['status'], order['phone_number'],)
                    await cursor.execute(
                        OrdersSQL.update_data_query,
                        values
                    )
                if len(insert_orders) != 0:
                    values = RowWrapper(
                        data=insert_orders
                    ).create_matrix()
                    await cursor.executemany(
                        OrdersSQL.insert_data_query,
                        values
                    )
        '''self.pool.close()
        await self.pool.wait_closed()'''
