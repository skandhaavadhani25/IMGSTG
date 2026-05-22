from django.shortcuts import render,redirect
from django.contrib.auth.models import User,auth 
from django.http import HttpResponseRedirect
import stepic
from PIL import Image # importing the Image module from the PIL library.
import io
import cv2
import stepic
from PIL import Image
import numpy as np
import io
from django.shortcuts import render
import os
import wave
from pydub import AudioSegment
# Create your views here.
from cryptography.fernet import Fernet
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
import base64
import pickle
import tempfile
from scipy.io import wavfile
import re
import shelve
from django.core.files.storage import default_storage
from django.core.files.base import ContentFile


import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
import random


def index(request):
    return render(request,"index.html")

def application(request):
    return render(request,"application.html")

def about(request):
    return render(request,"about.html")

def overview(request):
    return render(request,"overview.html")

def key(request):
    return render(request,"key.html")

def contacts(request):
    return render(request,"contacts.html")

def option(request):
    return render(request,"option.html")

def option2(request):
    return render(request,"option2.html")


def login(request):
    if request.method=="POST":
        un=request.POST['uname']
        pd=request.POST['psw']
        
        user=auth.authenticate(username=un,password=pd)
        if user is not None:
            auth.login(request,user)
            return redirect('/')
        else:
            return render(request,"login.html")
    return render(request,"login.html")

def hide_text_in_image(image, text):
    data = text.encode('utf-8')
    '''encode('utf-8') on a string, it translates the human-readable 
    characters into a sequence of bytes using the UTF-8 encoding.
     The result is a bytes object in Python.'''
    return stepic.encode(image, data)
#stepic.encode method is called to hide these bytes within the image

def encryption_view(request):
    message = ''
    if request.method == 'POST':
        text = request.POST['text']
        image_file = request.FILES['image']
        image = Image.open(image_file)

        # Convert to PNG if not already in that format
        if image.format != 'PNG':  # checks whether the image format is not PNG.
            image = image.convert('RGBA')
            # image is converted to RGBA mode if it's not already
            # This ensures the image has the correct color channels.
            buffer = io.BytesIO()
            # A BytesIO object is created,
            # which is a binary stream (an in-memory bytes buffer).
            image.save(buffer, format="PNG")
            image = Image.open(buffer)

        # hide text in image
        new_image = hide_text_in_image(image, text)

        # save the new image in a project folder
        image_path = 'encrypted_images/' + 'new_' + image_file.name
        new_image.save(image_path, format="PNG")

        message = 'Text has been encrypted in the image.'


    return render(request, 'encryption.html', {'message': message})

    

def decryption_view(request):
    text = ''
    if request.method == 'POST':
        image_file = request.FILES['image']
        image = Image.open(image_file)

        # Convert to PNG if not already in that format
        if image.format != 'PNG':#checks whether the image format is not PNG.
            image = image.convert('RGBA')
            #image is converted to RGBA mode if it's not already
            #This ensures the image has the correct color channels.
            buffer = io.BytesIO()
            #A BytesIO object is created,
            # which is a binary stream (an in-memory bytes buffer).
            image.save(buffer, format="PNG")
            image = Image.open(buffer)

        # extract text from image
        text = extract_text_from_image(image)

    return render(request, 'decryption.html', {'text': text})


def extract_text_from_image(image):
    data = stepic.decode(image)
    # uses the decode function from the stepic library to extract the
    # hidden data from the given image. This hidden data is
    # typically stored as bytes.
    if isinstance(data, bytes):
        return data.decode('utf-8')
    return data



def register(request):
    if request.method=="POST":
        un=request.POST['uname']
        em=request.POST['email']
        pd=request.POST['psw']
        cp=request.POST['cpsw']
        
        #Create database connection
        user=User.objects.create_user(username=un,email=em,password=pd,)
        user.save()
        return HttpResponseRedirect('login')
    else:
        return render(request,"register.html")
    return render(request,"register.html")

