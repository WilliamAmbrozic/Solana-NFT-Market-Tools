import sys
import time
import requests
from tqdm import tqdm
import pickle
import os.path

delay = 0.50

def delay_call(clock_since_call):
    delay_since_call = time.time() - clock_since_call
    if delay_since_call < delay:
        time.sleep(delay - delay_since_call)

def save(item, file_name):
    with open(file_name + '.pickle', 'wb') as handle:
        pickle.dump(item, handle, protocol=pickle.HIGHEST_PROTOCOL)

def load(file_name):
    with open(file_name + '.pickle', 'rb') as handle:
        return pickle.load(handle)

def get_meta_from_mint(mint):
    url = "http://api-mainnet.magiceden.dev/v2/tokens/" + mint
    response = requests.request("GET", url)
    return response.json()

def get_how_collections():
    url = "https://api.howrare.is/v0.1/collections"
    response = requests.request("GET", url)
    response = response.json()
    list = response['result']['data']
    ret = {}
    for i in list:
        ret[i['url'].replace('/', '')] = i['floor']
    return ret

def get_first_mint(HR_symbol):
    url = "https://api.howrare.is/v0.1/collections/" + HR_symbol + "/only_rarity/"
    try:
        response = requests.request("GET", url)
        response = response.json()
        return response['result']['data']['items'][0]['mint']
    except:
        return None

def get_me_symbol(HR_symbol):
    mint = get_first_mint(HR_symbol)
    try:
        return get_meta_from_mint(mint)['collection']
    except:
        return None

def gen_magic_how_pair(HR_symbols, ME_HR_map):
    ret = {}

    for sym in tqdm(HR_symbols):
        clock_since_call = time.time()
        try:
            ret[sym] = get_me_symbol(sym)
            delay_call(clock_since_call)
        except:
            print("Could not add: " + sym)

    return ret

def update_magic_how_pair(HR_symbols, ME_HR_map):

    for sym in tqdm(HR_symbols):
        if sym not in ME_HR_map.keys():
            clock_since_call = time.time()
            try:
                ME_HR_map[sym] = get_me_symbol(sym)

                delay_call(clock_since_call)
            except:
                print("Could not add: " + sym)

    return ME_HR_map

def get_attr_floor_new(collection, all):
    price_map = {}
    if not all:
        print(collection + ": Fetching current listings (this will take a minute)")

    listed = 0
    clock_since_call = time.time()
    try:
        url = "https://api-mainnet.magiceden.dev/v2/collections/" + collection + "/stats"
        response = requests.request("GET", url)
        listed = response.json()['listedCount']
        delay_call(clock_since_call)
        clock_since_call = time.time()

        url = "https://api-mainnet.magiceden.dev/v2/collections/" + collection + "/listings?offset=" + str(listed - 20) + "&limit=20"
        response = requests.request("GET", url)
        listings = response.json()

        delay_call(clock_since_call)
    except:
        return {}

    for listing in listings:
        try:
            price_map[listing['tokenMint']] = listing['price']
        except:
            continue

    return price_map

def get_attr_floor(collection, all):
    price_map = {}
    if not all:
        print(collection + ": Fetching current listings (this will take a minute)")
    i = 0
    while True:
        clock_since_call = time.time()
        try:
            url = "https://api-mainnet.magiceden.dev/v2/collections/" + collection + "/listings?offset=" + str(i*20) + "&limit=20"
            response = requests.request("GET", url)
            listings = response.json()
        except:
            break;

        if response.json() == []:
            break;

        for listing in listings:
            price_map[listing['tokenMint']] = listing['price']

        delay_call(clock_since_call)

        i+=1

    return price_map

def filter(ME_HR_map, syms, bounds):

    for hr_name in list(syms):
        if not (hr_name in syms.keys() and float(syms[hr_name]) >= bounds[0] and float(syms[hr_name]) <= bounds[1]):
            ME_HR_map.pop(hr_name, None)

    return ME_HR_map

