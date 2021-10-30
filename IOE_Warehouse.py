import matplotlib.pyplot as plt, mpld3
import matplotlib.animation as animation
from matplotlib import style
import numpy as np
import random
import serial
import tkinter as tk

win=tk.Tk()
 

#initialize serial port
ser = serial.Serial('COM3',9600)
ser.timeout = 10 #specify timeout when using readline()
#ser.open()
if ser.is_open==True:
	print("\nAll right, serial port now open. Configuration:\n")
	print(ser, "\n") #print serial parameters

# Create figure for plotting
fig = plt.figure()
ax = fig.add_subplot(1, 1, 1)
xs = [] #store trials here (n)
ys = [] 
rs = [] 

the_temp = tk.Label(win, text="Temp", fg="black", bg="white", font="36")
the_humd = tk.Label(win, text="Humd", fg="black", bg="white", font="36")


def READ(hum,temp):
       
    #global temp
    temp=temp
    hum=hum
    #humidity, temperature = Adafruit_DHT.read_retry(11, 27)
    #temp = temperature * 9/5.0 + 32
    the_temp.configure(text="Temperature : "+str(temp)+" C")
    the_humd.configure(text="Humidity : "+str(hum)+"%")
    the_temp.pack()
    the_humd.pack()

def read_every_second(hum,temp):
    READ(hum,temp)
    win.after(1000, read_every_second(hum,temp))


    
# This function is called periodically from FuncAnimation
def animate(i, xs, ys):

    #Aquire and parse data from serial port
    line=ser.readline()      #ascii
    hum,temp=float(line.split()[0]),float(line.split()[1])
    
    #line_as_list = line.split(',')
    #read_every_second(hum,temp)
    READ(hum,temp)
	
    # Add x and y to lists
    xs.append(i)
    ys.append(temp)
    rs.append(hum)
    
    if temp>50:
        print("WARNING HIGH TEMPERATURE. Can effect the items")
    elif hum>70:
        print("High humidity can affect the items.")
        
            
            

    #print(xs,ys,rs)

    # Limit x and y lists to 20 items
    #xs = xs[-10:]
    #ys = ys[-10:]

    # Draw x and y lists
    ax.clear()
    ax.plot(xs, ys, label="Temperature in C")
    ax.plot(xs, rs, label="Humidity in %")

    # Format plot
    plt.xticks(rotation=45, ha='right')
    plt.subplots_adjust(bottom=0.30)
    plt.title('Real Time Inventory data')
    plt.ylabel('Data from Sensor')
    plt.legend()
    plt.style.use("ggplot")
    plt.axis([1, None, 0, 80]) 
    #plt.axis([1, 100, 0, 1.1])

    i+=1

ani = animation.FuncAnimation(fig, animate, fargs=(xs, ys), interval=1000)
plt.show()
#mpld3.show()


win.mainloop()
