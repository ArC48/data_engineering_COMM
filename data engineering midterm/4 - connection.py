import asyncpg

class DBConnection:
    def __init__(self):
        self.master_dsn = "postgres://beqa:postgres@localhost:55432/postgres"
        self.slave_dsn = "postgres://beqa:postgres@localhost:55433/postgres"

    async def is_slave_alive(self) -> bool:
        try:
            conn = await asyncpg.connect(self.slave_dsn)
            await conn.execute("SELECT 1")
            await conn.close()
            return True
        except Exception:
            return False

    async def get_connection(self):
        if await self.is_slave_alive():
            print("request sent to slave")
            return await asyncpg.connect(self.slave_dsn)
        else:
            print("request sent to master")
            return await asyncpg.connect(self.master_dsn)
