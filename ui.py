import tkinter as tk
from tkinter import filedialog, messagebox
from tkinter.scrolledtext import ScrolledText
import subprocess
import os
import json

# Set the color scheme
primary_color = "#f17eac"
secondary_color = "#fafcfe"
background_color = "#edf3fd"
text_color = "#02060e"

# Set the font
font_family = "Arial"
font_size = 8

# Set the button style
button_color = secondary_color
button_text_color = "#FFFFFF"
button_hover_color = "#FF7043"

def browse_file():
    filename = filedialog.askopenfilename(initialdir="input-data")
    if filename:
        entry_file.delete(0, tk.END)
        entry_file.insert(tk.END, filename)

def browse_output_file():
    filename = filedialog.asksaveasfilename(defaultextension=".txt")
    if filename:
        entry_output_file.delete(0, tk.END)
        entry_output_file.insert(tk.END, filename)

def run_ocr():
    input_file = entry_file.get()
    if not input_file:
        messagebox.showerror("Error", "Please select an input file.")
        return

    # Read the configuration file
    with open("config.json") as config_file:
        config = json.load(config_file)
        
    # Set the OCR language
    ocr_language = config["ocr"]["language"]

    try:
        os.chdir("OCR")  # Change directory to OCR folder
        config["ocr"]["input_file"] = input_file  # Update the input file path
        with open("../config.json", "w") as config_file:
            json.dump(config, config_file, indent=4)
        subprocess.run(["python", "ocr.py"])
        messagebox.showinfo("OCR", "OCR script completed successfully.")
        os.chdir("..")  # Change back to the previous directory
        display_output("OCR/ocr_output.txt")
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during OCR: {str(e)}")

def run_gpt():
    input_file = entry_file.get()
    output_file = entry_output_file.get()
    if not input_file:
        messagebox.showerror("Error", "Please select an input file.")
        return

    # Read the configuration file
    with open("config.json") as config_file:
        config = json.load(config_file)

    # Set the GPT prompt
    gpt_prompt = config["gpt"]["prompt"]

    try:
        os.chdir("GPT")  # Change directory to GPT folder
        config["gpt"]["output_file"] = output_file  # Update the output file path
        with open("../config.json", "w") as config_file:
            json.dump(config, config_file, indent=4)
        subprocess.run(["python", "GPTAPI.py"])
        messagebox.showinfo("GPT-3.5", "GPT-3.5 script completed successfully.")
        os.chdir("..")  # Change back to the previous directory
        display_output(output_file)
    except Exception as e:
        messagebox.showerror("Error", f"An error occurred during GPT-3.5: {str(e)}")

def display_output(output_file):
    if not os.path.exists(output_file):
        messagebox.showerror("Error", "Output file not found.")
        return

    with open(output_file, "r") as file:
        output_text = file.read()

    output_window = tk.Toplevel(window)
    output_window.title("Output")
    output_window.geometry("400x300")

    text_output = ScrolledText(output_window, height=15)
    text_output.pack(fill=tk.BOTH, expand=True)
    text_output.insert(tk.END, output_text)
    text_output.configure(state="disabled")

# Read the configuration file
with open("config.json") as config_file:
    config = json.load(config_file)

# Set the input file from the config
input_file_path = config["ocr"]["input_file"]

# Create the main window
window = tk.Tk()
window.title("OCR and GPT-3.5 Scripts UI")
window.geometry("800x500")
window.configure(bg=background_color)

# Create the settings section
label_settings = tk.Label(window, text="Projet d'Intégration", font=(font_family, 16, "bold"), bg=background_color)
label_settings.pack()

# Create the OCR settings section
frame_ocr_settings = tk.Frame(window, bg=background_color)
frame_ocr_settings.pack(pady=10)

label_ocr_settings = tk.Label(frame_ocr_settings, text="OCR Settings", font=(font_family, 14, "bold"), bg=background_color)
label_ocr_settings.pack(anchor=tk.W)

# Create the OCR language selection
frame_ocr_language = tk.Frame(frame_ocr_settings, bg=background_color)
frame_ocr_language.pack(pady=5)

label_ocr_language = tk.Label(frame_ocr_language, text="OCR Language:", font=(font_family, font_size), bg=background_color, fg=text_color)
label_ocr_language.pack(side=tk.LEFT)

entry_ocr_language = tk.Entry(frame_ocr_language, width=20)
entry_ocr_language.pack(side=tk.LEFT)
entry_ocr_language.insert(tk.END, config["ocr"]["language"])

# Create the OCR API key entry
frame_ocr_api_key = tk.Frame(frame_ocr_settings, bg=background_color)
frame_ocr_api_key.pack(pady=5)

label_ocr_api_key = tk.Label(frame_ocr_api_key, text="OCR API Key:", font=(font_family, font_size), bg=background_color, fg=text_color)
label_ocr_api_key.pack(side=tk.LEFT)

