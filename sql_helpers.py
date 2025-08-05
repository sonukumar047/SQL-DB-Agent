import mysql.connector, pandas as pd, time
from config import MYSQL_HOST, MYSQL_USER, MYSQL_PASS

# ── Schema ─────────────────────────────────────────────────────────────────────
def get_db_schema(db_name: str) -> dict:
    """Return {{table: {columns:list, types:dict}}} for given DB."""
    cnx = mysql.connector.connect(
        host=MYSQL_HOST, user=MYSQL_USER,
        password=MYSQL_PASS, database=db_name
    )
    cur = cnx.cursor()
    cur.execute("SHOW TABLES")
    tables = [t[0] for t in cur.fetchall()]
    schema = {}

    for tbl in tables:
        try:
            cur.execute(f"DESCRIBE `{tbl}`")         # back-ticks fix 1064 error
            cols = cur.fetchall()
            schema[tbl] = {
                "columns": [c[0] for c in cols],
                "types":   {c[0]: c[1] for c in cols}
            }
        except Exception as e:
            print(f"⚠️  DESCRIBE `{tbl}` failed: {e}")
            continue

    cur.close(); cnx.close()
    return schema

# ── Query Execution ────────────────────────────────────────────────────────────
def run_sql_query(sql: str, db_name: str):
    """Execute query and return (DataFrame, exec_time_s)."""
    t0 = time.time()
    cnx = mysql.connector.connect(
        host=MYSQL_HOST, user=MYSQL_USER,
        password=MYSQL_PASS, database=db_name
    )
    cur = cnx.cursor()
    try:
        cur.execute(sql)
        df = (pd.DataFrame(cur.fetchall(), columns=[c[0] for c in cur.description])
              if cur.description else pd.DataFrame())
    finally:
        cur.close(); cnx.close()
    return df, time.time() - t0

# ── Safety ─────────────────────────────────────────────────────────────────────
def validate_sql(sql: str):
    bad = ["DROP","DELETE","UPDATE","INSERT","ALTER","CREATE","TRUNCATE"]
    up  = sql.upper()
    if not up.lstrip().startswith("SELECT"):
        return False, "Only SELECT statements are allowed."
    for kw in bad:
        if kw in up:
            return False, f"Keyword '{kw}' is prohibited."
    return True, "Safe"
