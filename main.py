import tkinter as tk
from tkinter import filedialog
import pandas as pd
import json

# FUNCTIONS

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
                
            else:
                current_data = pd.read_csv(file_path, encoding='latin-1')
                print(current_data)
            
        except Exception as e:
            print(e)


def clear_current_data():
    global current_data
    current_data = None
    print(current_data)

# GLOBAL VARIABLES

current_data = None

# GUI

# Create the main window
window = tk.Tk()
window.title("AP Assignment")
window.geometry("500x500")

# Create a button to load csv file into dataframesig
load_csv_button = tk.Button(window, text='Load CSV file', command=load_csv_file)
load_csv_button.pack(pady=10)

# Create a button to load json file into dataframe
load_json_button = tk.Button(window, text="Load JSON", command=load_json)
load_json_button.pack(pady=10)

# Create a button to convert data to json format and save it to a file
convert_button = tk.Button(window, text="Save Data to JSON", command=save_to_json)
convert_button.pack(pady=10)

# Create a button to clear the current dataframe
clear_button = tk.Button(window, text='Clear Data', command=clear_current_data)
clear_button.pack(pady=10)

# Create a label to display the status
status_label = tk.Label(window, text="", bg='blue', width=50)
status_label.pack()

# Run the main event loop
window.mainloop()