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
    
    try:
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
        canvas.get_tk_widget().grid(row=1, column=0, pady=10, padx=10)


        # Set the Matplotlib figure as the plot area
        canvas.get_tk_widget().configure(width=400, height=200)
        canvas._tkcanvas.grid(row=1, column=0, pady=10, padx=10)


        # Scatter plot
        fig2, bx = plt.subplots()
        bx.scatter(current_data[x_column], current_data[y_column])
        bx.set_xlabel('Longitude/Latitude')
        bx.set_ylabel("Site Height")
        bx.set_title("Scatter Plot")

        canvas2 = FigureCanvasTkAgg(fig2, master=plot_frame)
        canvas2.draw()
        canvas2.get_tk_widget().grid(row=2, column = 0, pady=10, padx=10)
        canvas2.get_tk_widget().configure(width=400, height=200)
        canvas2._tkcanvas.grid(row=2, column=0, pady=10, padx=10)

        status_label['text'] = "Visualisations generated successfully"

    except Exception as e:
        status_label['text'] = f"Error: {str(e)}"




def save_to_json():
    global current_data
    try:
        json_data = current_data.to_json(orient='records')
        save_path = filedialog.asksaveasfilename(defaultextension='.json', filetypes=[("JSON Files", "*.json")])

        if save_path:
            with open(save_path, 'w') as json_file:
                json_file.write(json_data)

            status_label['text'] = "Data converted to JSON format and saved successfully"

        else:
            status_label['text'] = "Save cancelled"

    except Exception as e:
        status_label['text'] = f"Error: {str(e)}"



def load_json():
    global current_data, records
    file_path = filedialog.askopenfilename(filetypes=[("JSON Files", "*.json")])
    if file_path:
        try:
            with open(file_path, 'r') as json_file:
                json_data = json.load(json_file)
                current_data = pd.DataFrame(json_data)
                status_label['text'] = "JSON data loaded successfully"
                df_string = current_data.to_string(index=False, col_space=25, justify='left')
                records = df_string.strip().split('\n')
                text_widget.delete('1.0', tk.END)
                for record in records:
                    text_widget.insert(tk.END, record + '\n')

        except Exception as e:
            status_label['text'] = f"Error: {str(e)}"

    else:
        status_label['text'] = "No file selected"


                


def load_csv_file():
    global current_data
    file_path = filedialog.askopenfilename(filetypes=[('CSV Files', '.csv')])
    if file_path:
        try:
            if current_data is not None:   
                data = pd.read_csv(file_path, encoding='latin-1')
                current_data = current_data.merge(data)
                status_label['text'] = "Data merged successfully"
                df_string = current_data.to_string(index=False, col_space=25, justify='left')
                records = df_string.strip().split('\n')
                text_widget.delete('1.0', tk.END)
                for record in records:
                    text_widget.insert(tk.END, record + '\n')
                
            else:
                current_data = pd.read_csv(file_path, encoding='latin-1')
                status_label['text'] = "Data loaded from csv file successfully"
                df_string = current_data.to_string(index=False, col_space=25, justify='left')
                records = df_string.strip().split('\n')
                text_widget.delete('1.0', tk.END)
                for record in records:
                    text_widget.insert(tk.END, record + '\n')
            
        except Exception as e:
            status_label['text'] = f"Error: {str(e)}"


def clear_current_data():
    global current_data
    current_data = None
    status_label['text'] = "Current data deleted"
    text_widget.delete('1.0', tk.END)
    text_widget.insert(tk.END, 'No data loaded...')

def clean_data():
    global current_data
    try:
        # 1.
        ngr_to_exclude = ['NZ02553847', 'SE213515', 'NT05399374', 'NT25265908']
        current_data = current_data[~current_data['NGR'].isin(ngr_to_exclude)]
        df_string = current_data.to_string(index=False, col_space=25, justify='left')
        records = df_string.strip().split('\n')
        text_widget.delete('1.0', tk.END)
        for record in records:
            text_widget.insert(tk.END, record + '\n')

        # 2. Create new columns for each DAB multiplex

        current_data[['C18A', 'C18F', 'C188']] = current_data['EID'].str.extract('(C18A|C18F|C188)')

        # Join each category to the 'NGR' column
        current_data['NGR_C18A'] = current_data['NGR'] + ' ' + current_data['C18A']
        current_data['NGR_C18F'] = current_data['NGR'] + ' ' + current_data['C18F']
        current_data['NGR_C188'] = current_data['NGR'] + ' ' + current_data['C188']

        # Rename the columns 'In-Use Ae Ht' and 'In-Use ERP Total':
        # current_data = current_data.rename(columns={'In-Use Ae Ht': 'Aerial height(m)', 'In-Use ERP Total': 'Power(kW)'})

               
        status_label['text'] = "Data cleaned"
    except Exception as e:
        status_label['text'] = f"Error: {str(e)}"

# GLOBAL VARIABLES -------------------------

current_data = None
df_string = ''
records = []

