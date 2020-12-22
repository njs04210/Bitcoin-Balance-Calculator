from bitcoin.rpc import RawProxy

p = RawProxy(btc_conf_file='/Users/jinjookim/Library/Application Support/Bitcoin/testnet3/bitcoin.conf')

totalBlocks = p.getblockcount()
address = '2N7RCjNbJcJy9QY9Q86w2RrK8aSuTxWHF32'

i = 1807734 # block height
txlist = []
totalreceived = 0
totalspent = 0


def getReceived():
    global blockhash, block, transactions, txid, raw_tx, decoded_tx, output, j, totalreceived, i
    # 총 받은 양 계산
    while i <= 1863758:
        blockhash = p.getblockhash(i)
        block = p.getblock(blockhash)
        transactions = block['tx']
        for txid in transactions:
            raw_tx = p.getrawtransaction(txid)
            decoded_tx = p.decoderawtransaction(raw_tx)
            output = decoded_tx['vout']
            for j in output:
                a = j['scriptPubKey']
                if 'addresses' in a:  # addresses 라는 key를 가진 애일경우
                    if a['addresses'][0] == address:  # 정해놓은 address와 같을 경우
                        totalreceived = totalreceived + j['value']
                        txlist.append(txid)
        i = i + 1
    print('총 받은 bitcoin = : ', totalreceived, 'btc')
    return totalreceived

def getSpent():
    global i, blockhash, block, transactions, txid, raw_tx, decoded_tx, j, output, totalspent
    # 총 사용한 양 계산
    i = 1807734
    while i <= 1863758:
        blockhash = p.getblockhash(i)
        block = p.getblock(blockhash)
        transactions = block['tx']
        for txid in transactions:
            raw_tx = p.getrawtransaction(txid)
            decoded_tx = p.decoderawtransaction(raw_tx)
            input = decoded_tx['vin']
            for j in input:
                if 'txid' in j:  # coinbase 걸러내기
                    id = j['txid']  # vin의 txid.
                    order = j['vout']  # vin의 vout
                    if id in txlist:
                        raw_tx_2 = p.getrawtransaction(id)
                        decoded_tx_2 = p.decoderawtransaction(raw_tx_2)
                        output = decoded_tx_2['vout']
                        real_output = output[order]
                        if real_output['scriptPubKey']['addresses'][0] == address:
                            totalspent = totalspent + real_output['value']
        i = i + 1
    print('총 사용한 bitcoin = ', totalspent, 'btc')
    return totalspent

balance = getReceived()-getSpent()

#balance 계산
print('balance = ', balance)