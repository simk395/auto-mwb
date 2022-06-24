import os
import json
import pyautogui
import win32gui, win32com.client
from tkinter import *
from tkinter import filedialog

path = None
version = None

def windowEnumerationHandler(hwnd, top_windows):
    top_windows.append((hwnd, win32gui.GetWindowText(hwnd)))

def getProcess(app_name):
    app = ''
    top_windows = []
    win32gui.EnumWindows(windowEnumerationHandler, top_windows)
    for i in top_windows:
        if app_name in i[1].lower():
            app = i[0]
            break
    return app
  
def getPath(entry):
    global path
    path = filedialog.askopenfilename(initialdir="/", title="Select file",
                    filetypes=((".exe", "*.exe"),("All Files", "*.*")))
    if path != "":
        entry.configure(state = "normal")
        entry.delete(0,"end")
        entry.insert(0, path)
        entry.configure(state = "disabled")

def handleConfirm(win):
    global path
    if path != "":
        win.destroy()

def handleCancel():
    quit()
    
def createGUI():
    global version
    win = Tk()
    win.geometry("560x90")
    win.resizable(False, False)

    version = IntVar()
    version.set(1)

    frame = Frame(win)
    frame.pack()

    label = Label(frame, text = "Find MalwareBytes executable(mbam.exe)")
    label.grid(row = 0, column = 0)
 
    entry = Entry(frame, width = 80)
    entry.insert(0, path)
    entry.configure(state = "disabled")
    entry.grid(row = 1, column = 0, padx = 5, pady = 5, )

    browse = Button(frame, text = "Browse", width = 6, command = lambda: getPath(entry))
    browse.grid(row = 1, column = 1)

    free = Radiobutton(frame, text = "Free", variable = version, value = 1)
    free.grid(row = 2, column = 0, sticky = "w", padx = 5, pady = 5)

    premium = Radiobutton(frame, text = "Premium Trial", variable = version, value = 2)
    premium.grid(row = 2, column = 0, padx = 5, pady = 5)

    confirm = Button(frame, text = "OK", width = 6, command = lambda:handleConfirm(win) )
    confirm.grid(row = 2, column = 0, sticky="e" , padx = 5, pady = 5)

    cancel = Button(frame, text = "Cancel", width = 6, command = handleCancel)
    cancel.grid(row = 2, column = 1 , pady = 5)
    
    win.title("Auto-MWB Setup")
    win.mainloop()

def openGUI(data, input):
    global version
    createGUI()
    data["settings"]["location"] = path
    data["settings"]["setup"] = True
    version = version.get()

    match version:
        case 1: data["settings"]["presses"] = 11
        case 2: data["settings"]["presses"] = 16
    input.seek(0)
    json.dump(data, input)
    input.truncate()

def main():
    if __name__ == "__main__":
        try:
            with open('config.json', 'r+') as input:
                global path, free
                data = json.load(input)
                path = data["settings"]["location"]

                if data["settings"]["setup"] == False:
                    openGUI(data, input)

                if "mbam.exe" in path:
                    os.startfile(path)
                    free = ""
                    premium = ""
                    while free == "" and premium == "":
                        free = getProcess("malwarebytes free")
                        premium = getProcess("malwarebytes premium trial")

                    fg = None
                    mb = None
                    shell = win32com.client.Dispatch("WScript.Shell")
                    if premium == "":
                        mb = free
                    else:
                        mb = premium
                        
                    while fg != mb:
                        win32gui.ShowWindow(mb, 5)
                        shell.SendKeys('%')
                        win32gui.SetForegroundWindow(mb)
                        fg = win32gui.GetForegroundWindow()
                    
                    pyautogui.press("tab" , presses = data["settings"]["presses"], interval = 0.00000001)
                    pyautogui.press("space")
                else:
                    openGUI(data, input)
                    
        except FileNotFoundError:
            settings = {"settings": {"setup": False,"presses": 11, "location": "C:/Program Files/Malwarebytes/Anti-Malware/mbam.exe"}}
            with open('config.json', 'w') as input:
                json.dump(settings, input)
            main()
                                    
main()
