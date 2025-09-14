class BasePage:
    def __init__(self, page, base_url="https://the-internet.herokuapp.com"):
        self.page = page
        self.base_url = base_url.rstrip('/')

    def goto(self, path=""):
        url = f"{self.base_url}/{path.lstrip('/')}".rstrip('/')
        self.page.goto(url)

    def click(self, selector):
        self.page.click(selector)

    def fill(self, selector, text):
        self.page.fill(selector, text)

    def text(self, selector):
        return self.page.text_content(selector)

    def is_visible(self, selector):
        return self.page.is_visible(selector)

    def wait_for(self, selector, timeout=5000):
        self.page.wait_for_selector(selector, timeout=timeout)
