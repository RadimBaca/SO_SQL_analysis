import psycopg2
from .base import BaseDAO

class PostgresDAO(BaseDAO):
    def __init__(self, conn_str):
        self.conn = psycopg2.connect(conn_str)
        self.conn.autocommit = True

    def insert_post(self, post_id, is_question, creation_date, body, tags, score, parent_id=None):
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO post (id_post, is_question, date, body, tags, parent_id, score)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
                ON CONFLICT DO NOTHING
            """, (post_id, is_question, creation_date, body, tags, parent_id, score))

    def insert_sql(self, post_id, sql_text):
        with self.conn.cursor() as cur:
            cur.execute("""
                INSERT INTO sql (id_post, sql_text) VALUES (%s, %s)
            """, (post_id, sql_text))

    def post_exists(self, post_id):
        with self.conn.cursor() as cur:
            cur.execute("SELECT 1 FROM post WHERE id_post = %s", (post_id,))
            return cur.fetchone() is not None
