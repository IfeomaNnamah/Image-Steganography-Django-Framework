import mimetypes
from wsgiref.util import FileWrapper

from django.contrib.auth import authenticate, login, logout
from django.http import HttpResponse, JsonResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.conf import settings
from django.contrib import messages
from django.core.files import File
import os
import time
from django.utils.encoding import smart_str
from cryptography.fernet import Fernet
from .lsb import LSB
from .lsb8bit import LSB8bit
from .ipsnr import IPSNR
from .ipsnr8bit import IPSNR8bit

from .forms import ShareStegoImageForm, CreateUserForm
from .models import ShareImage, verifykey

# Create your views here.


def p_encode(request):
    user = request.user.username
    mails = ShareImage.objects.filter(recipient_username=user)
    mailcount = mails.count()
    title_page = 'Encode'
    return render(request, 'app/encode.html', {'title_page': title_page, 'mailcount': mailcount})


def p_decode(request):
    user = request.user.username
    mails = ShareImage.objects.filter(recipient_username=user)
    mailcount = mails.count()
    title_page = 'Decode'
    return render(request, 'app/decode.html', {'title_page': title_page, 'mailcount': mailcount})


def index(request):
    title_page = 'Home'
    user = request.user.username
    mails = ShareImage.objects.filter(recipient_username=user)
    mailcount = mails.count()
    return render(request, 'app/index.html', {'title_page': title_page, 'mailcount': mailcount})


def login_page(request):
    user = request.user.username
    mails = ShareImage.objects.filter(recipient_username=user)
    mailcount = mails.count()
    if request.method == 'POST':
        username = request.POST.get("username")
        password = request.POST.get("password")

        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return render(request, 'app/index.html', {})
        else:
            messages.info(request, 'invalid username or password')

    return render(request, 'app/login.html', {'mailcount':mailcount})


def register(request):
    form = CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            form.save()
            user = form.cleaned_data.get("username")
            messages.success(request, 'Account has been created for ' + user)
            form = CreateUserForm()

    context = {
        'form': form
    }
    return render(request, 'app/register.html', context)


def logout_page(request):
    user = request.user.username
    mails = ShareImage.objects.filter(recipient_username=user)
    mailcount = mails.count()
    logout(request)
    return render(request, 'app/login.html', {'mailcount': mailcount})


def sharestegoimage(request):
    user = request.user.username
    mails = ShareImage.objects.filter(recipient_username=user)
    mailcount = mails.count()
    form = ShareStegoImageForm()
    submitted_form = ShareStegoImageForm(request.POST, request.FILES)
    if submitted_form.is_valid():
        submitted_form.save()
        form = ShareStegoImageForm() #refresh
        return render(request, 'app/index.html', {})
    context = {
        'form': form,
        'mailcount': mailcount
    }
    return render(request, 'app/sharestegoimage.html', context)


def mail_view(request):
    user = request.user.username
    mails = ShareImage.objects.filter(recipient_username=user)
    mailcount = mails.count()
    context = {
        "mails": mails,
        'mailcount': mailcount
    }
    return render(request, "app/mails.html", context)


def download(request, id=id):
    obj = ShareImage.objects.get(id=id)
    cur_image = obj.photo.url[7:]
    file_name = cur_image
    file_path = os.path.join(settings.MEDIA_ROOT,file_name)
    file_wrapper = FileWrapper(open(file_path,'rb'))
    file_mimetype = mimetypes.guess_type(file_path)
    response = HttpResponse(file_wrapper, content_type=file_mimetype)
    response['X-Sendfile'] = file_path
    response['Content-Length'] = os.stat(file_path).st_size
    response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(file_name)
    return response


def checkecondefile(request):
    if request.is_ajax and request.method == "GET":
        imagetoencode = request.GET.get("imagetoencode", None)
        stego_bit = request.GET.get("stegoBit", None)

        imagetoencode = imagetoencode.split('.')  # result is in an array
        imagetoencode_fe = imagetoencode[0]  # first element of the array without .jpg or .png
        # check for the filename in the database.
        if verifykey.objects.filter(photo_title=imagetoencode_fe + stego_bit).exists():
            return JsonResponse({"valid": False}, status=200)
        else:
            return JsonResponse({"valid": True}, status=200)

    return JsonResponse({}, status=400)


