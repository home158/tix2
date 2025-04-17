import os
import sys
import platform
import json
import time
import random
from selenium import webdriver
from selenium.webdriver.chrome.service import Service
from selenium.common.exceptions import NoSuchWindowException
from selenium.common.exceptions import UnexpectedAlertPresentException
from selenium.common.exceptions import NoAlertPresentException
from selenium.common.exceptions import WebDriverException
from selenium_stealth import stealth

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
        with open(config_filepath, "r", encoding="utf-8") as json_data:
            config_dict = json.load(json_data)
    return config_dict
def load_chromdriver_normal(webdriver_path, driver_type, adblock_plus_enable):
    chrome_options = webdriver.ChromeOptions()

    chromedriver_path = get_chromedriver_path(webdriver_path)

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

    chrome_service = Service(chromedriver_path)
    # 合併 capabilities
    chrome_options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    })

    # method 6: Selenium Stealth
    driver = webdriver.Chrome(service=chrome_service, options=chrome_options)

    if driver_type=="stealth":
        # Selenium Stealth settings
        stealth(driver,
              languages=["zh-TW", "zh"],
              vendor="Google Inc.",
              platform="Win32",
              webgl_vendor="Intel Inc.",
              renderer="Intel Iris OpenGL Engine",
              fix_hairline=True,
          )
    #print("driver capabilities", driver.capabilities)

    return driver
def get_chromedriver_path(webdriver_path):
    if platform.system().lower()=="windows":
        chromedriver_path = os.path.join(webdriver_path,"chromedriver.exe")
    return chromedriver_path
def get_favoriate_extension_path(webdriver_path):
    no_google_analytics_path = os.path.join(webdriver_path,"no_google_analytics_1.1.0.0.crx")
    no_ad_path = os.path.join(webdriver_path,"Adblock_3.15.2.0.crx")
    return no_google_analytics_path, no_ad_path

def load_chromdriver_uc(webdriver_path,chrome_path, adblock_plus_enable):
    import undetected_chromedriver as uc

    chromedriver_path = get_chromedriver_path(webdriver_path)

    options = uc.ChromeOptions()
    options.page_load_strategy="eager"

    #print("strategy", options.page_load_strategy)

    if adblock_plus_enable:
        no_google_analytics_path, no_ad_path = get_favoriate_extension_path(webdriver_path)
        no_google_analytics_folder_path = no_google_analytics_path.replace('.crx','')
        no_ad_folder_path = no_ad_path.replace('.crx','')
        load_extension_path = ""
        if os.path.exists(no_google_analytics_folder_path):
            load_extension_path += "," + no_google_analytics_folder_path
        if os.path.exists(no_ad_folder_path):
            load_extension_path += "," + no_ad_folder_path
        if len(load_extension_path) > 0:
            options.add_argument('--load-extension=' + load_extension_path[1:])

    options.add_argument('--disable-features=TranslateUI')
    options.add_argument('--disable-translate')
    options.add_argument('--lang=zh-TW')
    options.add_argument("--disable-blink-features=AutomationControlled")

    options.add_argument("--password-store=basic")
    options.add_experimental_option("prefs", 
            {
                "credentials_enable_service": False, 
                "profile.password_manager_enabled": False
            }
    )
    options.binary_location = chrome_path
    caps = options.to_capabilities()
    caps["unhandledPromptBehavior"] = u"accept"

    driver = None
    if os.path.exists(chromedriver_path):
        print("Use user driver path:", chromedriver_path)
        is_local_chrome_browser_lower = False
        try:
            driver = uc.Chrome(executable_path=chromedriver_path, options=options, desired_capabilities=caps, suppress_welcome=False)
        except Exception as exc:
            if "cannot connect to chrome" in str(exc):
                if "This version of ChromeDriver only supports Chrome version" in str(exc):
                    is_local_chrome_browser_lower = True
            print(exc)
            pass

        if is_local_chrome_browser_lower:
            print("Use local user downloaded chromedriver to lunch chrome browser.")
            driver_type = "selenium"
            driver = load_chromdriver_normal(webdriver_path, driver_type, adblock_plus_enable)
    else:
        print("Oops! web driver not on path:",chromedriver_path )
        print('let uc automatically download chromedriver.')
        driver = uc.Chrome(options=options, desired_capabilities=caps, suppress_welcome=False)
        stealth(driver,
            languages=["zh-TW", "zh"],
            vendor="Google Inc.",
            platform="Win32",
            webgl_vendor="Intel Inc.",
            renderer="Intel Iris OpenGL Engine",
            fix_hairline=True,
        )

    if driver is None:
        print("create web drive object fail!")
    else:
        download_dir_path="."
        params = {
            "behavior": "allow",
            "downloadPath": os.path.realpath(download_dir_path)
        }
        #print("assign setDownloadBehavior.")
        driver.execute_cdp_cmd("Page.setDownloadBehavior", params)
    #print("driver capabilities", driver.capabilities)

    return driver