# GUI ----------------------------------------

# Create the main window
window = tk.Tk()
window.title("AP Assignment")
window.geometry("1800x1000")
window.protocol("WM_DELETE_WINDOW", window.quit())


# Create frames to hold UI elements

button_frame = tk.Frame(window, bg='lightblue', width=270, height=400)
button_frame.grid(row=0, column=0, sticky='nsew')

text_frame = tk.Frame(window, bg='lightgreen', width=800, height=400)
text_frame.grid(row=0, column=1, sticky='nsew')

plot_frame = tk.Frame(window, bg='yellow', width=800, height=400)
plot_frame.grid(row=1, column=1, sticky='nsew')

statistics_frame = tk.Frame(window, bg='green', width=600, height=400)
statistics_frame.grid(row=1, column=0, sticky='nw')

# BUTTON UI ELEMENTS

controls_label = tk.Label(button_frame, text='Controls', bg='lightgrey', width=80)
controls_label.grid(row=0, column=0, padx=5, pady=5, sticky='w', columnspan=2)

# Create a button to load csv file into dataframesig
load_csv_button = tk.Button(button_frame, text='Load CSV file', command=load_csv_file, width=30)
load_csv_button.grid(row=1, column=0, pady=10, padx=10)

# Create a button to load json file into dataframe
load_json_button = tk.Button(button_frame, text="Load JSON", command=load_json, width=30)
load_json_button.grid(row=1, column=1, pady=10, padx=10)

# Create a button to convert data to json format and save it to a file
convert_button = tk.Button(button_frame, text="Save Data to JSON", command=save_to_json, width=30)
convert_button.grid(row=2, column=0, pady=10, padx=10)

# Create a button to clear the current dataframe
clear_button = tk.Button(button_frame, text='Clear Data', command=clear_current_data, width=30)
clear_button.grid(row=2, column=1, pady=10, padx=10)

# Create a button to display visualisation
visualise_button = tk.Button(button_frame, text='Generate visualisation', command=plot_dataframe, width=30)
visualise_button.grid(row=3, column=0, pady=10, padx=10)


# Create a button to clean the data according to client specifications
clean_button = tk.Button(button_frame, text='Clean Data', command=clean_data, width=30)
clean_button.grid(row=3, column=1, pady=10, padx=10)

# Create a label to display the status
status_label = tk.Label(button_frame, text="", bg='white', width=70, height=5)
status_label.grid(row=4, column=0, padx=10, columnspan=2)


# TEXT UI ELEMENTS

text_label = tk.Label(text_frame, text='Data read out', bg='lightgrey', width=120)
text_label.grid(row=0, column=0, padx=5, pady=5, sticky='w', columnspan=2)

text_widget = tk.Text(text_frame, height=20, width=120, wrap='none')
text_widget.insert(tk.END, df_string)
text_widget.grid(row=1, column=0, pady=10)


vertical_scrollbar = ttk.Scrollbar(text_frame)
vertical_scrollbar.grid(row=1, column=1, sticky='nsew')
vertical_scrollbar.config(command=text_widget.yview)
text_widget.configure(yscrollcommand=vertical_scrollbar.set)

horizontal_scrollbar = ttk.Scrollbar(text_frame, orient=tk.HORIZONTAL)
horizontal_scrollbar.grid(row=2, sticky='nsew')
horizontal_scrollbar.config(command=text_widget.xview)
text_widget.configure(xscrollcommand=horizontal_scrollbar.set)


# STATISTICS UI ELEMENTS

statistics_label = tk.Label(statistics_frame, text='Statistics', width=80, bg='lightgrey')
statistics_label.grid(row=0, column=0, padx=5, pady=5, columnspan=2)

# MEAN
mean_label = tk.Label(statistics_frame, text='Mean:', width=30, bg='lightgrey')
mean_label.grid(row=1, column=0, sticky='w', padx=5, pady=5)

mean_display = tk.Label(statistics_frame, bg='white', width=30)
mean_display.grid(row=1, column=1, padx=5, pady=5, sticky='w')

# MODE
mode_label = tk.Label(statistics_frame, text='Mode:', width=30, bg='lightgrey')
mode_label.grid(row=2, column=0, padx=5, pady=5, sticky='w')

mode_display = tk.Label(statistics_frame, text='', width=30, bg='white')
mode_display.grid(row=2, column=1, padx=5, pady=5, sticky='w')

# MEDIAN
median_label = tk.Label(statistics_frame, text='Median:', width=30, bg='lightgrey')
median_label.grid(row=3, column=0, padx=5, pady=5, sticky='w')

median_display = tk.Label(statistics_frame, text='', bg='white', width=30)
median_display.grid(row=3, column=1, padx=5, pady=5, sticky='w')


# DISPLAY UI ELEMENTS

display_label = tk.Label(plot_frame, text='Display', bg='lightgrey', width=100)
display_label.grid(row=0, column=0, padx=5, pady=5, sticky='w')



# Run the main event loop
window.mainloop()