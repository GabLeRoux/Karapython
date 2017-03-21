#!/usr/bin/env python

# This example shows how to use pygame to build a graphic frontend for
#  a karaoke application.
# Requires: pygame.

import midifile, time, datetime, sys
import pygame

try:
    # for Python2
    import Tkinter as tk
    import tkFileDialog as filedialog
    root = tk.Tk()
    root.withdraw()
except ImportError:
    # for Python3
    from tkinter import *
    from tkinter import filedialog
    root = tk.Tk()
    root.withdraw()

karaoke_file = ''

def open_file_dialog():
    global karaoke_file
    karaoke_file = filedialog.askopenfilename(filetypes=(("Karaoke Files", ".kar .midi"), ("All Files", "*.*")))

open_file_dialog()

# filename = raw_input('Please enter filename of .mid or .kar file:')
# karaoke_file = "dust_in_the_wind_karaoke_songs_NifterDotCom.kar"

pygame.init()
screenx = 1200
screeny = 400
screen = pygame.display.set_mode((screenx, screeny))
pygame.display.set_caption(karaoke_file)

font = pygame.font.Font(None, 60)
purple = (100, 100, 250, 0)
white = (250, 250, 250, 0)

active_text_color = purple
base_text_color = white

m = midifile.midifile()
m.load_file(karaoke_file)

pygame.mixer.init()
pygame.mixer.music.load(karaoke_file)
pygame.mixer.music.play(0, 0)  # Start song at 0 and don't loop
start = datetime.datetime.now()

done = False

if not m.karfile:
    print "This is not a karaoke file. I'll just play it"
    while pygame.mixer.music.get_busy():
        time.sleep(1)
    sys.exit(0)

start = start - datetime.timedelta(0, 9)  # To start lyrics at a later point
dt = 0.

# Main event loop
while pygame.mixer.music.get_busy() and not done:

    # todo: space to pause

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            done = True

    dt = (datetime.datetime.now() - start).total_seconds()
    m.update_karaoke(dt)

    for iline in range(3):
        l = font.size(m.karlinea[iline] + m.karlineb[iline])[0]
        x0a = screenx / 2 - l / 2.
        line_a = font.render(m.karlinea[iline], 0, active_text_color)
        line_b = font.render(m.karlineb[iline], 0, base_text_color)
        rect_a = screen.blit(line_a, [x0a, 80 + iline * 60])
        x0b = x0a + rect_a.width
        rect_b = screen.blit(line_b, [x0b, 80 + iline * 60])

    pygame.display.flip()
    screen.fill(0)

    time.sleep(.1)

pygame.quit()
