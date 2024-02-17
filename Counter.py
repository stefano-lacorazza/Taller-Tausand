import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import keyboard


# Variables
counter = 0
time= 0.0
# Functions

#create a function that increments the time every second and updates the label
def increment_time():
    global time
    time += 0.1
    rounded_time = round(time, 2)
    label_time.config(text=f"Time: {rounded_time}")
    label_time.after(100, increment_time)  # Schedule increment_time to be called again after 1000ms (1 second)



def increment_counter(pressed_key):
    global counter, ax, time, canvas
    counter = counter + int(pressed_key)
    label_total.config(text=f"Total: {counter}")
    ax.plot(counter, counter, 'ro')  # For example, add a point at (counter, counter)
    canvas.draw()

def reset_counter():
    global counter
    global time
    counter = 0
    time = 0
    label_total.config(text=f"Total: {counter}")
    label_time.config(text=f"Time: {time}")

def create_window():
    global label_total
    global label_time
    global canvas
    window = tk.Tk()
    window.title("Counter")
    window.geometry("800x600")
    # Create some widgets
    label_total = tk.Label(window, text=f"Total: {counter}")
    label_time = tk.Label(window, text=f"Time: {time}")
    button_restart = tk.Button(window, text="Restart", command=reset_counter)
    button_end = tk.Button(window, text="Increment", command=increment_counter)

    # Arrange the widgets in a grid
    label_total.grid(row=0, column=0)
    label_time.grid(row=1, column=0)
    button_end.grid(row=2, column=0)
    button_restart.grid(row=1, column=1)

    canvas = FigureCanvasTkAgg(create_graph(), master=window)
    canvas.draw()
    canvas.get_tk_widget().grid(row=2, column=0, columnspan=2)  # Use grid instead of pack
    increment_time()  # Start the timer
    window.mainloop()

def create_graph():
    global ax
    fig = Figure(figsize=(5, 4), dpi=100)
    t = np.arange(0, 3, .01)
    ax = fig.add_subplot(111)
    
    return fig

def on_key_event(event):
    if event.name == '1' or event.name == '2' or event.name == '3' or event.name == '4' or event.name == '5' :
        increment_counter(event.name)




# Main
keyboard.on_press(on_key_event)
create_window()

