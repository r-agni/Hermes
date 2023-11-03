import tkinter as tk
import xrpl
import json

#############################################
## OTHER FUNCTIONS #################################
#############################################

import xrpl

testnet_url = "https://s.altnet.rippletest.net:51234/"

def get_account(seed):
    """get_account"""
    client = xrpl.clients.JsonRpcClient(testnet_url)
    if (seed == ''):
        new_wallet = xrpl.wallet.generate_faucet_wallet(client)
    else:
        new_wallet = xrpl.wallet.Wallet.from_seed(seed)
    return new_wallet

def get_account_info(accountId):
    """get_account_info"""
    client = xrpl.clients.JsonRpcClient(testnet_url)
    acct_info = xrpl.models.requests.account_info.AccountInfo(
        account=accountId,
        ledger_index="validated"
    )
    response = client.request(acct_info)
    return response.result['account_data']

def send_xrp(seed, amount, destination):
    sending_wallet = xrpl.wallet.Wallet.from_seed(seed)
    client = xrpl.clients.JsonRpcClient(testnet_url)
    payment = xrpl.models.transactions.Payment(
        account=sending_wallet.address,
        amount=xrpl.utils.xrp_to_drops(int(amount)),
        destination=destination,
    )
    try:	
        response = xrpl.transaction.submit_and_wait(payment, client, sending_wallet)	
    except xrpl.transaction.XRPLReliableSubmissionException as e:	
        response = f"Submit failed: {e}"
    return response

import xrpl
from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet


testnet_url = "https://s.altnet.rippletest.net:51234"

#####################
# create_trust_line #
#####################

def create_trust_line(seed, issuer, currency, amount):
    """create_trust_line"""
# Get the client
    receiving_wallet = Wallet.from_seed(seed)
    client = JsonRpcClient(testnet_url)
# Define the trust line transaction
    trustline_tx=xrpl.models.transactions.TrustSet(
        account=receiving_wallet.address,
        limit_amount=xrpl.models.amounts.IssuedCurrencyAmount(
            currency=currency,
            issuer=issuer,
            value=int(amount)
        )
    )

    response =  xrpl.transaction.submit_and_wait(trustline_tx,
        client, receiving_wallet)
    return response.result

#################
# send_currency #
#################

def send_currency(seed, destination, currency, amount):
    """send_currency"""
# Get the client
    sending_wallet=Wallet.from_seed(seed)
    client=JsonRpcClient(testnet_url)
# Define the payment transaction.
    send_currency_tx=xrpl.models.transactions.Payment(
        account=sending_wallet.address,
        amount=xrpl.models.amounts.IssuedCurrencyAmount(
            currency=currency,
            value=int(amount),
            issuer=sending_wallet.address
        ),
        destination=destination
    )
    response=xrpl.transaction.submit_and_wait(send_currency_tx, client, sending_wallet)
    return response.result

###############
# get_balance #
###############

def get_balance(sb_account_id, op_account_id):
    """get_balance"""
    client=JsonRpcClient(testnet_url)
    balance=xrpl.models.requests.GatewayBalances(
        account=sb_account_id,
        ledger_index="validated",
        hotwallet=[op_account_id]
    )
    response = client.request(balance)
    return response.result
    
#####################
# configure_account #
#####################

def configure_account(seed, default_setting):
    """configure_account"""
# Get the client
    wallet=Wallet.from_seed(seed)
    client=JsonRpcClient(testnet_url)
# Create transaction
    if (default_setting):
        setting_tx=xrpl.models.transactions.AccountSet(
            account=wallet.classic_address,
            set_flag=xrpl.models.transactions.AccountSetAsfFlag.ASF_DEFAULT_RIPPLE
        )
    else:
        setting_tx=xrpl.models.transactions.AccountSet(
            account=wallet.classic_address,
            clear_flag=xrpl.models.transactions.AccountSetAsfFlag.ASF_DEFAULT_RIPPLE
        )
    response=xrpl.transaction.submit_and_wait(setting_tx,client,wallet)
    return response.result    

import xrpl
from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from xrpl.models.requests import AccountNFTs

testnet_url = "https://s.altnet.rippletest.net:51234"

def mint_token(seed, uri, flags, transfer_fee, taxon):
    """mint_token"""
# Get the client
    minter_wallet=Wallet.from_seed(seed)
    client=JsonRpcClient(testnet_url)
# Define the mint transaction
    mint_tx=xrpl.models.transactions.NFTokenMint(
        account=minter_wallet.address,
        uri=xrpl.utils.str_to_hex(uri),
        flags=int(flags),
        transfer_fee=int(transfer_fee),
        nftoken_taxon=int(taxon)
    )
