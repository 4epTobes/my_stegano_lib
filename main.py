import os
import sys


def encrypt():
    while True:
        degree = int(input("Encryption degree (1,2,4,8): "))
        if degree in [1, 2, 4, 8]:
            break
    text_len = os.stat("text.txt").st_size
    img_len = os.stat("test.bmp").st_size
    if text_len >= (img_len * degree / 8) - 54:
        print("Too long text!")
        return None

    text = open("text.txt", "r")
    start_bmp = open("test.bmp", "rb")
    encode_bmp = open("encoded.bmp", "wb")

    first54 = start_bmp.read(54)
    encode_bmp.write(first54)

    text_mask, img_mask = create_mask(degree)

    while True:
        symbol = text.read(1)
        if not symbol:
            break

        symbol = ord(symbol)

        for byte_amount in range(0, 8, degree):
            img_byte = int.from_bytes(start_bmp.read(1), sys.byteorder) & img_mask
            bits = symbol & text_mask
            bits >>= (8 - degree)
            img_byte |= bits
            encode_bmp.write(img_byte.to_bytes(1, sys.byteorder))

            symbol <<= degree

    encode_bmp.write(start_bmp.read())

    print("Text lenght = {0}, degree = {1}".format(text_len, degree))

    text.close()
    start_bmp.close()
    encode_bmp.close()


def decrypt():
    while True:
        degree = int(input("Encryption degree (1,2,4,8): "))
        if degree in [1, 2, 4, 8]:
            break
    to_read = int(input("How many symbols you want to read? "))
    img_len = os.stat("encoded.bmp").st_size
    if to_read >= (img_len * degree / 8) - 54:
        print("Too long text!")
        return None

    text = open("decoded_text.txt", "w")
    encoded_bmp = open("encoded.bmp", "rb")

    encoded_bmp.seek(54)

    text_mask, img_mask = create_mask(degree)
    img_mask = ~img_mask

    read = 0
    while read < to_read:
        symbol = 0

        for bits_read in range(0, 8, degree):
            img_byte = int.from_bytes(encoded_bmp.read(1), sys.byteorder) & img_mask

            symbol <<= degree
            symbol |= img_byte
        read += 1
        text.write(chr(symbol))

    text.close()
    encoded_bmp.close()


def create_mask(degree):
    text_mask = 0b11111111
    img_mask = 0b11111111
    text_mask >>= (8-degree)
    text_mask <<= (8-degree)
    img_mask >>= degree
    img_mask <<= degree
    return text_mask, img_mask
