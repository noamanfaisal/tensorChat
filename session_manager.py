# session_manager.py
from tinydb import TinyDB, Query
from threading import Lock

class SessionManager:
    _instance = None
    _lock = Lock()

    def __new__(cls, db_path='session.json'):
        with cls._lock:
            if cls._instance is None:
                cls._instance = super(SessionManager, cls).__new__(cls)
                cls._instance._init_db(db_path)
            return cls._instance

    def _init_db(self, db_path):
        self.db = TinyDB(db_path)

    def set(self, key, value, table='default'):
        tbl = self.db.table(table)
        tbl.upsert({'key': key, 'value': value}, Query().key == key)

    def get(self, key, default=None, table='default'):
        tbl = self.db.table(table)
        res = tbl.get(Query().key == key)
        return res['value'] if res else default

    def delete(self, key, table='default'):
        tbl = self.db.table(table)
        tbl.remove(Query().key == key)

    def clear_table(self, table='default'):
        self.db.table(table).truncate()

    def clear_all(self):
        self.db.drop_tables()

    def all(self, table='default'):
        return self.db.table(table).all()

    def table(self, table='default'):
        return self.db.table(table)

