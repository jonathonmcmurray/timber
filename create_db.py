import sqlite3

DBNAME = 'timber.db'

## open connection to DB

con = sqlite3.connect(DBNAME)
cur = con.cursor()

cur.execute("CREATE TABLE timbercut4u(date,speciesid,species,width,thickness,length,price)")

## commit & close DB connection
con.commit()
con.close()
