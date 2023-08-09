import tkinter as tk
from tkinter import filedialog
import pandas as pd
import json


# FUNCTIONS

def convert_to_json():
    file_path = filedialog.askopenfilename(filetypes=[('CSV Files', '.csv')])
    if file_path:
        try:
            df = pd.read_csv(file_path, encoding='latin-1')
            json_data = df.to_json(orient='records')
            save_path = filedialog.asksaveasfilename(defaultextension='json', filetypes=[("JSON Files", "*.json")])

            if save_path:
                with open(save_path, 'w') as json_file:
                    json_file.write(json_data)

                status_label['text'] = "File converted and saved successfully"

            else:
                status_label['text'] = "Save cancelled"

        except Exception as e:
            status_label['text'] = f"Error: {str(e)}"

    else:
        status_label['text'] = "No file selected."


# GUI

# Create the main window
window = tk.Tk()
window.title("AP Assignment")

# Create a button to trigger file selection and conversion
convert_button = tk.Button(window, text="Convert to JSON", command=convert_to_json)
convert_button.pack(pady=10)

# Create a label to display the status
status_label = tk.Label(window, text="")
status_label.pack()

# Run the main event loop
window.mainloop()