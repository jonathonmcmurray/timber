import requests
import json
import pandas
from bs4 import BeautifulSoup
import re

# globals
widths = [5,19,26,32,44,57,69,94,119,144,169,194,220]
thicknesses = [6,18,25,30,42,55,67,96]

def getprice(species,width,thickness,length=2400):
    # send HTTP request with relevant parameters
    r = requests.post('https://www.timbercut4u.co.uk/shop/ajax.php',
                  data={'action':'calculate','item_id':species,'quantity':1000,'profile_id':0,'width':width,'thickness':thickness,'length':length,'units':'mm'})
    # parse response & union with knowns
    d = json.loads(r.text) | {'length':length,'width':width,'thickness':thickness,'species':species}
    if d['status'] == 'ok':
        d['price'] = float(d['price'])/1000
    else:
        d.pop('error')
        d['price'] = None
    return d

def speciesprices(species):
    return pandas.DataFrame([getprice(species,x,y) for x in widths for y in thicknesses])

def getspecies(url):
    ## clean up species name
    # remove leading url
    species_name = url[37:]
    # remove leading buy- if present
    if 'buy-' in species_name:
        species_name = species_name[4:]
    # remove trailing -timber if present
    if '-timber' in species_name:
        species_name = species_name[:-7]
        
    ## parse timber page to get species item_id
    st = BeautifulSoup(requests.get(url).text,features="lxml")
    pattern = re.compile(r"'id': '([0-9]*)'", re.MULTILINE | re.DOTALL)
    script = st.find('script',text=pattern)
    species_id = int(pattern.search(script.string).group(1))
    
    ## return species name & ID
    return [species_name,species_id]

def price_dimensions(width,thickness,length=2400):
    if not 'species' in globals():
        raise NameError('Please run make_helpers()')
    # get prices for all species
    df = pandas.DataFrame([getprice(x,width,thickness,length) for _,x in species])
    # map species IDs to names
    df['species_name'] = df['species'].map(idtospec)
    # sort asc by price
    return df.sort_values('price')

# generate useful helpers
def make_helpers():
    global spectoid, idtospec, species
    s = BeautifulSoup(requests.get('https://www.timbercut4u.co.uk/timber').text,features="lxml")
    timber_urls = set([x for x in [x for x in [link.get('href') for link in s.findAll('a')] if x is not None] if 'https://www.timbercut4u.co.uk/timber/' in x])
    species = [getspecies(x) for x in timber_urls]
    spectoid = {spec:id for spec,id in species}
    idtospec = {id:spec for spec,id in species}
    return