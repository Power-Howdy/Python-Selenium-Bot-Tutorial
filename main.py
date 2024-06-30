from selenium import webdriver
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from time import sleep
import pandas as pd

def get_currencies(currencies, start, end, export_csv=False):
  frames = []
  for currency in currencies:
    while True:
      try:        
        my_url = f'https://br.investing.com/currencies/usd-{currency.lower()}-historical-data'
        option = Options()
        option.headless = False
        driver = webdriver.Chrome(options=option)
        driver.get(my_url)
        driver.maximize_window()

        date_button = WebDriverWait(driver, 120).until(
          EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[2]/div[1]/div[2]/div[1]/div[3]/div[2]/div[2]/div[2]/span'))
        )
        date_button.click()

        start_bar = WebDriverWait(driver, 120).until(EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[2]/div[1]/div[2]/div[1]/div[2]/div[2]/div[2]/div[3]/div[1]/div[1]/input')))
        start_bar.clear()
        start_bar.send_keys(start)

        end_bar = WebDriverWait(driver, 120).until(
          EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[2]/div[1]/div[2]/div[1]/div[2]/div[2]/div[2]/div[3]/div[1]/div[2]/input'))
        )
        end_bar.clear()
        end_bar.send_keys(end)

        apply = WebDriverWait(driver, 20).until(
          EC.element_to_be_clickable((By.XPATH, '//*[@id="__next"]/div[2]/div[1]/div[2]/div[1]/div[2]/div[2]/div[2]/div[3]/div[2]/span[2]'))
        )
        apply.click()
        sleep(5)


        dataframes = pd.read_html(driver.page_source)
        driver.quit()
        print(f'{currency} scraped')

        break
      except:
        driver.quit()
        print(f'Failed to scrap {currency}. Try again in 30 seconds')
        sleep(30)
        continue
  for dataframe in dataframes:
    if dataframe.columns.tolist() == ['Date', 'Price', 'Open', 'High', 'Low', 'Change%']:
      df = dataframe
      break
    frames.append(df)
    #Exporting the .csv file
    if export_csv:
      df.to_csv(f'{currency}.csv', index=False)
      print(f'{currency}.csv exported')
  return frames

get_currencies(['eur'], '2024-05-28', '2024-06-30', True)