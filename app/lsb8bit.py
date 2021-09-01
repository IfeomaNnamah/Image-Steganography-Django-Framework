from PIL import Image
from .ipsnr8bit import IPSNR8bit
import numpy as np


class LSB8bit(IPSNR8bit):
    def embed_msg(self, filename, message, dest):
        img = Image.open(filename, 'r')
        width, height = img.size
        array = np.array(list(img.getdata()))

        total_pixels = width * height
        message += "$t3g0"
        b_message = ''.join([format(ord(i), "08b") for i in message])
        req_pixels = len(b_message)

        if req_pixels > total_pixels:
            print("ERROR: Need larger file size")
        else:
            index = 0
            for p in range(total_pixels):
                if index < req_pixels:
                    array[p] = int(format(array[p], "#010b")[2:9] + b_message[index], 2)
                    index += 1
            array = array.reshape(height, width)
            enc_img = Image.fromarray(array.astype('uint8'), img.mode)
            enc_img.save(dest, "gif")
            print("Image Encoded Successfully")
            return True
        return False  # incorrect image mode, couldn't hide

    def extract_msg(self, filename):
        img = Image.open(filename, 'r')
        width, height = img.size
        array = np.array(list(img.getdata()))

        total_pixels = width * height
        hidden_bits = ""
        for p in range(total_pixels):
            hidden_bits += format(array[p], "#010b")[2:][-1:]
        h_bits = []
        index = 0
        for i in range(0, len(hidden_bits), 8):
            h_bits.append(hidden_bits[i:i + 8])
            index += 1
        message = ""
        for i in range(len(h_bits)):
            if message[-5:] == "$t3g0":
                self.bpp = (i * 8) / total_pixels
                break
            else:
                message += chr(int(h_bits[i], 2))

        bits_in_total_pixels = total_pixels * 1  # total pixels multiplied by total number of bits per pixel for stego 3
        self.number_of_characters = bits_in_total_pixels / 8  # bits_in_total_pixels divided by total bits per character

        if "$t3g0" in message:
            print("Hidden Message:", message[:-5])
            return message[:-5]
        else:
            print("No Hidden Message Found")

        return False  # incorrect image mode, couldn't retrieve

    def embed_msg_stego2bit(self, filename, message, dest):
        img = Image.open(filename, 'r')
        width, height = img.size
        array = np.array(list(img.getdata()))

        total_pixels = width * height
        message += "$t3g0"
        b_message = ''.join([format(ord(i), "08b") for i in message])
        req_pixels = len(b_message)

        if req_pixels > total_pixels:
            print("ERROR: Need larger file size")
        else:
            index = 0
            for p in range(total_pixels):
                if index < req_pixels:
                    array[p] = int(format(array[p], "#010b")[2:8] + b_message[index] + b_message[index + 1], 2)
                    index += 2
            array = array.reshape(height, width)
            enc_img = Image.fromarray(array.astype('uint8'), img.mode)
            enc_img.save(dest, "gif")
            print("Image Encoded Successfully")
            return True
        return False  # incorrect image mode, couldn't hide

    def extract_msg_stego2bit(self, filename):
        img = Image.open(filename, 'r')
        width, height = img.size
        array = np.array(list(img.getdata()))

        total_pixels = width * height
        hidden_bits = ""
        for p in range(total_pixels):
            hidden_bits += format(array[p], "#010b")[2:][-2:]
        h_bits = []
        index = 0
        for i in range(0, len(hidden_bits), 8):
            h_bits.append(hidden_bits[i:i + 8])
            index += 1
        print(h_bits[0:8])
        print(h_bits[8:16])
        print(h_bits[16:24])
        print(h_bits[24:32])
        print(h_bits[32:40])
        message = ""
        for i in range(len(h_bits)):
            if message[-5:] == "$t3g0":
                self.bpp = (i * 8) / total_pixels
                break
            else:
                message += chr(int(h_bits[i], 2))

        bits_in_total_pixels = total_pixels * 2  # total pixels multiplied by total number of bits per pixel for stego 3
        self.number_of_characters = bits_in_total_pixels / 8  # bits_in_total_pixels divided by total bits per character
        if "$t3g0" in message:
            print("Hidden Message:", message[:-5])
            return message[:-5]
        else:
            print("No Hidden Message Found ss")
        return False  # incorrect image mode, couldn't retrieve
    def embed_msg_stego3bit(self, filename, message, dest):
        img = Image.open(filename, 'r')
        width, height = img.size
        array = np.array(list(img.getdata()))

        total_pixels = width * height
        message += "$t3g0"
        b_message = ''.join([format(ord(i), "08b") for i in message])
        req_pixels = len(b_message)

        if req_pixels > total_pixels:
            print("ERROR: Need larger file size")
        else:
            index = 0
            for p in range(total_pixels):
                if index < req_pixels:
                    array[p] = int(format(array[p], "#010b")[2:7] + b_message[index] + b_message[index + 1] + b_message[index + 2], 2)
                    index += 3
            array = array.reshape(height, width)
            enc_img = Image.fromarray(array.astype('uint8'), img.mode)
            enc_img.save(dest, "gif")
            print("Image Encoded Successfully")
            return True
        return False  # incorrect image mode, couldn't hide

    def extract_msg_stego3bit(self, filename):
        img = Image.open(filename, 'r')
        width, height = img.size
        array = np.array(list(img.getdata()))

        total_pixels = width * height

        hidden_bits = ""
        for p in range(total_pixels):
            hidden_bits += format(array[p], "#010b")[2:][-3:]
        h_bits = []
        index = 0
        for i in range(0, len(hidden_bits), 8):
            h_bits.append(hidden_bits[i:i + 8])
            index += 1
        message = ""
        for i in range(len(h_bits)):
            if message[-5:] == "$t3g0":
                self.bpp = (i * 8) / total_pixels
                break
            else:
                message += chr(int(h_bits[i], 2))

        bits_in_total_pixels = total_pixels * 3  # total pixels multiplied by total number of bits per pixel for stego 3
        self.number_of_characters = bits_in_total_pixels / 8  # bits_in_total_pixels divided by total bits per character
        if "$t3g0" in message:
            print("Hidden Message:", message[:-5])
            return message[:-5]
        else:
            print("No Hidden Message Found")

        return False  # incorrect image mode, couldn't retrieve

    def embed_msg_stego4bit(self, filename, message, dest):
        img = Image.open(filename, 'r')
        width, height = img.size
        array = np.array(list(img.getdata()))

        total_pixels = width * height
        message += "$t3g0"
        b_message = ''.join([format(ord(i), "08b") for i in message])
        # print(b_message)
        req_pixels = len(b_message)

        if req_pixels > total_pixels:
            print("ERROR: Need larger file size")
        else:
            index = 0
            for p in range(total_pixels):
                if index < req_pixels:
                    array[p] = int(format(array[p], "#010b")[2:6] + b_message[index] + b_message[index + 1]
                                   + b_message[index + 2] + b_message[index + 3], 2)
                    index += 4
            array = array.reshape(height, width)
            enc_img = Image.fromarray(array.astype('uint8'), img.mode)
            enc_img.save(dest, "gif")
            print("Image Encoded Successfully")
            return True

        return False  # incorrect image mode, couldn't hide

    def extract_msg_stego4bit(self, filename):
        img = Image.open(filename, 'r')
        width, height = img.size
        array = np.array(list(img.getdata()))

        total_pixels = width * height

        hidden_bits = ""
        for p in range(total_pixels):
            hidden_bits += format(array[p], "#010b")[2:][-4:]
        h_bits = []
        index = 0
        for i in range(0, len(hidden_bits), 8):
            h_bits.append(hidden_bits[i:i + 8])
            index += 1
        message = ""
        for i in range(len(h_bits)):
            if message[-5:] == "$t3g0":
                self.bpp = (i * 8) / total_pixels
                break
            else:
                message += chr(int(h_bits[i], 2))
        bits_in_total_pixels = total_pixels * 4  # total pixels multiplied by total number of bits per pixel for stego 4
        self.number_of_characters = bits_in_total_pixels / 8  # bits_in_total_pixels divided by total bits per character

        if "$t3g0" in message:
            print("Hidden Message:", message[:-5])
            return message[:-5]
        else:
            print("No Hidden Message Found")
        return False  # incorrect image mode, couldn't retrieve

    def get_bpp(self):
        return self.bpp

    def get_number_of_characters(self):
            return self.number_of_characters