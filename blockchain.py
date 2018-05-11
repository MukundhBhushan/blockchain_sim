import hashlib as hasher
import datetime
import json


#making of the block -->
class Block():
    def __init__(self, index, time_stamp, data, peri_hash):
        self.data=data
        self.index=index
        self.time_stamp=time_stamp
        self.peri_hash=peri_hash
        self.hash=self.make_hash()

    def make_hash(self):
        sha = hasher.sha256((str(self.index) + str(self.time_stamp) +str(self.data) +str(self.peri_hash)).encode())

        return sha.hexdigest() #retuns a hexademcimal hash


def genisi_block(): #first block has no data
    blk = Block(0, datetime.datetime.now(), "Genesis Block", "0")
    return blk

def next_block(blockObj,in_data):
    index=blockObj.index +1
    time_stamp=datetime.datetime.now()
    data=in_data
    peri_hash=blockObj.hash
    return(Block(index, time_stamp, data, peri_hash))

def json_serial(obj):
    if isinstance(obj, (datetime.datetime, datetime.date)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))


if __name__=="__main__":
    blockchain = [genisi_block()]
    #blockchain .append()
    res=input("add a new block [yes / no] ")

    previous_block=blockchain[0]
    blockchain.pop()
    blockchain.append(json.dumps(previous_block.__dict__,default=json_serial))

    while res=="yes":
        data=input("enter data ")
        new_block=next_block(previous_block,data)
        previous_block=new_block
        new_block=json.dumps(new_block.__dict__,default=json_serial)
        blockchain.append(new_block)
        print(new_block,"\n")
        res = input("add a new block [yes / no] ")


    if res=="no":
        print("blockchain==>")
        for i,j in enumerate(blockchain):
            print(i,j,"\n")

