import undetected_chromedriver as uc

if __name__ == "__main__":

    # instantiate a Chrome browser
    driver = uc.Chrome(
        use_subprocess=False,
    )

    # visit the target URL
    driver.get("https://www.hapag-lloyd.com/en/home.html")

    # print the URL
    print(driver.current_url)  # https://www.hapag-lloyd.com/en/home.html

    # get the website's title
    print(driver.title)  # Hapag-Lloyd - Global container liner shipping - Hapag-Lloyd
    try:
       time.sleep(0.1)
    except:
       pass

    # close the browser
    driver.quit()
