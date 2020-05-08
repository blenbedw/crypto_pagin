import json, requests, time, os

def check_f_file():
    try:
        os.remove("data/int_values.txt")
        print("OLD int_values.txt enteries has been deleted")
    except FileNotFoundError:
        print("Files not present already")

def imp_addr():
    check_f_file()
    addr = open("data/addresses.txt", "r")
    addresses = addr.read()
    addresses = (addresses.replace("'", ""))
    addresses = (addresses.replace("[", ""))
    addresses = (addresses.replace("]", ""))
    addresses = list(addresses.split(","))
    return addresses


def get_int_values(a):
    int_values = open("data/int_values.txt", "a")
    data = requests.get("https://blockchain.info/rawaddr/{}".format(a))
    data = data.json()
    int_txs = []
    n_of_tx = data['n_tx']
    th_hold=0.00001
    for i in range(n_of_tx):
        try:
            n_of_inp = data['txs'][i]['vin_sz']
        except IndexError:
            pass
        for inp in range(n_of_inp):
            try:
                tx = data['txs'][i]['inputs'][inp]['prev_out']['value']/10**8
                if tx<th_hold:
                    int_txs.append('{:.8f}'.format(tx))
            except (IndexError, KeyError):
                pass
    int_values.write(str(int_txs))
    int_values.close()

addresses = imp_addr()
for a in addresses:
    get_int_values(a)
    time.sleep(15)
