import tkinter as tk
import xrpl
import json
from xrpl.clients import JsonRpcClient
from xrpl.wallet import Wallet
from xrpl.models.requests import AccountNFTs
from xrpl.wallet import Wallet

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

testnet_url = "https://s.altnet.rippletest.net:51234"

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

def standby_configure_account():
    results = configure_account(
        ent_standby_seed.get(),
        standbyRippling)
    text_standby_results.delete("1.0", tk.END)
    text_standby_results.insert("1.0", json.dumps(results, indent=4))

def get_standby_account():
    new_wallet = get_account(ent_standby_seed.get())
    ent_standby_account.delete(0, tk.END)
    ent_standby_seed.delete(0, tk.END)
    ent_standby_account.insert(0, new_wallet.classic_address)
    ent_standby_seed.insert(0, new_wallet.seed)
    accountInfo = get_account_info(ent_standby_account.get())
    text_standby_results.delete("1.0", tk.END)
    text_standby_results.insert("1.0",json.dumps(accountInfo, indent=4))


# Create a new window with the title "Quickstart Module 3"
window = tk.Tk()
window.title("MINT HEALTH PASSPORT")

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
cb_standby_allow_rippling = tk.Checkbutton(master=frm_form, text="Allow Rippling", variable=standbyRippling, onvalue=True, offvalue=False)
lbl_standby_uri = tk.Label(master=frm_form, text="NFT URI")
ent_standby_uri = tk.Entry(master=frm_form, width=50)
ent_standby_flags = 8
ent_standby_transfer_fee = 0
ent_standby_taxon = 0
lbl_standby_nft_id = tk.Label(master=frm_form, text="NFT ID")
ent_standby_nft_id = tk.Entry(master=frm_form, width="50")
lbl_standby_results = tk.Label(master=frm_form,text='Results')
text_standby_results = tk.Text(master=frm_form, height = 20, width = 65)

# Place field in a grid.
lbl_standy_seed.grid(row=0, column=0, sticky="w")
ent_standby_seed.grid(row=0, column=1)
lbl_standby_account.grid(row=2, column=0, sticky="e")
ent_standby_account.grid(row=2, column=1)
lbl_standy_amount.grid(row=3, column=0, sticky="e")
ent_standby_amount.grid(row=3, column=1)
cb_standby_allow_rippling.grid(row=7,column=1, sticky="w")
lbl_standby_uri.grid(row=8, column=0, sticky="e")
ent_standby_uri.grid(row=8, column=1, sticky="w")
lbl_standby_nft_id.grid(row=9, column=0, sticky="e")
ent_standby_nft_id.grid(row=9, column=1, sticky="w")
lbl_standby_results.grid(row=10, column=0, sticky="ne")
text_standby_results.grid(row=10, column=1, sticky="nw")
cb_standby_allow_rippling.select()

# Create the Standby Account Buttons
btn_get_standby_account = tk.Button(master=frm_form, text="Get Standby Account",
                                    command = get_standby_account)
btn_get_standby_account.grid(row=0, column=2, sticky = "nsew")
btn_standby_mint_token = tk.Button(master=frm_form, text="Mint NFT",
                                   command = standby_mint_token)
btn_standby_mint_token.grid(row=2, column=2, sticky="nsew")
btn_standby_get_tokens = tk.Button(master=frm_form, text="Get NFTs",
                                   command = standby_get_tokens)
btn_standby_get_tokens.grid(row=3, column=2, sticky="nsew")

# Start the application
window.mainloop()