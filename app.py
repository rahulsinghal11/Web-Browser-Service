from flask import Flask
import webbrowser
from flask import request
from pywinauto import Application
import os
import shutil
import uiautomation as auto

app = Flask(__name__)

@app.route('/')
def connect():
    print("Connected")

@app.route('/start')
def getURL():
    browser = request.args.get('browser')
    url = request.args.get('url')
    if browser == "firefox":
        webbrowser.open('url')
    else:
        webbrowser.register('chrome', None, webbrowser.BackgroundBrowser("C://Program Files//Google//Chrome//Application//chrome.exe"))
        webbrowser.get('chrome').open_new_tab(url)

@app.route('/geturl')
def currentURL():
    browser = request.args.get('browser')
    window_index = 1
    if browser == "firefox":
        addr_bar = auto.Control(Depth=1, ClassName='MozillaWindowClass', foundIndex=window_index).ToolBarControl(AutomationId='nav-bar').ComboBoxControl(Depth=1, foundIndex=1).EditControl(Depth=1, foundIndex=1)
        print(addr_bar.GetValuePattern().Value)
    else:
        win = auto.Control(Depth=1, ClassName='Chrome_WidgetWin_1', SubName=browser_name, foundIndex=window_index)
        win_pane = win.PaneControl(Depth=1, Compare=lambda control, _depth: control.Name != '')
            

@app.route('/stop')
def close():
    browser = request.args.get('browser')
    if browser == "firefox":
        os.system("taskkill /im firefox.exe /f")
    else:
        os.system("taskkill /im chrome.exe /f")

@app.route('/cleanup')
def delete():
    browser = request.args.get('browser')
    firefox_path = os.path.join("C:",os.sep,"Users", "rahul", "AppData", "Roaming","Mozilla","Firefox","Profiles", "test")
    chrome_path = os.path.join("C:",os.sep,"Users", "rahul", "AppData", "Local","Google","Chrome","User Data","Default")   
    os.chmod(firefox_path, 0o777)
    if browser == "firefox":        
        for dir in os.listdir(firefox_path):
            shutil.rmtree(os.path.join(firefox_path,dir))
        print("Cleanup successful")
    else:
        for dir in os.listdir(chrome_path):
            shutil.rmtree(os.path.join(chrome_path,dir))
        print("Cleanup successful")


if __name__ == "__main__":
    app.run(debug=True)

