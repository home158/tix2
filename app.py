import os
import sys
import json
import pt_config
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
        with open(config_filepath, "r", encoding="utf-8") as json_data:
            config_dict = json.load(json_data)
    return config_dict

def init_driver():
    chromedriver_executable_path = pt_config.CHROMEDRIVER_EXECUTABLE_PATH
    options = uc.ChromeOptions()
    options.binary_location = pt_config.CHROME_BINARY_PATH

    caps = options.to_capabilities()
    print(chromedriver_executable_path)
    driver = uc.Chrome(driver_executable_path=chromedriver_executable_path, options=options, desired_capabilities=caps, suppress_welcome=False)
    driver.set_window_size(1920,1080)

    return driver    
def main():
    config_dict = get_config_dict()
    driver = None
    if not config_dict is None:
        driver = init_driver()
    else:
        print("Load config error!")
if __name__ == "__main__":
    main()
