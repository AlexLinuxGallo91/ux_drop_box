from selenium.webdriver.remote.webdriver import WebDriver
import selenium.common.exceptions as selExcep

class ValidacionesHtml():

    @staticmethod
    def verificar_elemento_html_por_id(id: str, web_driver: WebDriver):

        try:
            web_driver.find_element_by_id(id)
            return True
        except selExcep.NoSuchElementException:
            return False

    @staticmethod
    def verificar_elemento_html_por_xpath(xpath: str, web_driver: WebDriver):

        try:
            web_driver.find_element_by_xpath(xpath)
            return True
        except selExcep.NoSuchElementException:
            return False