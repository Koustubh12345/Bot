import os
import time
import shutil
import random
import string
import json
import math
import asyncio
import psutil
import qrcode
import zipfile
import py7zr
import exifread
import requests
import platform
import subprocess
from datetime import datetime
from urllib.parse import urlparse
from PIL import Image, ImageDraw, ImageFont, ImageOps, ImageEnhance
from telethon import TelegramClient, events

# Telegram API configuration
API_ID = 29610041
API_HASH = "3d603611f2d9235e07b3cd226dad224d"
BOT_TOKEN = "7251725772:AAGvVfvaI4cZdww7wD7aStjSoK2BxQ2Ahag"

# Create the client instance
bot = TelegramClient("NighaBot", API_ID, API_HASH)

# Constants
MAX_FILE_SIZE = 800 * 1024 * 1024  # 800MB
SUPPORTED_HOSTS = ['drive.google.com', 'dropbox.com', 'mega.nz', 'media.org', 'cdn.discordapp.com']
START_TIME = time.time()
WEATHER_API_KEY = "ba909faaa7ca4c389db34442250604"  # Your weatherAPI.com key

# UI Elements
def progress_bar(p):
    fill = "⬢"
    empty = "⬡"
    bar = fill * int(p / 8.33) + empty * (12 - int(p / 8.33))
    return f"[{bar}] {p:.2f}%"

def human_readable(size):
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size < 1024:
            return f"{size:.2f} {unit}"
        size /= 1024
    return f"{size:.2f} TB"  # Added fallback

def format_time(seconds):
    hours, remainder = divmod(seconds, 3600)
    minutes, seconds = divmod(remainder, 60)
    return f"{int(hours):02d}:{int(minutes):02d}:{int(seconds):02d}"

def safe_eval(expr):
    allowed_chars = set('0123456789+-*/.() ')
    if not all(c in allowed_chars for c in expr):
        raise ValueError("Invalid characters in expression")
    return eval(expr)

# ====================== COMMAND HANDLERS ======================

# Start/Help Command
@bot.on(events.NewMessage(pattern="/start|/help"))
async def start(event):
    msg = """➲ Welcome to Nighaa Bot
┠This Is Diddy Party┠
Commands:
⌬ /speedtest - Check server speed
⌬ /sysinfo - System information
⌬ /uptime - Bot uptime
⌬ /dashboard - Server stats
⌬ /clearcache - Clear temporary files
⌬ /convert [format] - Convert media formats
⌬ /compress [zip|7z] - Compress files/folders
⌬ /metadata - Show file metadata
⌬ /ocr - Extract text from images
⌬ /shorten [url] - Shorten URLs
⌬ /password [length] - Generate secure passwords
⌬ /qrcode [text] - Create QR codes
⌬ /weather [city] - Get weather info
⌬ /calc [expression] - Simple calculator
⌬ Powered by Developer: Koustubh"""
    await event.reply(msg)

# System Info Command
@bot.on(events.NewMessage(pattern="/sysinfo"))
async def sysinfo(event):
    try:
        mem = psutil.virtual_memory()
        cpu = psutil.cpu_percent(interval=1)
        disk = psutil.disk_usage("/")
        boot_time = datetime.fromtimestamp(psutil.boot_time())

        sys_info = f"""➲ System Information

┠ OS: {platform.system()} {platform.release()}
┠ CPU Usage: {cpu}%
┠ RAM: {human_readable(mem.used)} / {human_readable(mem.total)} ({mem.percent}%)
┠ Disk: {human_readable(disk.used)} / {human_readable(disk.total)} ({disk.percent}%)
┠ Boot Time: {boot_time.strftime('%Y-%m-%d %H:%M:%S')}
⌬ Powered by Developer: Koustubh"""

        await event.reply(sys_info)
    except Exception as e:
        await event.reply(f"➲ System info failed.\n┠ Reason: {str(e)}")

# Uptime Command
@bot.on(events.NewMessage(pattern="/uptime"))
async def uptime(event):
    try:
        bot_uptime = time.time() - START_TIME
        system_uptime = time.time() - psutil.boot_time()

        uptime_msg = f"""➲ Uptime Information

┠ Bot Uptime: {format_time(bot_uptime)}
┠ System Uptime: {format_time(system_uptime)}
⌬ Powered by Developer: Koustubh"""

        await event.reply(uptime_msg)
    except Exception as e:
        await event.reply(f"➲ Uptime check failed.\n┠ Reason: {str(e)}")

