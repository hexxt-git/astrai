from pyray import *

def circle(x, y, r, camera, color=WHITE):
    draw_circle(int((x+camera[0])*camera[2] + camera[3]/2), int((y+camera[1])*camera[2] + camera[4]/2), int(r*camera[2]), color)

def line(x1, y1, x2, y2, camera, color=WHITE):
    draw_line(int((x1+camera[0])*camera[2] + camera[3]/2), int((y1+camera[1])*camera[2] + camera[4]/2), int((x2+camera[0])*camera[2] + camera[3]/2), int((y2+camera[1])*camera[2] + camera[4]/2), color)

def text(text, x, y, s, camera, color=WHITE):
    if s*camera[2] > 5:
        draw_text(text, int((x+camera[0])*camera[2] + camera[3]/2), int((y+camera[1])*camera[2] + camera[4]/2), int(s*camera[2]), color)
