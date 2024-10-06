import time
import unittest
from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.chrome.options import Options
from selenium.webdriver.support.select import Select
from webdriver_manager.chrome import ChromeDriverManager
from selenium.webdriver.common.by import By


class BookMain(unittest.TestCase):

# Initialize chromedriver

    def setUp(self):
        chrome_options = Options()
        self.driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=chrome_options)
        self.driver.maximize_window()
        self.driver.get("https://mysitebook.io/")

# Write test case
    def test_visit_url(self):
        self.driver.implicitly_wait(10)
        login_button = self.driver.find_element(By.XPATH, '//a[@data-event-name="LOGIN"]')
        login_button.click()
        time.sleep(7)
        new_window = self.driver.window_handles[-1]
        self.driver.switch_to.window(new_window)
        self.afterLogin()

# Method for after click login button

    def afterLogin(self):
        mobile_number = self.driver.find_element(By.XPATH, '//input[@id="mobileNumber"]')
        mobile_number.send_keys('9970539817')
        continue_button = self.driver.find_element(By.XPATH, '//button[@type="submit"]')
        continue_button.click()
        try:
            if self.driver.find_element(By.XPATH,
                    '//small[text()=" Mobile number is not registered, sign up to register "]'):
                self.userCreation()

            else:
               self.login()
        except NoSuchElementException:
            self.login()

# method for user already present
    def login(self):
        try:

            password_field = self.driver.find_element(By.XPATH, '//input[@id="password"]')
            password_field.send_keys("Nikita@123")
            login_button_field = self.driver.find_element(By.XPATH, '//button[@type="submit"]')
            login_button_field.click()
            time.sleep(5)
            sample_project_element = self.driver.find_element(By.XPATH, '//span[text()=" Sample bungalow project"]')
            sample_project_element.click()
            time.sleep(5)
            first_project = self.driver.find_element(By.XPATH,'//p[text()=" Detailed Estimate"]')
            first_project.click()
            time.sleep(10)
            self.readData()
        except NoSuchElementException:
            print("elements not found.")
            raise

# user not present (new user)
    def userCreation(self):
        self.driver.find_element(By.XPATH, '//a[text()="Sign up for free"]').click()
        self.driver.find_element(By.XPATH,'//input[@placeholder="Enter Name"]').send_keys("ABC")
        dropdown = self.driver.find_element(By.XPATH, '//select[@id="country"]')
        select_dropdown = Select(dropdown)
        select_dropdown.select_by_value("India")
        self.driver.find_element(By.XPATH,'//input[@id="mobileNumber"]').send_keys("9322477367")
        self.driver.find_element(By.XPATH,'//button[text()="Sign Up"]').click()
        # Enter otp
        otp_fields = self.driver.find_elements(By.XPATH, '//input[@autocomplete="one-time-code"]')
        otp = "1234"
        for index, digit in enumerate(otp):
            otp_fields[index].send_keys(digit)
        self.driver.find_element(By.XPATH,'// button[text() = "Verify "]').click()

        # dropdown.click()


# method for read data and check testcases for quantity and rate multiplication is correct or not
    def readData(self):
        row_index = 4

        while True:
            try:
                row_xpath = f'//*[@id="tpl-app"]/mbc-app/mbc-project-cost/div/div/mbc-create-quotes/div/div[2]/mbc-quote-items-preview/div/table/tbody/tr[{row_index}]'
                row = self.driver.find_element(By.XPATH, row_xpath)

                serial_no = row.find_element(By.XPATH, f"{row_xpath}/td[1]").text

                if not serial_no:
                    row_index += 1
                    continue

                description = row.find_element(By.XPATH, f"{row_xpath}/td[2]").text
                quantityVal = row.find_element(By.XPATH, f"{row_xpath}/td[3]").text
                quantity = float(quantityVal.replace(",", "").replace("₹", ""))
                unit = row.find_element(By.XPATH, f"{row_xpath}/td[4]").text
                rateVal = row.find_element(By.XPATH, f"{row_xpath}/td[5]").text
                rate = float(rateVal.replace(",", "").replace("₹", ""))
                # rate = self.convert_to_float(rateVal)
                totalCostVal = row.find_element(By.XPATH, f"{row_xpath}/td[6]").text
                total_cost = float(totalCostVal.replace(",", "").replace("₹", ""))

                if quantity * rate == total_cost:
                    print(f"Serial number: {serial_no} - Test case pass")
                else:
                    print(f"Serial number: {serial_no} - Test case fail")

                row_index += 1
            except Exception as e:
                print("Error occurred:", e)

# close the browser and end the webdriver session.
    def tearDown(self):
        self.driver.quit()

if __name__ == "__main__":
    unittest.main()