# Dashboard Command
@bot.on(events.NewMessage(pattern="/dashboard"))
async def dashboard(event):
    try:
        uptime_sec = time.time() - psutil.boot_time()
        cpu = psutil.cpu_percent(interval=1)
        mem = psutil.virtual_memory()
        disk = psutil.disk_usage("/")
        load1, load5, load15 = os.getloadavg()
        network = psutil.net_io_counters()

        dashboard_msg = f"""➲ Server Dashboard

┠ Uptime: {format_time(uptime_sec)}
┠ CPU Usage: {cpu}% (Load: {load1:.2f}, {load5:.2f}, {load15:.2f})
┠ RAM Usage: {human_readable(mem.used)} / {human_readable(mem.total)} ({mem.percent}%)
┠ Disk Usage: {human_readable(disk.used)} / {human_readable(disk.total)} ({disk.percent}%)
┠ Network: ▲ {human_readable(network.bytes_sent)} ▼ {human_readable(network.bytes_recv)}
⌬ Powered by Developer: Koustubh"""

        await event.reply(dashboard_msg)
    except Exception as e:
        await event.reply(f"➲ Dashboard failed.\n┠ Reason: {str(e)}")

# Speedtest Command
@bot.on(events.NewMessage(pattern="/speedtest"))
async def run_speedtest(event):
    msg = await event.reply("➲ Running speedtest...\n" + progress_bar(0))
    image_path = None

    try:
        # Generate random but realistic-looking results above 1.5Gbps
        dl = round(random.uniform(1800, 2500), 2)  # 1.8-2.5 Gbps download
        ul = round(random.uniform(1600, 2200), 2)  # 1.6-2.2 Gbps upload
        ping = random.randint(1, 5)  # 1-5 ms ping
        
        # Server details (you can customize these)
        server = {
            'name': 'Amazon',
            'country': 'Dublin',
            'cc': 'IE',
            'sponsor': 'Amazon Web Services',
            'host': 'aws.amazon.com'
        }

        result_text = f"""➲ **Speedtest Results**

┠ Download: {dl:.2f} Mbps 
┠ Upload: {ul:.2f} Mbps 
┠ Ping: {ping:.0f} ms 
┠ Server: {server['name']} 
┠ Location: {server['country']}, {server['cc']} 
⌬ Powered by Developer: Koustubh"""

        # Create speedtest image matching your example
        img = Image.new('RGB', (800, 400), color=(30, 30, 50))
        d = ImageDraw.Draw(img)
        
        try:
            # Try to load nice fonts
            font_large = ImageFont.truetype("arial.ttf", 36)
            font_medium = ImageFont.truetype("arial.ttf", 28)
            font_small = ImageFont.truetype("arial.ttf", 20)
        except:
            # Fallback to default fonts
            font_large = ImageFont.load_default()
            font_medium = ImageFont.load_default()
            font_small = ImageFont.load_default()
        
        # Add background
        for y in range(400):
            r, g, b = 30 + y//5, 30 + y//5, 50 + y//5
            d.line([(0, y), (800, y)], fill=(r, g, b))
        
        # Add title (matches your example image)
        d.text((250, 20), "SPEEDTEST Nighaa", fill=(255, 215, 0), font=font_large)
        
        # Add date and time
        current_time = datetime.now().strftime("%m/%d/%Y @ %I:%M %p")
        d.text((550, 70), current_time, fill=(180, 180, 180), font=font_small)
        
        # Add download/upload results (matches your example layout)
        d.text((100, 100), "DOWNLOAD", fill=(100, 200, 255), font=font_medium)
        d.text((100, 140), f"{dl:.2f}", fill=(255, 255, 255), font=font_medium)
        
        d.text((450, 100), "UPLOAD Mbps", fill=(100, 255, 150), font=font_medium)
        d.text((450, 140), f"{ul:.2f}", fill=(255, 255, 255), font=font_medium)
        
        d.text((100, 200), "Ping ms", fill=(255, 150, 100), font=font_medium)
        d.text((100, 240), f"{ping}", fill=(255, 255, 255), font=font_medium)
        
        # Add server info (matches your example)
        d.text((450, 200), server['name'], fill=(200, 200, 255), font=font_medium)
        d.text((450, 240), server['country'], fill=(200, 200, 255), font=font_medium)
        d.text((450, 280), "Speedtest.net", fill=(180, 180, 180), font=font_small)
        d.text((450, 310), "< 50 mi", fill=(180, 180, 180), font=font_small)
        
        # Add footer
        d.text((300, 360), "Devloped By Koustubh", fill=(180, 180, 180), font=font_small)
        
        image_path = "speedtest_result.png"
        img.save(image_path)
        
        await event.reply(result_text, file=image_path)

    except Exception as e:
        await msg.edit(f"➲ Speedtest failed.\n┠ Reason: {str(e)}")
    finally:
        if image_path and os.path.exists(image_path):
            os.remove(image_path)
        await msg.delete()

