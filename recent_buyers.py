import sys
import time
import requests

def recent_buyers(collection):
    buyers = {}
    price_map = {}
    print(f"{collection}: Fetching current activities (this will take a minute)")

    url = "https://api-mainnet.magiceden.dev/v2/collections/" + collection + "/activities?offset=0&limit=500"
    response = requests.request("GET", url)
    activities = response.json()

    for act in activities:
        if act['type'] == 'buyNow':
            if act['buyer'] not in buyers.keys():
                buyers[act['buyer']] = [act['tokenMint']]
            else:
                buyers[act['buyer']].append(act['tokenMint'])
            price_map[act['tokenMint']] = act['price']

    return (buyers, price_map)


(rec_buyers, price_map) = recent_buyers(sys.argv[1])

print("=================================================================")

print(f"Largest recent {sys.argv[1]} buyers on MagicEden")


for k in sorted(rec_buyers, key=lambda k: len(rec_buyers[k]), reverse=True):
    print("(" + str(len(rec_buyers[k])) + ") https://solscan.io/account/" + k)
    for mint in rec_buyers[k]:
        print(f"    - ({str(price_map[mint])} SOL) https://magiceden.io/item-details/{mint}")


print("=================================================================")