# Submit the transaction and get results
    reply=""
    try:
        response=xrpl.transaction.submit_and_wait(mint_tx,client,minter_wallet)
        reply=response.result
    except xrpl.transaction.XRPLReliableSubmissionException as e:
        reply=f"Submit failed: {e}"
    return reply


def get_tokens(account):
    """get_tokens"""
    client=JsonRpcClient(testnet_url)
    acct_nfts=AccountNFTs(
        account=account
    )
    response=client.request(acct_nfts)
    return response.result


def burn_token(seed, nftoken_id):
    """burn_token"""
# Get the client
    owner_wallet=Wallet.from_seed(seed)
    client=JsonRpcClient(testnet_url)
    burn_tx=xrpl.models.transactions.NFTokenBurn(
        account=owner_wallet.address,
        nftoken_id=nftoken_id    
    )
# Submit the transaction and get results
    reply=""
    try:
        response=xrpl.transaction.submit_and_wait(burn_tx,client,owner_wallet)
        reply=response.result
    except xrpl.transaction.XRPLReliableSubmissionException as e:
        reply=f"Submit failed: {e}"
    return reply
import xrpl
import json
from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from datetime import datetime
from datetime import timedelta
from xrpl.models.requests import NFTSellOffers
from xrpl.models.requests import NFTBuyOffers
from xrpl.models.transactions import NFTokenAcceptOffer
testnet_url = "https://s.altnet.rippletest.net:51234"

def create_sell_offer(seed, amount, nftoken_id, expiration, destination):
    """create_sell_offer"""
# Get the client
    owner_wallet = Wallet.from_seed(seed)
    client = JsonRpcClient(testnet_url)
    expiration_date = datetime.now()
    if expiration != '':
        expiration_date = xrpl.utils.datetime_to_ripple_time(expiration_date)
        expiration_date = expiration_date + int(expiration)
# Define the sell offer
    sell_offer_tx=xrpl.models.transactions.NFTokenCreateOffer(
        account=owner_wallet.address,
        nftoken_id=nftoken_id,
        amount=amount,
        destination=destination if destination != '' else None,
        expiration=expiration_date if expiration != '' else None,
        flags=1
    )
# Submit the transaction and report the results
    reply=""
    try:
        response=xrpl.transaction.submit_and_wait(sell_offer_tx,client,owner_wallet)
        reply=response.result
    except xrpl.transaction.XRPLReliableSubmissionException as e:
        reply=f"Submit failed: {e}"
    return reply

def accept_sell_offer(seed, offer_index):
    """accept_sell_offer"""
    buyer_wallet=Wallet.from_seed(seed)
    client=JsonRpcClient(testnet_url)
    accept_offer_tx=xrpl.models.transactions.NFTokenAcceptOffer(
       account=buyer_wallet.classic_address,
       nftoken_sell_offer=offer_index
    )
# Submit the transaction and report the results
    reply=""
    try:
        response=xrpl.transaction.submit_and_wait(accept_offer_tx,client,buyer_wallet)
        reply=response.result
    except xrpl.transaction.XRPLReliableSubmissionException as e:
        reply=f"Submit failed: {e}"
    return reply


def create_buy_offer(seed, amount, nft_id, owner, expiration, destination):
    """create_buy_offer"""
# Get the client
    buyer_wallet=Wallet.from_seed(seed)
    client=JsonRpcClient(testnet_url)
    expiration_date=datetime.now()
    if (expiration!=''):
        expiration_date=xrpl.utils.datetime_to_ripple_time(expiration_date)
        expiration_date=expiration_date + int(expiration)
# Define the buy offer transaction with an expiration date
    buy_offer_tx=xrpl.models.transactions.NFTokenCreateOffer(
        account=buyer_wallet.address,
        nftoken_id=nft_id,
        amount=amount,
        owner=owner,
        expiration=expiration_date if expiration!='' else None,
        destination=destination if destination!='' else None,
        flags=0
    )
# Submit the transaction and report the results
    reply=""
    try:
        response=xrpl.transaction.submit_and_wait(buy_offer_tx,client,buyer_wallet)
        reply=response.result
    except xrpl.transaction.XRPLReliableSubmissionException as e:
        reply=f"Submit failed: {e}"
    return reply


def accept_buy_offer(seed, offer_index):
    """accept_buy_offer"""
    buyer_wallet=Wallet.from_seed(seed)
    client=JsonRpcClient(testnet_url)
    accept_offer_tx=xrpl.models.transactions.NFTokenAcceptOffer(
       account=buyer_wallet.address,
       nftoken_buy_offer=offer_index
    )
