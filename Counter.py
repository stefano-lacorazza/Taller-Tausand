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

def increment_time():
    """
    This function is responsible for incrementing the time by 0.1 every 100 milliseconds and updating the time label.
    It also styles the graph, and updates the x-axis limits of the graph if the time exceeds 30 seconds.
    """
    global time, ax
    time += 0.1
    rounded_time = round(time, 2)
    label_time.config(text=f"Time: {rounded_time}")
    label_time.after(100, increment_time)  
    increment_counter("0")

    canvas.draw()
    style_graph()
    if time > 30:
        ax.set_xlim([time-30, time])
        canvas.draw()

def has_grid():
    """
    This function returns True if the graph has gridlines, and False otherwise.
    """
    global ax
    x_gridlines = ax.get_xgridlines()
    y_gridlines = ax.get_ygridlines()
    return len(x_gridlines) > 0 and len(y_gridlines) > 0


def style_graph():
    """
    This function is responsible for styling the graph.
    It sets the title, labels, and grid of the graph, and vertical range of the graph.
    """
    global ax, y
    ax.grid(True) 
    ax.set_xlabel('Time (s)') 
    ax.set_ylabel('Total count') 
    ax.set_title('Total count over time')
    ax.set_ylim([0, y[-1] + 5])
    canvas.draw()


def increment_counter(pressed_key):
    """
    This function is responsible for incrementing the counter based on the key pressed by the user.
    It updates the total label and the scrolled text widget, and it adds a point to the graph.

    Parameters:
    key (str): The key pressed by the user. It should be a string containing a single digit from '1' to '5'.

    """
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
    """
    This function is responsible for resetting the program.
    It updates the total label and the scrolled text widget, and it clears the graph.
    """
    global counter, ax, time, canvas, t, y
    counter = 0
    time = 0
    t = np.array([0])
    y = np.array([0])
    label_total.config(text=f"Total: {counter}")
    label_time.config(text=f"Time: {time}")
    ax.clear()
    canvas.draw()
    clear_history()

def add_history(key):
    """
    This function is responsible for adding the key pressed by the user to the history in the scrolled text widget.

    Parameters:
    key (str): The key pressed by the user. It should be a string containing a single digit from '1' to '5'.
    """
    text = "You pressed " + key + " at " + str(round(time, 2)) + " s"

    global scrolled_window
    scrolled_window.config(state=tk.NORMAL)
    scrolled_window.insert(tk.END, text + "\n")
    scrolled_window.config(state=tk.DISABLED)
    scrolled_window.see(tk.END)

def clear_history():
    """
    This function is responsible for clearing the history in the scrolled text widget.
    """
    global scrolled_window
    scrolled_window.config(state=tk.NORMAL) 
    scrolled_window.delete('1.0', tk.END)
    scrolled_window.config(state=tk.DISABLED) 


def create_window():
    """
    This function is responsible for creating the main window of the application.
    It sets up the window properties, creates and places the widgets, and starts the main event loop.
    """
    global label_total, label_time, canvas, ax, scrolled_window, window
    window = tk.Tk()
    window.title("Counter")
    window.geometry("850x500")

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

    increment_time() 
    
    window.mainloop()

def close_window():
    """
    This function is responsible for closing the main window of the application.
    """
    global window
    window.destroy()
    
def create_graph():
    """
    This function is responsible for creating the graph in the application.

    It initializes two global variables, `t` and `y`, as numpy arrays with a single element 0. These variables represent the x and y coordinates of the points in the graph.

    It also creates teh Figure object, and adds a subplot to it. The subplot is a step graph.

    Returns:
    fig (Figure): The created Figure object.
    """
    global ax, t, y
    fig = Figure(figsize=(6, 4), dpi=100)
    t = np.array([0])
    y = np.array([0])
    ax = fig.add_subplot(111)
    ax.step(t, y, where='post')  
    return fig

def on_key_event(event):
    """
    This function is responsible for handling key press events.

    It checks if the name of the event is '1', '2', '3', '4', or '5'. If it is, it calls the `increment_counter` function w and the `add_history` functions.

    Parameters:
    event (pynput.keyboard.Events): The event that triggered the function. It should be a key press event.
    """
    if event.name == '1' or event.name == '2' or event.name == '3' or event.name == '4' or event.name == '5' :
        increment_counter(event.name)
        add_history(event.name)




# Main
keyboard.on_press(on_key_event)
create_window()


