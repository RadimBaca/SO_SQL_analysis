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

    def get_next_new_sql(self, n):
        with self.conn.cursor() as cur:
            cur.execute("""
                SELECT id_sql, sql_text FROM sql
                WHERE can_be_parsed IS NULL
                ORDER BY id_sql
                LIMIT %s
            """, (n,))
            return cur.fetchall()

    def update_sql(self, id_sql, can_be_parsed, is_select, duplicate_tables=None):
        with self.conn.cursor() as cur:
            cur.execute("""
                UPDATE sql
                SET can_be_parsed = %s, is_select = %s, has_duplicate_table = %s
                WHERE id_sql = %s
            """, (can_be_parsed, is_select, duplicate_tables, id_sql))
