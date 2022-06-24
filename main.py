import os
import json
import keyboard
import pyautogui
import win32gui
from tkinter import *
from tkinter import filedialog

path = None

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

def focusWindow(app):
    win32gui.ShowWindow(app, 5)
    win32gui.SetForegroundWindow(app)

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
    win = Tk()
    win.geometry("560x90")
    win.resizable(False, False)
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

    confirm = Button(frame, text = "OK", width = 6, command = lambda:handleConfirm(win) )
    confirm.grid(row = 2, column = 0, sticky="e" , padx = 5, pady = 5)

    cancel = Button(frame, text = "Cancel", width = 6, command = handleCancel)
    cancel.grid(row = 2, column = 1 , pady = 5)
    
    win.title("Auto-MWB Setup")
    win.mainloop()

def openGUI(data, input):
    createGUI()
    data["settings"]["location"] = path
    data["settings"]["setup"] = True
    input.seek(0)
    json.dump(data, input)
    input.truncate()

def main():
    if __name__ == "__main__":
        with open('config.json', 'r+') as input:
            global path
            data = json.load(input)
            path = data["settings"]["location"]

            if data["settings"]["setup"] == False:
                openGUI(data, input)

            if "mbam.exe" in path:
                try:
                    os.startfile(path)
                    mb = None
                    found = None
                    while mb == None or mb == "":
                        mb = getProcess("malwarebytes free")
                    
                    while True:
                        focusWindow(mb)
                        found = pyautogui.locateCenterOnScreen("scan.png")
                        if found != None:
                            break
                    
                    # move to and click on mwb scan button
                    pyautogui.moveTo(found[0], found[1])
                    pyautogui.click()
                    # minimize mwb window
                    win32gui.ShowWindow(mb, 2)
                except TypeError:
                    print("hello")
            else:
                openGUI(data, input)
        
main()
