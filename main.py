import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import pandas as pd
import json
import matplotlib.pyplot as plt
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg


# FUNCTIONS

def plot_dataframe():
    x_column = 'Longitude/Latitude'
    y_column = 'Site Height'
    

    # Bar chart

    fig, ax = plt.subplots()
    ax.bar(current_data[x_column], current_data[y_column])
    ax.set_xlabel('Longitude/Latitude')
    ax.set_ylabel("Site Height")
    ax.set_title('Bar Chart')

    # Create a Matplotlib figure and canvas
    canvas = FigureCanvasTkAgg(fig, master=plot_frame)
    canvas.draw()

    # Embed the Matplotlib canvas in the tkinter window
    canvas.get_tk_widget().grid(row=4, column=0, pady=10, padx=10)


    # Set the Matplotlib figure as the plot area
    canvas.get_tk_widget().configure(width=400, height=200)
    canvas._tkcanvas.grid(row=4, column=0, pady=10, padx=10)


    # Scatter plot
    fig2, bx = plt.subplots()
    bx.scatter(current_data[x_column], current_data[y_column])
    bx.set_xlabel('Longitude/Latitude')
    bx.set_ylabel("Site Height")
    bx.set_title("Scatter Plot")

    canvas2 = FigureCanvasTkAgg(fig2, master=plot_frame)
    canvas2.draw()

    canvas2.get_tk_widget().grid(row=4, column = 1, pady=10, padx=10)

    canvas2.get_tk_widget().configure(width=400, height=200)
    canvas2._tkcanvas.grid(row=4, columns=1, pady=10, padx=10)








def save_to_json():
    global current_data
    try:
        json_data = current_data.to_json(orient='records')
        save_path = filedialog.asksaveasfilename(defaultextension='.json', filetypes=[("JSON Files", "*.json")])

        if save_path:
            with open(save_path, 'w') as json_file:
                json_file.write(json_data)

            status_label['text'] = "File converted and saved successfully"

        else:
            status_label['text'] = "Save cancelled"

    except Exception as e:
        status_label['text'] = f"Error: {str(e)}"



def load_json():
    global current_data
    file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
    if file_path:
        try:
            with open(file_path, 'r') as json_file:
                json_data = json.load(json_file)
                current_data = pd.DataFrame(json_data)
                print(current_data)
                df_string = current_data.to_string(index=False)
                text_widget.insert(tk.END, df_string)

        except Exception as e:
            print(e)

    else:
        print('no file selected')


                


def load_csv_file():
    global current_data
    file_path = filedialog.askopenfilename(filetypes=[('CSV Files', '.csv')])
    if file_path:
        try:
            if current_data is not None:   
                data = pd.read_csv(file_path, encoding='latin-1')
                current_data = current_data.merge(data)
                print(current_data)
                df_string = current_data.to_string(index=False)
                text_widget.insert(tk.END, df_string)
                
            else:
                current_data = pd.read_csv(file_path, encoding='latin-1')
                print(current_data)
                df_string = current_data.to_string(index=False)
                text_widget.insert(tk.END, df_string)
            
        except Exception as e:
            print(e)


def clear_current_data():
    global current_data
    current_data = None
    print(current_data)
    df_string = current_data.to_string(index=False)
    text_widget.insert(tk.END, df_string)

# GLOBAL VARIABLES

current_data = None
df_string = ''

# GUI

# Create a frame for the controls
# ---------------------------------


# Create the main window
window = tk.Tk()
window.title("AP Assignment")
window.geometry("1800x1000")


# Create frames to hold UI elements

button_frame = tk.Frame(window, bg='lightblue')
button_frame.grid(row=0, column=0, padx=10, sticky='nsew')


text_frame = tk.Frame(window, bg='lightgreen')
text_frame.grid(row=0, column=1, padx=10, sticky='nsew')


plot_frame = tk.Frame(window, bg='yellow')
plot_frame.grid(row=1, column=0, sticky='nsew')


statistics_frame = tk.Frame(window, bg='green', width=600, height=400)
statistics_frame.grid(row=0, column=2, sticky='nw')

# BUTTON UI ELEMENTS

# Create a button to load csv file into dataframesig
load_csv_button = tk.Button(button_frame, text='Load CSV file', command=load_csv_file, width=30)
load_csv_button.grid(row=0, column=0, pady=10, padx=10)

# Create a button to load json file into dataframe
load_json_button = tk.Button(button_frame, text="Load JSON", command=load_json, width=30)
load_json_button.grid(row=0, column=1, pady=10, padx=10)

# Create a button to convert data to json format and save it to a file
convert_button = tk.Button(button_frame, text="Save Data to JSON", command=save_to_json, width=30)
convert_button.grid(row=1, column=0, pady=10, padx=10)

# Create a button to clear the current dataframe
clear_button = tk.Button(button_frame, text='Clear Data', command=clear_current_data, width=30)
clear_button.grid(row=1, column=1, pady=10, padx=10)

# Create a button to display visualisation
visualise_button = tk.Button(button_frame, text='Generate visualisation', command=plot_dataframe, width=30)
visualise_button.grid(row=2, column=0, pady=10, padx=10)

# Create a label to display the status
status_label = tk.Label(button_frame, text="", bg='blue', width=50)
status_label.grid(row=3, column=0, padx=10)


# TEXT UI ELEMENTS

text_widget = tk.Text(text_frame, height=15, width=60)
text_widget.insert(tk.END, df_string)
text_widget.grid(row=0, column=0, pady=10)

vertical_scrollbar = ttk.Scrollbar(text_frame)
vertical_scrollbar.grid(row=0, column=1, sticky='nsew')
vertical_scrollbar.config(command=text_widget.yview)

horizontal_scrollbar = ttk.Scrollbar(text_frame, orient=tk.HORIZONTAL)
horizontal_scrollbar.grid(row=1, sticky='nsew')
horizontal_scrollbar.config(command=text_widget.xview)
# STATISTICS UI ELEMENTS

statistics_label = tk.Label(statistics_frame, text='Statistics', width=60)
statistics_label.grid(row=0, column=0, padx=5, pady=5)

mean_label = tk.Label(statistics_frame, text='Mean:', width=60)
mean_label.grid(row=1, column=0)



# Run the main event loop
window.mainloop()