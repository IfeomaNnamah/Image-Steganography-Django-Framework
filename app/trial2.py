from PIL import Image
# import cv2
# from .ipsnr import IPSNR
import numpy as np


class Trial:
    # img = Image.open("heart.gif", 'r')
    # width, height = img.size
    # array = np.array(list(img.getdata()))
    # print(img.size)
    # print(list(img.getdata())[:20])
    # total_pixels = array.size
    # message = "ifeoma"
    # message += "xxx"
    # b_message = ''.join([format(ord(i), "08b") for i in message])
    # print(b_message)
    # req_pixels = len(b_message)
    #
    # if req_pixels > total_pixels:
    #     print("ERROR: Need larger file size")
    #
    # else:
    #     index = 0
    #     for p in range(total_pixels):
    #         if index < req_pixels:
    #             # array[p][q] = int(bin(array[p][q])[2:9] + b_message[index], 2)
    #             # array[p][q] = int(bin(array[p][q])[2:8] + b_message[index] + b_message[index + 1], 2)
    #             # print(format(array[p], "#010b"))
    #             array[p] = int(format(array[p], "#010b")[2:7] + b_message[index] + b_message[index + 1] + b_message[index + 2], 2)
    #             # print(format(array[p], "#010b")[2:7] + b_message[index] + b_message[index + 1] + b_message[index + 2])
    #
    #             index += 3
    #     print(bin(array[0]))
    #     print(bin(array[1]))
    #     print(bin(array[2]))
    #     print(bin(array[3]))
    #     array = array.reshape(height, width)
    #     enc_img = Image.fromarray(array.astype('uint8'), img.mode)
    #     enc_img.save("heart_out.gif")

    img = Image.open("heart_out.gif", 'r')
    array = np.array(list(img.getdata()))
    # print(list(img.getdata()))
    total_pixels = array.size

    hidden_bits = ""
    for p in range(int(total_pixels/2)):
        # print(q)
        hidden_bits += format(array[p], "#010b")[2:][-3:]
    h_bits = []
    index = 0
    for i in range(0, len(hidden_bits), 8):
        h_bits.append(hidden_bits[i:i + 8])
        print(h_bits[index])
        index +=1
    message = ""
    # for i in range(len(h_bits)):
    #     if message[-5:] == "$t3g0":
    #         break
    #     else:
    #         message += chr(int(h_bits[i], 2))
    # if "$t3g0" in message:
    #     print("Hidden Message:", message[:-5])
    # else:
    #     print("No Hidden Message Found")
    for i in range(len(h_bits)):
        if message[-3:] == "xxx":
            break
        else:
            message += chr(int(h_bits[i], 2))
    if "xxx" in message:
        print("Hidden Message:", message[:-3])
    else:
        print("No Hidden Message Found")
