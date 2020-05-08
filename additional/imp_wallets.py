import json, requests, os

def check_f_file():
    try:
        os.remove("data/addresses.txt")
        os.remove("data/values.txt")
        print("OLD Addresses and Values .txt enteries has been deleted")
    except FileNotFoundError:
        print("Files not present already")

def get_val_addr():
    check_f_file()
    tx = "d2fc5dc604d7b806213a02a2b94bd99b25d8c0e933921b03a0102aca680f1d25"
    data = requests.get("https://blockchain.info/rawtx/{}".format(tx))
    data = data.json()
    num_of_tx = len(data['out']) #countwordsfree.com/jsonviewer
    value_list = []
    addr_list = []
    addresses = open("data/addresses.txt", "a")
    values = open("data/values.txt", "a")

    for t in range(0,num_of_tx):
        value = data['out'][t]['value']/10**8
        if value<1:
            addr = data['out'][t]['addr']
            addr_list.append(addr)
            value_list.append(value)

    addresses.write(str(addr_list))
    values.write(str(value_list))
    print("NEW Addresses and Values .txt files created")
    return addr_list,value_list
