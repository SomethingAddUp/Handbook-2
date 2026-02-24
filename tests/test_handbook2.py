import pytest
from selenium.webdriver.common.by import By
import POM.ecommerce as Ecom

@pytest.mark.login
def test_handbook2(driver):
    ecom = Ecom.SwagLabs(driver)
    assert ecom.login_check()

    ecom.add_to_cart("sauce-labs-backpack")
    cart1_items = ecom.open_cart()
    assert len(cart1_items) == 1
    assert cart1_items[0].text.strip() == "1"

    ecom.remove_cart("sauce-labs-backpack")
    after_remove = ecom.empty_cart()
    assert not len(after_remove)

    ecom.resume_shopping()
    ecom.add_to_cart("sauce-labs-fleece-jacket")      # split due to for loop cause overlap page rendering error
    ecom.add_to_cart("sauce-labs-bolt-t-shirt")
    ecom.add_to_cart("test.allthethings()-t-shirt-(red)")
    cart2_items = ecom.open_cart()
    assert len(cart2_items) == 3
    assert cart2_items[0].text.strip() == "1"

    ecom.checkout()
    assert ecom.display_check("Checkout: Your Information")

    ecom.checkout_info()
    assert ecom.display_check("Checkout: Overview")

    wrapper = ecom.wrapper()
    assert len(wrapper["qty"]) == len(cart2_items)                      # Match qty in 2 different pages
    assert sum(wrapper["qty"]) == 3
    assert wrapper["name"] == ["Sauce Labs Fleece Jacket", "Sauce Labs Bolt T-Shirt", "Test.allTheThings() T-Shirt (Red)" ]

    assert sum(wrapper["price"]) == wrapper["subtotal"]                  #6 verify subtotal cost
    assert round(sum(wrapper["price"]) * 1.08, 2) == wrapper["total"]    #7 verify total cost

    assert ecom.finish()

