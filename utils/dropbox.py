import dropbox
from utils import Database
import os

class Dropbox:

    def __init__(self):
        self.database = Database()
        self.DROPBOX_TOKEN = os.environ["DROPBOX_TOKEN"]
        self.dbx = dropbox
        self.database_name = "sora.db"

    def upload_database(self, database_name =None):
        """
        DropBox上にデータベースをアップロードします。
        """
        if not self.database.has_database(database_name):
            return

        if not database_name:
            database_name = self.database_name
        
        dbx :dropbox = self.dbx
        with open(self.PATH_LOCAL, "rb") as f:
            dbx.files_upload(
                f.read(),
                self.PATH_DBX,
                mode=dropbox.files.WriteMode.overwrite
            )
        
    
    def download_database(self, database_name =None):
        """
        DropBox上からデータベースを取得します。
        """
        if not database_name:
            database_name = self.database_name

        dbx = self.dbx
        dbx.files_download_to_file(self.PATH_LOCAL, self.PATH_DBX)
