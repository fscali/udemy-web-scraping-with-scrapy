from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from shutil import which

#chrome_path = which("chromedriver")

driver = webdriver.Chrome(executable_path="./chromedriver")
driver.get("https://duckduckgo.com")
search_input = driver.find_element(By.XPATH,
                                   "(//input[contains(@class,'js-search-input')])[1]")
search_input.send_keys("my user agent")

""" search_btn = driver.find_element(By.XPATH,
                                 "//input[contains(@class,'js-search-button')]")
search_btn.click()
 """
search_input.send_keys(Keys.ENTER)
