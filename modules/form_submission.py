from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.chrome.service import Service
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC

class FormSubmission:
    def __init__(self):
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()))

    def submit_form(self, name, email):
        self.driver.get('https://tally.so/r/waDMG2')
        
        wait = WebDriverWait(self.driver, 10)  # Adding explicit wait

        try:
            # Locate and fill the Name field using aria-label
            name_field = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@aria-label="Name"]')))
            name_field.send_keys(name)

            # Locate and fill the Email field using aria-label
            email_field = wait.until(EC.presence_of_element_located((By.XPATH, '//input[@aria-label="Email"]')))
            email_field.send_keys(email)

            # Submit the form
            done_button = wait.until(EC.element_to_be_clickable((By.XPATH, '//button[contains(text(),"Done")]')))
            done_button.click()

        except Exception as e:
            print(f"Error occurred while submitting form for {name}: {str(e)}")

        finally:
            self.driver.quit()
