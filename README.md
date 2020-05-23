# ENS Bot
Telegram chatbot for renewal of ENS domain names (https://ens.domains/), made during https://hackathon.money/.

Start chatting with https://t.me/EasyENS_bot

## Flow
When users start chatting, their Ethereum address is retreived from the mapper. 
This will only work if users use the Telegram Totality client (https://github.com/Evert0x/Telegram).

The ENS registrar is being queried to retreive all the `.eth` domain names that belong to the user. 
Users are able to renew a domain name with `/renew <name>` and will receive a notification if the domain name expires. 

If users use the Telegram Totality fork, they are able renew their domain name by pressing an in chat button!

![In chat buttons for renewal](https://i.imgur.com/UhZ95bY.png)

## Run it yourself

**Fill in .env file**

BOT_TOKEN={Ask @botfather}</br>
NETWORK=3</br>
PROVIDER=https://ropsten.infura.io/v3/{INFUA_TOKEN}</br>
PROVIDER_WS=wss://ropsten.infura.io/ws/v3/{INFUA_TOKEN}</br>
ENS_ADDRESS=0x283Af0B28c62C092C9727F1Ee09c02CA627EB7F5</br>
MAPPER={tg address mappen}</br>
FLASK_HOST=localhost</br>
FLASK_PORT=5000</br>
ETHERSCAN=https://ropsten.etherscan.io



- `python database.py`, create SQLite database
- `pip install -r requirements.txt`, install all dependencies (virtualenv recommended)
- `python app.py`, run the application
