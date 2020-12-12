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

    