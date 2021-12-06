#!/usr/bin/env python3
from PIL import Image, ImageDraw, ImageFont

im = Image.open('BTC_PaperWallet_Design_blank.psd')
# get a font
#fnt = ImageFont.truetype("Pillow/Tests/fonts/FreeMono.ttf", 40)
# get a drawing context
d = ImageDraw.Draw(im)

# draw multiline text
d.multiline_text((36,472), "Hello\nWorld", fill=(0, 0, 0))
im.save('BTC_PaperWallet_Design.pdf')