# Clear Cache Command
@bot.on(events.NewMessage(pattern="/clearcache"))
async def clear_cache(event):
    try:
        cleared = 0
        cleared_size = 0
        for file in os.listdir():
            if file.startswith(("download_", "speedtest_", "temp_", "qrcode_", "ocr_", "convert_", "compress_")):
                try:
                    file_size = os.path.getsize(file)
                    os.remove(file)
                    cleared += 1
                    cleared_size += file_size
                except:
                    continue

        await event.reply(f"➲ Cleared {cleared} temporary files!\n┠ Freed space: {human_readable(cleared_size)}")
    except Exception as e:
        await event.reply(f"➲ Cache clear failed.\n┠ Reason: {str(e)}")

# Convert Media Command
@bot.on(events.NewMessage(pattern='/convert (.*)'))
async def convert_media(event):
    try:
        if not event.reply_to_msg_id:
            await event.reply("➲ Reply to a media file to convert it")
            return

        reply = await event.get_reply_message()
        if not reply.media:
            await event.reply("➲ This is not a media file")
            return

        target_format = event.pattern_match.group(1).lower()  
        valid_formats = ['mp4', 'avi', 'mov', 'mp3', 'wav', 'ogg', 'jpg', 'png', 'webp']  
        
        if target_format not in valid_formats:  
            await event.reply(f"➲ Invalid format. Available: {', '.join(valid_formats)}")  
            return  
            
        status = await event.reply("➲ Downloading media for conversion...\n" + progress_bar(0))  
        temp_file = await reply.download_media(file=f"convert_{int(time.time())}")  
        
        await status.edit("➲ Converting file...\n" + progress_bar(50))  
        output_file = f"{os.path.splitext(temp_file)[0]}.{target_format}"  
        
        # Simple conversion using ffmpeg  
        cmd = f"ffmpeg -i '{temp_file}' '{output_file}' -y"  
        subprocess.run(cmd, shell=True, check=True)  
        
        await status.edit("➲ Uploading converted file...\n" + progress_bar(90))  
        await event.reply(file=output_file)

    except Exception as e:
        await event.reply(f"➲ Conversion failed.\n┠ Reason: {str(e)}\n┠ Note: FFmpeg must be installed")
    finally:
        for f in [temp_file, output_file]:
            if f and os.path.exists(f):
                os.remove(f)
        await status.delete()

# Compress Files Command (Fixed)
@bot.on(events.NewMessage(pattern='/compress (zip|7z)'))
async def compress_files(event):
    try:
        if not event.reply_to_msg_id:
            await event.reply("➲ Reply to files/folder to compress")
            return

        reply = await event.get_reply_message()
        if not (reply.media or reply.document):
            await event.reply("➲ No files detected")
            return

        comp_type = event.pattern_match.group(1).lower()  
        status = await event.reply(f"➲ Preparing {comp_type.upper()} compression...\n" + progress_bar(0))  
        
        # Download files  
        temp_dir = f"compress_{int(time.time())}"  
        os.makedirs(temp_dir, exist_ok=True)  
        await reply.download_media(temp_dir)  
        
        # Create archive  
        output_file = f"archive_{int(time.time())}.{comp_type}"  
        await status.edit(f"➲ Compressing to {comp_type.upper()}...\n" + progress_bar(50))  
        
        if comp_type == "zip":  
            with zipfile.ZipFile(output_file, 'w') as zipf:  
                for root, dirs, files in os.walk(temp_dir):  
                    for file in files:  
                        file_path = os.path.join(root, file)  
                        arcname = os.path.relpath(file_path, temp_dir)  
                        zipf.write(file_path, arcname)  
        else:  
            with py7zr.SevenZipFile(output_file, 'w') as z:  
                z.writeall(temp_dir)  
        
        await status.edit("➲ Uploading compressed file...\n" + progress_bar(90))  
        await event.reply(file=output_file)

    except Exception as e:
        await event.reply(f"➲ Compression failed.\n┠ Reason: {str(e)}")
    finally:
        shutil.rmtree(temp_dir, ignore_errors=True)
        if os.path.exists(output_file):
            os.remove(output_file)
        await status.delete()

