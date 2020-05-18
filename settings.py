from decouple import config
from web3 import Web3, HTTPProvider, WebsocketProvider
import os, json
BOT_TOKEN=config("BOT_TOKEN")

MAPPER=config("MAPPER")

# Ethereum
NETWORK_ID = config('NETWORK', cast=int)

ENDPOINT = Web3(HTTPProvider(config('PROVIDER')))
ENDPOINT_WS = Web3(WebsocketProvider(config('PROVIDER_WS')))

ENS_ADDRESS = config('ENS_ADDRESS')
with open(os.path.join("ensdata", "RegistrarController_abi.json")) as json_data:
    ENS_ABI = json.load(json_data)

CONTRACT_ENS = ENDPOINT.eth.contract(address=ENS_ADDRESS, abi=ENS_ABI)
CONTRACT_ENS_WS = ENDPOINT_WS.eth.contract(address=ENS_ADDRESS, abi=ENS_ABI)