# Submit the transaction and report the results
    reply=""
    try:
        response=xrpl.transaction.submit_and_wait(accept_offer_tx,client,buyer_wallet)
        reply=response.result
    except xrpl.transaction.XRPLReliableSubmissionException as e:
        reply=f"Submit failed: {e}"
    return reply

def get_offers(nft_id):
    """get_offers"""
    client=JsonRpcClient(testnet_url)
    offers=NFTBuyOffers(
        nft_id=nft_id
    )
    response=client.request(offers)
    allOffers="Buy Offers:\n"+json.dumps(response.result, indent=4)
    offers=NFTSellOffers(
        nft_id=nft_id
    )
    response=client.request(offers)
    allOffers+="\n\nSell Offers:\n"+json.dumps(response.result, indent=4)
    return allOffers

def cancel_offer(seed, nftoken_offer_ids):
    """cancel_offer"""
    owner_wallet=Wallet.from_seed(seed)
    client=JsonRpcClient(testnet_url)
    tokenOfferIDs=[nftoken_offer_ids]
    nftSellOffers="No sell offers"
    cancel_offer_tx=xrpl.models.transactions.NFTokenCancelOffer(
				account=owner_wallet.classic_address,
				nftoken_offers=tokenOfferIDs
    )
    reply=""
    try:
        response=xrpl.transaction.submit_and_wait(cancel_offer_tx,client,owner_wallet)
        reply=response.result
    except xrpl.transaction.XRPLReliableSubmissionException as e:
        reply=f"Submit failed: {e}"
    return reply

#############################################
## Handlers #################################
#############################################

# Module 4 Handlers

def standby_create_sell_offer():
    results = create_sell_offer(
        ent_standby_seed.get(),
        ent_standby_amount.get(),
        ent_standby_nft_id.get(),
        ent_standby_expiration.get(),
        ent_standby_destination.get()
    )
    text_standby_results.delete("1.0", tk.END)
    text_standby_results.insert("1.0", json.dumps(results, indent=4))


def standby_accept_sell_offer():
    results = accept_sell_offer (
        ent_standby_seed.get(),
        ent_standby_nft_offer_index.get()
    )
    text_standby_results.delete("1.0", tk.END)
    text_standby_results.insert("1.0", json.dumps(results, indent=4))


def standby_create_buy_offer():
    results = create_buy_offer(
        ent_standby_seed.get(),
        ent_standby_amount.get(),
        ent_standby_nft_id.get(),
        ent_standby_owner.get(),
        ent_standby_expiration.get(),
        ent_standby_destination.get()
    )
    text_standby_results.delete("1.0", tk.END)
    text_standby_results.insert("1.0", json.dumps(results, indent=4))


def standby_accept_buy_offer():
    results = accept_buy_offer (
        ent_standby_seed.get(),
        ent_standby_nft_offer_index.get()
    )
    text_standby_results.delete("1.0", tk.END)
    text_standby_results.insert("1.0", json.dumps(results, indent=4))


def standby_get_offers():
    results = get_offers(ent_standby_nft_id.get())
    text_standby_results.delete("1.0", tk.END)
    text_standby_results.insert("1.0", results)


def standby_cancel_offer():
    results = cancel_offer(
        ent_standby_seed.get(),
        ent_standby_nft_offer_index.get()
    )
    text_standby_results.delete("1.0", tk.END)
    text_standby_results.insert("1.0", json.dumps(results, indent=4))


def op_create_sell_offer():
    results = create_sell_offer(
        ent_operational_seed.get(),
        ent_operational_amount.get(),
        ent_operational_nft_id.get(),
        ent_operational_expiration.get(),
        ent_operational_destination.get()
    )
    text_operational_results.delete("1.0", tk.END)
    text_operational_results.insert("1.0", json.dumps(results, indent=4))


def op_accept_sell_offer():
    results = accept_sell_offer (
        ent_operational_seed.get(),
        ent_operational_nft_offer_index.get()
    )
    text_operational_results.delete("1.0", tk.END)
    text_operational_results.insert("1.0", json.dumps(results, indent=4))


def op_create_buy_offer():
    results = create_buy_offer(
        ent_operational_seed.get(),
        ent_operational_amount.get(),
        ent_operational_nft_id.get(),
        ent_operational_owner.get(),
        ent_operational_expiration.get(),
        ent_operational_destination.get()
    )
    text_operational_results.delete("1.0", tk.END)
    text_operational_results.insert("1.0", json.dumps(results, indent=4))


def op_accept_buy_offer():
    results = accept_buy_offer (
        ent_operational_seed.get(),
        ent_operational_nft_offer_index.get()
    )
    text_operational_results.delete("1.0", tk.END)
    text_operational_results.insert("1.0", json.dumps(results, indent=4))