def get_driver_by_config(config_dict, driver_type):
    global driver
    # read config.
    browser = config_dict["browser"]
    browse_version = config_dict["browse_version"]
    print("browser", browser)
    Root_Dir = get_app_root()
    webdriver_path = os.path.join(Root_Dir, "webdriver", browse_version )
    chrome_path = os.path.join(Root_Dir, browser , browse_version , "GoogleChromePortable.exe")
    print("platform.system().lower():", platform.system().lower())

    adblock_plus_enable = config_dict["advanced"]["adblock_plus_enable"]
    print("adblock_plus_enable:", adblock_plus_enable)
    
    if browser == "chrome":
        # method 6: Selenium Stealth
        if driver_type != "undetected_chromedriver":
            driver = load_chromdriver_normal(webdriver_path, driver_type, adblock_plus_enable)
        else:
            # method 5: uc
            # multiprocessing not work bug.
            if platform.system().lower()=="windows":
                if hasattr(sys, 'frozen'):
                    from multiprocessing import freeze_support
                    freeze_support()
            driver = load_chromdriver_uc(webdriver_path,chrome_path, adblock_plus_enable)

    return driver
def smart_form_filler(driver,section):
    config_dict = get_config_dict()
    formfillers = config_dict[section]["smart_form_filler"]
    for formfiller in formfillers:
        script_str = """
        var element = document.querySelector("{}");
        if (element) {{
            element.value = "{}";
            element.dispatchEvent(new Event("input"));
        }}
        """
        formatted_script = script_str.format(formfiller["selector"], formfiller["value"])
        
        print(formatted_script)  # Debugging
        driver.execute_script(formatted_script)

def main():
    config_dict = get_config_dict()

    driver_type = 'selenium'
    driver_type = 'undetected_chromedriver'

    driver = None
    if not config_dict is None:
        driver = get_driver_by_config(config_dict, driver_type)
    else:
        print("Load config error!")

    # internal variable. 說明：這是一個內部變數，請略過。
    url = ""
    last_url = ""



    DISCONNECTED_MSG = 'Unable to evaluate script: no such window: target window already closed'

    debugMode = False
    if 'debug' in config_dict:
        debugMode = config_dict["debug"]
    if debugMode:
        print("Start to looping, detect browser url...")


    driver.get("https://www.railway.gov.tw/tra-tip-web/tip")

    while True:
        time.sleep(2)

        is_alert_popup = False

        # pass if driver not loaded.
        if driver is None:
            print("web driver not accessible!")
            break

        #is_alert_popup = check_pop_alert(driver)

        #MUST "do nothing: if alert popup.
        #print("is_alert_popup:", is_alert_popup)
        if is_alert_popup:
            continue

        url = ""
        try:
            url = driver.current_url
        except NoSuchWindowException:
            print('NoSuchWindowException at this url:', url )
            if DISCONNECTED_MSG in driver.get_log('driver')[-1]['message']:
                print('quit bot by NoSuchWindowException')
                driver.quit()
                driver = None  # 避免 __del__() 之後還會執行 quit()
                sys.exit()
                break
            try:
                window_handles_count = len(driver.window_handles)
                if window_handles_count > 1:
                    driver.switch_to.window(driver.window_handles[0])
            except Exception as excSwithFail:
                pass
        except UnexpectedAlertPresentException as exc1:
            # PS: DON'T remove this line.
            is_verifyCode_editing = False
            print('UnexpectedAlertPresentException at this url:', url )
            #time.sleep(3.5)
            # PS: do nothing...
            # PS: current chrome-driver + chrome call current_url cause alert/prompt dialog disappear!
            # raise exception at selenium/webdriver/remote/errorhandler.py
            # after dialog disappear new excpetion: unhandled inspector error: Not attached to an active page
            is_pass_alert = False
            is_pass_alert = True
            if is_pass_alert:
                try:
                    driver.switch_to.alert.accept()
                except Exception as exc:
                    pass

        except Exception as exc:
            is_verifyCode_editing = False


            #UnicodeEncodeError: 'ascii' codec can't encode characters in position 63-72: ordinal not in range(128)
            str_exc = ""
            try:
                str_exc = str(exc)
            except Exception as exc2:
                pass

            if len(str_exc)==0:
                str_exc = repr(exc)

            exit_bot_error_strings = [u'Max retries exceeded'
            , u'chrome not reachable'
            , u'unable to connect to renderer'
            , u'failed to check if window was closed'
            , u'Failed to establish a new connection'
            , u'Connection refused'
            , u'disconnected'
            , u'without establishing a connection'
            , u'web view not found'
            ]
            for each_error_string in exit_bot_error_strings:
                # for python2
                # say goodbye to python2
                '''
                try:
                    basestring
                    if isinstance(each_error_string, unicode):
                        each_error_string = str(each_error_string)
                except NameError:  # Python 3.x
                    basestring = str
                '''
                if isinstance(str_exc, str):
                    if each_error_string in str_exc:
                        print('quit bot by error:', each_error_string)
                        driver.quit()
                        sys.exit()
                        break

            # not is above case, print exception.
            print("Exception:", str_exc)
            pass

        if url is None:
            continue
        else:
            if len(url) == 0:
                continue

        # 說明：輸出目前網址，覺得吵的話，請註解掉這行。
        if debugMode:
            print("url:", url)

        if len(url) > 0 :
            if url != last_url:
                print(url)
            last_url = url

        # for Railway's  test.
        if '/tip811/memberLogin' in url:
            smart_form_filler(driver, "railway")
        if '/tra-tip-web/tip/tip001/tip121/query' in url:
            smart_form_filler(driver, "tip121")

        if '/rid=294db33674eba75de7e9' in url:
            smart_form_filler(driver, "294db33674eba75de7e9")

if __name__ == "__main__":
    main()
