from tkinter import *
from tkinter import ttk
import sys 
from gpiozero import LED
from time import sleep
import time
import sys
import RPi.GPIO as GPIO
from hx711 import HX711
num = 0 

pump = LED(13)
solenoid = LED(19)

weights = [500, 1000, 4000]

####################
#Code for the scale#
####################
def cleanAndExit():
    print("Cleaning...")
        
    print("Bye!")
    sys.exit()

hx = HX711(5, 6)

hx.set_reading_format("MSB", "MSB")
referenceUnit = -214
hx.set_reference_unit(referenceUnit)

hx.reset()

hx.tare()

print("Tare done! Add weight now...")


######################
#Code for the screen##
######################
root = Tk()
root.geometry("1920x1080")
frm = ttk.Frame(root, padding=10)
frm.grid()
numBottles = DoubleVar()
scale_slider = Scale(frm, from_=0, to=100, variable=numBottles, width=50).grid(column=1, row=1)
listbox = Listbox(frm, width=6, height=3)
listbox.insert(1,"500ml")
listbox.insert(2, "1L")
listbox.insert(3,"4L") 
bottles_remaining = ttk.Label(frm, text='0', width=3)
bottles_remaining.grid(column=6,row=3)

def test():
    print(listbox.curselection())

#############################
#function to fill the bottle#
#############################
def fillBottle():
    full = False
    size_of_bottle = listbox.curselection()[0]
    print('The size of bottle is ' + str(size_of_bottle))
    num_of_bottles = int(numBottles.get())
    print('The number of bottles is ' + str(num_of_bottles))
    bottle_weight = weights[size_of_bottle]

    for i in range(num_of_bottles):
        full = False
        start = time.time()
        counter = 5
        begin = False
        bottles_remaining.configure(text=str(num_of_bottles - i))
        bottles_remaining.update()
        while not full:
            try:
                val = hx.get_weight(5)

                hx.power_down()
                hx.power_up()

            except (KeyboardInterrupt, SystemExit):
                cleanAndExit()
            print(val)
            if time.time() - start > 1 and begin == False:
                start = time.time()
                counter = counter - 1

            if counter < 1:
                begin = True

            if val > 10 and begin == True and val < 120:
                pump.on()
                #allow for a delay for the pump to spin up
                sleep(0.2)
                solenoid.on()

            if val > int(bottle_weight) and begin == True:
                full = True
                pump.off()
                solenoid.off()
                begin = False



def update_weights():
    weights[0] = t1.get()
    weights[1] = t2.get()
    weights[2] = t3.get()
    print('updated weights')

listbox.grid(column=0, row=1)
ttk.Label(frm, text='Bottle Selection').grid(column=0, row=0)
ttk.Label(frm, text='Bottles Remaining',width=50).grid(column=5, row=3)
ttk.Button(frm, text="Start Filling", command=fillBottle).grid(column=1, row=0)
ttk.Label(frm, text='500ml weight').grid(column=0, row=4)
ttk.Label(frm, text='1L weight').grid(column=0, row=5)
ttk.Label(frm, text='4L weight').grid(column=0, row=6)
t1 = ttk.Entry(frm)
t2 = ttk.Entry(frm )
t3 = ttk.Entry(frm)
t1.grid(column=1, row=4)
t2.grid(column=1, row=5)
t3.grid(column=1, row=6)
t1.insert(0, str(weights[0]))
t2.insert(0, str(weights[1]))
t3.insert(0, str(weights[2]))
ttk.Button(frm, text='Update weights', command=update_weights).grid(column=1,row=7)
root.mainloop()

