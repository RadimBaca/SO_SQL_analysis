import duckdb
from .base import BaseDAO

class DuckDBDAO(BaseDAO):
    def __init__(self, db_path):
        self.conn = duckdb.connect(db_path)
        self._init_schema()

    def _init_schema(self):
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS post (
                id_post     INTEGER PRIMARY KEY,
                is_question BOOLEAN NOT NULL,
                date        TIMESTAMP NOT NULL,
                body        TEXT NOT NULL,
                tags        VARCHAR[],
                parent_id   INTEGER,
                score       INTEGER NOT NULL
            )
        """)
        self.conn.execute("""
            CREATE SEQUENCE seq_personid START 1;
        """)
        self.conn.execute("""
            CREATE TABLE IF NOT EXISTS sql (
                id_sql   INTEGER PRIMARY KEY default nextval('seq_personid'),
                id_post  INTEGER NOT NULL,
                sql_text TEXT NOT NULL
            )
        """)

    def insert_post(self, post_id, is_question, creation_date, body, tags, score, parent_id=None):
        self.conn.execute("""
            INSERT INTO post (id_post, is_question, date, body, tags, parent_id, score)
            SELECT ?, ?, ?, ?, ?, ?, ?
            WHERE NOT EXISTS (SELECT 1 FROM post WHERE id_post = ?)
        """, (post_id, is_question, creation_date, body, tags, parent_id, score, post_id))

    def insert_sql(self, post_id, sql_text):
        self.conn.execute("""
            INSERT INTO sql (id_post, sql_text) VALUES (?, ?)
        """, (post_id, sql_text))

    def post_exists(self, post_id):
        result = self.conn.execute("SELECT 1 FROM post WHERE id_post = ?", (post_id,)).fetchone()
        return result is not None