entry_ocr_api_key = tk.Entry(frame_ocr_api_key, width=50)
entry_ocr_api_key.pack(side=tk.LEFT)
entry_ocr_api_key.insert(tk.END, config["ocr"]["api_key"])

# Create the file selection widgets
frame_file = tk.Frame(frame_ocr_settings, bg=background_color)
frame_file.pack(anchor=tk.CENTER)  # Set the anchor to CENTER

label_file = tk.Label(frame_file, text="Input File:", font=(font_family, font_size), bg=background_color, fg=text_color)
label_file.pack(side=tk.LEFT)  # Align the label to the left

entry_file_frame = tk.Frame(frame_file, bg=background_color)  # Create a new frame for the entry and button
entry_file_frame.pack()

entry_file = tk.Entry(entry_file_frame, width=50)
entry_file.pack(side=tk.LEFT)  # Align the entry to the left
entry_file.insert(tk.END, input_file_path)

button_browse = tk.Button(entry_file_frame, text="Browse", command=browse_file, bg=primary_color)
button_browse.pack(side=tk.LEFT)  # Align the button to the left

# Create the GPT-3.5 settings section
frame_gpt_settings = tk.Frame(window, bg=background_color)
frame_gpt_settings.pack(pady=20)

label_gpt_settings = tk.Label(frame_gpt_settings, text="GPT-3.5 Settings", font=(font_family, 14, "bold"), bg=background_color)
label_gpt_settings.pack(anchor=tk.W)

# Create the GPT API key entry
frame_gpt_api_key = tk.Frame(frame_gpt_settings, bg=background_color)
frame_gpt_api_key.pack(pady=5)

label_gpt_api_key = tk.Label(frame_gpt_api_key, text="GPT API Key:", font=(font_family, font_size), bg=background_color, fg=text_color)
label_gpt_api_key.pack(side=tk.LEFT)

entry_gpt_api_key = tk.Entry(frame_gpt_api_key, width=50)
entry_gpt_api_key.pack(side=tk.LEFT)
entry_gpt_api_key.insert(tk.END, config["openai"]["api_key"])

# Create the GPT prompt entry
frame_gpt_prompt = tk.Frame(frame_gpt_settings, bg=background_color)
frame_gpt_prompt.pack(pady=5)

label_gpt_prompt = tk.Label(frame_gpt_prompt, text="GPT Prompt:", font=(font_family, font_size), bg=background_color, fg=text_color)
label_gpt_prompt.pack(side=tk.LEFT)

entry_gpt_prompt = ScrolledText(frame_gpt_prompt, width=50, height=5)
entry_gpt_prompt.pack(side=tk.LEFT)
entry_gpt_prompt.insert(tk.END, config["gpt"]["prompt"])

# Create the output file selection widgets
frame_output_file = tk.Frame(frame_gpt_settings, bg=background_color)
frame_output_file.pack(pady=5)  

label_output_file = tk.Label(frame_output_file, text="Output File:", font=(font_family, font_size), bg=background_color, fg=text_color)
label_output_file.pack(side=tk.LEFT)  # Align the label to the left

entry_output_file_frame = tk.Frame(frame_output_file, bg=background_color, width=50)  # Create a new frame for the entry and button
entry_output_file_frame.pack(side=tk.LEFT)

entry_output_file = tk.Entry(entry_output_file_frame, width=50)
entry_output_file.pack(side=tk.LEFT)  # Align the entry to the left
entry_output_file.insert(tk.END, config["gpt"]["output_file"])

button_output_file = tk.Button(entry_output_file_frame, text="Browse", command=browse_output_file, bg=primary_color)
button_output_file.pack(side=tk.LEFT)  # Align the button to the left

def save_settings():
    config["ocr"]["language"] = entry_ocr_language.get()
    config["ocr"]["api_key"] = entry_ocr_api_key.get()
    config["ocr"]["input_file"] = entry_file.get()
    config["openai"]["api_key"] = entry_gpt_api_key.get()
    config["gpt"]["prompt"] = entry_gpt_prompt.get("1.0", tk.END)
    config["gpt"]["output_file"] = entry_output_file.get()
    
    with open("config.json", "w") as config_file:
        json.dump(config, config_file, indent=4)

    messagebox.showinfo("Settings", "Settings saved successfully.")

button_save_settings = tk.Button(window, text="Save Settings", command=save_settings)
button_save_settings.pack()

# Create the OCR and GPT-3.5 run buttons
button_ocr = tk.Button(window, text="Run OCR", command=run_ocr)
button_ocr.pack()

button_gpt = tk.Button(window, text="Run GPT-3.5", command=run_gpt)
button_gpt.pack()

# Start the Tkinter event loop
window.mainloop()