def op_get_offers():
    results = get_offers(ent_operational_nft_id.get())
    text_operational_results.delete("1.0", tk.END)
    text_operational_results.insert("1.0", results)


def op_cancel_offer():
    results = cancel_offer(
        ent_operational_seed.get(),
        ent_operational_nft_offer_index.get()
    )
    text_operational_results.delete("1.0", tk.END)
    text_operational_results.insert("1.0", json.dumps(results, indent=4))


# Module 3 Handlers

def standby_mint_token():
    results = mint_token(
        ent_standby_seed.get(),
        ent_standby_uri.get(),
        ent_standby_flags.get(),
        ent_standby_transfer_fee.get(),
        ent_standby_taxon.get()
    )
    text_standby_results.delete("1.0", tk.END)
    text_standby_results.insert("1.0", json.dumps(results, indent=4))


def standby_get_tokens():
    results = get_tokens(ent_standby_account.get())
    text_standby_results.delete("1.0", tk.END)
    text_standby_results.insert("1.0", json.dumps(results, indent=4))


def standby_burn_token():
    results = burn_token(
        ent_standby_seed.get(),
        ent_standby_nft_id.get()
    )
    text_standby_results.delete("1.0", tk.END)
    text_standby_results.insert("1.0", json.dumps(results, indent=4))


def operational_mint_token():
    results = mint_token(
        ent_operational_seed.get(),
        ent_operational_uri.get(),
        ent_operational_flags.get(),
        ent_operational_transfer_fee.get(),
        ent_operational_taxon.get()
    )
    text_operational_results.delete("1.0", tk.END)
    text_operational_results.insert("1.0", json.dumps(results, indent=4))


def operational_get_tokens():
    results = get_tokens(ent_operational_account.get())
    text_operational_results.delete("1.0", tk.END)
    text_operational_results.insert("1.0", json.dumps(results, indent=4))


def operational_burn_token():
    results = burn_token(
        ent_operational_seed.get(),
        ent_operational_nft_id.get()
    )
    text_operational_results.delete("1.0", tk.END)
    text_operational_results.insert("1.0", json.dumps(results, indent=4))


# Module 2 Handlers

def standby_create_trust_line():
    results = create_trust_line(ent_standby_seed.get(),
        ent_standby_destination.get(),
        ent_standby_currency.get(),
        ent_standby_amount.get())
    text_standby_results.delete("1.0", tk.END)
    text_standby_results.insert("1.0", json.dumps(results, indent=4))


def standby_send_currency():
    results = send_currency(ent_standby_seed.get(),
        ent_standby_destination.get(),
        ent_standby_currency.get(),
        ent_standby_amount.get())
    text_standby_results.delete("1.0", tk.END)
    text_standby_results.insert("1.0", json.dumps(results, indent=4))


def standby_configure_account():
    results = configure_account(
        ent_standby_seed.get(),
        standbyRippling)
    text_standby_results.delete("1.0", tk.END)
    text_standby_results.insert("1.0", json.dumps(results, indent=4))


def operational_create_trust_line():
    results = create_trust_line(ent_operational_seed.get(),
        ent_operational_destination.get(),
        ent_operational_currency.get(),
        ent_operational_amount.get())
    text_operational_results.delete("1.0", tk.END)
    text_operational_results.insert("1.0", json.dumps(results, indent=4))


def operational_send_currency():
    results = send_currency(ent_operational_seed.get(),
        ent_operational_destination.get(),
        ent_operational_currency.get(),
        ent_operational_amount.get())
    text_operational_results.delete("1.0", tk.END)
    text_operational_results.insert("1.0", json.dumps(results, indent=4))


def operational_configure_account():
    results = configure_account(
        ent_operational_seed.get(),
        operationalRippling)
    text_operational_results.delete("1.0", tk.END)
    text_operational_results.insert("1.0", json.dumps(results, indent=4))


def get_balances():
    results = get_balance(ent_operational_account.get(), ent_standby_account.get())
    text_standby_results.delete("1.0", tk.END)
    text_standby_results.insert("1.0", json.dumps(results, indent=4))
    results = get_balance(ent_standby_account.get(), ent_operational_account.get())
    text_operational_results.delete("1.0", tk.END)
    text_operational_results.insert("1.0", json.dumps(results, indent=4))


# Module 1 Handlers
def get_standby_account():
    new_wallet = get_account(ent_standby_seed.get())
    ent_standby_account.delete(0, tk.END)
    ent_standby_seed.delete(0, tk.END)
    ent_standby_account.insert(0, new_wallet.classic_address)
    ent_standby_seed.insert(0, new_wallet.seed)