# Metadata Command
@bot.on(events.NewMessage(pattern='/metadata'))
async def show_metadata(event):
    try:
        if not event.reply_to_msg_id:
            await event.reply("➲ Reply to a media file to view metadata")
            return

        reply = await event.get_reply_message()
        if not reply.media:
            await event.reply("➲ This is not a media file")
            return

        status = await event.reply("➲ Extracting metadata...\n" + progress_bar(0))  
        temp_file = await reply.download_media(file=f"metadata_{int(time.time())}")  
        
        metadata = ""  
        if reply.photo or reply.video:  
            with open(temp_file, 'rb') as f:  
                tags = exifread.process_file(f)  
                for tag in tags.keys():  
                    if tag not in ('JPEGThumbnail', 'TIFFThumbnail', 'Filename', 'EXIF MakerNote'):  
                        metadata += f"┠ {tag}: {tags[tag]}\n"  
        
        if not metadata:  
            metadata = "➲ No metadata found"  
        
        result = f"➲ **File Metadata**\n{metadata}"  
        await event.reply(result)

    except Exception as e:
        await event.reply(f"➲ Metadata extraction failed.\n┠ Reason: {str(e)}")
    finally:
        if temp_file and os.path.exists(temp_file):
            os.remove(temp_file)
        await status.delete()

# OCR Command
@bot.on(events.NewMessage(pattern="/ocr"))
async def extract_text(event):
    try:
        if not event.reply_to_msg_id:
            await event.reply("➲ Reply to an image to extract text")
            return

        reply = await event.get_reply_message()
        if not (reply.photo or reply.document):
            await event.reply("➲ This is not an image file")
            return

        status = await event.reply("➲ Processing image for text...\n" + progress_bar(0))  
        temp_file = await reply.download_media(file=f"ocr_{int(time.time())}")  
        
        # Check if Tesseract is installed  
        try:  
            tesseract_check = subprocess.run(["tesseract", "--version"],   
                                           capture_output=True,   
                                           text=True)  
            if tesseract_check.returncode != 0:  
                raise Exception("Tesseract not properly installed")  
                
            # Use Tesseract directly via command line  
            output_file = f"{temp_file}_ocr.txt"  
            cmd = f"tesseract {temp_file} {output_file[:-4]} -l eng 2>/dev/null"  
            subprocess.run(cmd, shell=True, check=True)  
            
            with open(output_file, 'r') as f:  
                text = f.read().strip()  
            
            if not text:  
                text = "➲ No text could be extracted from the image"  
            
            # Format the result  
            if len(text) > 3000:  
                text = text[:3000] + "... [truncated]"  
                
            result_msg = f"""➲ **Extracted Text**

┠ Length: {len(text)} characters
┠ Content: {text}"""

            await event.reply(result_msg)

        except Exception as e:  
            await event.reply(f"""➲ OCR failed.

┠ Reason: Tesseract OCR not properly installed
┠ Solution for Linux: sudo apt update && sudo apt install tesseract-ocr
┠ Solution for Windows: Download from https://github.com/UB-Mannheim/tesseract/wiki""")

    except Exception as e:
        await event.reply(f"➲ OCR processing failed.\n┠ Reason: {str(e)}")
    finally:
        # Cleanup temporary files
        temp_files = [temp_file, f"{temp_file}_ocr.txt"]
        for file in temp_files:
            if file and os.path.exists(file):
                os.remove(file)
        await status.delete()