def filter_bound(deals, bound, price_map):

    for mint in list(deals):
        if not (mint in price_map.keys() and float(price_map[mint]) <= bound):
            deals.pop(mint, None)

    return deals



def get_rarity(collection):
    url = "https://api.howrare.is/v0.1/collections/" + collection + "/only_rarity/"
    try:
        response = requests.request("GET", url)
        response = response.json()
        data = response['result']['data']['items']
    except:
        return None

    size = len(data)

    rarity = {}

    for nft in data:
        rarity[nft['mint']] = nft['rank']

    return rarity

def get_rarity_price(rarity_map, price_map):
    rarity_price_map = {}

    size = len(rarity_map.keys())

    for mint in price_map.keys():
        if mint in rarity_map.keys() and mint in price_map.keys():
            rarity_price_map[mint] = (float(rarity_map[mint]) / size) * price_map[mint]
        else:
            rarity_price_map[mint] = 9999999

    return rarity_price_map


if "-a" in sys.argv:
    top_n = 10 if len(sys.argv) <= 2 else int(sys.argv[2])

    bound = [float(sys.argv[3]), float(sys.argv[4])] if len(sys.argv) >= 5 else None

    syms = get_how_collections()

    if os.path.isfile('./ME_HR_map.pickle'):
        print("Checking for new HowRare-ME key mappings")
        ME_HR_map  = load('ME_HR_map')
        ME_HR_map = update_magic_how_pair(syms.keys(), ME_HR_map)
    else:
        print("Downloading HowRare-ME key mapping")
        ME_HR_map = gen_magic_how_pair(syms.keys())

    save(ME_HR_map, 'ME_HR_map')

    price_map = {}
    rarity_map = {}
    rarity_price_map = {}
    if bound != None:
        ME_HR_map = filter(ME_HR_map, syms, bound)

    print("Fetching deals per collection")
    for hr_name in tqdm(ME_HR_map.keys()):
        if ME_HR_map[hr_name] == None:
            continue
        tmp_price_map = get_attr_floor_new(ME_HR_map[hr_name], True)
        price_map.update(tmp_price_map)
        tmp_rarity_map = get_rarity(hr_name)
        rarity_map.update(tmp_rarity_map)
        tmp_rarity_price_map = get_rarity_price(tmp_rarity_map, tmp_price_map)
        rarity_price_map.update(tmp_rarity_price_map)

    if bound != None:
        rarity_price_map = filter_bound(rarity_price_map, bound[1], price_map)

    deals = dict(sorted(rarity_price_map.items(), key=lambda item: item[1]))

    print("=================================================================")

    if bound != None:
        print("Top " + str(top_n) + " deals on MagicEden priced between " + bound[0] + "-" + bound[1] + " SOL ")
    else:
        print("Top " + str(top_n) + " deals on MagicEden")

    top_deals = list(deals.keys())[:top_n]
    for i in range(0, len(top_deals)):
        print("\t- Rank " + str(rarity_map[top_deals[i]]) + ", " + str(price_map[top_deals[i]]) + " SOL: https://magiceden.io/item-details/" + top_deals[i])

    print("=================================================================\n")

else:
    ME_name = sys.argv[1]

    HR_name = sys.argv[2]

    top_n = 10 if len(sys.argv) <= 3 else int(sys.argv[3])

    price_map = get_attr_floor(ME_name, False)
    rarity_map = get_rarity(HR_name)
    rarity_price_map = get_rarity_price(rarity_map, price_map)

    deals = dict(sorted(rarity_price_map.items(), key=lambda item: item[1]))

    print("=================================================================")

    print("Top " + str(top_n) + " " + ME_name + " deals on MagicEden")

    top_deals = list(deals.keys())[:top_n]
    for i in range(0, len(top_deals)):
        print("\t- Rank " + str(rarity_map[top_deals[i]]) + ", " + str(price_map[top_deals[i]]) + " SOL: https://magiceden.io/item-details/" + top_deals[i])

    print("=================================================================\n")
