import os
import pytest
import allure
from playwright.sync_api import sync_playwright

def pytest_addoption(parser):
    parser.addoption("--browser", action="store", default=os.getenv("BROWSER", "chromium"),
                     help="Browser: chromium, firefox, webkit")
    parser.addoption("--headless", action="store", default=os.getenv("HEADLESS", "True"),
                     help="Headless: True/False")

@pytest.fixture(scope="session")
def pw():
    p = sync_playwright().start()
    yield p
    p.stop()

@pytest.fixture(scope="function")
def page(pw, request):
    browser_name = request.config.getoption("--browser")
    headless_opt = request.config.getoption("--headless")
    headless = str(headless_opt).lower() in ("true", "1", "yes")
    browser_type = getattr(pw, browser_name)
    browser = browser_type.launch(headless=headless)
    context = browser.new_context()
    page = context.new_page()
    # attach page to the test node so hooks can access it
    request.node._page = page
    yield page
    context.close()
    browser.close()

# Hook that attaches screenshot to Allure on failure
@pytest.hookimpl(hookwrapper=True, tryfirst=True)
def pytest_runtest_makereport(item, call):
    outcome = yield
    rep = outcome.get_result()
    if rep.when == "call" and rep.failed:
        page = getattr(item, "_page", None)
        if page:
            try:
                png = page.screenshot()
                allure.attach(png, name="screenshot", attachment_type=allure.attachment_type.PNG)
            except Exception as e:
                print("Could not take screenshot:", e)
