from flask import render_template, session
from functools import wraps
from classes import Chain

def showmsg(msg: str="Done"):
    return render_template("message.html", msg=msg)


def updatechain(dst: Chain, src: Chain):
    if src.isvalid():
        dst.chain = src.chain.copy()
        dst.pool = src.pool.copy()


usercount = 0
diff = 2
chains = {}
pool = []
longestchain = Chain(diff, pool)


def check_session():
        global usercount
        if session.get("user_id") is None:
            session["user_id"] = usercount
            chains[usercount] = Chain(diff, pool)
            chains[usercount].chain = longestchain.chain.copy()
            usercount += 1
        else:
            if session["user_id"] not in chains:
                chains[session["user_id"]] = Chain(diff, pool)
                chains[session["user_id"]].chain = longestchain.chain.copy()