#!/usr/bin/env python3

from bitcoinlib.mnemonic import Mnemonic
from bitcoinlib.wallets import Wallet, WalletError

passphrase = 'upper badge major focus menu adjust awake accuse loan fit mandate lecture lock ignore wealth speak second expire power usage small match century victory'
print(passphrase)
try:
    w = Wallet.create("upper badge", keys=passphrase, network='bitcoin', witness_type='segwit')
except WalletError:
    w = Wallet("upper badge")
w.get_key()
w.info(5)
w.get_keys(number_of_keys=10)
print(w.addresslist())
print(w.public_master().wif)
print(w.main_key.wif)
