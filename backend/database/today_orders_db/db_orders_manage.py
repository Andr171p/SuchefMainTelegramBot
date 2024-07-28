from aiomysql import Pool, DictCursor

from backend.database.db_connect import db_connect

from backend.database.today_orders_db.db_orders_sql import OrdersSQL

from misc.row_wrapper import RowWrapper, RowWrapperFromKeys
from misc.row_wrapper import InsertValues, ValuesFromKeys

from misc.utils import DataUtils

from misc.format_data import format_phone_number, format_order_number


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

    async def db_insert_order_data(self, order_from_db):
        values = InsertValues(
            db_row_data=order_from_db
        )
        async with self.pool.acquire() as connection:
            async with connection.cursor(DictCursor) as cursor:
                await cursor.execute(
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

    async def db_update_sent(self, triggers):
        values = "', '".join(triggers)
        async with self.pool.acquire() as connection:
            async with connection.cursor(DictCursor) as cursor:
                await cursor.execute(
                    f"{OrdersSQL.update_sent_query}('{values}')"
                )
        self.pool.close()
        await self.pool.wait_closed()

    async def db_check_sent(self, phone_number):
        '''values = (
            format_phone_number(
                phone_number=phone_number
            )
        )'''
        values = (
            phone_number
        )
        async with self.pool.acquire() as connection:
            async with connection.cursor(DictCursor) as cursor:
                await cursor.execute(
                    OrdersSQL.check_sent_query,
                    values
                )
                result = await cursor.fetchall()
        self.pool.close()
        await self.pool.wait_closed()
        return result

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
        self.pool.close()
        await self.pool.wait_closed()


c = [{'phone_number': '9829878254', 'client': 'Юлия', 'number': 'БТ-074093', 'date': '2024-07-28T00:00:00',
      'status': 'Принят оператором', 'amount': 1537, 'pay_link': 'https://securepayments.tinkoff.ru/RZr49tBu',
      'pay_status': 'DEADLINE_EXPIRED', 'cooking_time_from': '0001-01-01T00:00:00',
      'cooking_time_to': '0001-01-01T13:40:00', 'delivery_time_from': '0001-01-01T14:00:00',
      'delivery_time_to': '0001-01-01T14:20:00', 'project': 'Сушеф.рф', 'trade_point': 'Велижанская, 66 к1',
      'trade_point_card': 'BeJIu}I{aHcka9I 66 k.1 https://go.2gis.com/eg0zzr', 'delivery_method': 'Самовывоз',
      'delivery_adress': ''},
     {'phone_number': '9829667223', 'client': 'Марина', 'number': 'БТ-074344', 'date': '2024-07-27T00:00:00',
      'status': 'Принят оператором', 'amount': 1403, 'pay_link': '', 'pay_status': 'AUTH_FAIL',
      'cooking_time_from': '0001-01-01T00:00:00', 'cooking_time_to': '0001-01-01T21:00:00',
      'delivery_time_from': '0001-01-01T21:30:00', 'delivery_time_to': '0001-01-01T22:00:00', 'project': 'Сушеф.рф',
      'trade_point': 'Московский тракт, 87к1', 'trade_point_card': "MockoBcku'u TpakT 87 k.1 https://go.2gis.com/pdacd",
      'delivery_method': 'Курьер',
      'delivery_adress': 'Тюменская обл, Тюмень г, Московский тракт ул, дом № 150, кв. 157 П3 Э12'},
     {'phone_number': '9199392904', 'client': 'Наталья', 'number': 'БТ-074355', 'date': '2024-07-27T00:00:00',
      'status': 'Новый', 'amount': 2159, 'pay_link': '', 'pay_status': '', 'cooking_time_from': '0001-01-01T00:00:00',
      'cooking_time_to': '0001-01-01T00:00:00', 'delivery_time_from': '0001-01-01T12:00:00',
      'delivery_time_to': '0001-01-01T12:30:00', 'project': 'Сушеф.рф', 'trade_point': 'Ростовцева 24 к1',
      'trade_point_card': 'PocToBu,eBa 24 k.1 https://go.2gis.com/j8g6j', 'delivery_method': 'Самовывоз',
      'delivery_adress': ''},
     {'phone_number': '9224709472', 'client': 'Инна', 'number': 'БТ-074305', 'date': '2024-07-27T00:00:00',
      'status': 'Принят оператором', 'amount': 3114, 'pay_link': 'https://securepayments.tinkoff.ru/e5YgaJnO',
      'pay_status': 'CONFIRMED', 'cooking_time_from': '0001-01-01T00:00:00', 'cooking_time_to': '0001-01-01T17:50:00',
      'delivery_time_from': '0001-01-01T18:30:00', 'delivery_time_to': '0001-01-01T19:00:00', 'project': 'Сушеф.рф',
      'trade_point': 'Московский тракт, 87к1', 'trade_point_card': "MockoBcku'u TpakT 87 k.1 https://go.2gis.com/pdacd",
      'delivery_method': 'Курьер',
      'delivery_adress': '625001, Тюменская обл, г.о. город Тюмень, г Тюмень, ул Полевая, д. 12а, кв. 55, подъезд 2, этаж 6'}]

from backend.client.order_status import OrdersAtTheMoment
from backend.database.db_loader import loop


async def main():
    db = OrdersEngineDB()
    '''o = OrdersAtTheMoment()
    await db.db_insert_orders_data(orders=await o.orders_at_the_moment())'''
    # await db.db_update_sent(triggers=['Принят оператором', 'fddb'])
    await db.db_update_orders_data(orders=c)
    '''result = await db.db_select_all_data()
    print(result)'''


loop.run_until_complete(main())
