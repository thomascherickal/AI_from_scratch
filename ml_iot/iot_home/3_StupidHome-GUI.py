"""
    A HMI for IoT devices an AC and a lamp
    Author: Ndombasi Diakusala Joao Andre
    Date: October 3rd, 2024
"""
from tkinter import *
from tkinter import ttk
import tkinter as tk
import queue
from PIL import Image, ImageTk
import time
import serial
import random as rd
from threading import Thread


class IoTHomeWindow():

    def __init__(self, title:str, size:str) -> None:
        self.Running = False
        self.title = title
        self.size = size
        self.root = tk.Tk()
        self.tree = ttk.Treeview(self.root, column=("c0", "c1", "c2"), height=40)
        self.title_label = tk.Label(self.root, text="Smart IoT-Devices HMI")
        self.ac_image_paths = ["img/ac-off.png", "img/ac-on.png"]
        self.led_image_paths = ["img/led-off.png", "img/led-on.png"]
        
        self.speech_no = 0
        self.queue = queue.Queue()
        
        # initializations
        self.__customize_window()


    def __customize_window(self) -> None:
        self.root.title(self.title)
        # self.root.geometry(self.size)
        self.title_label.grid(row=0, column=0)

        self.ac_label = tk.Label(self.root)
        self.temp_label = tk.Label(self.root, text="28 ºC", 
                                   font=("Arial", 18), bg="white")
        self.led_label = tk.Label(self.root)
        self.show_images(states=(0, 0, 0))

        
        # Create button
        self.change_button = tk.Button(self.root, text="Play", command=self.toggle_simu)
        self.change_button.grid(row=0, column=1)

        # style
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("TreeView", background="lightblue", fieldbackground="grey", foreground="yellow")
        style.configure("TreeView.heading", background="lightgray", foreground="black")

        # treeview
        col_names = ("Timestamp", "occupancy", "room temp", "out temp")
        for i in range(len(col_names)):
            self.tree.column("#" + str(i), anchor=CENTER)
            self.tree.heading("#" + str(i), text=col_names[i])
        self.tree.grid(row=2, column=0, columnspan=2, sticky="nsew")

        
    def showGUI(self) -> None:
        self.root.mainloop()


    def close(self):
        self.root.destroy()
        print('Window Closed!')


    def update_cmds(self, input_buffer:queue.Queue) -> None:
        """
            input_buffer: data from UDP
                user: sensor name
                values: [ac_state, ac_value, led_state]
        """
        while True:
            try:
                values = input_buffer.get(timeout=1) # day_hour, occupancy, ac_temp, light_on
                
                try:
                    self.show_images(states=values[1:4]) # 1, 2, 3
                    self.tree.insert("", 0, values=values[1:2]+values[-2:], text=values[0])
                except IndexError:
                    print('Index Error')
                
                self.root.update()
            
            except queue.Empty:
                print('Waiting...', end='\r')
            time.sleep(.1)

    
    def show_images(self, states:tuple) -> None:
        """
            states = [ac_state, ac_value, led_state]
        """
        ac_state, ac_value, led_state = states 
        # AC
        self.ac_image = Image.open(self.ac_image_paths[ac_state])
        self.ac_image = self.ac_image.resize((600, 250)) # if need
        self.ac_photo = ImageTk.PhotoImage(self.ac_image)  # Keep reference to avoid garbage collection
       
        self.ac_label.config(image=self.ac_photo) # reset image
        self.ac_label.grid(row=1, column=0)
        self.temp_label.config(text=f"{ac_value} ºC" if ac_state else "")
        self.temp_label.place(x=500, y=180, anchor="center")  # Place text label on top

        # LED
        self.led_image = Image.open(self.led_image_paths[led_state])
        self.led_image = self.led_image.resize((160, 250)) # if need
        self.led_photo = ImageTk.PhotoImage(self.led_image)  # Keep reference to avoid garbage collection
         
        self.led_label.config(image=self.led_photo) # reset image
        self.led_label.grid(row=1, column=1)

 
    def toggle_simu(self):

        self.Running = not self.Running
        self.change_button.config(text="Pause" if self.Running else "Play")



# features: 'outside_temperature', 'room_temperature', 'occupancy', 'hour', 'day_of_week'
days = ["Sun", "Mon", "Tue", "Wed", "Thu", "Fri", "Sat"]
def stupid_data(app:IoTHomeWindow, out_buffer:queue.Queue): 
    while True:
        if app.Running:
            day_of_week = rd.randint(0, 6)
            hour = rd.randint(0, 23)
            occupancy = rd.randint(0,1)
            ac_temp = rd.randint(-50, 50)
            light_on = rd.randint(0,1)
            room_temp = rd.randint(-50, 50)
            out_temp = rd.randint(-50, 50)
            values = (
                        f"{days[day_of_week]} {hour}h",
                        bool(occupancy),
                        f"{ac_temp} °C",
                        light_on,
                        f"{room_temp} °C",
                        f"{out_temp} °C"
                    )
            QUEUE.put(values)
            print(values)
            time.sleep(1)


if __name__=="__main__":
    
    app = IoTHomeWindow(size="1000x700", title="Smart-IoT-Home")
   
    QUEUE = queue.Queue() 
        
    Thread(target=stupid_data, args=(app, QUEUE), daemon=True).start()
    Thread(target=app.update_cmds, args=(QUEUE,), daemon=True).start()
    app.showGUI()