def encode(request):
    title_page = "result"
    result = "No images and text was entered"
    data = False
    if request.method == 'POST':
        msg = request.POST['pesan']
        stegokey = request.POST['stegokey']

        imagetoencode = request.FILES['img']
        imagetoencode = imagetoencode.name.split('.')  # result is in an array
        imagetoencode_fe = imagetoencode[0]  # first element of the array without .jpg or .png
        imagetoencode_format = imagetoencode[1] # file format
        print(request.POST['bit_type'])

        if imagetoencode_format == "gif":
            if request.POST['bit_type'] == 'encodelsb':
                folderimg = 'imgforlsb'
                uploaded_filename = handle_upload_file(request.FILES['img'], folderimg)
                lsb = LSB8bit()  # create object from LSB class
                destination = os.path.join(settings.MEDIA_ROOT, folderimg, uploaded_filename)
                data = lsb.embed_msg(uploaded_filename, msg, destination)
                filename = uploaded_filename[51:]
                if data:  # insert message into picture
                    bitnum = "1"
                    savestegokey(stegokey, imagetoencode_fe, bitnum)
                    result = "Message Encoded Successfully"

            elif request.POST['bit_type'] == 'stego2bitencodelsb':
                folderimg = 'stego2bitlsb'
                uploaded_filename = handle_upload_file(request.FILES['img'], folderimg)
                lsb = LSB8bit()  # create object from LSB class
                destination = os.path.join(settings.MEDIA_ROOT, folderimg, uploaded_filename)
                data = lsb.embed_msg_stego2bit(uploaded_filename, msg, destination)
                filename = uploaded_filename[54:]
                if data:  # insert message into picture
                    bitnum = "2"
                    savestegokey(stegokey, imagetoencode_fe, bitnum)
                    result = "Message Encoded Successfully"

            elif request.POST['bit_type'] == 'stego3bitencodelsb':
                start_time = time.time()
                folderimg = 'stego3bitlsb'
                uploaded_filename = handle_upload_file(request.FILES['img'], folderimg)
                lsb = LSB8bit()  # create object from LSB class
                destination = os.path.join(settings.MEDIA_ROOT, folderimg, uploaded_filename)
                data = lsb.embed_msg_stego3bit(uploaded_filename, msg, destination)
                # filename = uploaded_filename[54:]
                if data:  # insert message into picture
                    bitnum = "3"
                    savestegokey(stegokey, imagetoencode_fe, bitnum)
                    result = "Message Encoded Successfully"

            elif request.POST['bit_type'] == 'stego4bitencodelsb':
                folderimg = 'stego4bitlsb'
                uploaded_filename = handle_upload_file(request.FILES['img'], folderimg)
                lsb = LSB8bit()  # create object from LSB class
                destination = os.path.join(settings.MEDIA_ROOT, folderimg, uploaded_filename)
                data = lsb.embed_msg_stego4bit(uploaded_filename, msg, destination)
                # filename = uploaded_filename[54:]
                if data:  # insert message into picture
                    bitnum = "4"
                    savestegokey(stegokey, imagetoencode_fe, bitnum)
                    result = "Message Encoded Successfully"
            else:
                result = "Failed to enter message, picture type does not match"

            return render(request, 'app/encode.html', {'title_page': title_page, 'result': result, 'data': data})
        else:
            # if 'encodelsb' in request.POST:
            if request.POST['bit_type'] == 'encodelsb':
                uploaded_filename = handle_upload_file(request.FILES['img'], 'imgforlsb')
                folderimg = 'imgforlsb'
                lsb = LSB()  # create object from LSB class
                destination = os.path.join(settings.MEDIA_ROOT, folderimg, uploaded_filename)
                data = lsb.embed_msg(uploaded_filename, msg, destination)

                if data:  # insert message into picture
                    # save stego key in database
                    bitnum = "1"
                    savestegokey(stegokey, imagetoencode_fe, bitnum)
                    result = "Message Encoded Successfully"
                else:
                    result = "Failed to enter message, picture type does not match"

            elif request.POST['bit_type'] == 'stego2bitencodelsb':
                start_time = time.time()
                folderimg = 'stego2bitlsb'
                uploaded_filename = handle_upload_file(request.FILES['img'], folderimg)
                lsb = LSB()  # create object from LSB class
                destination = os.path.join(settings.MEDIA_ROOT, folderimg, uploaded_filename)
                data = lsb.embed_msg_stego2bit(uploaded_filename, msg, destination)

                if data:  # insert message into picture
                    # save stego key in database
                    bitnum = "2"
                    savestegokey(stegokey, imagetoencode_fe, bitnum)
                    result = "Message Encoded Successfully"
                else:
                    result = "Failed to enter message, picture type does not match"

            elif request.POST['bit_type'] == 'stego3bitencodelsb':
                start_time = time.time()
                folderimg = 'stego3bitlsb'
                uploaded_filename = handle_upload_file(request.FILES['img'], folderimg)
                lsb = LSB()  # create object from LSB class
                destination = os.path.join(settings.MEDIA_ROOT, folderimg, uploaded_filename)
                data = lsb.embed_msg_stego3bit(uploaded_filename, msg, destination)
                if data:  # insert message into picture
                    # save stego key in database
                    bitnum = "3"
                    savestegokey(stegokey, imagetoencode_fe, bitnum)
                    result = "Message Encoded Successfully"
                else:
                    result = "Failed to enter message, picture type does not match"

            elif request.POST['bit_type'] == 'stego4bitencodelsb':
                start_time = time.time()
                folderimg = 'stego4bitlsb'
                uploaded_filename = handle_upload_file(request.FILES['img'], folderimg)
                lsb = LSB()  # create object from LSB class
                destination = os.path.join(settings.MEDIA_ROOT, folderimg, uploaded_filename)
                data = lsb.embed_msg_stego4bit(uploaded_filename, msg, destination)

                if data:  # insert message into picture
                    # save stego key in database
                    bitnum = "4"
                    savestegokey(stegokey, imagetoencode_fe, bitnum)
                    result = "Message Encoded Successfully"
                else:
                    result = "Failed to enter message, picture type does not match"

            else:
                result = "Failed to encrypt message, picture type does not match." \
                             " Please choose another file to encrypt message"
        return render(request, 'app/encode.html', {'title_page' : title_page, 'result': result})


