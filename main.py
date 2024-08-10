from tkinter import *
from tkinter import filedialog
from PIL import Image

import time
import pyperclip
import math

print("Welcome to the ASCII art generator! Upload an image and generate ASCII art using this program!")

root = Tk()
root.withdraw()
filepath = filedialog.askopenfilename(initialdir = "/", title = "Upload an image", filetypes = [("Image files", ".png .jpg")])

image = Image.open(filepath)

original_w, original_h = image.size

width = int(input("Input a width for your ASCII art (a number larger than 1): "))
height = math.floor(original_h * width / original_w)
image = image.resize((width*2, height), Image.LANCZOS)

pixels = image.load()

ascii_chars = ".-:=;+!rc/z?sLTvJ7|FiCfI31tluneoZ5Yxjya2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@"

print("Current ASCII glyph string: " + ascii_chars)

prompting = True
while prompting:
    change_chars = input("Would you like to change the ASCII glyph string? (y/n): ").lower()
    if change_chars == "y":
        prompting = False
        changed_chars = input("Input a new ASCII glyph string (from lightest to darkest, input nothing to cancel): ").replace(" ", "")
        if changed_chars != "":
            ascii_chars = changed_chars
        else:
            print("Cancelled. ASCII glyph string unchanged. ")
            time.sleep(0.2)
    elif change_chars == "n":
        prompting = False
    else:
        print("Invalid input, please try again.\n")
        time.sleep(0.2)

dark_vals = len(ascii_chars)

darknesses = []

for y in range(height):
    darknesses.append([])
    for x in range(width):
        R, G, B = pixels[x, y][:3]
        darknesses[y].append(round((R + G + B) / 3))

ascii_art = []

for i in range(len(darknesses)):
    ascii_art.append([])
    for val in darknesses[i]:
        char_index = math.ceil(val / (255 / dark_vals))
        ascii_art[i].append(ascii_chars[char_index-1] if char_index != 0 else ascii_chars[0])

final_piece = []

for sublist in ascii_art:
    final_piece.append("".join(sublist))

print("Displaying art... ")
time.sleep(0.2)
print("\n".join(final_piece))

prompting = True
while prompting:
    change_chars = input("Would you to copy your art to your clipboard? (y/n): ").lower()
    if change_chars == "y":
        pyperclip.copy("\n".join(final_piece))
        print("\nCopied to clipboard!\n")
    elif change_chars == "n":
        prompting = False
    else:
        print("Invalid input, please try again.\n")
        time.sleep(0.2)