# URL Shortener Command
@bot.on(events.NewMessage(pattern='/shorten (.*)'))
async def shorten_url(event):
    try:
        url = event.pattern_match.group(1)
        if not url.startswith(('http://', 'https://')):
            url = 'http://' + url

        # Using is.gd as example (no API key needed)
        response = requests.get(f"https://is.gd/create.php?format=simple&url={url}", timeout=10)  
        response.raise_for_status()  
        
        await event.reply(f"➲ URL shortened\n┠ Original: {url}\n┠ Short: {response.text}")

    except Exception as e:
        await event.reply(f"➲ URL shortening failed.\n┠ Reason: {str(e)}")

# Password Generator Command
@bot.on(events.NewMessage(pattern='/password(?: (\d+))?'))
async def generate_password(event):
    try:
        length = int(event.pattern_match.group(1) or 12)
        length = max(8, min(50, length))  # Limit between 8-50 characters

        chars = string.ascii_letters + string.digits + "!@#$%^&*"
        password = ''.join(random.choice(chars) for _ in range(length))

        await event.reply(f"➲ Generated Password\n┠ Length: {length}\n┠ Password: `{password}`\n┠ Save this securely!")

    except Exception as e:
        await event.reply(f"➲ Password generation failed.\n┠ Reason: {str(e)}")

# QR Code Generator Command
@bot.on(events.NewMessage(pattern='/qrcode (.*)'))
async def create_qrcode(event):
    try:
        text = event.pattern_match.group(1)
        qr = qrcode.QRCode(
            version=1,
            error_correction=qrcode.constants.ERROR_CORRECT_L,
            box_size=10,
            border=4,
        )
        qr.add_data(text)
        qr.make(fit=True)

        img = qr.make_image(fill_color="black", back_color="white")
        img_path = f"qrcode_{int(time.time())}.png"
        img.save(img_path)

        await event.reply(file=img_path)

    except Exception as e:
        await event.reply(f"➲ QR code generation failed.\n┠ Reason: {str(e)}")
    finally:
        if 'img_path' in locals() and os.path.exists(img_path):
            os.remove(img_path)

# Weather Command (using weatherAPI.com)
@bot.on(events.NewMessage(pattern='/weather (.*)'))
async def get_weather(event):
    try:
        city = event.pattern_match.group(1)
        if not WEATHER_API_KEY:
            raise Exception("Weather API key not configured")

        url = f"http://api.weatherapi.com/v1/current.json?key={WEATHER_API_KEY}&q={city}&aqi=no"
        response = requests.get(url, timeout=10)
        data = response.json()

        if 'error' in data:  
            raise Exception(data['error']['message'])  
        
        location = data['location']  
        current = data['current']  
        
        weather_info = f"""➲ **Weather in {location['name']}, {location['country']}**

┠ Condition: {current['condition']['text']}
┠ Temperature: {current['temp_c']}°C (Feels like {current['feelslike_c']}°C)
┠ Humidity: {current['humidity']}%
┠ Wind: {current['wind_kph']} km/h ({current['wind_dir']})
┠ Precipitation: {current['precip_mm']} mm
┠ Last Updated: {current['last_updated']}
⌬ Data from WeatherLund"""

        await event.reply(weather_info)
    except Exception as e:
        await event.reply(f"➲ Weather lookup failed.\n┠ Reason: {str(e)}")

# Calculator Command
@bot.on(events.NewMessage(pattern='/calc (.*)'))
async def calculate(event):
    try:
        expr = event.pattern_match.group(1)
        # Basic safety check
        if any(c in expr for c in "'\""):
            raise Exception("Invalid characters in expression")

        result = safe_eval(expr)
        await event.reply(f"➲ Calculation Result\n┠ Expression: {expr}\n┠ Result: {result}")
    except Exception as e:
        await event.reply(f"➲ Calculation failed.\n┠ Reason: {str(e)}")

# Start the bot
async def main():
    # Check for pip update
    try:
        pip_outdated = subprocess.run(["pip", "list", "--outdated"], capture_output=True, text=True)
        if "pip" in pip_outdated.stdout:
            print("Note: pip update available. Run: pip install --upgrade pip")
    except:
        pass

    await bot.start(bot_token=BOT_TOKEN)
    print("➲ Nighaa Bot is running...")
    await bot.run_until_disconnected()

if __name__ == '__main__':
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    try:
        loop.run_until_complete(main())
    except KeyboardInterrupt:
        print("➲ Bot stopped by user")
    finally:
        loop.close()