def decode(request):
    title_page 	= "Decode"
    result 		= "seems you are not entering any images"
    message = ''
    val_psnr	= 0
    folderimg	= ''

    if request.method == 'POST':
        uploaded_filename = request.FILES['img']
        dstegokey = request.POST['dstegokey']

        splitted_filename = uploaded_filename.name.split('.') # result is in an array
        splitted_filename_firstelement = splitted_filename[0]
        splitted_filename_format = splitted_filename[1]# first element of the array without .jpg or .png

        p_title = ""
        if request.POST['bit_type'] == 'decodelsb':
            p_title = uploaded_filename.name[:-8] + "1"
        elif request.POST['bit_type'] == 'stego2bitdecodelsb':
            p_title = uploaded_filename.name[:-8] + "2"
        elif request.POST['bit_type'] == 'stego3bitdecodelsb':
            p_title = uploaded_filename.name[:-8] + "3"
        elif request.POST['bit_type'] == 'stego4bitdecodelsb':
            p_title = uploaded_filename.name[:-8] + "4"

        try:
            obj = verifykey.objects.get(photo_title=p_title)
        except:
            return render(request, 'app/decode.html', {
                'result'	: "Invalid stego key. It may seem that this message isn't for you.",
            })
        key = b'BLEXlEdEGsRrzL4vFmEms0f0_dEMeA7QGLRNrnC5qBc='
        cipher_suite = Fernet(key)
        unciphered_text = (cipher_suite.decrypt(obj.stegokey.encode()))

        if unciphered_text.decode() != dstegokey:
            return render(request, 'app/decode.html', {
                'result'		: "Invalid stego key. It may seem that this message isn't for you.",
            })
        else:
            if splitted_filename_format == "gif":
                if request.POST['bit_type'] == 'decodelsb':
                    folderimg = 'imgforlsb'
                    lsb = LSB8bit() # create object from LSB8bit class
                    message = lsb.extract_msg(uploaded_filename)
                elif request.POST['bit_type'] == 'stego2bitdecodelsb':
                    folderimg = 'stego2bitlsb'
                    lsb = LSB8bit() # create object from LSB8bit class
                    message = lsb.extract_msg_stego2bit(uploaded_filename)
                elif request.POST['bit_type'] == 'stego3bitdecodelsb':
                    folderimg = 'stego3bitlsb'
                    lsb = LSB8bit() # create object from LSB8bit class
                    message = lsb.extract_msg_stego3bit(uploaded_filename)
                elif request.POST['bit_type'] == 'stego4bitdecodelsb':
                    folderimg = 'stego4bitlsb'
                    lsb = LSB8bit() # create object from LSB8bit class
                    message = lsb.extract_msg_stego4bit(uploaded_filename)
            else:
                if request.POST['bit_type'] == 'decodelsb':
                    start_time = time.time()
                    folderimg = 'imgforlsb'
                    lsb = LSB() # create object from LSB class
                    message = lsb.extract_msg(uploaded_filename)

                elif request.POST['bit_type'] == 'stego2bitdecodelsb':
                    start_time = time.time()
                    folderimg = 'stego2bitlsb'
                    lsb = LSB() # create object from LSB class
                    message = lsb.extract_msg_stego2bit(uploaded_filename)

                elif request.POST['bit_type'] == 'stego3bitdecodelsb':
                    start_time = time.time()
                    folderimg = 'stego3bitlsb'
                    lsb = LSB() # create object from LSB class
                    message = lsb.extract_msg_stego3bit(uploaded_filename)

                elif request.POST['bit_type'] == 'stego4bitdecodelsb':
                    start_time = time.time()
                    folderimg = 'stego4bitlsb'
                    lsb = LSB() # create object from LSB class
                    message = lsb.extract_msg_stego4bit(uploaded_filename)
            if not result:
                result = "picture type does not match, failed to extract message"
            else:
                stego_img = os.path.join(settings.MEDIA_ROOT, folderimg, uploaded_filename.name)
                temp = uploaded_filename.name.split('.')
                original_img = temp[0][:-4] + "." + temp[1]
                original_img = os.path.join(settings.MEDIA_ROOT, folderimg, original_img)
                # stego_image_size = os.path.getsize(stego_img)
                # original_image_size = os.path.getsize(original_img)
                stego_image_size = os.stat(stego_img).st_size
                original_image_size = os.stat(original_img).st_size
                img_format = uploaded_filename.name.split('.')[1]
                # enc_time = time.time() - start_time
                bpp_value = lsb.get_bpp()
                total_number_of_characters = lsb.get_number_of_characters()
                result = ""

                if splitted_filename_format != "gif":
                    psnr = IPSNR()
                    val_psnr = psnr.count_psnr(original_img, stego_img) # calculate psnr value
                    val_mse = psnr.count_MSE(original_img, stego_img) # calculate mse value
                else:
                    psnr = IPSNR8bit()
                    val_psnr = psnr.count_psnr(original_img, stego_img)  # calculate psnr value
                    val_mse = psnr.count_MSE(original_img, stego_img)  # calculate mse value

            return render(request, 'app/decode.html', {
                'title_page': title_page,
                'result': result,
                'message': message.strip(),
                'psnr': val_psnr,
                'mse': val_mse,
                'stego_image_size': stego_image_size,
                'original_image_size': original_image_size,
                'bpp_value': bpp_value,
                'total_number_of_characters': total_number_of_characters,
                'format': img_format,
                'filename': uploaded_filename.name[:-8],
                })

    return render(request, 'app/decode.html', {
    'title_page' 	: title_page,
    'result'		: result,
    })


