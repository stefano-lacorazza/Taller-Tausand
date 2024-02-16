import tkinter as tk
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import numpy as np



# Variables
counter = 0
# Functions



def increment_time():
    global time
    time += 1
    label_time.after(1000, increment_time)



def increment_counter():
    global counter
    counter += 1
    label_total.config(text=f"Total: {counter}")

def reset_counter():
    global counter
    counter = 0
    label_total.config(text=f"Total: {counter}")

def create_window():
    global label_total
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
    button_end.grid(row=1, column=0)
    button_restart.grid(row=1, column=1)

    canvas = FigureCanvasTkAgg(create_graph(), master=window)
    canvas.draw()
    canvas.get_tk_widget().grid(row=2, column=0, columnspan=2)  # Use grid instead of pack

    window.mainloop()

def create_graph():
    fig = Figure(figsize=(5, 4), dpi=100)
    t = np.arange(0, 3, .01)
    fig.add_subplot(111).plot(t, 2 * np.sin(2 * np.pi * t))
    return fig

# Main
create_window()