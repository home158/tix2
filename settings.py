import sys
import os
import json
from tkinter import Tk
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
CONST_APP_VERSION = u"MaxBot (2025.03.23)"
import platform
def get_default_config():
    config_dict={}

    config_dict['debug']=False

    return config_dict

def get_app_root():
    # 讀取檔案裡的參數值
    basis = ""
    
    # 檢查是否為凍結（打包）執行
    if hasattr(sys, 'frozen'):
        basis = sys.executable  # 取得執行檔（如 .exe）的路徑
    else:
        basis = sys.argv[0]  # 取得 Python 腳本的路徑
    # 取得應用程式的根目錄
    app_root = os.path.dirname(basis)
    
    return app_root

def load_json():
    app_root = get_app_root()
    # overwrite config path.
    config_filepath = os.path.join(app_root, 'settings.json')

    config_dict = None
    if os.path.isfile(config_filepath):
        with open(config_filepath) as json_data:
            config_dict = json.load(json_data)
    else:
        config_dict = get_default_config()
    return config_filepath, config_dict
def clearFrame(frame):
    # destroy all widgets from frame
    for widget in frame.winfo_children():
       widget.destroy()
def get_language_code_by_name(new_language):
    language_code = "en_us"
    if u'繁體中文' in new_language:
        language_code = 'zh_tw'
    if u'簡体中文' in new_language:
        language_code = 'zh_cn'
    if u'日本語' in new_language:
        language_code = 'ja_jp'
    #print("new language code:", language_code)

    return language_code
def load_translate():
    translate = {}
    en_us={}
    en_us["preference"] = 'Preference'
    en_us["advanced"] = 'Advanced'
    en_us["about"] = 'About'
    translate['en_us']=en_us
    return translate
def load_GUI(root, config_dict):
    clearFrame(root)
    language_code="en_us"
    if not config_dict is None:
        if u'language' in config_dict:
            language_code = get_language_code_by_name(config_dict["language"])
    row_count = 2

    global tabControl
    tabControl = ttk.Notebook(root)
    tab1 = Frame(tabControl)
    tabControl.add(tab1, text=translate[language_code]['preference'])
    tab2 = Frame(tabControl)
    tabControl.add(tab2, text=translate[language_code]['advanced'])
    tab3 = Frame(tabControl)
    tabControl.add(tab3, text=translate[language_code]['about'])
    tabControl.grid(column=0, row=0)

def main():
    global translate
    # only need to load translate once.
    translate = load_translate()
    global config_filepath
    global config_dict
    # only need to load json file once.
    config_filepath, config_dict = load_json()

    print(config_filepath)
    print(config_dict)

    root = Tk()  # 直接初始化 root，不需要 global
    root.title(CONST_APP_VERSION)
    global UI_PADDING_X
    UI_PADDING_X = 15
    load_GUI(root, config_dict)

    GUI_SIZE_WIDTH = 460
    GUI_SIZE_HEIGHT = 615

    GUI_SIZE_MACOS = str(GUI_SIZE_WIDTH) + 'x' + str(GUI_SIZE_HEIGHT)
    GUI_SIZE_WINDOWS=str(GUI_SIZE_WIDTH-60) + 'x' + str(GUI_SIZE_HEIGHT-90)

    GUI_SIZE =GUI_SIZE_MACOS
    
    print(GUI_SIZE)
    if platform.system() == 'Windows':
        GUI_SIZE = GUI_SIZE_WINDOWS

    root.geometry(GUI_SIZE)
    # 這裡可以加上 root.mainloop() 來啟動 GUI 迴圈
    root.mainloop()


if __name__ == "__main__":
    main()