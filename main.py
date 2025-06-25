import os
import re
import xml.etree.ElementTree as ET
from datetime import datetime
from dotenv import load_dotenv

from dao.base import BaseDAO
from dao.postgres import PostgresDAO
from dao.duckdb import DuckDBDAO

load_dotenv()
INPUT_FILE = os.getenv("INPUT_FILE")
DB_TYPE = os.getenv("DB_TYPE")
DB_CONN = os.getenv("DB_CONN")
DUCKDB_FILE = os.getenv("DUCKDB_FILE")

CODE_REGEX = re.compile(r'&lt;code&gt;.*?SELECT\s.*?FROM\s.*?&lt;/code&gt;', re.IGNORECASE)

def decode_html(text):
    return text.replace('&lt;', '<').replace('&gt;', '>').replace('&#xA;', '\n')

def extract_sql_snippets(body):
    decoded = decode_html(body)
    matches = re.findall(r'<code>(.*?)</code>', decoded, re.DOTALL | re.IGNORECASE)
    return [
        m.strip() for m in matches
        if 'select' in m.lower() and 'from' in m.lower()
    ]

def get_dao() -> BaseDAO:
    if DB_TYPE == "postgres":
        return PostgresDAO(DB_CONN)
    elif DB_TYPE == "duckdb":
        return DuckDBDAO(DUCKDB_FILE)
    else:
        raise ValueError("Unsupported DB_TYPE. Use 'postgres' or 'duckdb'.")

def process_large_file():
    dao = get_dao()

    with open(INPUT_FILE, encoding="utf-8") as f:
        for line in f:
            if not line.strip().startswith("<row"):
                continue

            try:
                row = ET.fromstring(line.strip())
            except ET.ParseError:
                continue

            post_type = row.get("PostTypeId")
            tags = row.get("Tags") or ""
            tags_list = re.findall(r"<(.*?)>", tags)
            body = row.get("Body", "")
            decoded_body = decode_html(body)
            post_id = int(row.get("Id"))
            creation_date = datetime.fromisoformat(row.get("CreationDate"))
            score = int(row.get("Score"))
            is_question = post_type == "1"
            parent_id = int(row.get("ParentId")) if row.get("ParentId") else None

            if post_type == "1":
                if "postgresql" not in tags_list:
                    continue
            elif post_type == "2":
                if not dao.post_exists(parent_id):
                    continue
            else:
                continue

            # print(f'checking regex {body} for post {post_id}')

            if not re.search(r'<code>.*?SELECT\s+.*?FROM\s+.*?</code>', decoded_body, re.IGNORECASE | re.DOTALL):
                continue
            # print(f'checking passed')

            sql_snippets = extract_sql_snippets(decoded_body)
            if not sql_snippets:
                continue

            dao.insert_post(post_id, is_question, creation_date, decoded_body, tags_list, score, parent_id)
            for snippet in sql_snippets:
                dao.insert_sql(post_id, snippet)

if __name__ == "__main__":
    process_large_file()
