import os
import json
import pytest
from pages.login_page import LoginPage

def load_test_data():
    here = os.path.dirname(__file__)
    path = os.path.join(here, "..", "data", "login_data.json")
    with open(path, "r") as f:
        return json.load(f)

@pytest.mark.parametrize("data", load_test_data())
def test_login(page, data):
    base_url = os.getenv("BASE_URL", "https://the-internet.herokuapp.com")
    login = LoginPage(page, base_url)
    login.open()
    login.login(data["username"], data["password"])

    if data["expected"] == "success":
        # successful login redirects to /secure and shows success flash
        assert page.url.endswith("/secure")
        assert "You logged into a secure area!" in login.flash_text()
    else:
        # invalid credentials show an error message in flash
        assert ("Your username is invalid!" in login.flash_text()) or ("Your password is invalid!" in login.flash_text())
