import timbercut4u as tb
import sqlite3
from datetime import date

DBNAME = 'timber.db'

# cur.execute("CREATE TABLE timbercut4u(speciesid,species,width,thickness,length,price)")

## open connection to DB

con = sqlite3.connect(DBNAME)
cur = con.cursor()

## download all the prices

# get species list etc.
tb.make_helpers()
# iterate over each species & get all the prices, write to DB
for speciesid in tb.idtospec:
    print(f"Getting prices for {speciesid}")
    # get prices for each combination of width & thickness
    r = [tb.getprice(speciesid,x,y) for x in tb.widths for y in tb.thicknesses]
    # add species name to each price dict
    r = [x|{'species_name':tb.idtospec[speciesid]} for x in r]
    # add date to each price dict
    r = [x|{'date':date.today()} for x in r]
    print(f"Writing to db for {speciesid} : {r[0]['species_name']}")
    cur.executemany("INSERT INTO timbercut4u VALUES(:date,:species,:species_name,:width,:thickness,:length,:price)",
                    r)
    
# delete any null prices
cur.execute("DELETE FROM timbercut4u WHERE price IS NULL")

## commit & close DB connection
con.commit()
con.close()

    