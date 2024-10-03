from tkinter import *
from tkinter import ttk
import tkinter as tk
import queue
from PIL import Image, ImageTk
import time

class Window():

    def __init__(self, title:str, size:str) -> None:
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
        self.change_button = tk.Button(self.root, text="Change Image", command=self.change_image)
        self.change_button.grid(row=0, column=1)

        # style
        style = ttk.Style(self.root)
        style.theme_use("clam")
        style.configure("TreeView", background="lightblue", fieldbackground="grey", foreground="yellow")
        style.configure("TreeView.heading", background="lightgray", foreground="black")

        # treeview
        col_names = ("SENSOR", "outside_temp", "room_temp", "occupancy/hour")
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
                values = input_buffer.get(timeout=1)
                user, values = values
                print(values)
                try:
                    self.show_images(states=values)
                    self.tree.insert("", 0, values=values, text=user)
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

 
    def change_image(self):
        self.show_images(states=(1, 25, 1))


def get_data(out_buffer:queue.Queue): 
        for i in range(10_000):
            QUEUE.put(("Andre", (rd.randint(0,1), rd.randint(-50, 50), rd.randint(0,1))))
            time.sleep(1)
  
            
if __name__=="__main__":
    
    app = Window(size="1000x700", title="Smart-IoT-Home")

    import random as rd
    from threading import Thread
   
    QUEUE = queue.Queue() 
        
    Thread(target=get_data, args=(QUEUE,), daemon=True).start()
    Thread(target=app.update_cmds, args=(QUEUE,), daemon=True).start()
    app.showGUI()