def get_standby_account_info():
    accountInfo = get_account_info(ent_standby_account.get())
    ent_standby_balance.delete(0, tk.END)
    ent_standby_balance.insert(0,accountInfo['Balance'])
    text_standby_results.delete("1.0", tk.END)
    text_standby_results.insert("1.0",json.dumps(accountInfo, indent=4))


def standby_send_xrp():
    response = send_xrp(ent_standby_seed.get(),ent_standby_amount.get(),
                       ent_standby_destination.get())
    text_standby_results.delete("1.0", tk.END)
    text_standby_results.insert("1.0",json.dumps(response.result, indent=4))
    get_standby_account_info()
    get_operational_account_info()


def get_operational_account():
    new_wallet = get_account(ent_operational_seed.get())
    ent_operational_account.delete(0, tk.END)
    ent_operational_account.insert(0, new_wallet.classic_address)
    ent_operational_seed.delete(0, tk.END)
    ent_operational_seed.insert(0, new_wallet.seed)


def get_operational_account_info():
    accountInfo = get_account_info(ent_operational_account.get())
    ent_operational_balance.delete(0, tk.END)
    ent_operational_balance.insert(0,accountInfo['Balance'])
    text_operational_results.delete("1.0", tk.END)
    text_operational_results.insert("1.0",json.dumps(accountInfo, indent=4))


def operational_send_xrp():
    response = send_xrp(ent_operational_seed.get(),ent_operational_amount.get(), ent_operational_destination.get())
    text_operational_results.delete("1.0", tk.END)
    text_operational_results.insert("1.0",json.dumps(response.result,indent=4))
    get_standby_account_info()
    get_operational_account_info()


# Create a new window with the title "Quickstart Module 4"
window = tk.Tk()
window.title("Quickstart Module 4")


standbyRippling = tk.BooleanVar()
operationalRippling = tk.BooleanVar()


# Form frame
frm_form = tk.Frame(relief=tk.SUNKEN, borderwidth=3)
frm_form.pack()

# Create the Label and Entry widgets for "Standby Account"
lbl_standy_seed = tk.Label(master=frm_form, text="Standby Seed")
ent_standby_seed = tk.Entry(master=frm_form, width=50)
lbl_standby_account = tk.Label(master=frm_form, text="Standby Account")
ent_standby_account = tk.Entry(master=frm_form, width=50)
lbl_standy_amount = tk.Label(master=frm_form, text="Amount")
ent_standby_amount = tk.Entry(master=frm_form, width=50)
lbl_standby_destination = tk.Label(master=frm_form, text="Destination")
ent_standby_destination = tk.Entry(master=frm_form, width=50)
lbl_standby_balance = tk.Label(master=frm_form, text="XRP Balance")
ent_standby_balance = tk.Entry(master=frm_form, width=50)
lbl_standby_currency = tk.Label(master=frm_form, text="Currency")
ent_standby_currency = tk.Entry(master=frm_form, width=50)
cb_standby_allow_rippling = tk.Checkbutton(master=frm_form, text="Allow Rippling", variable=standbyRippling, onvalue=True, offvalue=False)
lbl_standby_uri = tk.Label(master=frm_form, text="NFT URI")
ent_standby_uri = tk.Entry(master=frm_form, width=50)
lbl_standby_flags = tk.Label(master=frm_form, text="Flags")
ent_standby_flags = tk.Entry(master=frm_form, width=50)
lbl_standby_transfer_fee = tk.Label(master=frm_form, text="Transfer Fee")
ent_standby_transfer_fee = tk.Entry(master=frm_form, width="50")
lbl_standby_taxon = tk.Label(master=frm_form, text="Taxon")
ent_standby_taxon = tk.Entry(master=frm_form, width="50")
lbl_standby_nft_id = tk.Label(master=frm_form, text="NFT ID")
ent_standby_nft_id = tk.Entry(master=frm_form, width="50")
lbl_standby_nft_offer_index = tk.Label(master=frm_form, text="NFT Offer Index")
ent_standby_nft_offer_index = tk.Entry(master=frm_form, width="50")
lbl_standby_owner = tk.Label(master=frm_form, text="Owner")
ent_standby_owner = tk.Entry(master=frm_form, width="50")
lbl_standby_expiration = tk.Label(master=frm_form, text="Expiration")
ent_standby_expiration = tk.Entry(master=frm_form, width="50")
lbl_standby_results = tk.Label(master=frm_form,text='Results')
text_standby_results = tk.Text(master=frm_form, height = 20, width = 65)




