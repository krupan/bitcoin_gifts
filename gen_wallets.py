#!/usr/bin/env python3

from bitcoinlib.mnemonic import Mnemonic
from bitcoinlib.wallets import Wallet, WalletError

passphrase = Mnemonic('english').generate(256)
print('the passphrase:')
print(passphrase)
w = Wallet.create("blah1", keys=passphrase, network='bitcoin', witness_type='segwit')

print('master private key:')
print(w.main_key.wif)
print('master public key:')
print(w.public_master().wif)
