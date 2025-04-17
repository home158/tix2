import os
import sys
import platform
import json
import time
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc

def get_app_root():
    # 讀取檔案裡的參數值
    basis = ""
    if hasattr(sys, 'frozen'):
        basis = sys.executable
    else:
        basis = sys.argv[0]
    app_root = os.path.dirname(basis)
    return app_root

def get_config_dict():
    config_json_filename = 'settings.json'
    app_root = get_app_root()
    config_filepath = os.path.join(app_root, config_json_filename)
    config_dict = None
    if os.path.isfile(config_filepath):
        with open(config_filepath, encoding='utf-8') as json_data:
            config_dict = json.load(json_data)
    return config_dict

def load_chromdriver_uc(webdriver_path):
    options = uc.ChromeOptions()
    driver = uc.Chrome(executable_path=webdriver_path)
    return driver
def get_driver_by_config(config_dict, driver_type):
    global driver
    # read config.
    browser = config_dict["browser"]
    print("browser", browser)
    Root_Dir = get_app_root()
    webdriver_path = os.path.join(Root_Dir, "webdriver","135","chromedriver-win64","chromedriver.exe")

    
    driver = load_chromdriver_uc(webdriver_path)
    
            

    return driver
def main():
    config_dict = get_config_dict()

    driver_type = 'undetected_chromedriver'

    if not config_dict is None:
        driver = get_driver_by_config(config_dict, driver_type)
    else:
        print("Load config error!")

    driver.get("https://www.railway.gov.tw/tra-tip-web/tip")


    try:
        # Your code here
        pass
    finally:
        try:
            driver.quit()
        except OSError as e:
            print(f"Error occurred while quitting the driver: {e}")

if __name__ == "__main__":
    main()