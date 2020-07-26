from selenium.webdriver.remote.webdriver import WebDriver
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
import time


class ValidacionesHtml():

    @staticmethod
    def verificar_elemento_html_por_id(id: str, web_driver: WebDriver):

        try:
            web_driver.find_element_by_id(id)
            return True
        except NoSuchElementException:
            return False

    @staticmethod
    def verificar_elemento_html_por_xpath(xpath: str, web_driver: WebDriver):

        try:
            web_driver.find_element_by_xpath(xpath)
            return True
        except NoSuchElementException:
            return False

    @staticmethod
    def se_encuentran_mas_ventanas_en_sesion(web_driver: WebDriver, tiempo_espera: int):
        count = 0
        while count < tiempo_espera:
            if len(web_driver.window_handles) > 1:
                return True
            else:
                count = count + 1

            time.sleep(1)

        driverExcep = WebDriverException('Han transcurrido mas de {} seg. sin obtener la nueva ventana de '
                                         'inicio de sesion mediante Gmail'.format(tiempo_espera))

        raise TimeoutException(driverExcep)

    @staticmethod
    def verificar_remover_ventana_configuracion(web_driver: WebDriver):

        try:
            btn_cierre_ventana_configuracion = WebDriverWait(web_driver, 10).until(
                EC.element_to_be_clickable((By.ID, 'continuous-onboarding-collapse-btn')))
            btn_cierre_ventana_configuracion.click()
        except TimeoutException:
            pass

    @staticmethod
    def verificar_archivo_ya_existente_en_portal(web_driver: WebDriver, nombre_archivo_sin_ext: str):

        try:
            lista_archivos_actuales = web_driver.find_elements_by_xpath('//div[@data-item-id]')

            if len(lista_archivos_actuales) > 0:
                for div_archivo in lista_archivos_actuales:
                    div_recent_item_header = div_archivo.find_element_by_class_name('recents-item-header')
                    div_recent_item_header_content = div_recent_item_header.find_element_by_class_name(
                        'recents-item-header__content')
                    link_nombre_archivo = div_recent_item_header_content.find_element_by_tag_name('a')

                    if link_nombre_archivo.text.strip() == nombre_archivo_sin_ext.strip():
                        div_item_actions = WebDriverWait(web_driver, 10).until(
                            EC.presence_of_element_located((By.CLASS_NAME, 'recents-item__actions')))

                        WebDriverWait(div_item_actions, 10).until(
                            EC.element_to_be_clickable((By.CLASS_NAME, 'dig-IconButton-content')))

                        btn_mas = div_item_actions.find_element_by_class_name('dig-IconButton-content')
                        btn_mas.click()

                        sub_menu_acciones = WebDriverWait(web_driver, 10).until(
                            EC.element_to_be_clickable((By.CLASS_NAME, 'dig-Layer')))

                        btn_eliminar = WebDriverWait(sub_menu_acciones, 10).until(
                            EC.element_to_be_clickable((By.XPATH, '//span[text()="Eliminar…"]')))

                        btn_eliminar.click()

                        modal_eliminacion = WebDriverWait(web_driver, 10).until(
                            EC.element_to_be_clickable((By.CLASS_NAME, 'db-modal-box')))

                        btn_eliminacion_definitivo = WebDriverWait(modal_eliminacion, 10).until(
                            EC.element_to_be_clickable(
                                (By.XPATH, '//button[@class="button-primary dbmodal-button"][text()="Eliminar"]')))

                        btn_eliminacion_definitivo.click()

                        WebDriverWait(web_driver, 10).until(
                            EC.presence_of_element_located((By.XPATH, '//span[@id="notify-msg"]')))

        except ElementNotInteractableException as e:
            pass
        except NoSuchElementException:
            pass
        except TimeoutException:
            pass
        except ElementClickInterceptedException:
            pass
