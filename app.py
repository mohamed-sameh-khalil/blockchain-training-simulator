from functionality import *
from flask import Flask, render_template, session, request
from urllib.request import urlopen
from classes import Chain, translimit
import hashlib
import json
app = Flask(__name__)

app.config["TEMPLATES_AUTO_RELOAD"] = True
app.config["SESSION_TYPE"] = "filesystem"
app.secret_key = 'darth is the best'
app.debug = "on"


@app.route('/')
def index():
    link = "https://min-api.cryptocompare.com/data/pricemulti?fsyms=ETH,BTC,LTC,NEO,ADA,EOS,BCC,XRP&tsyms=USD,EUR"
    data = json.loads(urlopen(link).read().decode("utf-8"))
    return render_template("index.html", data=data)


@app.route("/pool")
def Pool():
    return render_template("pool.html", pool=pool)

@app.route('/transact', methods=['GET', 'POST'])
def transact():
    global pool
    if request.method == "GET":
        return render_template("transact.html")
    else:
        sender = request.form.get("sender_id")
        receiver = request.form.get("receiver_id")
        amount = request.form.get("amount")
        trx = sender + " sent " + amount + " to " + receiver
        print(trx)
        pool.append(trx)
        for chain in chains.values():
            chain.pool.append(trx)
        return showmsg(f"your transaction of {amount} coins from {sender} to {receiver} "
                       + "was added to the pool successfully, waiting to be added to a block")


@app.route('/mine', methods=['GET'])
def mine():
    check_session()
    chain = chains[session["user_id"]]
    # if server has a longer chain
    if len(chain.chain) < len(longestchain.chain):
        updatechain(chain, longestchain)
    if chain.readytomine():
        chain.mine()
        updatechain(longestchain, chain)
        return showmsg("Mining was done successfully and ur block was accepted")
    else:
        return showmsg(f"need at least {translimit - len(pool)} transactions more in the pool to fulfill the block ")


@app.route("/history", methods=['GET'])
def history():
    result = ""
    for block in reversed(longestchain.chain):
        result += block.trans
    result = result.split('\n')
    return render_template("history.html", result=result)


if __name__ == '__main__':
    app.run()