def logout(request):
    auth.logout(request)
    return HttpResponseRedirect('/')

def AES(request):
    return render(request,"AES.html")



def ensure_directory_exists(directory):
    """Ensure the specified directory exists"""
    if not os.path.exists(directory):
        os.makedirs(directory)

def vencryption_view(request):
    message = ''
    if request.method == 'POST':
        text = request.POST.get('text', '')
        password="qwertyuiopasdfghjklzxcvbnm"
        if 'video' in request.FILES:
            video_file = request.FILES['video']
        #output_video = "C:/Users/Abhiram K R/Downloads/creatine_encrypted.avi"
        output_video = r"C:\Users\Admin\Desktop\IMGSTG\encrypted_videos\encypt.avi"
        steganography = VideoSteganography()
        message1 = steganography.encrypt_into_video(video_file, output_video, text, password, frame_index=10)
        if message1==True:
            message = 'Text has been encrypted in the video.'
            return render(request, 'vencryption.html', {
                'message': message,
            })
        else:
            message = 'Error encrypting the video.'
    else:
        message = 'Please upload a video file.'
    
    return render(request, 'vencryption.html', {'message': message})


def vdecryption_view(request):
    text = ''
    error = ''
    
    if request.method == 'POST':
        if 'video' in request.FILES:
            video_file = request.FILES['video']
            steganography = VideoSteganography()
            password = "qwertyuiopasdfghjklzxcvbnm"
            try:
                output_video = video_file
                decrypted_text = steganography.decrypt_from_video(output_video, password)
                text=decrypted_text
                error=True
            except:
                text="error in decoding the text"
                error=False

    return render(request, 'vdecryption.html', {'text': text, 'error': error})


def decrypt_text_from_video(video_path):
    try:
        # Open the video file
        cap = cv2.VideoCapture(video_path)
        if not cap.isOpened():
            return "Error opening video file", False
        
        # Read the first frame
        ret, frame = cap.read()
        if not ret:
            return "Error reading video frame", False
        
        # Convert frame to PIL Image for steganography
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        pil_image = Image.fromarray(rgb_frame)
        
        # Decode the hidden text
        try:
            data = stepic.decode(pil_image)
            
            if isinstance(data, bytes):
                text = data.decode('utf-8')
                # Check for marker and remove it
                if text.startswith("STEGO:"):
                    return text[6:], True
                return text, True
            elif data:
                text = str(data)
                # Check for marker and remove it
                if text.startswith("STEGO:"):
                    return text[6:], True
                return text, True
            else:
                return "No hidden data found in video", False
        except Exception as e:
            return f"Error decoding data: {str(e)}", False
        finally:
            cap.release()
    except Exception as e:
        return f"Decryption error: {str(e)}", False
#--------------------------------------------------------------------------
def aencryption(request):
    return render(request,"aencryption.html")

def adecryption(request):
    return render(request,"adecryption.html")



#---------------------------------------------------------------------------------------------------------

def mp3_to_wav(mp3_path, wav_path):
    audio = AudioSegment.from_mp3(mp3_path)
    audio = audio.set_channels(1).set_sample_width(2)  # Mono, 16-bit
    audio.export(wav_path, format="wav")

def wav_to_mp3(wav_path, mp3_path):
    audio = AudioSegment.from_wav(wav_path)
    audio.export(mp3_path, format="mp3")

def xor_encrypt_decrypt(data: str, key: str) -> str:
    return ''.join(chr(ord(c) ^ ord(key[i % len(key)])) for i, c in enumerate(data))

