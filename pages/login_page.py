from pages.base_page import BasePage

class LoginPage(BasePage):
    LOGIN_PATH = "/login"
    USER = "input#username"
    PASS = "input#password"
    SUBMIT = "button[type='submit']"
    FLASH = "div#flash"

    def open(self):
        self.goto(self.LOGIN_PATH)

    def login(self, username, password):
        self.fill(self.USER, username)
        self.fill(self.PASS, password)
        self.click(self.SUBMIT)

    def flash_text(self):
        # returns the flash message text (trimmed)
        raw = self.text(self.FLASH)
        return raw.strip() if raw else ""
