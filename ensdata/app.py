import settings
import pytz
from database import Domains
from datetime import datetime
import web3

def get_price(address, duration):
    return float(settings.Web3.fromWei(
        settings.CONTRACT_ENS.functions.rentPrice(address, duration).call(),
        "gwei"))

def get_domains(address):
    filter = settings.CONTRACT_ENS_WS.events.NameRegistered.createFilter(
        fromBlock=0,
        toBlock='latest',
        argument_filters={
            "owner": address
        }
    )

    rt = []
    for data in filter.get_all_entries():
        name = data["args"]["name"]
        expires = datetime.fromtimestamp(data["args"]["expires"], tz=pytz.UTC)

        q = settings.CONTRACT_ENS_WS.events.NameRenewed.createFilter(
            fromBlock=0,
            toBlock='latest',
            argument_filters={
                "name": name
            }
        )
        for renewal in q.get_all_entries():
            newtimestamp = datetime.fromtimestamp(renewal["args"]["expires"], tz=pytz.UTC)
            if newtimestamp > expires:
                expires = newtimestamp

        rt.append(Domains(
            domain=name,
            expires=expires
        ))

    return rt