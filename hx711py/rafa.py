import pygame 
import pygame_widgets
import sys 
from gpiozero import LED
from time import sleep
import time
import sys
import RPi.GPIO as GPIO
from hx711 import HX711
from pygame_widgets.dropdown import Dropdown

led = LED(13)
led2 = LED(19)
led1Status = False


def cleanAndExit():
    print("Cleaning...")
        
    print("Bye!")
    sys.exit()

hx = HX711(5, 6)

hx.set_reading_format("MSB", "MSB")
referenceUnit = 214
hx.set_reference_unit(referenceUnit)

hx.reset()

hx.tare()

print("Tare done! Add weight now...")

# initializing the constructor 
pygame.init() 

# screen resolution 
res = (1920,1080) 

# opens up a window 
screen = pygame.display.set_mode(res) 

# white color 
color = (255,255,255) 

# light shade of the button 
color_light = (170,170,170) 

# dark shade of the button 
color_dark = (100,100,100) 

# stores the width of the 
# screen into a variable 
width = screen.get_width() 

# stores the height of the 
# screen into a variable 
height = screen.get_height() 

# defining a font 
smallfont = pygame.font.SysFont('Corbel',35) 

# rendering a text written in 
# this font 
text = smallfont.render('quit' , True , color) 

dropdown = Dropdown(screen, 250, 50, 250, 50, name='secect size',choices=['500ml', '1l', '4l'], direction='down')

while True: 
    for ev in pygame.event.get(): 

        if ev.type == pygame.QUIT: 
            pygame.quit() 

        #checks if a mouse is clicked 
        if ev.type == pygame.MOUSEBUTTONDOWN: 

            #if the mouse is clicked on the 
            # button the game is terminated 
            if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40: 
                print('switching')
                if led1Status == True:
                    led1Status = False
                    led.off()
                else:
                    led1Status = True
                    led.on()

    # fills the screen with a color 
    screen.fill((60,25,60)) 

    # stores the (x,y) coordinates into 
    # the variable as a tuple 
    mouse = pygame.mouse.get_pos() 

    # if mouse is hovered on a button it 
    # changes to lighter shade 
    if width/2 <= mouse[0] <= width/2+140 and height/2 <= mouse[1] <= height/2+40: 
        pygame.draw.rect(screen,color_light,[width/2,height/2,140,40]) 

    else: 
        pygame.draw.rect(screen,color_dark,[width/2,height/2,140,40]) 

    # superimposing the text onto our button 
    screen.blit(text , (width/2+50,height/2)) 

    try:
        val = hx.get_weight(5)

        hx.power_down()
        hx.power_up()

    except (KeyboardInterrupt, SystemExit):
        cleanAndExit()

    number = smallfont.render(str(val), True, color_dark)
    screen.blit(number, (500, 400))
    # updates the frames of the game 
    pygame_widgets.update(ev)
    pygame.display.update() 







