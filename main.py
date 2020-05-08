# This program was written by Edvards Galuzo for CS3590 - Individual project 2020
# Aim of this project is to build application that allows to find specific transaction (in real time) on Bitcoin blockchain and notify users thought Telegram chat as soon as new block is mined
import time, json, requests, telebot #importing necessary libraries
# time library will be used to control speed of program execution
# json library will be used for data conversion
# request library will be used to receive responds to a request from blockchain.info server
# telebot library will be used to control telegram bot behaviour
from websocket import create_connection # websocket library will be used for server connection to receive notifications for a new block

tx_values= [0.00000555,0.00000777,0.00000666,0.00008888,0.00000667,0.00002019,0.00002020] # transaction value we are monitoring

srv = "wss://ws.blockchain.info/inv" #Blockchain.info server - will be used to receive notifications when new bitcoin block is mined (https://www.blockchain.com/api/api_websocket)
ws = create_connection(srv) #creates connection with Blockchain.info server
ws.send("""{"op":"blocks_sub"}""") #sends ""op":"blocks_sub"" to a server which subscribes client (this python program)
print("Connection to '{}' initialised \nWaiting for new block to be mined".format(srv)) #lets the user know that connection with notification server is established
f = open("data/used_blocks.txt", "a") #opens used_blocks.txt with "a" parameter which stands for append mode
TOKEN = '559265852:AAE0fhujfcgDRoKwzaReGIcGM_21iOPoEmc' # This is Telegram bot token which will send us direct notification when block with transaction we are interested in is found
bot = telebot.TeleBot(TOKEN) #creates Telegram bot object

def get_full_block(height): # method that accepts (height) as a parameter that allows to get current new mined block in Bitcoin network
    tx = [] # tx list - will be used for current transactions
    r_tx = [] # r_tx list - will be used for transactions we are interested in
    full_block = requests.get("https://blockchain.info/block-height/{}?format=json".format(height)) #requests from blockchain.info server correct block which was mined when we received notification
    full_block = full_block.json() #converts received data into JSON
    number_of_tx = full_block["blocks"][0]["n_tx"] #skips block header and accesses transactions
    for i in range(number_of_tx):# for loop which go through every transaction extracted from block
        tx.append(full_block["blocks"][0]["tx"][i]["out"][0]["value"]/10**8) #appends all transaction to list of transaction, 10**8 - is used to convert Satoshi to Bitcoins
    for t in tx: #for loop that goes through every transaction previously extracted from the block
        if t in tx_values: # compares every transaction extracted from the block to transaction we are interested in - tx_values list
            r_tx.append(format(t, '.8f')) #if transaction matches it  appends value we are interested in to r_tx list, '.8f' - converts scientific notation to decimal numbers
    r_tx = set(r_tx) # converting list to set instead of list to avoid duplicates
    print(r_tx) #shows to the users all transaction that match tx_values list
    if len(r_tx) > 0: # acts a s filter if we found any values in current block from tx_values only in that case bot sends message to telegram chat
        bot.send_message(-311298975,str(r_tx)) #sends transaction to Telegram chat (-311298975 - is chat id where messages need to be sent to)

def listen_for_new_blocks():#method that listens for new blocks all the time
    block = ws.recv() #waits for notification from Blockchain.info server
    block = json.loads(block) #converts received data into JSON data
    if len(block)>0: # checks if we recived empty data
        current_block_height = block["x"]["height"] # extracts height of current block after receiving notification
        get_full_block(current_block_height) # initialises get_full_block() method that allows to deconstruct newly mined block and analysed it
    return block # method listen_for_new_blocks() returns block - in JSON data type to write it to the used_blocks.txt file


while True: # main loop where program runs all the time
    latest_block = listen_for_new_blocks() # initializes listen_for_new_blocks() method allowing to receive notification about newly mined blocks
    print("\n") # inserts new line to keep data apart
    f.write(str(latest_block)) # writes received data into used_blocks.txt file which was previously received from listen_for_new_blocks() method
    time.sleep(60) # keeps loop controlled - after receiving new block it will wait for 60 seconds before waiting a new one

f.close() #closes the file we were writing to
ws.close() #closes the connection with Blockchain.info notification server
