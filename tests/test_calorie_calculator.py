from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import unittest
import time

class TestCalorieCalculator(unittest.TestCase):
    def setUp(self):
        self.driver = webdriver.Chrome()
        self.driver.get("http://127.0.0.1:5000/calorie-calculator")
        self.driver.implicitly_wait(10)
        self.wait = WebDriverWait(self.driver, 10)
        
    def tearDown(self):
        self.driver.quit()

    # Test that all form elements are present on the page
    def test_form_elements_exist(self):

        self.wait.until(EC.presence_of_element_located((By.ID, "calorieForm")))      
        elements = ["weight", "height", "age", "gender", "activity"]
        for element_id in elements:
            element = self.wait.until(EC.presence_of_element_located((By.ID, element_id)))
            self.assertIsNotNone(element)

    # Test the calorie calculation with sample data 
    def test_calorie_calculation(self):
        
        self.wait.until(EC.presence_of_element_located((By.ID, "calorieForm")))
        weight = self.wait.until(EC.presence_of_element_located((By.ID, "weight")))
        weight.send_keys("70")       
        height = self.wait.until(EC.presence_of_element_located((By.ID, "height")))
        height.send_keys("170") 
        age = self.wait.until(EC.presence_of_element_located((By.ID, "age")))
        age.send_keys("30")
        gender_select = Select(self.wait.until(EC.presence_of_element_located((By.ID, "gender"))))
        gender_select.select_by_value("male")
        activity_select = Select(self.wait.until(EC.presence_of_element_located((By.ID, "activity"))))
        activity_select.select_by_value("1.3")
        submit_button = self.wait.until(EC.element_to_be_clickable((By.TAG_NAME, "button")))
        submit_button.click()
        result = self.wait.until(EC.presence_of_element_located((By.ID, "result")))
        self.assertEqual(result.text, "Your estimated daily calorie requirement is: 2103 kcal")
        
    # Test that form validation works
    def test_form_validation(self):

        self.wait.until(EC.presence_of_element_located((By.ID, "calorieForm")))
        submit_button = self.wait.until(EC.element_to_be_clickable((By.TAG_NAME, "button")))
        submit_button.click()
        time.sleep(0.5)
        result = self.driver.find_element(By.ID, "result")
        self.assertEqual(result.text, "")

if __name__ == "__main__":
    unittest.main() 