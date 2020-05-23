# ENS Bot
Telegram chatbot for renewal of ENS domain names (https://ens.domains/), made during https://hackathon.money/.


## Flow
When users start chatting, their Ethereum address is retreived from the mapper. 
This will only work if users use the Telegram Totality client (https://github.com/Evert0x/Telegram).

The ENS registrar is being queried to retreive all the `.eth` domain names that belong to the user. 
Users are able to renew a domain name with `/renew <name>` and will receive a notification if the domain name expires. 

If users use the Telegram Totality fork, they are able renew their domain name by pressing an in chat button!

![In chat buttons for renewal](https://i.imgur.com/UhZ95bY.png)
