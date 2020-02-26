#!/usr/bin/env python

import RPi.GPIO as GPIO
import MFRC522
import signal
import time
import sys
import json
import soco

music_file = sys.argv[1]
device_ip_address = sys.argv[2]
volume = sys.argv[3]

f = open(music_file, "r")
music = json.loads(f.read())
f.close()
print("Ready")


continue_reading = True


def end_read(signal, frame):
    # Capture SIGINT for cleanup when the script is aborted
    global continue_reading
    print("Ctrl+C captured, ending read.")
    continue_reading = False
    GPIO.cleanup()


def play_album(album_name, device, volume):
    print(f"Playing album '{album_name}'")
    albums = device.music_library.get_albums(
        search_term=album_name, complete_result=True)

    device.clear_queue()
    device.add_multiple_to_queue(albums)
    device.volume = volume
    device.play_from_queue(0)


def play_webradio(title, uri, device, volume):
    print(f"Playing web radio '{title}'")
    device.volume = volume
    device.play_uri(title=title, uri=uri, force_radio=True)


def stop():
    print("Stopping playback")
    device.stop()


# Connect to Sonos device
device = soco.SoCo(device_ip_address)

# Hook the SIGINT
signal.signal(signal.SIGINT, end_read)

# Create an object of the class MFRC522
MIFAREReader = MFRC522.MFRC522()

current_card = None

# This loop keeps checking for chips. If one is near it will get the UID and authenticate
while continue_reading:

    # Scan for cards
    (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)

    # Get the UID of the card
    (status, uid) = MIFAREReader.MFRC522_Anticoll()

    # If we have the UID, continue
    if status == MIFAREReader.MI_OK:
        card = f"{uid[0]:02X}{uid[1]:02X}{uid[2]:02X}{uid[3]:02X}"

        if (card != current_card):
            current_card = card
            print("Card was detected: " + current_card)

            if current_card in music:
                music_entry = music[current_card]

                if "album" in music_entry:
                    play_album(music_entry["album"], device, volume)
                elif "title" in music_entry and "uri" in music_entry:
                    play_webradio(music_entry["title"],
                                  music_entry["uri"], device, volume)

        # Scan for cards a second time due to reading will always fail after a successful read
        (status, TagType) = MIFAREReader.MFRC522_Request(MIFAREReader.PICC_REQIDL)
    else:
        if (current_card != None):
            current_card = None
            print("Card was removed")

            stop()