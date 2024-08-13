from tkinter import *
from tkinter import filedialog
from PIL import Image

import time
import pyperclip
import math

def clamp(nval, nmin, nmax):
    if nval < nmin:
        nval = nmin
    elif nval > nmax:
        nval = nmax
    return nval

def promptClamped(oval, nval, nmin=None, nmax=None):
    if nval != "":
        if nmin != None and nval < nmin:
            nval = nmin
        elif nmax != None and nval > nmax:
            nval = nmax
        return nval
    return oval

print("Welcome to the ASCII art generator! Upload an image and generate ASCII art using this program!")

root = Tk()
root.withdraw()
filepath = filedialog.askopenfilename(initialdir = "/", title = "Upload an image", filetypes = [("Image files", ".png .jpg")])

image = Image.open(filepath)

original_w, original_h = image.size

generating = True
while generating:
    width = 1
    inp_success = False
    while inp_success != True:
        try:
            width = int(input("\nInput a width for your ASCII art (>=1): "))
            if width >= 1:
                inp_success = True
            else:
                print("Invalid input. Input a number greater than or equal to 1.")
        except:
            print("Invalid input. Please try again.")
            time.sleep(0.2)
    height = math.floor(original_h * width / original_w)
    image = image.resize((width, height), Image.LANCZOS)

    pixels = image.load()

    ascii_chars = ".-:=;+!rc/z?sLTvJ7|FiCfI31tluneoZ5Yxjya2ESwqkP6h9d4VpOGbUAKXHm8RD#$Bg0MNWQ%&@"

    print("\nCurrent ASCII glyph string: " + ascii_chars)

    prompting = True
    while prompting:
        change_chars = input("Would you like to change the ASCII glyph string? (y/n): ").lower()
        if change_chars == "y":
            prompting = False
            changed_chars = input("Input a new ASCII grayscale glyph string (from lightest to darkest, input nothing to cancel): ").replace(" ", "")
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
    
    mode = False
    prompting = True
    while prompting:
        change_chars = input("\nChoose a display mode? (y for lighten mode / n for darken mode): ").lower()
        if change_chars == "y":
            prompting = False
            mode = True
        elif change_chars == "n":
            prompting = False
            mode = False
        else:
            print("Invalid input, please try again.\n")
            time.sleep(0.2)

    spacing = 2
    spacing_inp = input("\nCurrent spacing between ASCII chars is " + str(spacing) + ".\nPress ENTER to accept the current value, or input a value greater than 0: ")
    spacing = promptClamped(spacing, int(spacing_inp) if spacing_inp != "" else "", nmin=0)

    # use a quadratic equation to control the contrast
    # contrast is amplified by making lighter parts lighter and darker parts darker
    contrast_curve_multipler = -4.0 # -4 is default, recommended values between -4 to 4
    contrast_amount = 0 if contrast_curve_multipler > 0 else 255 # the most a contrast
    contrast_curve_horizontal_shift = 255/2
    contrast_dampener = 1 # number larger than or equal to 1

    prompting = True
    while prompting:
        use_contrast_curve = input("\nWould you like to use a contrast curve to amplify or reduce the contrast of the final piece? A quadratic equation is used to amplify the contrast according to how light/dark the values are. (y/n): ").lower()
        if use_contrast_curve == "y":
            prompting = False

            contrast_curve_multiplier_input = input("\nCurrent contrast curve multiplier is "+ str(contrast_curve_multipler) +".\nA negative value separates gray-er values into light and dark. A positive value makes light or darker values even lighter or darker. \nPress ENTER to accept the current value, or input a value between -4.0 to 4.0: ")
            contrast_curve_multipler = promptClamped(contrast_curve_multipler, float(contrast_curve_multiplier_input) if contrast_curve_multiplier_input != "" else "", nmin=-4.0, nmax=4.0)

            contrast_amount_input = input("\nCurrent contrast amount is " + str(contrast_amount) + ".\nThis is the height of the vertex of the quadratic equation. Increasing this number makes the change in contrast more extreme. \nPress ENTER to accept the current value, or input a number between 0 and 255: ")
            contrast_amount = promptClamped(contrast_amount, int(contrast_amount_input) if contrast_amount_input != "" else "", nmin=0, nmax=255)
            
            contrast_curve_horizontal_shift_input = input("\nCurrent contrast horizontal shift amount is " + str(contrast_curve_horizontal_shift) + ".\nA value less than 127.5 will make the final art piece darker. A value greater than 127.5 will make the final art piece lighter.\nPress ENTER to accept the current value, or input a value between 0 and 255: ")
            contrast_curve_horizontal_shift = promptClamped(contrast_curve_horizontal_shift, float(contrast_curve_horizontal_shift_input) if contrast_curve_horizontal_shift_input != "" else "", nmin=0, nmax=255)

            contrast_dampener_inp = input("\nCurrent contrast dampener factor is " + str(contrast_dampener) + ".\nThe contrast dampener factor reduces the effects of the contrast curve that is configured above. A factor of 1 changes nothing, any number greater than that will diminish the contrast change.\nPress ENTER to accept the current value, or input a number greater than 1: ")
            contrast_dampener = promptClamped(contrast_dampener, int(contrast_dampener_inp) if contrast_dampener_inp != "" else "", nmin=1)

            print("\ny=[(a/255-h)^2 + k )] / c")
            print("Contrast curve multiplier (a): " + str(contrast_curve_multipler))
            print("Contrast amount (k): " + str(contrast_amount))
            print("Contrast curve horizontal shift (h): " + str(contrast_curve_horizontal_shift))
            print("Contrast dampener (c): " + str(contrast_dampener) + "\n")
        elif use_contrast_curve == "n":
            prompting = False
            contrast_curve_multipler = 0
            contrast_amount = 0
        else:
            print("Invalid input, please try again.\n")
            time.sleep(0.2)

    dark_vals = len(ascii_chars)

    darknesses = []

    for y in range(height):
        darknesses.append([])
        for x in range(width):
            R, G, B = pixels[x, y][:3]
            original_val = round((R + G + B) / 3)
            
            # this is a quadratic equation, like this: y = -4/255(x-255/2)^2 + 255
            quadratic_transform = (contrast_curve_multipler/255) * ((original_val - contrast_curve_horizontal_shift)**2) + contrast_amount
            if original_val == contrast_curve_horizontal_shift:
                quadratic_transform = 0
            
            if original_val > contrast_curve_horizontal_shift:
                darknesses[y].append(clamp(original_val + (quadratic_transform / contrast_dampener), 0, 255))
            else:
                darknesses[y].append(clamp(original_val + (quadratic_transform / contrast_dampener), 0, 255))

    ascii_art = []

    for i in range(len(darknesses)):
        ascii_art.append([])
        for val in darknesses[i]:
            char_index = math.ceil(val / (255 / dark_vals))
            if mode:
                ascii_art[i].append(ascii_chars[char_index] if char_index != len(ascii_chars) else ascii_chars[len(ascii_chars)-1])
            else:
                ascii_art[i].append(ascii_chars[len(ascii_chars) - (char_index)] if char_index != 0 else ascii_chars[len(ascii_chars)-1])

    final_piece = []

    spacing_str = " " * spacing

    for sublist in ascii_art:
        final_piece.append(spacing_str.join(sublist))

    print("Displaying art... ")
    time.sleep(0.2)
    print("\n".join(final_piece))

    prompting = True
    while prompting:
        change_chars = input("Would you to copy your art to your clipboard? (y/n): ").lower()
        if change_chars == "y":
            prompting = False
            pyperclip.copy("\n".join(final_piece))
            print("\nCopied to clipboard!\n")
        elif change_chars == "n":
            prompting = False
        else:
            print("Invalid input, please try again.\n")
            time.sleep(0.2)

    prompting = True
    while prompting:
        redo = input("Would you like to change the current parameters? (y/n): ").lower()
        if redo == "y":
            prompting = False
        elif redo =="n":
            prompting = False
            generating = False
        else:
            print("Invalid input, please try again.\n")
            time.sleep(0.2)