# Place field in a grid.
lbl_standy_seed.grid(row=0, column=0, sticky="w")
ent_standby_seed.grid(row=0, column=1)
lbl_standby_account.grid(row=2, column=0, sticky="e")
ent_standby_account.grid(row=2, column=1)
lbl_standy_amount.grid(row=3, column=0, sticky="e")
ent_standby_amount.grid(row=3, column=1)
lbl_standby_destination.grid(row=4, column=0, sticky="e")
ent_standby_destination.grid(row=4, column=1)
lbl_standby_balance.grid(row=5, column=0, sticky="e")
ent_standby_balance.grid(row=5, column=1)
lbl_standby_currency.grid(row=6, column=0, sticky="e")
ent_standby_currency.grid(row=6, column=1)
cb_standby_allow_rippling.grid(row=7,column=1, sticky="w")
lbl_standby_uri.grid(row=8, column=0, sticky="e")
ent_standby_uri.grid(row=8, column=1, sticky="w")
lbl_standby_flags.grid(row=9, column=0, sticky="e")
ent_standby_flags.grid(row=9, column=1, sticky="w")
lbl_standby_transfer_fee.grid(row=10, column=0, sticky="e")
ent_standby_transfer_fee.grid(row=10, column=1, sticky="w")
lbl_standby_taxon.grid(row=11, column=0, sticky="e")
ent_standby_taxon.grid(row=11, column=1, sticky="w")
lbl_standby_nft_id.grid(row=12, column=0, sticky="e")
ent_standby_nft_id.grid(row=12, column=1, sticky="w")
lbl_standby_nft_offer_index.grid(row=13, column=0, sticky="ne")
ent_standby_nft_offer_index.grid(row=13, column=1, sticky="w")
lbl_standby_owner.grid(row=14, column=0, sticky="ne")
ent_standby_owner.grid(row=14, column=1, sticky="w")
lbl_standby_expiration.grid(row=15, column=0, sticky="ne")
ent_standby_expiration.grid(row=15, column=1, sticky="w")
lbl_standby_results.grid(row=17, column=0, sticky="ne")
text_standby_results.grid(row=17, column=1, sticky="nw")

cb_standby_allow_rippling.select()

###############################################
## Operational Account ########################
###############################################

# Create the Label and Entry widgets for "Operational Account"
lbl_operational_seed = tk.Label(master=frm_form, text="Operational Seed")
ent_operational_seed = tk.Entry(master=frm_form, width=50)
lbl_operational_account = tk.Label(master=frm_form, text="Operational Account")
ent_operational_account = tk.Entry(master=frm_form, width=50)
lbl_operational_amount = tk.Label(master=frm_form, text="Amount")
ent_operational_amount = tk.Entry(master=frm_form, width=50)
lbl_operational_destination = tk.Label(master=frm_form, text="Destination")
ent_operational_destination = tk.Entry(master=frm_form, width=50)
lbl_operational_balance = tk.Label(master=frm_form, text="XRP Balance")
ent_operational_balance = tk.Entry(master=frm_form, width=50)
lbl_operational_currency = tk.Label(master=frm_form, text="Currency")
ent_operational_currency = tk.Entry(master=frm_form, width=50)
cb_operational_allow_rippling = tk.Checkbutton(master=frm_form, text="Allow Rippling", variable=operationalRippling, onvalue=True, offvalue=False)
lbl_operational_uri = tk.Label(master=frm_form, text="NFT URI")
ent_operational_uri = tk.Entry(master=frm_form, width=50)
lbl_operational_flags = tk.Label(master=frm_form, text="Flags")
ent_operational_flags = tk.Entry(master=frm_form, width=50)
lbl_operational_transfer_fee = tk.Label(master=frm_form, text="Transfer Fee")
ent_operational_transfer_fee = tk.Entry(master=frm_form, width="50")
lbl_operational_taxon = tk.Label(master=frm_form, text="Taxon")
ent_operational_taxon = tk.Entry(master=frm_form, width="50")
lbl_operational_nft_id = tk.Label(master=frm_form, text="NFT ID")
ent_operational_nft_id = tk.Entry(master=frm_form, width="50")
lbl_operational_nft_offer_index = tk.Label(master=frm_form, text="NFT Offer Index")
ent_operational_nft_offer_index = tk.Entry(master=frm_form, width="50")
lbl_operational_owner = tk.Label(master=frm_form, text="Owner")
ent_operational_owner = tk.Entry(master=frm_form, width="50")
lbl_operational_expiration = tk.Label(master=frm_form, text="Expiration")
ent_operational_expiration = tk.Entry(master=frm_form, width="50")
lbl_operational_results = tk.Label(master=frm_form,text="Results")
text_operational_results = tk.Text(master=frm_form, height = 20, width = 65)

