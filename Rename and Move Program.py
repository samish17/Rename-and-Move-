import os
import shutil
import tkinter as tk
from tkinter import filedialog, messagebox


def get_next_file_number(target_directory):
    """
    Find the next available number for renaming files in the target directory.
    """
    existing_numbers = []
    for file_name in os.listdir(target_directory):
        if file_name.isdigit() or file_name.split(".")[0].isdigit():
            # Extract the numeric part of the file name
            number = int(os.path.splitext(file_name)[0])
            existing_numbers.append(number)

    # Get the next number after the highest one
    return max(existing_numbers, default=0) + 1


def get_unique_file_name(directory, file_name):
    """
    Generate a unique file name if the file already exists in the directory.
    """
    base_name, extension = os.path.splitext(file_name)
    counter = 1
    unique_name = file_name
    while os.path.exists(os.path.join(directory, unique_name)):
        unique_name = f"{base_name}_{counter}{extension}"
        counter += 1
    return unique_name


def move_and_rename_files(source_directory, target_directory):
    if not os.path.exists(target_directory):
        os.makedirs(target_directory)

    # Determine the starting file number
    file_count = get_next_file_number(target_directory)

    # Iterate through all folders in the source directory
    for folder_name in os.listdir(source_directory):
        folder_path = os.path.join(source_directory, folder_name)

        if os.path.isdir(folder_path):  # Ensure it's a folder
            for file_name in os.listdir(folder_path):
                file_path = os.path.join(folder_path, file_name)

                # Check if it is a file
                if os.path.isfile(file_path):
                    # Create a new file name with an incrementing counter
                    file_extension = os.path.splitext(file_name)[1]  # Preserve file extension
                    new_file_name = f"{file_count}{file_extension}"
                    new_file_name = get_unique_file_name(target_directory, new_file_name)
                    new_file_path = os.path.join(target_directory, new_file_name)

                    # Move and rename the file
                    try:
                        shutil.move(file_path, new_file_path)
                        print(f"Moved and renamed: {file_path} -> {new_file_path}")
                        file_count += 1
                    except Exception as e:
                        messagebox.showerror("Error", f"Failed to move {file_path}: {e}")
                        return

    messagebox.showinfo("Success", f"Processed {file_count - 1} files successfully!")


def select_source_directory():
    folder = filedialog.askdirectory(title="Select Source Directory")
    if folder:
        source_var.set(folder)


def select_target_directory():
    folder = filedialog.askdirectory(title="Select Target Directory")
    if folder:
        target_var.set(folder)


def process_files():
    source_directory = source_var.get()
    target_directory = target_var.get()

    if not source_directory or not target_directory:
        messagebox.showwarning("Warning", "Please select both source and target directories.")
        return

    if not os.path.exists(source_directory):
        messagebox.showerror("Error", "Source directory does not exist.")
        return

    move_and_rename_files(source_directory, target_directory)


# Create the main tkinter window
root = tk.Tk()
root.title("File Renamer and Mover")

# Variables to store directory paths
source_var = tk.StringVar()
target_var = tk.StringVar()

# Create and arrange GUI elements
tk.Label(root, text="Made by Samish.", font=("Helvetica", 16, "bold"), fg="black").grid(row=0, column=0, columnspan=3, pady=10)

tk.Label(root, text="Source Directory:").grid(row=1, column=0, padx=10, pady=5, sticky="w")
tk.Entry(root, textvariable=source_var, width=50).grid(row=1, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=select_source_directory).grid(row=1, column=2, padx=10, pady=5)

tk.Label(root, text="Target Directory:").grid(row=2, column=0, padx=10, pady=5, sticky="w")
tk.Entry(root, textvariable=target_var, width=50).grid(row=2, column=1, padx=10, pady=5)
tk.Button(root, text="Browse", command=select_target_directory).grid(row=2, column=2, padx=10, pady=5)

tk.Button(root, text="Process Files", command=process_files, bg="green", fg="white").grid(row=3, column=0, columnspan=3, pady=20)

# Start the GUI event loop
root.mainloop()
