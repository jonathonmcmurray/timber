import timbercut4u as tb
import sqlite3
from datetime import date
from proglog import default_bar_logger

DBNAME = "timber.db"

# cur.execute("CREATE TABLE timbercut4u(speciesid,species,width,thickness,length,price)")

## open connection to DB

con = sqlite3.connect(DBNAME)
cur = con.cursor()

## download all the prices

# get species list etc.
tb.make_helpers()
# iterate over each species & get all the prices, write to DB
for speciesid in tb.idtospec:
    species = tb.idtospec[speciesid]
    print(f"Getting prices for {species} (ID: {speciesid})")
    # get list of all dimensions we want to request prices for
    d = [[x, y] for x in tb.widths for y in tb.thicknesses]
    # empty list to store price dictionaries
    r = []
    # init proglog progress bar
    logger = default_bar_logger("bar")
    # get prices for each combination of width & thickness, updating progress bar
    for w, t in logger.iter_bar(dimension=d):
        # get price, add species name & date
        a = tb.getprice(speciesid, w, t) | {
            "species_name": species,
            "date": date.today(),
        }
        # append dict for this dimension to the list
        r.append(a)
    print(f"Writing to db for {species} (ID: {speciesid})")
    cur.executemany(
        "INSERT INTO timbercut4u VALUES(:date,:species,:species_name,:width,:thickness,:length,:price)",
        r,
    )

# delete any null prices
cur.execute("DELETE FROM timbercut4u WHERE price IS NULL")

## commit & close DB connection
con.commit()
con.close()