#Place the widgets in a grid
lbl_operational_seed.grid(row=0, column=4, sticky="e")
ent_operational_seed.grid(row=0, column=5, sticky="w")
lbl_operational_account.grid(row=2,column=4, sticky="e")
ent_operational_account.grid(row=2,column=5, sticky="w")
lbl_operational_amount.grid(row=3, column=4, sticky="e")
ent_operational_amount.grid(row=3, column=5, sticky="w")
lbl_operational_destination.grid(row=4, column=4, sticky="e")
ent_operational_destination.grid(row=4, column=5, sticky="w")
lbl_operational_balance.grid(row=5, column=4, sticky="e")
ent_operational_balance.grid(row=5, column=5, sticky="w")
lbl_operational_currency.grid(row=6, column=4, sticky="e")
ent_operational_currency.grid(row=6, column=5)
cb_operational_allow_rippling.grid(row=7,column=5, sticky="w")
lbl_operational_uri.grid(row=8, column=4, sticky="e")
ent_operational_uri.grid(row=8, column=5, sticky="w")
lbl_operational_flags.grid(row=9, column=4, sticky="e")
ent_operational_flags.grid(row=9, column=5, sticky="w")
lbl_operational_transfer_fee.grid(row=10, column=4, sticky="e")
ent_operational_transfer_fee.grid(row=10, column=5, sticky="w")
lbl_operational_taxon.grid(row=11, column=4, sticky="e")
ent_operational_taxon.grid(row=11, column=5, sticky="w")
lbl_operational_nft_id.grid(row=12, column=4, sticky="e")
ent_operational_nft_id.grid(row=12, column=5, sticky="w")
lbl_operational_nft_offer_index.grid(row=13, column=4, sticky="ne")
ent_operational_nft_offer_index.grid(row=13, column=5, sticky="w")
lbl_operational_owner.grid(row=14, column=4, sticky="ne")
ent_operational_owner.grid(row=14, column=5, sticky="w")
lbl_operational_expiration.grid(row=15, column=4, sticky="ne")
ent_operational_expiration.grid(row=15, column=5, sticky="w")
lbl_operational_results.grid(row=17, column=4, sticky="ne")
text_operational_results.grid(row=17, column=5, sticky="nw")

cb_operational_allow_rippling.select()

#############################################
## Buttons ##################################
#############################################

# Create the Standby Account Buttons
btn_get_standby_account = tk.Button(master=frm_form, text="Get Standby Account",
                                    command = get_standby_account)
btn_get_standby_account.grid(row=0, column=2, sticky = "nsew")
btn_get_standby_account_info = tk.Button(master=frm_form,
                                         text="Get Standby Account Info",
                                         command = get_standby_account_info)
btn_get_standby_account_info.grid(row=1, column=2, sticky = "nsew")
btn_standby_send_xrp = tk.Button(master=frm_form, text="Send XRP >",
                                 command = standby_send_xrp)
btn_standby_send_xrp.grid(row=2, column = 2, sticky = "nsew")
btn_standby_create_trust_line = tk.Button(master=frm_form,
                                         text="Create Trust Line",
                                         command = standby_create_trust_line)
btn_standby_create_trust_line.grid(row=4, column=2, sticky = "nsew")
btn_standby_send_currency = tk.Button(master=frm_form, text="Send Currency >",
                                      command = standby_send_currency)
btn_standby_send_currency.grid(row=5, column=2, sticky = "nsew")
btn_standby_send_currency = tk.Button(master=frm_form, text="Get Balances",
                                      command = get_balances)
btn_standby_send_currency.grid(row=6, column=2, sticky = "nsew")
btn_standby_configure_account = tk.Button(master=frm_form,
                                          text="Configure Account",
                                          command = standby_configure_account)
btn_standby_configure_account.grid(row=7,column=0, sticky = "nsew")
btn_standby_mint_token = tk.Button(master=frm_form, text="Mint NFT",
                                   command = standby_mint_token)
btn_standby_mint_token.grid(row=8, column=2, sticky="nsew")
btn_standby_get_tokens = tk.Button(master=frm_form, text="Get NFTs",
                                   command = standby_get_tokens)
btn_standby_get_tokens.grid(row=9, column=2, sticky="nsew")
btn_standby_burn_token = tk.Button(master=frm_form, text="Burn NFT",
                                   command = standby_burn_token)
btn_standby_burn_token.grid(row=10, column=2, sticky="nsew")
btn_standby_create_sell_offer = tk.Button(master=frm_form, text="Create Sell Offer",
                                          command = standby_create_sell_offer)
