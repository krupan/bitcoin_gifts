#!/usr/bin/env python3
import math
from pathlib import Path

import qrcode
from PIL import Image, ImageDraw, ImageFont


def inc_tuple(tup, val):
    """increments every value in a tuple by the given amount, returns a
    new tuple

    """
    return tuple([x + val for x in tup])


def text_wrap(txt, width):
    """Dumb text wrapper.  Does not consider word boundaries at all."""
    wrapped = ''
    for char in txt:
        wrapped += char
        if len(wrapped) % width == 0:
            wrapped += '\n'
    return wrapped


class PaperWallet:
    def __init__(self, wallet, wallet_back):
        self.front = wallet
        self.back = wallet_back


def gen_paper_wallet(zpub, zprv):
    wallet = Image.open('BTC_PaperWallet_Design_blank.psd')
    wallet_back = Image.new(mode='RGB', size=(wallet.size[1], wallet.size[0]), color='white')
    pubkey_qr_pos = (35, 469)
    key_qr_size = (285, 285)
    pubkey_txt_pos = (350, 700)
    pubkey_txt_size = (708, 58)
    pubkey_txt_char_width = 58
    privkey_qr_pos = (1524, 40)
    privkey_txt_pos = (1031, 45)
    privkey_txt_size = (485, 88)
    privkey_txt_char_width = 39
    name_pos = (1207,558)
    name_size= (142, 36)
    amount_pos = (1454,559)
    amount_size = (96, 35)
    # get a font
    fnt = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSansCondensed.ttf", size=20)
    fnt_bigger = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSansCondensed.ttf", size=22)
    fnt_mono = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSansMono.ttf", size=20)
    # get a drawing context
    wallet_draw = ImageDraw.Draw(wallet)

    # as far as I can tell, the data, version, and box_size together
    # determine the final size of the qr code.  This combo creates 265
    # pixel square, which fits inside the square on this particular
    # template, and with the -10 crop offsets it is centered.
    zpub_qr = qrcode.make(zpub, version=1, box_size=5)

    zpub_qr = zpub_qr.crop(inc_tuple((0, 0), -10) + inc_tuple(key_qr_size, -10))

    zprv_qr = qrcode.make(zprv, version=1, box_size=5)
    zprv_qr = zprv_qr.crop(inc_tuple((0, 0), -10) + inc_tuple(key_qr_size, -10))
    wallet.paste(zpub_qr, pubkey_qr_pos + inc_tuple(pubkey_qr_pos, key_qr_size[0]))
    wallet.paste(zprv_qr, privkey_qr_pos + inc_tuple(privkey_qr_pos, key_qr_size[0]))

    wallet_draw.multiline_text(pubkey_txt_pos, text_wrap(zpub, pubkey_txt_char_width),
                               font=fnt_mono, fill=(0, 0, 0))
    wallet_draw.multiline_text(privkey_txt_pos, text_wrap(zprv, privkey_txt_char_width),
                               font=fnt_mono, fill=(0, 0, 0))
    wallet_draw.multiline_text(name_pos, "Bryan Murdock", font=fnt, fill=(0, 0, 0))
    wallet_draw.multiline_text(amount_pos, "$5", font=fnt, fill=(0, 0, 0))

    wallet = wallet.crop((0, 0) + wallet.size)
    # back page
    text_first = """Merry Christmas!  These codes are the keys to your new bitcoin
    wallet.  Keep them secret and safe (but I have kept a copy just in
    case you lose them)!  I recommend the BlueWallet phone app for doing
    anything with your bitcoin, but there are others you could choose.

    - To see how much bitcoin is in your wallet, scan the Public Key with
      the BlueWallet app

    - To add bitcoin to your wallet, scan the Public Key with the
      BlueWallet app and it will give you an address you can send bitcoin
      to

    - To send your bitcoin somewhere (I don't recommend this, try hanging
      on to it for a while and watch its value grow!), scan the Private
      Key with the Blue Wallet app and enter the address you want to send
      the bitcoin to

    To buy more bitcoin, I highly recommend using Swan Bitcoin.  If you
    sign up with this URL (or qrcode), Swan will give you $10 in bitcoin
    (full disclosure, I'll get some bitcoin from Swan too).
    """

    swan_url = 'https://www.swanbitcoin.com/bdmurdock/'
    text_second = f"""{swan_url}

    If you have any other questions feel free to ask me:
    bmurdock@gmail.com or 801-739-5754

    """
    swan_qr = qrcode.make(swan_url, version=1, box_size=5)
    wallet_back_draw = ImageDraw.Draw(wallet_back)
    wallet_back_draw.multiline_text((35, 70), text_first, font=fnt_bigger, fill=(0, 0, 0))
    wallet_back.paste(swan_qr, (35, 570))
    wallet_back_draw.multiline_text((35, 770), text_second, font=fnt_bigger, fill=(0, 0, 0))
    wallet_back = wallet_back.rotate(90, expand=True)
    wallet_back_crop = wallet_back.crop((0, 0) + wallet_back.size)
    return PaperWallet(wallet, wallet_back)


def gen_pages(wallets, output):
    # letter paper: 8.5" x 11"
    page_aspect_ratio = 11/8.5
    x_size = wallets[0].front.size[0] + 200
    y_size = round(x_size * page_aspect_ratio)
    # TODO: calculate this based on wallet's y dimension:
    num_wallets_per_page = 3
    Path(output).unlink(missing_ok=True)
    first_page = True
    while wallets:
        page = Image.new(mode='RGB', size=(x_size, y_size), color='white')
        page_back = Image.new(mode='RGB', size=(x_size, y_size), color='white')
        wallets_added = 0
        while wallets:
            wallet = wallets.pop()
            page.paste(wallet.front, (100, 100 + wallet.front.size[1] * wallets_added))
            page_back.paste(wallet.back, (100, 100 + wallet.back.size[1] * wallets_added))
            wallets_added += 1
            if wallets_added % num_wallets_per_page == 0:
                break
        if first_page:
            page.save(output)
            first_page = False
        else:
            page.save(output, append=True)
        page_back.save(output, append=True)


zpub = "zpub6qNRjPvTFR4vs9KCrwRu1vJgjbKAH629e6TCVjxEY9tZoE9DbcuDZW5KZtFFieooAo5X8NHT9MtcdKJNi5w1EH7oR9RtHQeiQdd8ZnkUakq"
zprv = "zprv6qNRjPvTFR4vs9KCrwRu1vJgjbKAH629e6TCVjxEY9tZoE9DbcuDZW5KZtFFieooAo5X8NHT9MtcdKJNi5w1EH7oR9RtHQeiQdd8ZnkUakq"

wallets = []
for i in range(28):
    wallets.append(gen_paper_wallet(zpub=zpub, zprv=zprv))

gen_pages(wallets, output='BTC_PaperWallet_Design.pdf')
