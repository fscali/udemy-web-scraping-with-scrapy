from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.options import Options
from shutil import which

#chrome_path = which("chromedriver")

chrome_options = Options()
chrome_options.add_argument("--headless")

driver = webdriver.Chrome(
    executable_path="./chromedriver", options=chrome_options)
driver.get("https://duckduckgo.com")
search_input = driver.find_element(By.XPATH,
                                   "(//input[contains(@class,'js-search-input')])[1]")
search_input.send_keys("my user agent")

""" search_btn = driver.find_element(By.XPATH,
                                 "//input[contains(@class,'js-search-button')]")
search_btn.click()
 """
search_input.send_keys(Keys.ENTER)
print(driver.page_source)

driver.close()
