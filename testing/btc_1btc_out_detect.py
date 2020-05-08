# This program was written by Edvards Galuzo for CS3590 - Individual project 2020
#The aim of this project is to conduct a test of previously written main.py program
import time, json, requests #importing necessary libraries
# time library will be used to control speed of program execution
# json library will be used for data conversion
# request library will be used to receive responds to a request from blockchain.info server
from websocket import create_connection #websocket library will be used for server connection to receive notifications for a new block

tx_values= [1] # transaction value we are monitoring for testing

srv = "wss://ws.blockchain.info/inv" #Blockchain.info server - will be used to receive notifications when new bitcoin block is mined (https://www.blockchain.com/api/api_websocket)
ws = create_connection(srv) #creates connection with Blockchain.info server
ws.send("""{"op":"blocks_sub"}""") #sends ""op":"blocks_sub"" to a server which subscribes client  (this python program)
print("Connection to '{}' initialised \nWaiting for new block to be mined".format(srv)) #lets the user know that connection with notification server is established
TOKEN = '559265852:AAE0fhujfcgDRoKwzaReGIcGM_21iOPoEmc' # This is Telegram bot token which will send us direct notification when block with transaction we are interested in is found

def get_full_block(height): # method that accepts (height) as a parameter that allows to get current new mined block in Bitcoin network
    f = open("blocks_with_1btc_output.txt", "a") #opens used_blocks.txt with "a" parameter which stands for append mode
    tx = [] # tx list - will be used for current transactions
    r_tx = [] # r_tx list - will be used for transactions we are interested in
    full_block = requests.get("https://blockchain.info/block-height/{}?format=json".format(height)) #requests from blockchain.info server correct block which was mined when we received notification
    full_block = full_block.json() #converts received data into JSON
    number_of_tx = full_block["blocks"][0]["n_tx"] #skips block header and accesses transactions
    for i in range(number_of_tx):# for loop which go through every transaction extracted from block
        tx.append(full_block["blocks"][0]["tx"][i]["out"][0]["value"]/10**8) #appends all transaction to list of transaction
    for t in tx: #for loop that goes through every transaction previously extracted from the block
        if t in tx_values: # comopares every transaction extracted from the block to transaction we are interested in - tx_values list
            r_tx.append(height) # if transaction matches it appends current block height to r_tx list, '.8f' - converts scientific notation to decimal numbers
            #break # exits the loop as if we found transaction in a block once there is no need to keep loking for others, we just write down block height we are interested in
    r_tx = set(r_tx) # converting list to set instead of list to avoid duplicates
    r_tx = str(r_tx) # converting tuple into a string so we can write it to file
    print(r_tx[1:7]) # shows to the users all transaction that match tx_values list
    f.write("\n"+r_tx[1:7]) # writes new block hight into a blocks_with_1btc_output.txt file
    f.close() #closes the file we were writing to

def listen_for_new_blocks():#method that listens for new blocks all the time
    block = ws.recv() #waits for notification from Blockchain.info server
    block = json.loads(block) #converts received data into JSON data
    if len(block)>0:# checks if we received empty data
        current_block_height = block["x"]["height"] # extracts height of current block after receiving notification
        get_full_block(current_block_height) # initialises get_full_block method that allows to deconstruct newly mined block and analysed it
    return block # method listen_for_new_blocks() returns block - in JSON data type to write it to the used_blocks.txt file


while True: # main loop where program runns all the time
    latest_block = listen_for_new_blocks() # initialies listen_for_new_blocks() method allowing to received notification about newly mined blocks
    time.sleep(60) # keeps loop controlled - after receiving new block it will wait for 60 seconds before waiting a new one


ws.close() #closes the connection with Blockchain.info notification server
