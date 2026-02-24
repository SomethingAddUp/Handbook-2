from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

class SwagLabs:
    def __init__(self, driver):
        self.driver = driver
        self.wait = WebDriverWait(driver, 12)
        self.quantity = (By. CSS_SELECTOR, "div.cart_quantity")

    def login(self, username, password):
        self.wait.until(EC.visibility_of_element_located((By.ID, "user-name"))).send_keys(username)
        self.driver.find_element(By.ID, "password").send_keys(password)
        self.wait.until(EC.element_to_be_clickable((By.ID, "login-button"))).click()

    def login_check(self):
        return self.wait.until(EC.url_contains("inventory.html"))

    def add_to_cart(self, item):   # add 1 item
        self.wait.until(EC.element_to_be_clickable((By.ID, f"add-to-cart-{item}"))).click()

    def open_cart(self):
        self.wait.until(EC.element_to_be_clickable((By.CSS_SELECTOR, "a.shopping_cart_link"))).click()
        self.display_check("Your Cart")
        return self.driver.find_elements(*self.quantity)

    def remove_cart(self, item):
        self.wait.until(EC.element_to_be_clickable((By.ID, f"remove-{item}"))).click()

    def empty_cart(self):
        self.wait.until(lambda d: len(d.find_elements(*self.quantity)) == 0)
        return self.driver.find_elements(*self.quantity)

    def resume_shopping(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "continue-shopping"))).click()
        self.wait.until(EC.url_contains("inventory.html"))

    def checkout(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "checkout"))).click()

    def display_check(self, header):
        self.wait.until(EC.visibility_of_element_located((By.CSS_SELECTOR, "span.title")))
        header_swap_wait = self.wait.until(EC.text_to_be_present_in_element((By.CSS_SELECTOR, "span.title"), header ))
        time.sleep(2)      # buffer wait time to allow title header refresh completely
        return header_swap_wait

    def checkout_info(self):
        first = self.wait.until(EC.visibility_of_element_located((By.ID, "first-name")))
        first.clear()
        first.send_keys("SomethingAdd")
        last = self.wait.until(EC.visibility_of_element_located((By.ID, "last-name")))
        last.clear()
        last.send_keys("Up")
        postal = self.wait.until(EC.visibility_of_element_located((By.ID, "postal-code")))
        postal.clear()
        postal.send_keys("12345")
        self.wait.until(EC.element_to_be_clickable((By.NAME, "continue"))).click()

    def checkout_overview(self, qty=False, name=False, price=False):
        flags = [qty, name, price]
        if flags.count(True) > 1:
            raise ValueError("only 1 argument can be True")
        if qty:
            return self.driver.find_elements(*self.quantity)
        if name:
            return self.driver.find_elements(By.CSS_SELECTOR, "div.inventory_item_name")
        if price:
            return self.driver.find_elements(By.CSS_SELECTOR, "div.inventory_item_price")
        return None

    def price_total(self, tax=False):
        if tax:
            return self.driver.find_element(By.CSS_SELECTOR, "div.summary_total_label")
        return self.driver.find_element(By.CSS_SELECTOR, "div.summary_subtotal_label")

    def finish(self):
        self.wait.until(EC.element_to_be_clickable((By.ID, "finish"))).click()
        return self.display_check("Checkout: Complete!")

    def wrapper(self):     # Format edit for checkout_overview and price_total
        item_count = [ int(el_qty.text.strip()) for el_qty in self.checkout_overview(True, False, False) ]
        item_type = [ el_name.text.strip() for el_name in self.checkout_overview(False,True, False) ]
        item_price = [ float(el_price.text.strip().replace("$", "")) for el_price in self.checkout_overview(False, False, True) ]
        total_after_tax = float(self.price_total(True).text.strip().replace("Total: $", ""))
        total_before_tax = float(self.price_total(False).text.strip().replace("Item total: $", ""))

        return {    "qty": item_count,
                    "name": item_type,
                    "price": item_price,
                    "total": total_after_tax,
                    "subtotal": total_before_tax    }
