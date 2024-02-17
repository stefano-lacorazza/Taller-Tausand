import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np
import keyboard
from tkinter import scrolledtext

# Variables
counter = 0
time= 0.0
# Functions

#create a function that increments the time every second and updates the label
def increment_time():
    global time, ax
    time += 0.1
    rounded_time = round(time, 2)
    label_time.config(text=f"Time: {rounded_time}")
    label_time.after(100, increment_time)  # Schedule increment_time to be called again after 1000ms (1 second)
    increment_counter("0")

    canvas.draw()
    style_graph()
    if time > 30:
        ax.set_xlim([time-30, time])
        canvas.draw()

def has_grid():
    global ax
    x_gridlines = ax.get_xgridlines()
    y_gridlines = ax.get_ygridlines()
    return len(x_gridlines) > 0 and len(y_gridlines) > 0


def style_graph():
    global ax, y
    ax.grid(True)  # Show grid
    ax.set_xlabel('Time (s)') 
    ax.set_ylabel('Total count') 
    ax.set_title('Total count over time')
    ax.set_ylim([0, y[-1] + 5])
    canvas.draw()


def increment_counter(pressed_key):
    n = int(pressed_key)
    global counter, ax, time, canvas,y,t
    
    counter = counter + n
    t = np.append(t, time)
    y = np.append(y, counter)
    label_total.config(text=f"Total: {counter}")
    
    ax.clear()
    ax.step(t, y, where='post') 
    canvas.draw()

def reset_counter():
    global counter, ax, time, canvas, t, y
    counter = 0
    time = 0
    t = np.array([0])
    y = np.array([0])
    label_total.config(text=f"Total: {counter}")
    label_time.config(text=f"Time: {time}")
    ax.clear()
    canvas.draw()

def add_history(num):
    text = "You pressed " + num + " at " + str(round(time, 2)) + " s"

    global scrolled_window
    scrolled_window.config(state=tk.NORMAL)
    scrolled_window.insert(tk.END, text + "\n")
    scrolled_window.config(state=tk.DISABLED)
    scrolled_window.see(tk.END)


def create_window():
    global label_total, label_time, canvas, ax, scrolled_window, window
    window = tk.Tk()
    window.title("Counter")
    window.geometry("850x500")
    # Create some widgets
    label_total = tk.Label(window, text=f"Total: {counter}", font=("Arial", 15))
    label_history = tk.Label(window, text=f"History")
    label_time = tk.Label(window, text=f"Time: {time}")
    label_count = tk.Label(window, text=f"Press 1-5 to increment the counter.", font=("Arial", 20))
    button_restart = tk.Button(window, text="Restart", command=reset_counter)
    button_end = tk.Button(window, text="Stop the program", command=close_window)

    # Create a ScrolledText widget
    scrolled_window = scrolledtext.ScrolledText(window, width=25, height=25)
    scrolled_window.grid(row=1, column=2, columnspan=2)
    scrolled_window.config(state=tk.DISABLED)

    # Arrange the widgets in a grid
    label_total.grid(row=2, column=2)
    label_count.grid(row=0, column=0)
    label_history.grid(row=0, column=2)
    label_time.grid(row=3, column=2)
    button_end.grid(row=2, column=0)
    button_restart.grid(row=2, column=1)

    canvas = FigureCanvasTkAgg(create_graph(), master=window)
    
    canvas.draw()
    canvas.get_tk_widget().grid(row=1, column=0, columnspan=2)  

    increment_time()  # Start the timer
    
    window.mainloop()

def close_window():
    global window
    window.destroy()
    
def create_graph():
    global ax, t, y
    fig = Figure(figsize=(6, 4), dpi=100)
    t = np.array([0])
    y = np.array([0])

    ax = fig.add_subplot(111)
    ax.step(t, y, where='post')  # Create a stairs graph


    return fig

def on_key_event(event):
    if event.name == '1' or event.name == '2' or event.name == '3' or event.name == '4' or event.name == '5' :
        increment_counter(event.name)
        add_history(event.name)




# Main
keyboard.on_press(on_key_event)
create_window()


