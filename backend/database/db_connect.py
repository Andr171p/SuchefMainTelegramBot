import aiomysql

from backend.database.db_loader import loop
from backend.database.db_config import AccessDB


async def connect():
    access_db = AccessDB
    return await aiomysql.create_pool(
        host=access_db.host,
        port=access_db.port,
        user=access_db.user,
        password=access_db.password,
        db=access_db.database,
        autocommit=True,
        pool_recycle=100,
        loop=loop
    )


db_connect = loop.run_until_complete(connect())
