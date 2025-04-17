import undetected_chromedriver as uc
import time
import psutil

def kill_chrome_processes():
    for proc in psutil.process_iter(attrs=['pid', 'name']):
        if 'chrome' in proc.info['name'].lower():
            proc.kill()

def main():
    # 设置 ChromeOptions
    options = uc.options.ChromeOptions()
    options.add_argument("--headless")  # 以无头模式启动浏览器
    options.add_argument("--no-sandbox")
    options.add_argument("--disable-dev-shm-usage")

    driver = None
    try:
        driver = uc.Chrome(options=options)
        print("浏览器已启动。")

        # 你可以在这里添加你的自动化代码，例如访问网页
        driver.get("https://www.google.com")
        print("访问了 Google 网页。")

        # 等待几秒钟来观察结果
        time.sleep(3)

        # 获取页面标题并输出
        title = driver.title
        print(f"页面标题: {title}")
    
    except Exception as e:
        print(f"发生错误: {e}")
    
    finally:
        if driver:
            try:
                print("等待 0.5 秒后退出浏览器...")
                time.sleep(0.5)
                driver.quit()
                print("浏览器已退出。")
            except OSError as e:
                print(f"退出浏览器时发生错误: {e}")
            
            # 强制杀死所有 Chrome 进程
            print("强制结束所有 Chrome 进程...")
            kill_chrome_processes()

if __name__ == "__main__":
    main()