def savestegokey(stegokey, imagetoencode_fe, bit_type):
    photo_title = imagetoencode_fe + bit_type
    # save stego key in database
    obj = verifykey()
    try:
        obj = verifykey.objects.get(photo_title=photo_title)
        key = b'BLEXlEdEGsRrzL4vFmEms0f0_dEMeA7QGLRNrnC5qBc='
        cipher_suite = Fernet(key)
        ciphered_text = cipher_suite.encrypt(stegokey.encode())
        obj.stegokey = ciphered_text.decode()
        obj.save()
    except:
        obj.photo_title = imagetoencode_fe + bit_type
        key = b'BLEXlEdEGsRrzL4vFmEms0f0_dEMeA7QGLRNrnC5qBc='
        cipher_suite = Fernet(key)
        ciphered_text = cipher_suite.encrypt(stegokey.encode())
        obj.stegokey = ciphered_text.decode()
        obj.save()
    # download encrypted stego image
    # file_path = destination
    # file_wrapper = FileWrapper(open(file_path, 'rb'))
    # file_mimetype = mimetypes.guess_type(file_path)
    # response = HttpResponse(file_wrapper, content_type=file_mimetype)
    # response['X-Sendfile'] = file_path
    # response['Content-Length'] = os.stat(file_path).st_size
    # response['Content-Disposition'] = 'attachment; filename=%s' % smart_str(filename)
    # return response


def handle_upload_file(file, tofolder):
    # create the folder if it doesn't exist.
    try:
        os.mkdir(os.path.join(settings.MEDIA_ROOT, tofolder))
    except:
        pass

    # save original file
    original_img = os.path.join(settings.MEDIA_ROOT, tofolder, file.name) # save the uploaded file inside that folder.
    fout = open(original_img, 'wb+')

    # Iterate through the chunks.
    for chunk in file.chunks():
        fout.write(chunk)
    fout.close()

    # save stego images
    temp = file.name.split('.')

    full_filename = os.path.join(settings.MEDIA_ROOT, tofolder, temp[0] +"_out." +temp[1]) # save the uploaded file inside that folder.
    fout = open(full_filename, 'wb+')

    # Iterate through the chunks.
    for chunk in file.chunks():
        fout.write(chunk)
    fout.close()

    return full_filename
