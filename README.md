# Solana-NFT-Market-Tools

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; This repo contains scripts that access NFT APIs such as MagicEden (marketplace) or HowRare.is (rarity tools) to analyze the Solana NFT market. These tools are designed to add to the original features MagicEden provides. At the point of writing each script MagicEden has not implemented the feature (to the best of my knowledge). If at any point MagicEden implements a feature in this repo or a similar feature I will do my best to note it in the sections below. The scripts in this repo are designed to be portable, each script functions independently.

## Contents
- [Getting Started](https://github.com/WilliamAmbrozic/MagicEden-NFT-Scripts#Getting-Started)
  - [Finding Market Symbols](https://github.com/WilliamAmbrozic/MagicEden-NFT-Scripts#Finding-Market-Symbols)
- [Listing Tools](https://github.com/WilliamAmbrozic/MagicEden-NFT-Scripts#Listings-Tools)
  - [Deal Scanner](https://github.com/WilliamAmbrozic/MagicEden-NFT-Scripts#Deal-Scanner) 
    - [Collection Scan](https://github.com/WilliamAmbrozic/MagicEden-NFT-Scripts#Collection-Scan)   
    - [Full Market Scan](https://github.com/WilliamAmbrozic/MagicEden-NFT-Scripts#Full-Market-Scan) 
  - [Unique Sellers](https://github.com/WilliamAmbrozic/MagicEden-NFT-Scripts#Unique-Sellers)
  - [Recent Buyers](https://github.com/WilliamAmbrozic/MagicEden-NFT-Scripts#Recent-Buyers)
- [Attribute Tools](https://github.com/WilliamAmbrozic/MagicEden-NFT-Scripts#Attribute-Tools)
  - [Attribute Count Floors](https://github.com/WilliamAmbrozic/MagicEden-NFT-Scripts#Attribute-Tools)
  - [Attribute Count Listing Search](https://github.com/WilliamAmbrozic/MagicEden-NFT-Scripts#Attribute-Count-Listing-Search)
  - [Wallet Attribute Evaluation](https://github.com/WilliamAmbrozic/MagicEden-NFT-Scripts#Wallet-Attribute-Evaluation)  
- [Find Me](https://github.com/WilliamAmbrozic/MagicEden-NFT-Scripts#find-me)
- [Tip Jar](https://github.com/WilliamAmbrozic/MagicEden-NFT-Scripts#Solana-Tip-Jar)

# Getting Started

## Finding Market Symbols

[[Back to contents]](https://github.com/WilliamAmbrozic/MagicEden-NFT-Scripts#contents)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; Any reference to a collection symbol in this repo refers to the collection symbols assigned by API providers (MagicEden, HowRare.is). 

**HowRare.is Collection Symbol:**

![HowRare](https://imgur.com/QgD1QYI.png)

* Search the collection in the search bar, the code after the ```/``` in the url is your collections HowRare.is collection symbol

**MagicEden Collection Symbol:**

![MagicEden](https://imgur.com/KF80Rwn.png)

* Search the collection in the search bar, the code after the ```/marketplace/``` in the url is your collections MagicEden collection symbol

# Listings Tools

## Deal Scanner

[[Back to contents]](https://github.com/WilliamAmbrozic/MagicEden-NFT-Scripts#contents)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; The ```deal_scanner.py``` script will output the top ```top_n``` deals found for a specified collection on MagicEden by HowRare.is rarity or the full marketplace (only collections on HowRare). All listings are looked at and placed in a hashmap that is sorted by values calculated through the following function:

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;**Deal Ratio :=** (NFT_RANK / NFTS_IN_COLLECTION) * LISTING_PRICE

### Collection Scan

![demo](https://imgur.com/WKNhXWr.png)

**Run With:**

```python3 deal_scanner.py ME_COLLECTION_SYMBOL HR_COLLECTION_SYMBOL top_n```

For Example:

```
python3 deal_scanner.py gooney_toons gooneytoons 15
```

or (top 10 default):

```
python3 deal_scanner.py gooney_toons gooneytoons
```

### Full Market Scan

![demo](https://imgur.com/WXjiu7u.png)

**Run With:**

```python3 deal_scanner.py -a top_n floor_lower_price_bound floor_upper_price_bound```

For Example (filters collections with floors outside range):

```
python3 deal_scanner.py -a 100 0.5 2.5
```

or (without floor price ranges):

```
python3 deal_scanner.py -a 100
```

or (top 10 default):

```
python3 deal_scanner.py -a
```

## Unique Sellers

[[Back to contents]](https://github.com/WilliamAmbrozic/MagicEden-NFT-Scripts#contents)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; The ```unique_sellers.py``` script will output all wallet addresses listing along with the NFTs they are selling in the ```ME_COLLECTION_SYMBOL``` collection. For example, this script could help indicate if downward floor pressure is natural or caused by a whale account. 

![Un_Seller](https://imgur.com/qTbnq1D.png)

**Run With:**

```python3 unique_sellers.py ME_COLLECTION_SYMBOL```

For Example:

```
python3 unique_sellers.py solgods
```

## Recent Buyers

[[Back to contents]](https://github.com/WilliamAmbrozic/MagicEden-NFT-Scripts#contents)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; The ```recent_buyers.py``` script will output all wallet addresses (in the last 500 activities) buying along with the NFTs they are buying in the ```ME_COLLECTION_SYMBOL``` collection. This script could help indicate if upward floor pressure is natural or caused by a whale account / the NFT project themselves. 

![Buyers](https://imgur.com/fubeDMN.png)

**Run With:**

```python3 recent_buyers.py ME_COLLECTION_SYMBOL```

For Example:

```
python3 recent_buyers.py gooney_toons
```

# Attribute Tools

## Attribute Count Floors

[[Back to contents]](https://github.com/WilliamAmbrozic/MagicEden-NFT-Scripts#contents)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ```attribute_count_floors.py``` will provide the current floors for attribute counts on MagicEden along with the link to the floor NFT per count.

![floors](https://imgur.com/oE8D5M3.png)

**Run With:**

```python3 attribute_count_floors.py ME_COLLECTION_SYMBOL``` or 

```python3 attribute_count_floors.py ME_COLLECTION_SYMBOL HR_COLLECTION_SYMBOL``` (much faster, if listed on HowRare.is)

For Example:

```
python3 attribute_count_floors.py solgods
``` 

or

```
python3 attribute_count_floors.py solgods solgods
```

## Attribute Count Listing Search

[[Back to contents]](https://github.com/WilliamAmbrozic/MagicEden-NFT-Scripts#contents)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; ```attribute_count_listings.py``` will provide the current listings for a specific attribute count on MagicEden along with the NFT links.

![listings](https://imgur.com/haKZDSt.png)

**Run With:**

```python3 attribute_count_listings.py ME_COLLECTION_SYMBOL ATTR_NUM``` or 

```python3 attribute_count_listings.py ME_COLLECTION_SYMBOL HR_COLLECTION_SYMBOL ATTR_NUM``` (much faster, if listed on HowRare.is)

For Example:

```
python3 attribute_count_listings.py solgods 3
``` 

or

```
python3 attribute_count_listings.py solgods solgods 3
```


## Wallet Attribute Evaluation

[[Back to contents]](https://github.com/WilliamAmbrozic/MagicEden-NFT-Scripts#contents)

&nbsp;&nbsp;&nbsp;&nbsp;&nbsp;&nbsp; MagicEden provides an evaluation of a users wallet by the floor value of each NFT. This evaluation is a lower bound on the true market value of the NFTs in a wallet because it ignores attribute rarity. The ```wallet_evaluation.py``` will instead look and add up the value of each NFT by it's highest attribute floor. Attributes with no floor are ignored. For now the script will only look one collection at a time in a users wallet.

**Run With:**

```python3 wallet_evaluation.py WALLET_ADDR ME_COLLECTION_SYMBOL```

For Example:

```
python3 wallet_evaluation.py 8vU6RfyFDk9WriVgaJohBxqtE86TLtjAR8cPWjdU6zEN gooney_toons
```


## Find Me

- [williamambrozic.info](https://williamambrozic.info)
- [Twitter](https://twitter.com/WilliamAmbrozic)

## Solana Tip Jar
  * wia.sol 
  * 8vU6RfyFDk9WriVgaJohBxqtE86TLtjAR8cPWjdU6zEN
### Bitcoin
  * bc1qa7vkam2w4cgw8njqx976ga5ns8egsq3yzxzlrt



