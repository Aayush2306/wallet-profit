@bot.message_handler(commands=['profitable'])
def profitable(message):
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
  b = a[:50]
  print(b)