import sqlite3 as sql

con = sql.connect("sqlite tests/sfscores.db")
cur = con.cursor()

out = cur.execute("SELECT count(business_id) FROM businesses;")

print(out.fetchall())

con.close()