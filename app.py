import os
import sys
import json
import pt_config
import undetected_chromedriver as uc
import time
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

def init_driver():
    Root_Dir = get_app_root()
    webdriver_path = os.path.join(Root_Dir, "webdriver")
    
    chromedriver_executable_path = pt_config.CHROMEDRIVER_EXECUTABLE_PATH
    binary_location = pt_config.CHROME_BINARY_PATH

    print(chromedriver_executable_path)
    print(binary_location)


    options = uc.ChromeOptions()

    options.binary_location = binary_location
    options.add_argument("--disable-gpu")
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")  # 很重要，在 Docker 上

    caps = options.to_capabilities()

    driver = uc.Chrome(
        driver_executable_path=chromedriver_executable_path, 
        options=options, 
        desired_capabilities=caps, 
        suppress_welcome=False, 
        use_subprocess=True
    )

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
    driver = None
    if not config_dict is None:
        driver = init_driver()
    else:
        print("Load config error!")
    driver.get("https://tixcraft.com/")

    # print the URL
    print(driver.current_url)  # https://www.hapag-lloyd.com/en/home.html

    # get the website's title
    print(driver.title)  # Hapag-Lloyd - Global container liner shipping - Hapag-Lloyd
    url = ""
    last_url = ""
    while True:
        time.sleep(2)
        url = driver.current_url
        if len(url) > 0 :
            if url != last_url:
                print(url)
            last_url = url
        # for Railway's  test.
        if '/tip811/memberLogin' in url:
            smart_form_filler(driver, "railway")
        if '/tra-tip-web/tip/tip001/tip121/query' in url:
            smart_form_filler(driver, "tip121")

if __name__ == "__main__":
    main()
