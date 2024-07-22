import os
import shutil
from tkinter import Tk, Label, Button, Listbox, filedialog, messagebox, simpledialog
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

root = Tk()
root.title("VersionPathfinder")
root.geometry("600x400")

def select_file():
    global filepath, version_dir, observer, event_handler
    filepath = filedialog.askopenfilename()
    if filepath:
        file_label.config(text=f"Selected File: {filepath}")
        version_dir = os.path.join(os.path.dirname(filepath), ".versions", os.path.basename(filepath))
        os.makedirs(version_dir, exist_ok=True)
        save_button.config(state='normal')
        save_selected_button.config(state='normal')
        refresh_versions()
        start_observer()

def start_observer():
    global observer, event_handler
    event_handler = FileSystemEventHandler()
    event_handler.on_modified = on_modified
    observer = Observer()
    observer.schedule(event_handler, filepath, recursive=False)
    observer.start()

def save_version():
    if not filepath:
        messagebox.showerror("Error", "No file selected")
        return

    version_name = simpledialog.askstring("Save Version", "Enter version name:")
    if version_name:
        version_path = os.path.join(version_dir, version_name)
        shutil.copy2(filepath, version_path)
        messagebox.showinfo("Success", f"Version '{version_name}' saved successfully")
        refresh_versions()

def save_selected_version():
    selection = version_listbox.curselection()
    if selection:
        selected_version = version_listbox.get(selection)
        if selected_version:
            version_path = os.path.join(version_dir, selected_version)
            shutil.copy2(version_path, filepath)
            messagebox.showinfo("Success", f"File updated to version '{selected_version}'")
    else:
        messagebox.showwarning("Warning", "No version selected")

def restore_version(event):
    save_selected_version()

def refresh_versions():
    version_listbox.delete(0, 'end')
    if os.path.exists(version_dir):
        for version in os.listdir(version_dir):
            version_listbox.insert('end', version)

def on_modified(event):
    if event.src_path == filepath:
        save_version()

filepath = ""
version_dir = ""
observer = None
event_handler = None

heading = Label(root, text="VersionPathfinder", font=("Arial", 16))
heading.pack(pady=10)

file_label = Label(root, text="No file selected")
file_label.pack(pady=10)

select_button = Button(root, text="Select File", command=select_file)
select_button.pack(pady=5)

save_button = Button(root, text="Save Version", command=save_version, state='disabled')
save_button.pack(pady=5)

version_listbox = Listbox(root)
version_listbox.pack(pady=10, fill='both', expand=True)
version_listbox.bind('<Double-1>', restore_version)

save_selected_button = Button(root, text="Save Selected Version", command=save_selected_version, state='disabled')
save_selected_button.pack(pady=5)

root.mainloop()