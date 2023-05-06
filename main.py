import telebot
import requests
import json

from web3 import Web3

import pickle


#Api_Key = "6128069220:AAGwBaVvB6lZO21ha6wnFCdvHpI8UhzlcIU"
Api_Key = "6256698675:AAF9QJlhl78lqSlxzFqmgnm2KJQFvVf7Hoc"
apii = "6221710889:AAGUxZLR80SzCuYg8KieAKGu05sVjXm-M2U"
bot = telebot.TeleBot(Api_Key)
mainData = {}
infura = "https://mainnet.infura.io/v3/c1f653384020470d942fdd4d8eb97795"
w3 = Web3(Web3.HTTPProvider(infura))
w4 = Web3(
  Web3.HTTPProvider(
    "https://shy-white-knowledge.discover.quiknode.pro/3dd1414d33024c972650675c3437e2a23c8db00f/"
  ))
moralis_key = "GFe9A3lNYWFSv1jO5NmC14bUHeW4oedryp1BPUHxAnAMZUL7C3Nd0Ppjaru3003R"
freeKey = "EK-cgMkq-f79VYYW-u1JY5"
ethApi = "7UMIKS3MQXWYW975VTPF84Y25EDW4B2NXA"
apikeyeth = "7UMIKS3MQXWYW975VTPF84Y25EDW4B2NXA"

ourTokenCa = "0x397b102deccace4aa8e5ba63eedb8e65ad83e20c"
allowed = []
addy_cache = 'addy.pickle'
file_name = 'cached_array.pickle'
addys_cache = 'addys.pickle'
addyVerified = []
verifiedAddyCache = {}
devid = [795341146]
wallets = []


def cache_data(data, file_name):
  with open(file_name, 'wb') as f:
    pickle.dump(data, f)


def load_cached_data(file_name):
  try:
    with open(file_name, 'rb') as f:
      return pickle.load(f)
  except FileNotFoundError:
    return None


#cache_data(allowed, file_name)
#cache_data(verifiedAddyCache, addy_cache)
#cache_data(wallets, addys_cache)
#print(verifiedAddyCache)
allowed = load_cached_data(file_name)
wallets = load_cached_data(addys_cache)
verifiedAddyCache = load_cached_data(addy_cache)
#print(allowed, wallets, verifiedAddyCache)


def profitWalletValue(wallet):

  freeKey2 = "EK-8RsfJ-ckCnNW5-ddbmS"
  try:
    url = f"https://api.ethplorer.io/getAddressInfo/{wallet}?apiKey={freeKey2}&showETHTotals=true"
    res = requests.get(url)
    data = res.text
    realD = json.loads(data)
    #print(realD)
    ethPrice = realD['ETH']['price']['rate']
    ethBalance = realD['ETH']['balance']
    ethPrice = round(ethPrice, 2)
    ethBalance = round(ethBalance, 2)
    totalUsd = round(ethPrice * ethBalance, 1)
    transactions = realD['countTxs']
    addressWallet = f"<a href ='etherscan.io/address/{wallet}'>Wallet</a>"
    opArr = []
    url5 = f"https://api.ethplorer.io/getAddressHistory/{wallet}?apiKey={freeKey}&type=transfer&limit=30"
    res5 = requests.get(url5)
    data5 = res5.text
    realData5 = json.loads(data5)
    hashess = realData5['operations']
    bpArr = []
    for hash in hashess:
      bpArr.append(hash['transactionHash'].lower())

    new_list = []
    for item in bpArr:
      if item not in new_list:
        new_list.append(item)
    for fresh in new_list:
      url2 = f"https://api.ethplorer.io/getTxInfo/{fresh}?apiKey={freeKey2}"
      #realh = w3.eth.get_transaction_receipt(fresh['transaction_hash'])
      #print(realh)
      res = requests.get(url2)
      data = res.text
      #print(data)
      realD = json.loads(data)
      opArr.append(realD)
      str = ""
      profit = 0

    opArr = opArr[:20]
    for op in opArr:
      lengthLelo = len(op["operations"])
      name = op["operations"][lengthLelo - 1]["tokenInfo"]['name']
      if name == "WETH":
        lengthHJi = len(op['operations'])
        value = op['operations'][lengthHJi - 1]['value']
        value = int(value) / 10**18
        value = round(value, 3)
        naam = op['operations'][0]['tokenInfo']['name']
        if naam == "WETH":
          continue
        address = op['operations'][0]['tokenInfo']['address']
        address = f"https://etherscan.io/token/{address}"
        stylenaam = f"<a href='{address}'>{naam}</a>"
        hash = op["hash"]
        hash = f"https://etherscan.io/tx/{hash}"
        hashLink = f"<a href='{hash}'>hash</a>"
        str = str + f"Sold {stylenaam} for {value}eth at {hashLink}\n\n"
        profit = profit + value

      else:
        weth = op["operations"][0]['tokenInfo']['name']
        length = len(op["operations"])
        if weth == "WETH":
          name = op["operations"][length - 1]['tokenInfo']['name']
          address = op["operations"][length - 1]['tokenInfo']['address']
          address = f"https://etherscan.io/token/{address}"
          stylenaam = f"<a href='{address}'>{name}</a>"
          value = op["operations"][0]['value']
          value = int(value) / 10**18
          value = round(value, 3)
          hash = op['hash']
          hash = f"https://etherscan.io/tx/{hash}"
          hashLink = f"<a href='{hash}'>hash</a>"
          str = str + f"Bought {stylenaam} for {value}eth at {hashLink}\n\n"
          profit = profit - value

    profit = round(profit, 3)
    return {"wallet": wallet, "profit": profit}
  except:
    return {"wallet": None, "profit": None}


