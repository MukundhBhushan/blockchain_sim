import hashlib
import json
import datetime
from flask import redirect,request,Flask,render_template,g,jsonify

#creating the blockchain

class BlockChain():
    def __init__(self):
        self.chain=[]
        self.makeBlock(proof=1,previous_hash='0')

    def makeBlock(self,proof,previous_hash):
        block={'index':len(self.chain)+1,
               'time_stamp':str(datetime.datetime.now()),
               'proof':proof,
               'previous_hash':previous_hash,
               }

        self.chain.append(block)

        return(block)

    def block_hasher(self,blockObj):
        blockJD=json.dumps(blockObj,sort_keys=True).encode()
        return(hashlib.sha256(blockJD).hexdigest())




    def previBlock(self):
        return(self.chain[-1])


    def hashin_POW(self,np,pp):
        return (hashlib.sha256(str(np  - pp ).encode()).hexdigest())

    def POW(self,previ_proof):
        new_proof=1
        proof_done=False

        while proof_done==False:
            hashing=self.hashin_POW(new_proof,previ_proof)
            if hashing[:4]=='0000':
                print(hashing)
                break

            else:
                new_proof +=1
                print(new_proof,"fail")

        return(new_proof)

    def chain_checker(self,chain):
        previ_block=chain[0]
        block_index=1

        while block_index <len(chain):
            current_block=chain[block_index]
            if current_block['previous_hash']!=self.block_hasher(previ_block):
                return False
            if self.hashin_POW(current_block['proof'],previ_block['proof'])!='0000':
                return False

            previ_block=current_block
            block_index +=1

        return True

blockchain=BlockChain() #object of the blockchain class



#web app
app=Flask(__name__,template_folder='templates')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/mine',methods=['GET','POST'])
def mine():
    previ=blockchain.previBlock()
    print('previ',previ)
    previProof=previ['proof']
    print('previProof',previProof)
    proof=blockchain.POW(previProof)
    newBlock=blockchain.makeBlock(proof,blockchain.block_hasher(previ))
    print(newBlock)
    res={'index':newBlock['index'],
               'time_stamp':newBlock['time_stamp'],
               'proof':newBlock['proof'],
               'previous_hash':newBlock['previous_hash']
        }
    print("res",jsonify(newBlock))
    #return(jsonify(newBlock))
    return render_template('mine.html',block=json.dumps(newBlock, indent=4, sort_keys=True))

@app.route('/blockchain',methods=['GET','POST'])
def blockchain_disp():
    res={'BlockChain':blockchain.chain}
    blo_chain=jsonify(res)
    #return(blo_chain)
    return render_template('block.html',chain=json.dumps(blockchain.chain, indent=4, sort_keys=True))



if __name__=="__main__":
    app.run(host='192.168.0.105',port=303)
    #app.run()uuuuuu