def embed_text_into_audio(audio_path, output_path, text, key):
    rate, data = wavfile.read(audio_path)
    if data.ndim > 1:
        data = data[:, 0]

    encrypted_text = xor_encrypt_decrypt(text, key)
    binary_data = ''.join(f"{ord(c):08b}" for c in encrypted_text)
    data_flat = data.copy().astype(np.int32)

    if len(binary_data) > len(data_flat):
        raise ValueError("Audio file is too short to hold the message.")

    for i in range(len(binary_data)):
        data_flat[i] = (data_flat[i] & ~1) | int(binary_data[i])

    wavfile.write(output_path, rate, data_flat.astype(np.int16))
    print(f"Text embedded successfully into {output_path}")

def extract_text_from_audio(audio_path, key, text_length):
    rate, data = wavfile.read(audio_path)
    if data.ndim > 1:
        data = data[:, 0]

    data = data.astype(np.int32)
    bits = [str(data[i] & 1) for i in range(text_length * 8)]
    chars = [chr(int(''.join(bits[i:i+8]), 2)) for i in range(0, len(bits), 8)]
    decrypted_text = xor_encrypt_decrypt(''.join(chars), key)

    return decrypted_text

# Aencryption view
def aencryption_view(request):
    import tempfile
    message = ''
    if request.method == 'POST':
        text = request.POST['text']
        audio_file = request.FILES['audio']
        try:
            with shelve.open("storage") as db:
                db["length"] = len(text)
            # Save uploaded file to a temporary location
            temp_mp3_path = tempfile.NamedTemporaryFile(delete=False, suffix=".mp3").name
            with open(temp_mp3_path, 'wb') as f:
                f.write(audio_file.read())

            wav_temp = r"encrypted_audio/temp.wav"
            stego_wav = r"encrypted_audio/stego.wav"
            stego_mp3 = r"encrypted_audio/output.mp3"
            secret_text = text
            key = "key"
            # Step 1: Convert MP3 to WAV
            mp3_to_wav(temp_mp3_path, wav_temp)

            # Step 2: Embed secret into WAV
            embed_text_into_audio(wav_temp, stego_wav, secret_text, key)

            # Step 3: (Optional) Convert stego WAV back to MP3
            wav_to_mp3(stego_wav, stego_mp3)
            # Hide text in audio
            message = 'Text has been encrypted in the audio file.'
        except:
            message = 'Failed to encrypt in the audio file.'
    
    return render(request, 'aencryption.html', {'message': message})


# Decryption view
def adecryption_view(request):
    text = ''
    if request.method == 'POST':
        audio_file = request.FILES['audio']
        key = "key"
        stego_wav = r"encrypted_audio/stego.wav"
        try:
            with shelve.open("storage") as db:
                text_length = db["length"]
            extracted = extract_text_from_audio(stego_wav, key, text_length)
            text = extracted
            #text = extract_initial_meaningful_text(text)
        except:
            text = "error while decoding the audio"
    return render(request, 'adecryption.html', {'text': text})

def extract_initial_meaningful_text(s):
    match = re.match(r"^[a-yA-Y0-9]+", s)  
    return match.group() if match else ""


