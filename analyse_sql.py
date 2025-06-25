import sqlglot
from dotenv import load_dotenv
from main import get_dao
from collections import Counter
from sqlglot.expressions import Table

def has_duplicate_table_references(parsed):
    if not parsed:
        return False
    tables = [t.name for t in parsed.find_all(Table) if t.name]
    table_counts = Counter(tables)
    return any(count > 1 for count in table_counts.values())


load_dotenv()
dao = get_dao()

counter = 0
# while counter < 10:
while True:
    counter += 1
    rows = dao.get_next_new_sql(10)
    if not rows:
        break

    for id_sql, sql_text in rows:
        can_parse = True
        is_select = False
        try:
            parsed = sqlglot.parse_one(sql_text, read='postgres', error_level='ignore')
            if parsed:
                duplicate_tables = has_duplicate_table_references(parsed)
                is_select = parsed.key.upper() == "SELECT"
            else:
                can_parse = False
        except Exception:
            can_parse = False

        dao.update_sql(id_sql, can_parse, is_select, duplicate_tables)
        print(f"Processed id {id_sql}: can_parse={can_parse}, is_select={is_select}")
