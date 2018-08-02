import time
import hashlib
class Block:
    def __init__(self, trans:str, bnum:int, prevhash:str) -> None:
        self.trans = trans
        self.timestamp = str(time.time())
        self.bnum = bnum
        self.prevhash = prevhash
        self.nounce = -1

    def updatetime(self):
        self.timestamp = str(time.time())

    def __str__(self):
        return self.trans + '\n' + self.timestamp\
               + '\n' + str(self.bnum) + '\n' + str(self.nounce) \
               + '\n' + self.prevhash + '\n' + str(self.nounce)

    def changeNounce(self):
        if self.nounce >= 4294967295:
            return False
        else:
            self.nounce += 1
            return True

    def hash(self) -> str:
        return hashlib.sha256(str(self).encode("utf-8")).hexdigest()


translimit = 1


class Chain:
    genisis = Block("transfer 1000 coins from nowhere to darthvader1010", 0,
                    "0000000000000000000000000000000000000000000000000000000000000000")
    def __init__(self, diff: int, pool:list) -> None:
        self.diff = diff
        self.pool = []
        self.chain = [Chain.genisis]
        self.starter = ""
        for i in range(diff):
            self.starter += '0'
        self.pool = pool.copy()


    def isvalid(self) -> bool:
        for i in range(1, len(self.chain)):
            if self.chain[i].prevhash != self.chain[i-1].hash():
                return False
            if not self.chain[i].hash().startswith(self.starter):
                return False        
        return True



    def readytomine(self):
        return len(self.pool) >= translimit

    def mine(self) -> bool:
        if len(self.pool) < translimit:
            return False
        else:
            trans = ""
            for tr in self.pool[0:translimit]:
                trans += tr + '\n'
            block = Block(trans, len(self.chain), self.chain[-1].hash())

            while True:
                if block.changeNounce():
                    if block.hash().startswith(self.starter):
                        break

                else:
                    block.updatetime()
            self.chain.append(block)
            del self.pool[0:translimit]
            return True