#-----------------------------------------------------------------------------
#-----------------------------------------------------------------------------
class VideoSteganography:
    def __init__(self):
        self.salt = os.urandom(16)  # Random salt for encryption key
    
    def _generate_key(self, password):
        """Generate encryption key from password"""
        password = password.encode()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=self.salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        return key
     
    def _encrypt_text(self, text, password):
        """Encrypt the text using the password"""
        key = self._generate_key(password)
        f = Fernet(key)
        encrypted_text = f.encrypt(text.encode())
        return encrypted_text
    
    def _decrypt_text(self, encrypted_text, password, salt):
        """Decrypt the text using the password and salt"""
        password = password.encode()
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=100000,
        )
        key = base64.urlsafe_b64encode(kdf.derive(password))
        f = Fernet(key)
        decrypted_text = f.decrypt(encrypted_text).decode()
        return decrypted_text
    
    def encrypt_into_video(self, input_video, output_video_path, text, password, frame_index=10):
        """
        Encrypt text into a video file and save metadata separately
        
        Args:
            input_video_path: Path to the input video
            output_video_path: Path to save the output video
            text: Text to encrypt
            password: Password to encrypt the text
            frame_index: Frame index to embed the data (default: 10, to avoid first frame)
        """
        try:
            status=True

            with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file:
                for chunk in input_video.chunks():
                    temp_file.write(chunk)
                temp_file_path = temp_file.name
            # Open the video
            cap = cv2.VideoCapture(temp_file_path)
            if not cap.isOpened():
                raise ValueError("Could not open the video file")
            
            # Get video properties
            width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
            height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
            fps = cap.get(cv2.CAP_PROP_FPS)
            total_frames = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
            
            # Check if the video has enough frames
            if frame_index >= total_frames:
                raise ValueError(f"Video has only {total_frames} frames, but frame index {frame_index} was specified")
            
            # Set up the video writer - use a lossless codec
            # This is key to prevent compression from destroying the embedded data
            fourcc = cv2.VideoWriter_fourcc(*'MJPG')  # Motion JPEG codec
            out = cv2.VideoWriter(output_video_path, fourcc, fps, (width, height))
            
            # Encrypt the text
            encrypted_text = self._encrypt_text(text, password)
            
            # Create metadata dictionary
            metadata = {
                "salt": self.salt,
                "encrypted_text": encrypted_text,
                "frame_index": frame_index
            }
            
            # Save metadata separately
            metadata_path = f"{output_video_path}.data"
            with open(metadata_path, 'wb') as f:
                pickle.dump(metadata, f)
            
            # Process frames
            frame_count = 0
            while True:
                ret, frame = cap.read()
                if not ret:
                    break
                
                # Mark the special frame (optional, for visual reference only)
                if frame_count == frame_index:
                    # Add a small invisible marker in the corner
                    frame[0:5, 0:5, 0] = (frame[0:5, 0:5, 0] & 254) | 1
                
                # Write the frame
                out.write(frame)
                frame_count += 1
            
            # Release resources
            cap.release()
            out.release()
            
            print(f"Text successfully encrypted into {output_video_path}")
            print(f"Metadata saved to {metadata_path}")
            print(f"IMPORTANT: Keep the .data file alongside the video file for decryption")
        except:
            status=False
        return status
    
    def decrypt_from_video(self, video_file, password):
    
    # Create a temporary file to store the uploaded video
        with tempfile.NamedTemporaryFile(delete=False, suffix='.mp4') as temp_file:
            for chunk in video_file.chunks():
                temp_file.write(chunk)
            temp_file_path = temp_file.name
        
        try:
            # We need to find the metadata file
            # Since we're working with an uploaded file, we need to look at the original filename
            original_name = video_file.name
            
            # Extract filename without extension
            filename_base = os.path.splitext(original_name)[0]
            
            metadata_dir = r"C:\Users\Admin\Desktop\IMGSTG\encrypted_videos"
            potential_metadata_paths = [
            f"{metadata_dir}\encypt.avi.data",  # Direct path to the data file shown in screenshot
            os.path.join(metadata_dir, f"{filename_base}.data"),
            os.path.join(metadata_dir, f"encrypted_{filename_base}.data")
        ]
            
            # Try to find metadata file
            metadata_path = None
            metadata = None
            
            for path in potential_metadata_paths:
                try:
                    with open(path, 'rb') as f:
                        metadata = pickle.load(f)
                        metadata_path = path
                        break
                except (FileNotFoundError, IOError):
                    continue
            
            if metadata is None:
                raise ValueError("No metadata file found. Cannot decrypt without the metadata file.")
            
            # Extract metadata
            salt = metadata["salt"]
            encrypted_text = metadata["encrypted_text"]
            
            # Decrypt the text
            decrypted_text = self._decrypt_text(encrypted_text, password, salt)
            
            return decrypted_text
        
        except Exception as e:
            raise ValueError(f"Error decrypting video: {str(e)}")




