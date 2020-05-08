import time, json, requests


sample = {"op":"block","x":{"txIndexes":[0,0,0,0,0,0,0,0],"nTx":2974,"estimatedBTCSent":58016479492,
"totalBTCSent":628840769257,"reward":0,"size":1332788,"weight":3993197,"blockIndex":0,"prevBlockIndex":0,
"height":614187,"hash":"0000000000000000000cd9a8dccfc8dc498d406f3a0dd594ea8dd0b9e113c5ae",
"mrklRoot":"b4dd8cc9304872a4506df18e33109d8e8a2ce29b37f5d86cb0bf5304736d0f8d","difficulty":1.4776367535688639E13,
"version":549453824,"time":1579797044,"bits":387124344,"nonce":1258174772,"foundBy":{"description":"","ip":"","link":"","time":0}}}

current_block_height = sample["x"]["height"]


full_block = requests.get("https://blockchain.info/block-height/{}?format=json".format(614202))
full_block = full_block.json()
#f.write(str(latest_block))
#f.close()
number_of_tx = full_block["blocks"][0]["n_tx"]
tx1 = full_block["blocks"][0]["tx"][0]["out"][0]["value"]
tx = []
for i in range(number_of_tx):
    tx.append(full_block["blocks"][0]["tx"][i]["out"][0]["value"]/10**8)

print(tx)
print(len(tx))
