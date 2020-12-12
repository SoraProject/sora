import aiosqlite3
import os

class Database:

    def __init__(self):
        self.database_name = "sora.db"

    def has_database(self, database_name =None):
        """
        指定したデータベースがあるか確認します。
        """

        if not database_name:
            database_name = self.database_name
    
        if os.path.isfile(database_name):
            return True
        
        return False

    async def fetch_database(self, table_name, db =None):
        """
        データベースから指定したテーブルのデータをすべて取得します。
        """
        if not self.has_database():
            return None

        if not db:
            db = self.database_name

        conn: aiosqlite3.Connection = await aiosqlite3.connect(db)
        c: aiosqlite3.Cursor = await conn.cursor()
        
        datas = []
        
        try:
            async for row in c.execute(f"SELECT * FROM {table_name}"):
                datas += row
        
        except:
            return None
        
        return datas

    async def add_data(self, table_name, data: list, db =None):
        """
        指定したテーブルにデータを1つ追加します。
        """
        if not self.has_database():
            return None
        
        if not db:
            db = self.database_name

        conn: aiosqlite3.Connection = await aiosqlite3.connect(db)
        c: aiosqlite3.Cursor = await conn.cursor()

        await c.execute(f"INSERT INTO {table_name} VALUES({[i for i in data]})")
        await conn.commit()
        await conn.close()

    async def add_datas(self, table_name, datas: list, db =None):
        """
        指定したテーブルにデータを複数個追加します。
        """
        for data in datas:
            await self.add_data(table_name, data, db=None)

        return True
    