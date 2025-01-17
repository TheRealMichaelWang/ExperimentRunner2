import tkinter as tk
from tkinter import ttk, messagebox
import os
import csv
from datetime import datetime

def get_experiment_info():
    def on_continue():
        name = name_entry.get().strip()
        if not name:
            messagebox.showerror("Error", "Please enter a participant name.")
            return
        protocol = protocol_var.get()
        date = datetime.now().strftime("%Y%m%d")
        root.destroy()
        root.result = (name, protocol, date)

    def on_cancel():
        root.destroy()
        root.result = None

    root = tk.Tk()
    root.title("Experiment Information")
    root.geometry("300x200")

    tk.Label(root, text="Participant Name:").pack(pady=5)
    name_entry = tk.Entry(root)
    name_entry.pack(pady=5)

    tk.Label(root, text="Protocol:").pack(pady=5)
    protocol_var = tk.StringVar(value="Protocol A")
    protocol_dropdown = ttk.Combobox(root, textvariable=protocol_var, values=["Protocol A"])
    protocol_dropdown.pack(pady=5)

    tk.Button(root, text="Continue", command=on_continue).pack(side=tk.LEFT, padx=10, pady=20)
    tk.Button(root, text="Cancel", command=on_cancel).pack(side=tk.RIGHT, padx=10, pady=20)

    #run the gui
    root.result = None
    root.mainloop()
    return root.result

def create_experiment_structure(name, protocol, date):
    base_dir = "BaselineFolder"  # Placeholder base directory
    data_dir = os.path.join(base_dir, "Data", date)
    os.makedirs(data_dir, exist_ok=True)

    experiment_num = 1
    while os.path.exists(os.path.join(data_dir, f"Experiment {experiment_num}")):
        experiment_num += 1

    experiment_dir = os.path.join(data_dir, f"Experiment {experiment_num}")
    os.makedirs(experiment_dir)

    metadata_file = os.path.join(experiment_dir, "metadata.csv")
    current_time = datetime.now().strftime("%H%M%S")

    with open(metadata_file, 'w', newline='') as csvfile:
        writer = csv.writer(csvfile)
        writer.writerow(["Participant Name", name])
        writer.writerow(["Protocol", protocol])
        writer.writerow(["Date", date])
        writer.writerow(["Time", current_time])

    return experiment_dir

# Main execution
if __name__ == "__main__":
    experiment_info = get_experiment_info()
    if experiment_info:
        name, protocol, date = experiment_info
        experiment_dir = create_experiment_structure(name, protocol, date)
        print(f"Experiment structure created at: {experiment_dir}")
    else:
        print("Operation cancelled by user.")