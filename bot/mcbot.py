import os
import json
import datetime

from selenium.webdriver import Chrome, ChromeOptions
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC


class MCBot(Chrome):
    def __init__(self, *args, **kwargs):

        self.hidden = kwargs.pop('hidden', False)
        self.amount = kwargs.pop('amount', 1)

        self.country = kwargs.pop('country')
        self.cnpj_mc = kwargs.pop('cnpj_mc')

        self.quantia = kwargs.pop('quantia')
        self.base_url = 'https://mcexperienciasurvey.com/Index.aspx'

        options = ChromeOptions()
        if self.hidden:
            options.add_argument('--headless')

        os.system("cls" if os.name == "nt" else 'clear')

        print(f"[>] Gerando códigos\n[>] 10s minimo para geração")

        super().__init__(*args, options=options, **kwargs)

    def get_country_xpath(self):
        script_dir = os.path.dirname(__file__)
        json_path = os.path.join(script_dir, 'countries.json')

        with open(json_path) as f:
            country_dict: dict = json.load(f)

        return country_dict.get(self.country.lower())

    def press_button(self, xpath: str):
        element = '//*[@id="NextButton"]' if xpath == 'next' else xpath
        self.find_element(By.XPATH, element).click()

    def start_gen(self):

        i = 0

        while i < self.quantia:

            self.get(self.base_url)
            self.implicitly_wait(2)
            self.press_button('next')

            # País
            self.implicitly_wait(2)
            self.find_element(By.XPATH, self.get_country_xpath()).click()
            self.press_button('next')

            # Visita
            self.find_element(By.XPATH, '//*[@id="InputCNPJ"]'
                              ).send_keys(self.cnpj_mc)

            self.implicitly_wait(2)
            self.find_element(
                By.XPATH, '//*[@id="Index_VisitDatecontainer"]/button').click()

            WebDriverWait(self, 2).until(
                EC.visibility_of_element_located((By.ID, 'ui-datepicker-div'))
            )

            self.find_element(
                By.CSS_SELECTOR, 'td.ui-datepicker-today a').click()
            self.find_element(By.XPATH, '//*[@id="InputHour"]'
                              ).send_keys(datetime.datetime.now().strftime("%H"))
            self.find_element(By.XPATH, '//*[@id="InputMinute"]'
                              ).send_keys(datetime.datetime.now().strftime("%M"))
            self.find_element(By.XPATH, '//*[@id="surveyQuestions"]/div[3]/span/span'
                              ).click()

            self.press_button('next')
            self.implicitly_wait(1)

            self.find_element(
                By.XPATH, '//*[@id="FNSR000001"]/div/div/div[5]/span/span').click()
            self.press_button('next')
            self.implicitly_wait(1)

            self.find_element(
                By.XPATH, '//*[@id="FNSR000004"]/td[2]/span').click()
            self.press_button('next')
            self.implicitly_wait(1)

            self.find_element(
                By.XPATH, '//*[@id="FNSR000059"]/span/span').click()
            self.press_button('next')
            self.implicitly_wait(1)
            self.press_button('next')

            self.find_element(
                By.XPATH, '//*[@id="FNSR000020"]/td[2]/span').click()
            self.implicitly_wait(1)
            self.press_button('next')

            invis_char = 'ㅤ'  # U+3164
            self.find_element(
                By.XPATH, '//*[@id="S000036"]').send_keys(invis_char)
            self.find_element(By.XPATH, '//*[@id="S000035"]').send_keys(1)
            self.find_element(
                By.XPATH, '//*[@id="S000033"]').send_keys('ㅤㅤㅤㅤ@gmail.com')
            self.find_element(
                By.XPATH, '//*[@id="S000034"]').send_keys('ㅤㅤㅤㅤ@gmail.com')

            self.press_button('next')
            self.implicitly_wait(1)

            self.find_element(
                By.XPATH, '//*[@id="FNSR000040"]/div/div/div[2]/span/span').click()
            self.press_button('next')
            self.implicitly_wait(1)

            code = self.find_element(
                By.XPATH, "//*[@id='CouponDemoImage']/span")
            date = self.find_element(By.XPATH, "//*[@id='CouponDemoImage']/p")

            with open('codigos.txt', 'a') as arquivo:
                arquivo.write(f"{code.text.strip()} [{date.text.strip()}]\n")

            i += 1
            print(f'[+] {code.text.strip()}')
            print(f'[*] Salvo em "codigos.txt".')

        self.quit()