btn_standby_create_sell_offer.grid(row=11, column=2, sticky="nsew")
btn_standby_accept_sell_offer = tk.Button(master=frm_form, text="Accept Sell Offer",
                                          command = standby_accept_sell_offer)
btn_standby_accept_sell_offer.grid(row=12, column=2, sticky="nsew")
btn_standby_create_buy_offer = tk.Button(master=frm_form, text="Create Buy Offer",
                                          command = standby_create_buy_offer)
btn_standby_create_buy_offer.grid(row=13, column=2, sticky="nsew")
btn_standby_accept_buy_offer = tk.Button(master=frm_form, text="Accept Buy Offer",
                                          command = standby_accept_buy_offer)
btn_standby_accept_buy_offer.grid(row=14, column=2, sticky="nsew")
btn_standby_get_offers = tk.Button(master=frm_form, text="Get Offers",
                                          command = standby_get_offers)
btn_standby_get_offers.grid(row=15, column=2, sticky="nsew")
btn_standby_cancel_offer = tk.Button(master=frm_form, text="Cancel Offer",
                                          command = standby_cancel_offer)
btn_standby_cancel_offer.grid(row=16, column=2, sticky="nsew")



# Create the Operational Account Buttons
btn_get_operational_account = tk.Button(master=frm_form,
                                        text="Get Operational Account",
                                        command = get_operational_account)
btn_get_operational_account.grid(row=0, column=3, sticky = "nsew")
btn_get_op_account_info = tk.Button(master=frm_form, text="Get Op Account Info",
                                    command = get_operational_account_info)
btn_get_op_account_info.grid(row=1, column=3, sticky = "nsew")
btn_op_send_xrp = tk.Button(master=frm_form, text="< Send XRP",
                            command = operational_send_xrp)
btn_op_send_xrp.grid(row=2, column = 3, sticky = "nsew")
btn_op_create_trust_line = tk.Button(master=frm_form, text="Create Trust Line",
                                    command = operational_create_trust_line)
btn_op_create_trust_line.grid(row=4, column=3, sticky = "nsew")
btn_op_send_currency = tk.Button(master=frm_form, text="< Send Currency",
                                 command = operational_send_currency)
btn_op_send_currency.grid(row=5, column=3, sticky = "nsew")
btn_op_get_balances = tk.Button(master=frm_form, text="Get Balances",
                                command = get_balances)
btn_op_get_balances.grid(row=6, column=3, sticky = "nsew")
btn_op_configure_account = tk.Button(master=frm_form, text="Configure Account",
                                     command = operational_configure_account)
btn_op_configure_account.grid(row=7,column=4, sticky = "nsew")
btn_op_mint_token = tk.Button(master=frm_form, text="Mint NFT",
                              command = operational_mint_token)
btn_op_mint_token.grid(row=8, column=3, sticky="nsew")
btn_op_get_tokens = tk.Button(master=frm_form, text="Get NFTs",
                              command = operational_get_tokens)
btn_op_get_tokens.grid(row=9, column=3, sticky="nsew")
btn_op_burn_token = tk.Button(master=frm_form, text="Burn NFT",
                              command = operational_burn_token)
btn_op_burn_token.grid(row=10, column=3, sticky="nsew")
btn_op_create_sell_offer = tk.Button(master=frm_form, text="Create Sell Offer",
                                          command = op_create_sell_offer)
btn_op_create_sell_offer.grid(row=11, column=3, sticky="nsew")
btn_op_accept_sell_offer = tk.Button(master=frm_form, text="Accept Sell Offer",
                                          command = op_accept_sell_offer)
btn_op_accept_sell_offer.grid(row=12, column=3, sticky="nsew")
btn_op_create_buy_offer = tk.Button(master=frm_form, text="Create Buy Offer",
                                          command = op_create_buy_offer)
btn_op_create_buy_offer.grid(row=13, column=3, sticky="nsew")
btn_op_accept_buy_offer = tk.Button(master=frm_form, text="Accept Buy Offer",
                                          command = op_accept_buy_offer)
btn_op_accept_buy_offer.grid(row=14, column=3, sticky="nsew")
btn_op_get_offers = tk.Button(master=frm_form, text="Get Offers",
                                          command = op_get_offers)
btn_op_get_offers.grid(row=15, column=3, sticky="nsew")
btn_op_cancel_offer = tk.Button(master=frm_form, text="Cancel Offer",
                                          command = op_cancel_offer)
btn_op_cancel_offer.grid(row=16, column=3, sticky="nsew")

# Start the application
window.mainloop()
