from factom.client import Factomd, FactomWalletd
from factom.exceptions import FactomAPIError


FA = 'FA2jK2HcLnRdS94dEcU27rF3meoJfpUcZPSinpb7AwQvPRY6RL1Q'
EC = 'EC1rs7S56bWgTXN8XvaqhFenzRoHiUpHV2dYvwS7cJpqfb9HaRhi'
FA2 = 'FA39PymAz9pqBPTQkupT7g72THwbM2XyRrUpodvBJHKWGLjpJAd5'
CHAIN = '8da74493b160a37e0fd4459c1c29e487081770905242cc13f7db564e50cf65ca'

fd = Factomd(ec_address=EC, fa_address=FA)
fw = FactomWalletd(ec_address=EC, fa_address=FA)


try:
    #xact_id = fw.xact_fact_to_ec(100000)
    #print("xact id: ", xact_id)
    #print(fd.factoid_submit(xact_id))

    #print(fd.entry_credit_balance())
    print(fw.create_entry(fd, CHAIN, ['some', 'more'], 'data'))

except FactomAPIError as e:
    print(e)
    print(e.data)
