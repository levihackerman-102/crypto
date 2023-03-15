import subprocess
from Crypto.Util.number import bytes_to_long, isPrime
import string
import random

won = False

N = 10

import hashlib

def pad_message(message: bytes) -> bytes:
    """
    Pads a given bytes object according to the MD5 algorithm.

    Args:
        message (bytes): The message to be padded.

    Returns:
        bytes: The padded message.
    """
    # Step 1: Append a single '1' bit to the message.
    padded_message = message + bytes([128])

    # Step 2: Pad the message with zeros until its length is congruent to 448 modulo 512.
    message_length = len(padded_message)
    padding_length = (448 - (message_length * 8) % 512) % 512
    padded_message += b'\0' * (padding_length // 8)

    # Step 3: Append the length of the original message in bits (as a 64-bit little-endian integer).
    message_hash = hashlib.md5(message)
    message_bit_length = message_length * 8
    padded_message += message_hash.digest()[:8]

    return padded_message


while not won:
    # Run the fastcoll executable to generate the two messages
    # pfx = ''.join(random.choices(string.ascii_uppercase + string.digits, k=random.randint(1, N)))
    # file = open("prefix", "w")
    # file.write(pfx)
    # file.close()

    subprocess.run(["./fastcoll_v1.0.0.5.exe", "-p", "prefix", "-o", "msg1.bin", "msg2.bin"])

    # Convert the messages to integers
    with open("msg1.bin", "rb") as f:
        msg1_int = bytes_to_long(f.read())
    print(msg1_int.bit_length())
    with open("msg2.bin", "rb") as f:
        msg2_int = bytes_to_long(f.read())
    print(msg2_int.bit_length())     

    print(msg1_int)
    if isPrime(msg1_int):
        won = True
    print(msg2_int)
    if isPrime(msg2_int):
        won = True

    # won = True

'''
Generating first block: ....
Generating second block: S10.........
Running time: 2.473 s
519761130725993758454222647036748693989815328059540996942804694251636691046951303347237634381558582510772995288152508837827949313858476196382100145170430479950494027859710414918639346120456489989084046702169656343068737869948690425299205228848179714807780274287850536386264828746653605655191420973291914079408715651332474927291159486335795658006219188642832247023493246384574521106855954882961527597889627451160989299889460616638480036727836261943390333971227613
False
519761130725993758454222647036748693989815328059540996942804694251636691046951303347237634381558582510772995288152508837827949313858476196382100145170430479950494027859710414918639346120456489989084030957765723781634041185475386972670160015168924583279339323157749128394078306323132141218877628576669133648535465982114552061364445171034217766436644048536354162915400498467145907619174369317952209200711280260431849960394797378882575265169763121329525912673739741
True
'''
