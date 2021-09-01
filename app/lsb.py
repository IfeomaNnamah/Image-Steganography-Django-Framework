from PIL import Image
from .ipsnr import IPSNR
import numpy as np


class LSB(IPSNR):
    def embed_msg(self, filename, message, dest):
        img = Image.open(filename, 'r')
        width, height = img.size
        array = np.array(list(img.getdata()))
        if img.mode == 'RGB' or img.mode == 'RGBA':
            n = 3
            m = 0

        total_pixels = width * height

        if len(message) % 3 == 0:
            pass
        elif len(message) % 3 == 1:
            message += " "
        elif len(message) % 3 == 2:
            message += "  "
        else:
            return False
        message += "$t3g0"
        print(message)
        b_message = ''.join([format(ord(i), "08b") for i in message])
        req_pixels = len(b_message)
        print(req_pixels)
        if req_pixels > total_pixels:
            print("ERROR: Need larger file size")

        else:
            index = 0
            for p in range(total_pixels):
                for q in range(m, n):
                    if index < req_pixels:
                        array[p][q] = int(format(array[p][q], "#010b")[2:9] + b_message[index], 2)
                        index += 1
            if img.mode == 'RGB':
                n = 3
            elif img.mode == 'RGBA':
                n = 4
            array = array.reshape(height, width, n)
            enc_img = Image.fromarray(array.astype('uint8'), img.mode)
            file_format = filename.split('.')[1]
            if file_format == 'png':
                enc_img.save(dest, 'png')
                print("Message Encoded Successfully")
                return True
            elif file_format == 'bmp':
                enc_img.save(dest, 'bmp')
                print("Message Encoded Successfully")
                return True
            else:
                return False
        return False # incorrect image mode, couldn't hide

    def extract_msg(self, filename):
        img = Image.open(filename, 'r')
        width, height = img.size
        array = np.array(list(img.getdata()))

        if img.mode == 'RGB' or img.mode == 'RGBA':
            n = 3
            m = 0

        total_pixels = width * height
        hidden_bits = ""
        for p in range(total_pixels):
            for q in range(m, n):
                hidden_bits += (format(array[p][q], "#010b")[2:][-1])

        hidden_bits = [hidden_bits[i:i + 8] for i in range(0, len(hidden_bits), 8)]

        message = ""
        for i in range(len(hidden_bits)):
            if message[-5:] == "$t3g0":
                print(i)
                self.bpp = (i * 8) / total_pixels
                break
            else:
                message += chr(int(hidden_bits[i], 2))

        bits_in_total_pixels = total_pixels * 3  # total pixels multiplied by total number of bits per pixel for stego 1
        self.number_of_characters = bits_in_total_pixels / 8  # bits_in_total_pixels divided by total bits per character

        if "$t3g0" in message:
            print("Hidden Message:", message[:-5])
            return message[:-5]
        else:
            print("No Hidden Message Found")
            self.bpp = 0
            self.number_of_characters = 0
        return False # incorrect image mode, couldn't retrieve

    def embed_msg_stego2bit(self, filename, message, dest):
        img = Image.open(filename, 'r')
        width, height = img.size
        array = np.array(list(img.getdata()))
        if img.mode == 'RGB' or img.mode == 'RGBA':
            n = 3
            m = 0

        total_pixels = width * height

        if len(message) % 3 == 0:
            pass
        elif len(message) % 3 == 1:
            message += " "
        elif len(message) % 3 == 2:
            message += "  "
        else:
            return False
        message += "$t3g0"
        print(message)
        b_message = ''.join([format(ord(i), "08b") for i in message])
        req_pixels = len(b_message)

        if req_pixels > total_pixels:
            print("ERROR: Need larger file size")

        else:
            index = 0
            for p in range(total_pixels):
                for q in range(m, n):
                    if index < req_pixels:
                        array[p][q] = int(format(array[p][q], "#010b")[2:8] + b_message[index] + b_message[index + 1], 2)
                        # 0 1 2 3 4 5
                        index += 2
            if img.mode == 'RGB':
                n = 3
            elif img.mode == 'RGBA':
                n = 4
            array = array.reshape(height, width, n)
            enc_img = Image.fromarray(array.astype('uint8'), img.mode)
            file_format = filename.split('.')[1]
            if file_format == 'png':
                enc_img.save(dest, 'png')
                print("Message Encoded Successfully")
                return True
            elif file_format == 'bmp':
                enc_img.save(dest, 'bmp')
                print("Message Encoded Successfully")
                return True
            else:
                return False
        return False

    def extract_msg_stego2bit(self, filename):
        img = Image.open(filename, 'r')
        width, height = img.size
        array = np.array(list(img.getdata()))
        if img.mode == 'RGB' or img.mode == 'RGBA':
            n = 3
            m = 0
        total_pixels = width * height

        hidden_bits = ""
        for p in range(total_pixels):
            for q in range(m, n):
                hidden_bits += (format(array[p][q], "#010b")[2:][-2:])

        hidden_bits = [hidden_bits[i:i + 8] for i in range(0, len(hidden_bits), 8)]
        print(hidden_bits[0:8])
        print(hidden_bits[8:16])
        print(hidden_bits[16:24])
        message = ""
        for i in range(len(hidden_bits)):
            if message[-5:] == "$t3g0":
                self.bpp = (i*8)/total_pixels
                break
            else:
                message += chr(int(hidden_bits[i], 2))

        bits_in_total_pixels = total_pixels * 6  # total pixels multiplied by total number of bits per pixel for stego 2
        self.number_of_characters = bits_in_total_pixels / 8  # bits_in_total_pixels divided by total bits per character

        if "$t3g0" in message:
            print("Hidden Message:", message[:-5])
            return message[:-5]
        else:
            print("No Hidden Message Found")
        return False  # incorrect image mode, couldn't retrieve

    def embed_msg_stego3bit(self, filename, message, dest):
        img = Image.open(filename, 'r')
        width, height = img.size
        array = np.array(list(img.getdata()))

        if img.mode == 'RGB' or img.mode == 'RGBA':
            n = 3
            m = 0
        total_pixels = width * height

        if len(message) % 3 == 0:
            message += " "
        elif len(message) % 3 == 1:
            pass
        elif len(message) % 3 == 2:
            message += "  "
        else:
            return False
        message += "$t3g0"
        print(message)
        b_message = ''.join([format(ord(i), "08b") for i in message])
        req_pixels = len(b_message)
        if req_pixels > total_pixels:
            print("ERROR: Need larger file size")
        else:
            index = 0
            for p in range(total_pixels):
                for q in range(m, n):
                    if index < req_pixels:
                        array[p][q] = int(format(array[p][q], "#010b")[2:7] + b_message[index] + b_message[index + 1] + b_message[index + 2], 2)
                        # print(format(array[p][q], "#010b")[2:7] + b_message[index] + b_message[index + 1] + b_message[index + 2])
                        index += 3
            if img.mode == 'RGB':
                n = 3
            elif img.mode == 'RGBA':
                n = 4
            array = array.reshape(height, width, n)
            enc_img = Image.fromarray(array.astype('uint8'), img.mode)
            file_format = filename.split('.')[1]
            if file_format == 'png':
                enc_img.save(dest, 'png')
                print("Message Encoded Successfully")
                return True
            elif file_format == 'bmp':
                enc_img.save(dest, 'bmp')
                print("Message Encoded Successfully")
                return True
            else:
                return False
        return False

    def extract_msg_stego3bit(self, filename):
        img = Image.open(filename, 'r')
        width, height = img.size
        array = np.array(list(img.getdata()))
        if img.mode == 'RGB' or img.mode == 'RGBA':
            n = 3
            m = 0
        total_pixels = width * height
        hidden_bits = ""
        for p in range(total_pixels):
            for q in range(m, n):
                hidden_bits += (format(array[p][q], "#010b")[2:][-3:])

        hidden_bits = [hidden_bits[i:i + 8] for i in range(0, len(hidden_bits), 8)]
        print(hidden_bits[0:8])
        print(hidden_bits[8:16])
        print(hidden_bits[16:24])
        print(hidden_bits[24:32])
        print(hidden_bits[32:40])
        message = ""
        for i in range(len(hidden_bits)):
            if message[-5:] == "$t3g0":
                self.bpp = (i * 8) / total_pixels
                break
            else:
                message += chr(int(hidden_bits[i], 2))

        bits_in_total_pixels = total_pixels * 9  # total pixels multiplied by total number of bits per pixel for stego 4
        self.number_of_characters = bits_in_total_pixels / 8  # bits_in_total_pixels divided by total bits per character

        if "$t3g0" in message:
            print("Hidden Message:", message[:-5])
            return message[:-5]
        else:
            print("No Hidden Message Found")
            return "No Hidden Message Found"
        return False

    def embed_msg_stego4bit(self, filename, message, dest):
        img = Image.open(filename, 'r')
        width, height = img.size
        array = np.array(list(img.getdata()))
        if img.mode == 'RGB' or img.mode == 'RGBA':
            n = 3
            m = 0

        total_pixels = width * height

        if len(message) % 3 == 0:
            pass
        elif len(message) % 3 == 1:
            message += " "
        elif len(message) % 3 == 2:
            message += "  "
        else:
            return False
        message += "$t3g0"
        print(message)
        b_message = ''.join([format(ord(i), "08b") for i in message])
        req_pixels = len(b_message)

        if req_pixels > total_pixels:
            print("ERROR: Need larger file size")
        else:
            index = 0
            for p in range(total_pixels):
                for q in range(m, n):
                    if index < req_pixels:
                        array[p][q] = int(format(array[p][q], "#010b")[2:6] + b_message[index] + b_message[index + 1]
                                          + b_message[index + 2] + b_message[index + 3], 2)
                        index += 4
            if img.mode == 'RGB':
                n = 3
            elif img.mode == 'RGBA':
                n = 4
            array = array.reshape(height, width, n)
            enc_img = Image.fromarray(array.astype('uint8'), img.mode)
            file_format = filename.split('.')[1]
            if file_format == 'png':
                enc_img.save(dest, 'png')
                print("Message Encoded Successfully")
                return True
            elif file_format == 'bmp':
                enc_img.save(dest, 'bmp')
                print("Message Encoded Successfully")
                return True
            else:
                return False
        return False

    def extract_msg_stego4bit(self, filename):
        img = Image.open(filename, 'r')
        width, height = img.size
        array = np.array(list(img.getdata()))
        if img.mode == 'RGB' or img.mode == 'RGBA':
            n = 3
            m = 0
        total_pixels = width * height
        hidden_bits = ""
        for p in range(total_pixels):
            for q in range(m, n):
                hidden_bits += format(array[p][q], "#010b")[2:][-4:]
        h_bits = []
        index = 0
        print(len(hidden_bits))
        for i in range(0, len(hidden_bits), 8):
            h_bits.append(hidden_bits[i:i + 8])
            index += 1
        message = ""
        for i in range(len(h_bits)):
            if message[-5:] == "$t3g0":
                self.bpp = (i*8)/total_pixels
                break
            else:
                message += chr(int(h_bits[i], 2))
        bits_in_total_pixels = total_pixels * 12  # total pixels multiplied by total number of bits per pixel for stego 4
        self.number_of_characters = bits_in_total_pixels/8  # bits_in_total_pixels divided by total bits per character

        if "$t3g0" in message:
            print("Hidden Message:", message[:-5])
            return message[:-5]
        else:
            print("No Hidden Message Found")
        return False

    def get_bpp(self):
        return self.bpp

    def get_number_of_characters(self):
        return self.number_of_characters
