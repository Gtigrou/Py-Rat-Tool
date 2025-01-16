import datetime
import time
import tkinter as tk
import cv2
import numpy as np
import mss
from PIL import Image, ImageTk

class UI:
    def __init__(self):
        self.root = tk.Tk()
        self.root.title("WNCD")
        self.root.iconbitmap("source/icon-WNCD.ico")
        self.root.geometry("960x560")
        #self.root.resizable(False, False)

        self.session = [f"User{i} : 192.168.67.31" for i in range(5)]

        self.load_menu()
        self.load_frame()
        self.show_screen()

    def log(self, str):
        self.consol.config(state="normal")
        self.consol.insert(tk.END, f"[{datetime.datetime.now()}] {str}\n")
        self.consol.config(state="disabled")

    def load_menu(self):
        """Crée et configure le menu principal avec un sous-menu Session"""
        self.mainmenu = tk.Menu(self.root)
        self.root.config(menu=self.mainmenu)

        # Sous-menu "Session"
        session_menu = tk.Menu(self.mainmenu, tearoff=0)
        for i in self.session:
            session_menu.add_command(label=i)
        session_menu.add_separator()
        session_menu.add_command(label="Quitter", command=self.root.quit)

        # Ajout du sous-menu au menu principal
        self.mainmenu.add_cascade(label="Session", menu=session_menu)

    def load_frame(self):
        # Action Frame à droite
        self.actionFrame = tk.Frame(self.root, bg="#fcfcfc", width=192)
        self.actionFrame.pack(side="right", fill="y")

        self.mainFrame = tk.Frame(self.root)
        self.mainFrame.pack(side="left", fill="both", expand=True)

        self.screenFrame = tk.Frame(self.mainFrame, bg="grey", height=432)
        self.screenFrame.pack(fill="x")
        self.screenFrame.pack_propagate(False)

        self.screen = tk.Label(self.screenFrame, bg="grey", text="No Signal")
        self.screen.pack(fill="both", expand=True)

        self.consolFrame = tk.Frame(self.mainFrame, bg="#e0e0e0", height=170)
        self.consolFrame.pack(fill="x")

        self.consol = tk.Text(self.consolFrame, height=5, state="disabled", bg="#e0e0e0")
        self.consol.pack(fill="x")

        self.inputFrame = tk.Frame(self.consolFrame, height=25, bg="#e0e0e0")
        self.inputFrame.pack(side="bottom", fill="x")

        self.userInput = tk.Entry(self.inputFrame)
        self.userInput.pack(side="left", fill="x", expand=True)

        self.sendButton = tk.Button(self.inputFrame, text=".EXE", width=10)
        self.sendButton.pack(side="right", fill="x")

    def show_screen(self):
        pass

    def call(self, obj, func_name):
        method = getattr(obj, func_name, None)
        if callable(method):
            method()
        else:
            self.log(f"La fonction '{func_name}' n'existe pas sur l'objet.")

    def run(self):
        """Démarre la boucle principale de Tkinter"""
        app.log("Initialization Success")
        self.root.mainloop()
        exit()

class COMMAND:
    def __init__(self):
        self.COMMAND_LIST = []

# Lancement de l'interface
if __name__ == '__main__':
    app = UI()
    app.run()