@bot.message_handler(commands=['profitable'])
def profitable(message):
  try:
    a = []
    ca = message.text.split(" ")[1]
    ca = w3.toChecksumAddress(ca)
    url = f'https://api.etherscan.io/api?module=account&action=txlist&address={ca}&startblock=0&endblock=99999999&sort=asc&apikey={ethApi}'
    response = requests.get(url)
    response_json = response.json()
    transaction_hash = response_json['result'][0]['hash']

    url = f'https://api.etherscan.io/api?module=proxy&action=eth_getTransactionByHash&txhash={transaction_hash}&apikey={ethApi}'
    response = requests.get(url)
    response_json = response.json()
    block_number_hex = response_json['result']['blockNumber']
    block_number = int(block_number_hex, 16)
    latest_block_number = int(w3.eth.blockNumber)
    next_block = block_number + 10000
    if latest_block_number < next_block:
      next_block = latest_block_number

    topic_hash = Web3.keccak(text='Transfer(address,address,uint256)').hex()
    event_filter = w3.eth.filter({
    'fromBlock': block_number,
    'toBlock': next_block,
    'address': ca,
    '  topics': [topic_hash]
  })
    transfer_events = event_filter.get_all_entries()[3:100]
    for event in transfer_events:
      if len(event['topics']) < 3:
        continue
#print(event['topics'])
      toAds = "0x" + (event['topics'][2].hex())[26:]

      if toAds.lower() != ca.lower():
      #print(toAds)
        if toAds not in a:
          a.append(toAds)

#print(a)
    b = a[:30]
    my_array = []
    for w in b:
      profitkya = profitWalletValue(w)
      my_array.append(profitkya)
  #print(profitarray)
    my_array = [
      obj for obj in my_array if all(v is not None for v in 
  obj.values())
  ]
    sorted_balances = sorted(my_array, key=lambda x: x["profit"], reverse=True)
    top_5_balances = sorted_balances[:10]
    #print(top_5_balances)
    text = ""
    for value in top_5_balances:
      wallet = value["wallet"]
      profit = value["profit"]
      link = f"<a href='etherscan.io/address/{wallet}'>Wallet</a>"
      text = text + f"{link} : <pre>{wallet}</pre>\nProfit: {profit} ETH\n\n "

    bot.send_message(message.chat.id,
                   f"<b>Most profitable wallets from the token</b>\n\n{text}",
                   parse_mode="html",
                   disable_web_page_preview=True)


  except:
    print("no")

bot.polling()
