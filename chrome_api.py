import os
import sys
import platform
import json
import time
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options

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
        with open(config_filepath) as json_data:
            config_dict = json.load(json_data)
    return config_dict
def get_chromedriver_path(webdriver_path):
    chromedriver_path = os.path.join(webdriver_path,"chromedriver-linux64","chromedriver")
    if platform.system().lower()=="windows":
        chromedriver_path = os.path.join(webdriver_path,"chromedriver-win64","chromedriver.exe")
    return chromedriver_path
def get_chromebinary_path(chrome_path,headless):
    binary_path = os.path.join(chrome_path,"chrome-headless-shell-linux64","chrome-headless-shell")
    if platform.system().lower()=="windows":
        if headless:
            binary_path = os.path.join(chrome_path,"chrome-headless-shell-win64","chrome-headless-shell.exe")
        else:
            binary_path = os.path.join(chrome_path,"chrome-win64","chrome.exe")
    return binary_path
def get_favoriate_extension_path(webdriver_path):
    no_google_analytics_path = os.path.join(webdriver_path,"no_google_analytics_1.1.0.0.crx")
    no_ad_path = os.path.join(webdriver_path,"Adblock_3.15.2.0.crx")
    return no_google_analytics_path, no_ad_path
def load_chromdriver_normal(webdriver_path, headless, driver_type, adblock_plus_enable):
    chrome_options = Options()
    chromedriver_path = get_chromedriver_path(webdriver_path)
    chromebinary_path = get_chromebinary_path(webdriver_path,headless)
    # some windows cause: timed out receiving message from renderer
    if adblock_plus_enable:
        # PS: this is ocx version.
        no_google_analytics_path, no_ad_path = get_favoriate_extension_path(webdriver_path)

        if os.path.exists(no_google_analytics_path):
            chrome_options.add_extension(no_google_analytics_path)
        if os.path.exists(no_ad_path):
            chrome_options.add_extension(no_ad_path)

    chrome_options.add_argument('--disable-features=TranslateUI')
    chrome_options.add_argument('--disable-translate')
    chrome_options.add_argument('--lang=zh-TW')

    # for navigator.webdriver
    chrome_options.add_experimental_option("excludeSwitches", ['enable-automation'])
    # Deprecated chrome option is ignored: useAutomationExtension
    #chrome_options.add_experimental_option('useAutomationExtension', False)
    chrome_options.add_experimental_option("prefs", {"credentials_enable_service": False, "profile.password_manager_enabled": False})

    #caps = DesiredCapabilities().CHROME
    chrome_options.set_capability("pageLoadStrategy", "eager")
    chrome_options.set_capability("unhandledPromptBehavior", "accept")

    #caps["pageLoadStrategy"] = u"normal"  #  complete
    #caps["pageLoadStrategy"] = u"eager"  #  interactive
    #caps["pageLoadStrategy"] = u"none"

    #caps["unhandledPromptBehavior"] = u"dismiss and notify"  #  default
    #caps["unhandledPromptBehavior"] = u"ignore"
    #caps["unhandledPromptBehavior"] = u"dismiss"
    #caps["unhandledPromptBehavior"] = u"accept"

    #chrome_options.binary_location = chromebinary_path

    chrome_service = Service(executable_path=chromedriver_path)
    # 合併 capabilities
    chrome_options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    })

    # method 6: Selenium Stealth
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)


    return driver
def get_driver_by_config(config_dict, driver_type):
    global driver
    # read config.
    browser = config_dict["browser"]
    headless = config_dict["headless"]
    print("browser", browser)
    Root_Dir = get_app_root()
    webdriver_path = os.path.join(Root_Dir, "chrome","134")
    print("platform.system().lower():", platform.system().lower())

    adblock_plus_enable = config_dict["advanced"]["adblock_plus_enable"]
    print("adblock_plus_enable:", adblock_plus_enable)
    
    if browser == "chrome":
        # method 6: Selenium Stealth
        if driver_type != "undetected_chromedriver":
            driver = load_chromdriver_normal(webdriver_path, headless, driver_type, adblock_plus_enable)

    return driver
def main():
    config_dict = get_config_dict()

    driver_type = 'selenium'
    #driver_type = 'stealth'
    driver_type = 'undetected_chromedriver'

    driver = None
    if not config_dict is None:
        driver = get_driver_by_config(config_dict, driver_type)
    else:
        print("Load config error!")

    driver.get("https://tixcraft.com/")

    while True:
        time.sleep(1)
if __name__ == "__main__":
    main()