import hashlib
from urllib.request import urlopen
import json

# print(hashlib.sha256(b"hello world").hexdigest())
link = "https://min-api.cryptocompare.com/data/pricemulti?fsyms=ETH,BTC,LTC,NEO,ADA&tsyms=USD,EUR"
data = json.loads(urlopen(link).read().decode("utf-8"))
for sym in data:
    print(sym)
    print(data[sym]['USD'])