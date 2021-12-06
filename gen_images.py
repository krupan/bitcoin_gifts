#!/usr/bin/env python3
import qrcode
from PIL import Image, ImageDraw, ImageFont


def inc_tuple(tup, val):
    return tuple([x + val for x in tup])


def text_wrap(txt, width):
    wrapped = ''
    for char in txt:
        wrapped += char
        if len(wrapped) % width == 0:
            wrapped += '\n'
    return wrapped


im = Image.open('BTC_PaperWallet_Design_blank.psd')
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
fnt = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSansCondensed.ttf", 20)
fnt_mono = ImageFont.truetype("/usr/share/fonts/TTF/DejaVuSansMono.ttf", 20)
# get a drawing context
d = ImageDraw.Draw(im)

zpub = "zpub6qNRjPvTFR4vs9KCrwRu1vJgjbKAH629e6TCVjxEY9tZoE9DbcuDZW5KZtFFieooAo5X8NHT9MtcdKJNi5w1EH7oR9RtHQeiQdd8ZnkUakq"
zprv = "zprv6qNRjPvTFR4vs9KCrwRu1vJgjbKAH629e6TCVjxEY9tZoE9DbcuDZW5KZtFFieooAo5X8NHT9MtcdKJNi5w1EH7oR9RtHQeiQdd8ZnkUakq"
# as far as I can tell, the data, version, and box_size together
# determine the final size of the qr code.  This combo creates 265
# pixel square, which fits inside the square on this particular
# template, and with the -10 crop offsets it is centered.
zpub_qr = qrcode.make(zpub, version=1, box_size=5)

zpub_qr = zpub_qr.crop(inc_tuple((0, 0), -10) + inc_tuple(key_qr_size, -10))
im.paste(zpub_qr, pubkey_qr_pos + inc_tuple(pubkey_qr_pos, key_qr_size[0]))

zprv_qr = qrcode.make(zprv, version=1, box_size=5)
zprv_qr = zprv_qr.crop(inc_tuple((0, 0), -10) + inc_tuple(key_qr_size, -10))
im.paste(zprv_qr, privkey_qr_pos + inc_tuple(privkey_qr_pos, key_qr_size[0]))

d.multiline_text(pubkey_txt_pos, text_wrap(zpub, pubkey_txt_char_width),
                 font=fnt_mono, fill=(0, 0, 0))
d.multiline_text(privkey_txt_pos, text_wrap(zprv, privkey_txt_char_width),
                 font=fnt_mono, fill=(0, 0, 0))
d.multiline_text(name_pos, "Bryan Murdock", font=fnt, fill=(0, 0, 0))
d.multiline_text(amount_pos, "$5", font=fnt, fill=(0, 0, 0))


im.save('BTC_PaperWallet_Design.pdf')

