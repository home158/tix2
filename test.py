import undetected_chromedriver as uc
from selenium_stealth import stealth
from selenium.webdriver.chrome.options import Options

def load_stealth_chromedriver():
    chrome_options = Options()

    # 隱藏 Selenium 特徵
    chrome_options.add_argument("--disable-blink-features=AutomationControlled")
    
    # 設定語言
    chrome_options.add_argument("--lang=zh-TW")

    # 禁用密碼管理彈窗
    chrome_options.add_experimental_option("prefs", {
        "credentials_enable_service": False,
        "profile.password_manager_enabled": False
    })

    # 啟動 `undetected_chromedriver`
    driver = uc.Chrome(options=chrome_options)

    # 使用 `selenium-stealth` 來隱藏 WebDriver
    stealth(driver,
        languages=["zh-TW", "zh"],
        vendor="Google Inc.",
        platform="Win32",
        webgl_vendor="Intel Inc.",
        renderer="Intel Iris OpenGL Engine",
        fix_hairline=True,
    )

    return driver

# 測試 Shopee
driver = load_stealth_chromedriver()
driver.get("https://shopee.tw")

input("按 Enter 退出...")
driver.quit()
