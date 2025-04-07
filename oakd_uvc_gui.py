import tkinter as tk
from tkinter import messagebox
import subprocess
import threading
import os
import signal
import time

UVC_SCRIPT = "/path to/depthai-python/examples/UVC/uvc_rgb.py" # update this path as per your setup
VENV_ACTIVATE = "/path to/environments/depthai/bin/activate" #update this path as per your setup
uvc_process = None

def is_device_connected():
    try:
        lsusb = subprocess.check_output(["lsusb"]).decode()
        return "03e7:2485" in lsusb
    except Exception:
        return False

def start_uvc():
    global uvc_process
    if uvc_process is not None:
        messagebox.showinfo("Info", "UVC mode is already running.")
        return

    if not is_device_connected():
        messagebox.showerror("Error", "OAK-D device not connected.")
        return

    def run_uvc():
        global uvc_process
        command = f"bash -c 'source {VENV_ACTIVATE} && python {UVC_SCRIPT}'"
        uvc_process = subprocess.Popen(command, shell=True, preexec_fn=os.setsid)

    threading.Thread(target=run_uvc).start()
    status_label.config(text="UVC Running...")

def stop_uvc():
    global uvc_process
    if uvc_process:
        os.killpg(os.getpgid(uvc_process.pid), signal.SIGINT)
        uvc_process = None
        status_label.config(text="Stopped")
        messagebox.showinfo("Info", "UVC mode stopped.")
    else:
        messagebox.showinfo("Info", "UVC mode is not running.")

def update_status():
    if is_device_connected():
        device_status.set("OAK-D connected")
    else:
        device_status.set("OAK-D not found")
    root.after(2000, update_status)

# GUI setup
root = tk.Tk()
root.title("OAK-D Webcam Control")

tk.Label(root, text="OAK-D UVC Control Panel", font=("Arial", 14)).pack(pady=10)

device_status = tk.StringVar()
device_status.set("Checking device...")
tk.Label(root, textvariable=device_status, fg="blue").pack()

status_label = tk.Label(root, text="Status: Idle", fg="green")
status_label.pack(pady=5)

btn_frame = tk.Frame(root)
btn_frame.pack(pady=10)

tk.Button(btn_frame, text="Start Webcam Mode", command=start_uvc, width=20).grid(row=0, column=0, padx=5)
tk.Button(btn_frame, text="Stop Webcam Mode", command=stop_uvc, width=20).grid(row=0, column=1, padx=5)

tk.Button(root, text="Quit", command=root.quit, fg="red").pack(pady=10)

update_status()
root.mainloop()
