"""
Spicetify updater tool installer
by Akakø (https://github.com/Akako0)
last update: 04-23-2023

This program is free software: you can redistribute it and/or modify 
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
GNU General Public License for more details.

Description:
This program is used to install the spicetify updater tool.
Spicetify updater tool is a program that automatically updates spicetify
every x amount of days.
"""

import os
import sys
import datetime


def main():
    global dir_path

    import tkinter as tk
    from tkinter import filedialog
    import requests

    root = tk.Tk()
    root.geometry("500x300")
    root.resizable(False, False)
    root.title("Spicetify updater tool installer  - by Akakø")

    class Install:
        def __init__(self):
            self.console = tk.Text(root, height=10, width=55)
            self.directory_frame = tk.Frame(
                root,
            )
            self.install_path = tk.Text(self.directory_frame, height=1, width=43)
            self.browser_directory = tk.Button(
                self.directory_frame,
                text="Browse",
                command=lambda: browse_directory(),
                width=10,
                height=1,
            )

            self.check_frame = tk.Frame(root)
            self.check_launch_on_startup_var = tk.BooleanVar()
            self.check_launch_on_startup = tk.Checkbutton(
                self.check_frame,
                text="Launch updater on startup",
                width=20,
                height=1,
                variable=self.check_launch_on_startup_var,
            )

            self.bottom_frame = tk.Frame(root)
            self.confirm_frame = tk.Frame(self.bottom_frame)

            self.install_button = tk.Button(
                self.confirm_frame,
                text="Install",
                command=lambda: install_program(),
                height=1,
                width=10,
            )
            self.cancel_button = tk.Button(
                self.confirm_frame,
                text="Cancel",
                command=lambda: sys.exit(),
                height=1,
                width=10,
            )

        def pack(self):
            self.console.pack(pady=10)
            self.directory_frame.pack()
            self.install_path.pack(side=tk.LEFT, padx=10)
            self.browser_directory.pack(side=tk.RIGHT, padx=10)
            self.check_frame.pack(pady=10, side=tk.LEFT)
            self.check_launch_on_startup.pack(side=tk.LEFT, padx=10)
            self.check_launch_on_startup.select()
            self.bottom_frame.pack(side=tk.BOTTOM, fill=tk.X)
            self.confirm_frame.pack(pady=10, side=tk.RIGHT)
            self.install_button.pack(side=tk.LEFT, padx=10)
            self.cancel_button.pack(side=tk.RIGHT, padx=10)

            self.install_path.insert(tk.END, dir_path)

        def unpack(self):
            self.console.pack_forget()
            self.directory_frame.pack_forget()
            self.install_path.pack_forget()
            self.browser_directory.pack_forget()
            self.check_frame.pack_forget()
            self.check_launch_on_startup.pack_forget()
            self.bottom_frame.pack_forget()
            self.confirm_frame.pack_forget()
            self.install_button.pack_forget()
            self.cancel_button.pack_forget()

        def log(self, text):
            now = datetime.datetime.now().strftime("%H:%M:%S")
            self.console.insert(tk.END, f"[{now}]: {text}\n")
            self.console.see(tk.END)

    def install_program():
        urls = [
            "https://raw.githubusercontent.com/Akako0/SpicetifyUpdateTool/main/spicetifyUpdate.bat",
            # "https://raw.githubusercontent.com/Akako0/SpicetifyUpdateTool/main/python_requirements.txt",
            "https://raw.githubusercontent.com/Akako0/SpicetifyUpdateTool/main/update.cache",
            "https://raw.githubusercontent.com/Akako0/SpicetifyUpdateTool/main/update.py",
            "https://raw.githubusercontent.com/Akako0/SpicetifyUpdateTool/main/update.conf",
        ]
        for url in urls:
            install.log(f"Downloading {url}")
            resp = requests.get(url)
            if resp.status_code == 200:
                install.log("Download successful")
                filename = url.split("/")[-1]
                open(
                    install.install_path.get(1.0, tk.END).strip() + f"\\{filename}",
                    "wb",
                ).write(resp.content.replace(b"\r", b""))

                install.log(f"File saved as {filename}")

            elif resp.status_code == 404:
                install.log("Download failed")
                install.log("File not found")
                install.log(
                    "you may have an older version of the installer, \nplease update it or try again later"
                )
                install.log("Installation failed")
                install_failed = True
                break

            else:
                install.log("Download failed")
                install.log("Unknown error")
                install.log("Installation failed")
                install_failed = True
                break
        if install.check_launch_on_startup_var.get():
            Windows10_11_path_startup = "C:/Users/{USERNAME}/AppData/Roaming\Microsoft/Windows/Start Menu/Programs/Startup"
            username = os.getlogin()
            Windows10_11_path_startup = Windows10_11_path_startup.replace(
                "{USERNAME}", username
            )
            install.log("Adding program to startup")
            # create a shortcut to the program in the startup folder
            from win32com.client import Dispatch

            shorcut_path = Windows10_11_path_startup + "\Spicetify updater tool.lnk"
            target = (
                install.install_path.get(1.0, tk.END).strip() + "\spicetifyUpdate.bat"
            )
            wDir = install.install_path.get(1.0, tk.END).strip()
            icon = (
                install.install_path.get(1.0, tk.END).strip() + "\spicetifyUpdate.bat"
            )

            shell = Dispatch("WScript.Shell")
            shortcut = shell.CreateShortCut(shorcut_path)
            shortcut.Targetpath = target
            shortcut.WorkingDirectory = wDir
            shortcut.IconLocation = icon
            shortcut.save()
        install.cancel_button.config(text="Finish")
        install.log("Installation complete")
        install.install_button.config(state=tk.DISABLED)

    def browse_directory():
        install.log("Browsing directory...")
        install_dir = filedialog.askdirectory()
        install.install_path.delete(1.0, tk.END)
        install.install_path.insert(tk.END, install_dir)
        install.log(f"Directory set to {install_dir}")

    install = Install()
    install.log("window initialized")
    install.pack()
    root.mainloop()


def install_requirements():
    global dir_path
    dir_path = os.path.dirname(os.path.realpath(__file__))

    os.chdir(dir_path)
    os.system("pip install -r requirements.txt")


if __name__ == "__main__":
    install_requirements()
    main()
