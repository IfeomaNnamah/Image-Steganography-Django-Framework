from PIL import Image
import math


class IPSNR8bit():
    def count_MSE(self, original_img, stego_img):
        img 	= Image.open(original_img)
        stega	= Image.open(stego_img)

        img 	= img.getdata()
        stega	= stega.getdata()

        MSE 	= 0

        width, height = img.size

        len_img = len(img)
        for i in range(len_img):
            img_pix		= (img[i])
            stega_pix	= (stega[i])

            MSE 		+= math.pow((stega_pix - img_pix), 2)

        MSE /= (width*height)

        return MSE

    def count_psnr(self, original_img, stego_img):
        PSNR = 0
        MSE  = self.count_MSE(original_img, stego_img)

        PSNR = 10 * math.log10((math.pow(255, 2)) / MSE)

        return PSNR