from src.webdriver_config.config_webdriver import ConfiguracionWebDriver
from selenium.webdriver.remote.webdriver import WebDriver
from src.validaciones_json.json_evaluacion_base import GeneradorJsonBaseEvaluacion
from os import path
from pathlib import Path
from src.utils.utils_html import ValidacionesHtml
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from src.utils.utils_temporizador import Temporizador
from src.utils.utils_format import FormatUtils
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import ElementClickInterceptedException
import src.validaciones_json.constantes_json as jsonConst
import time
import sys
import json


def inicio_sesion_dropbox(webdriver_test_ux: WebDriver, json_eval, json_args, url_login):
    tiempo_step_inicio = Temporizador.obtener_tiempo_timer()
    fecha_inicio = Temporizador.obtener_fecha_tiempo_actual()

    try:
        webdriver_test_ux.get(url_login)

        btn_inicio_sesion = WebDriverWait(webdriver_test_ux, 6).until(
            EC.element_to_be_clickable((By.XPATH, '//button[@class="auth-google button-primary"]')))
        btn_inicio_sesion.click()

        if ValidacionesHtml.se_encuentran_mas_ventanas_en_sesion(webdriver_test_ux, 20):
            ventana_padre = webdriver_test_ux.window_handles[0]
            ventana_hija = webdriver_test_ux.window_handles[1]

            webdriver_test_ux.switch_to.window(ventana_hija)

        input_correo_gmail = WebDriverWait(webdriver_test_ux, 6).until(
            EC.element_to_be_clickable((By.ID, 'identifierId')))
        input_correo_gmail.send_keys(json_args['user'])

        btn_next_gmail_sec_email = WebDriverWait(webdriver_test_ux, 6).until(
            EC.element_to_be_clickable((By.ID, 'identifierNext')))
        btn_next_gmail_sec_email.click()

        input_pass_gmail = WebDriverWait(webdriver_test_ux, 6).until(
            EC.element_to_be_clickable((By.NAME, 'password')))
        input_pass_gmail.send_keys(json_args['password'])

        btn_next_gmail_sec_password = WebDriverWait(webdriver_test_ux, 6).until(
            EC.element_to_be_clickable((By.ID, 'passwordNext')))
        btn_next_gmail_sec_password.click()

        webdriver_test_ux.switch_to.window(ventana_padre)

        WebDriverWait(webdriver_test_ux, 6).until(EC.element_to_be_clickable((By.CLASS_NAME, 'maestro-nav__contents')))

        json_eval["steps"][0]["output"][0]["status"] = jsonConst.SUCCESS
        json_eval["steps"][0]["status"] = jsonConst.SUCCESS
        json_eval["steps"][0]["output"][0]["output"] = 'Se ingresa correctamente al portal Drop Box'

    except ElementNotInteractableException as e:
        json_eval["steps"][0]["output"][0]["status"] = jsonConst.FAILED
        json_eval["steps"][0]["status"] = jsonConst.FAILED
        json_eval["steps"][0]["output"][0]["output"] = 'fue imposible ingresar al portal Drop Box: {}'.format(e.msg)
    except NoSuchElementException as e:
        json_eval["steps"][0]["output"][0]["status"] = jsonConst.FAILED
        json_eval["steps"][0]["status"] = jsonConst.FAILED
        json_eval["steps"][0]["output"][0]["output"] = 'fue imposible ingresar al portal Drop Box: {}'.format(e.msg)
    except TimeoutException as e:
        json_eval["steps"][0]["output"][0]["status"] = jsonConst.FAILED
        json_eval["steps"][0]["status"] = jsonConst.FAILED
        json_eval["steps"][0]["output"][0]["output"] = 'fue imposible ingresar al portal Drop Box: {}'.format(e.msg)
    except ElementClickInterceptedException as e:
        json_eval["steps"][0]["output"][0]["status"] = jsonConst.FAILED
        json_eval["steps"][0]["status"] = jsonConst.FAILED
        json_eval["steps"][0]["output"][0]["output"] = 'fue imposible ingresar al portal Drop Box: {}'.format(e.msg)

    tiempo_step_final = Temporizador.obtener_tiempo_timer() - tiempo_step_inicio
    fecha_fin = Temporizador.obtener_fecha_tiempo_actual()
    json_eval["steps"][0]["time"] = FormatUtils.truncar_float_cadena(tiempo_step_final)
    json_eval["steps"][0]["start"] = fecha_inicio
    json_eval["steps"][0]["end"] = fecha_fin

    return json_eval


def cargar_archivo_dropbox(webdriver_test_ux: WebDriver, json_eval, json_args, nombre_archivo_sin_ext,
                           nombre_archivo_con_ext):
    tiempo_step_inicio = Temporizador.obtener_tiempo_timer()
    fecha_inicio = Temporizador.obtener_fecha_tiempo_actual()

    try:
        ValidacionesHtml.verificar_remover_ventana_configuracion(webdriver_test_ux)

        ValidacionesHtml.verificar_archivo_ya_existente_en_portal(webdriver_test_ux, nombre_archivo_sin_ext)

        input_carga_de_archivo = WebDriverWait(webdriver_test_ux, 10).until(
            EC.presence_of_element_located((By.XPATH, '//body/div/div/input[1]')))

        input_carga_de_archivo.send_keys(json_args['pathImage'])

        WebDriverWait(webdriver_test_ux, 12).until(
            EC.presence_of_element_located((By.XPATH, '//div[@class="mc-util-modal-header"][text()="Cargar a…"]')))

        WebDriverWait(webdriver_test_ux, 12).until(
            EC.presence_of_element_located((By.XPATH, '//tbody[@class="mc-table-body folder-picker-view"]')))

        btn_cargar = WebDriverWait(webdriver_test_ux, 12).until(
            EC.element_to_be_clickable((By.XPATH, '//span[@class="mc-button-content"][text()="Cargar"]')))

        btn_cargar.click()

        link_archivo_cargado = WebDriverWait(webdriver_test_ux, 720).until(
            EC.element_to_be_clickable((By.LINK_TEXT, '{}'.format(nombre_archivo_sin_ext))))

        WebDriverWait(webdriver_test_ux, 10).until(EC.presence_of_element_located(
            (By.XPATH, '//p[@class="mc-snackbar-title"][text()="Se carg\u00F3 {}."]'.format(nombre_archivo_con_ext))))

        btn_cerrar_progreso_carga = WebDriverWait(webdriver_test_ux, 10).until(EC.presence_of_element_located(
            (By.XPATH, '//span[@class="mc-button-content"][text()="Cerrar"]')))

        btn_cerrar_progreso_carga.click()

        link_archivo_cargado.click()

        json_eval["steps"][1]["output"][0]["status"] = jsonConst.SUCCESS
        json_eval["steps"][1]["status"] = jsonConst.SUCCESS
        json_eval["steps"][1]["output"][0]["output"] = 'Se carga el archivo correctamente dentro del portal Drop Box'

    except ElementNotInteractableException as e:
        json_eval["steps"][1]["output"][0]["status"] = jsonConst.FAILED
        json_eval["steps"][1]["status"] = jsonConst.FAILED
        json_eval["steps"][1]["output"][0][
            "output"] = 'fue imposible cargar el archivo dentro del portal Drop Box: {}'.format(e.msg)
    except NoSuchElementException as e:
        json_eval["steps"][1]["output"][0]["status"] = jsonConst.FAILED
        json_eval["steps"][1]["status"] = jsonConst.FAILED
        json_eval["steps"][1]["output"][0][
            "output"] = 'fue imposible cargar el archivo dentro del portal Drop Box: {}'.format(e.msg)
    except TimeoutException as e:
        json_eval["steps"][1]["output"][0]["status"] = jsonConst.FAILED
        json_eval["steps"][1]["status"] = jsonConst.FAILED
        json_eval["steps"][1]["output"][0][
            "output"] = 'fue imposible cargar el archivo dentro del portal Drop Box: {}'.format(e.msg)
    except ElementClickInterceptedException as e:
        json_eval["steps"][1]["output"][0]["status"] = jsonConst.FAILED
        json_eval["steps"][1]["status"] = jsonConst.FAILED
        json_eval["steps"][1]["output"][0][
            "output"] = 'fue imposible cargar el archivo dentro del portal Drop Box: {}'.format(e.msg)

    tiempo_step_final = Temporizador.obtener_tiempo_timer() - tiempo_step_inicio
    fecha_fin = Temporizador.obtener_fecha_tiempo_actual()
    json_eval["steps"][1]["time"] = FormatUtils.truncar_float_cadena(tiempo_step_final)
    json_eval["steps"][1]["start"] = fecha_inicio
    json_eval["steps"][1]["end"] = fecha_fin

    return json_eval


def descargar_archivo_dropbox(webdriver_test_ux: WebDriver, json_eval, json_args):
    tiempo_step_inicio = Temporizador.obtener_tiempo_timer()
    fecha_inicio = Temporizador.obtener_fecha_tiempo_actual()

    try:

        btn_mas = WebDriverWait(webdriver_test_ux, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'more-button')))

        btn_mas.click()
        time.sleep(1)

        btn_descargar = WebDriverWait(webdriver_test_ux, 20).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'more-button__download')))

        btn_descargar.click()
        time.sleep(4)

        webdriver_test_ux.get('https://www.dropbox.com/home')

        json_eval["steps"][2]["output"][0]["status"] = jsonConst.SUCCESS
        json_eval["steps"][2]["status"] = jsonConst.SUCCESS
        json_eval["steps"][2]["output"][0]["output"] = 'Se descarga correctamente el archivo dentro del portal Drop Box'

    except ElementNotInteractableException as e:
        json_eval["steps"][2]["output"][0]["status"] = jsonConst.FAILED
        json_eval["steps"][2]["status"] = jsonConst.FAILED
        json_eval["steps"][2]["output"][0][
            "output"] = 'fue imposible descargar el archivo dentro del portal Drop Box: {}'.format(e.msg)
    except NoSuchElementException as e:
        json_eval["steps"][2]["output"][0]["status"] = jsonConst.FAILED
        json_eval["steps"][2]["status"] = jsonConst.FAILED
        json_eval["steps"][2]["output"][0][
            "output"] = 'fue imposible descargar el archivo dentro del portal Drop Box: {}'.format(e.msg)
    except TimeoutException as e:
        json_eval["steps"][2]["output"][0]["status"] = jsonConst.FAILED
        json_eval["steps"][2]["status"] = jsonConst.FAILED
        json_eval["steps"][2]["output"][0][
            "output"] = 'fue imposible descargar el archivo dentro del portal Drop Box: {}'.format(e.msg)
    except ElementClickInterceptedException as e:
        json_eval["steps"][2]["output"][0]["status"] = jsonConst.FAILED
        json_eval["steps"][2]["status"] = jsonConst.FAILED
        json_eval["steps"][2]["output"][0][
            "output"] = 'fue imposible descargar el archivo dentro del portal Drop Box: {}'.format(e.msg)

    tiempo_step_final = Temporizador.obtener_tiempo_timer() - tiempo_step_inicio
    fecha_fin = Temporizador.obtener_fecha_tiempo_actual()
    json_eval["steps"][2]["time"] = FormatUtils.truncar_float_cadena(tiempo_step_final)
    json_eval["steps"][2]["start"] = fecha_inicio
    json_eval["steps"][2]["end"] = fecha_fin

    return json_eval


def eliminar_archivo_dropbox(webdriver_test_ux: WebDriver, json_eval, nombre_archivo_con_ext):
    tiempo_step_inicio = Temporizador.obtener_tiempo_timer()
    fecha_inicio = Temporizador.obtener_fecha_tiempo_actual()

    try:

        archivo_por_eliminar = WebDriverWait(webdriver_test_ux, 12).until(
            EC.element_to_be_clickable((By.XPATH,
                                        '//tr[@data-filename="{}"]'.format(
                                            nombre_archivo_con_ext))))

        td_archivo_por_eliminar = archivo_por_eliminar.find_elements_by_tag_name('td')
        td_archivo_por_eliminar = td_archivo_por_eliminar[0]
        td_archivo_por_eliminar.click()

        btn_more = WebDriverWait(webdriver_test_ux, 12).until(
            EC.element_to_be_clickable((By.XPATH, '//span[@aria-label="Acciones"]')))

        btn_more.click()

        btn_eliminar = WebDriverWait(webdriver_test_ux, 12).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//span[@role="menuitem"][@class="action-delete mc-popover-content-item"]')))

        btn_eliminar.click()

        btn_eliminar_archivo_definitivo = WebDriverWait(webdriver_test_ux, 12).until(
            EC.element_to_be_clickable(
                (By.XPATH, '//span[@class="mc-button-content"][text()="Eliminar"]')))

        btn_eliminar_archivo_definitivo.click()

        WebDriverWait(webdriver_test_ux, 12).until(EC.element_to_be_clickable(
            (By.XPATH, '//p[@class="mc-snackbar-title"][text()="Se elimin\u00F3 1 elemento."]')))

        btn_cerrar_pop_up = WebDriverWait(webdriver_test_ux, 12).until(
            EC.element_to_be_clickable((By.XPATH, '//span[@class="mc-button-content"][text()="Cerrar"]')))

        btn_cerrar_pop_up.click()

        json_eval["steps"][3]["output"][0]["status"] = jsonConst.SUCCESS
        json_eval["steps"][3]["status"] = jsonConst.SUCCESS
        json_eval["steps"][3]["output"][0]["output"] = 'Se elimina archivo correctamente dentro del portal Drop Box'

    except ElementNotInteractableException as e:
        json_eval["steps"][3]["output"][0]["status"] = jsonConst.FAILED
        json_eval["steps"][3]["status"] = jsonConst.FAILED
        json_eval["steps"][3]["output"][0][
            "output"] = 'fue imposible eliminar el archivo dentro del portal Drop Box: {}'.format(e)
    except NoSuchElementException as e:
        json_eval["steps"][3]["output"][0]["status"] = jsonConst.FAILED
        json_eval["steps"][3]["status"] = jsonConst.FAILED
        json_eval["steps"][3]["output"][0][
            "output"] = 'fue imposible eliminar el archivo dentro del portal Drop Box: {}'.format(e)
    except TimeoutException as e:
        json_eval["steps"][3]["output"][0]["status"] = jsonConst.FAILED
        json_eval["steps"][3]["status"] = jsonConst.FAILED
        json_eval["steps"][3]["output"][0][
            "output"] = 'fue imposible eliminar el archivo dentro del portal Drop Box: {}'.format(e)
    except ElementClickInterceptedException as e:
        json_eval["steps"][3]["output"][0]["status"] = jsonConst.FAILED
        json_eval["steps"][3]["status"] = jsonConst.FAILED
        json_eval["steps"][3]["output"][0][
            "output"] = 'fue imposible eliminar el archivo dentro del portal Drop Box: {}'.format(e)

    tiempo_step_final = Temporizador.obtener_tiempo_timer() - tiempo_step_inicio
    fecha_fin = Temporizador.obtener_fecha_tiempo_actual()
    json_eval["steps"][3]["time"] = FormatUtils.truncar_float_cadena(tiempo_step_final)
    json_eval["steps"][3]["start"] = fecha_inicio
    json_eval["steps"][3]["end"] = fecha_fin

    return json_eval


def cerrar_sesion_dropbox(webdriver_test_ux: WebDriver, json_eval):
    tiempo_step_inicio = Temporizador.obtener_tiempo_timer()
    fecha_inicio = Temporizador.obtener_fecha_tiempo_actual()

    try:
        boton_imagen_perfil = WebDriverWait(webdriver_test_ux, 12).until(
            EC.element_to_be_clickable((By.CLASS_NAME, 'dig-Menu')))

        boton_imagen_perfil.click()

        boton_salir_sesion = WebDriverWait(webdriver_test_ux, 12).until(
            EC.element_to_be_clickable((By.XPATH, '//span[text()="Salir"]')))

        boton_salir_sesion.click()

        WebDriverWait(webdriver_test_ux, 12).until(EC.element_to_be_clickable((By.NAME, 'login_email')))

        WebDriverWait(webdriver_test_ux, 12).until(EC.element_to_be_clickable((By.NAME, 'login_password')))

        json_eval["steps"][4]["output"][0]["status"] = jsonConst.SUCCESS
        json_eval["steps"][4]["status"] = jsonConst.SUCCESS
        json_eval["steps"][4]["output"][0]["output"] = 'Se cierra sesion correctamente dentro del portal Drop Box'

    except ElementNotInteractableException as e:
        json_eval["steps"][4]["output"][0]["status"] = jsonConst.FAILED
        json_eval["steps"][4]["status"] = jsonConst.FAILED
        json_eval["steps"][4]["output"][0][
            "output"] = 'fue imposible cerrar sesion dentro del portal Drop Box: {}'.format(e.msg)

    except NoSuchElementException as e:
        json_eval["steps"][4]["output"][0]["status"] = jsonConst.FAILED
        json_eval["steps"][4]["status"] = jsonConst.FAILED
        json_eval["steps"][4]["output"][0][
            "output"] = 'fue imposible cerrar sesion dentro del portal Drop Box: {}'.format(e.msg)

    except TimeoutException as e:
        json_eval["steps"][4]["output"][0]["status"] = jsonConst.FAILED
        json_eval["steps"][4]["status"] = jsonConst.FAILED
        json_eval["steps"][4]["output"][0][
            "output"] = 'fue imposible cerrar sesion dentro del portal Drop Box: {}'.format(e.msg)

    except ElementClickInterceptedException as e:
        json_eval["steps"][4]["output"][0]["status"] = jsonConst.FAILED
        json_eval["steps"][4]["status"] = jsonConst.FAILED
        json_eval["steps"][4]["output"][0][
            "output"] = 'fue imposible cerrar sesion dentro del portal Drop Box: {}'.format(e.msg)

    tiempo_step_final = Temporizador.obtener_tiempo_timer() - tiempo_step_inicio
    fecha_fin = Temporizador.obtener_fecha_tiempo_actual()
    json_eval["steps"][4]["time"] = FormatUtils.truncar_float_cadena(tiempo_step_final)
    json_eval["steps"][4]["start"] = fecha_inicio
    json_eval["steps"][4]["end"] = fecha_fin

    return json_eval


def verificacion_estatus_final(json_evaluacion):
    val_paso_1 = True if json_evaluacion["steps"][0]["status"] == jsonConst.SUCCESS else False
    val_paso_2 = True if json_evaluacion["steps"][1]["status"] == jsonConst.SUCCESS else False
    val_paso_3 = True if json_evaluacion["steps"][2]["status"] == jsonConst.SUCCESS else False
    val_paso_4 = True if json_evaluacion["steps"][3]["status"] == jsonConst.SUCCESS else False
    val_paso_5 = True if json_evaluacion["steps"][4]["status"] == jsonConst.SUCCESS else False

    eval_final = val_paso_1 and val_paso_2 and val_paso_3 and val_paso_4 and val_paso_5

    return jsonConst.SUCCESS if eval_final else jsonConst.FAILED


def main():
    file_config = FormatUtils.lector_archivo_ini()

    path_web_driver = file_config.get('Driver', 'ruta')
    web_driver_por_usar = file_config.get('Driver', 'driverPorUtilizar')
    url_login = file_config.get('Dropbox_config', 'url_login')
    url_pagina_principal = file_config.get('Dropbox_config', 'url_pagina_principal')
    url_pagina_archivos = file_config.get('Dropbox_config', 'url_pagina_archivos')

    tiempo_inicial_ejecucion_prueba = Temporizador.obtener_tiempo_timer()
    fecha_prueba_inicial = Temporizador.obtener_fecha_tiempo_actual()

    # verifica que el usuario haya establecido el path de la imagen a subir
    args = sys.argv[1:]

    if len(args) == 0:
        print('Favor de establecer el parametro json')
        sys.exit()

    json_args = args[0]

    if not FormatUtils.cadena_a_json_valido(json_args):
        sys.exit()
    else:
        json_args = json.loads(json_args)

    if not FormatUtils.verificar_keys_json(json_args):
        sys.exit()

    if not path.exists(json_args['pathImage']):
        print('La imagen/archivo por cargar no existe o no se localiza, favor de corregir el path del archivo')
        sys.exit()
    elif not path.isfile(json_args['pathImage']):
        print('La ruta establecida no corresponde a un archivo o imagen valido, favor de corregir el path del archivo')
        sys.exit()

    nombre_archivo_imagen_sin_ext = Path(json_args['pathImage']).stem
    nombre_archivo_imagen_con_ext = path.basename(json_args['pathImage'])

    # se establece el navegador (por defecto firefox)
    webdriver_config = ConfiguracionWebDriver(path_web_driver, web_driver_por_usar)
    webdriver_ux_test = webdriver_config.configurar_obtencion_web_driver()

    # se genera el json de evaluacion
    json_evaluacion_drop_box = GeneradorJsonBaseEvaluacion.generar_nuevo_template_json()

    json_evaluacion_drop_box = inicio_sesion_dropbox(webdriver_ux_test, json_evaluacion_drop_box, json_args,
                                                     url_login)

    json_evaluacion_drop_box = cargar_archivo_dropbox(webdriver_ux_test, json_evaluacion_drop_box, json_args,
                                                      nombre_archivo_imagen_sin_ext, nombre_archivo_imagen_con_ext)

    json_evaluacion_drop_box = descargar_archivo_dropbox(webdriver_ux_test, json_evaluacion_drop_box, json_args)

    json_evaluacion_drop_box = eliminar_archivo_dropbox(webdriver_ux_test, json_evaluacion_drop_box,
                                                        nombre_archivo_imagen_con_ext)

    json_evaluacion_drop_box = cerrar_sesion_dropbox(webdriver_ux_test, json_evaluacion_drop_box)

    tiempo_final_ejecucion_prueba = Temporizador.obtener_tiempo_timer() - tiempo_inicial_ejecucion_prueba
    fecha_prueba_final = Temporizador.obtener_fecha_tiempo_actual()

    json_evaluacion_drop_box['start'] = fecha_prueba_inicial
    json_evaluacion_drop_box['end'] = fecha_prueba_final
    json_evaluacion_drop_box['time'] = tiempo_final_ejecucion_prueba
    json_evaluacion_drop_box['status'] = verificacion_estatus_final(json_evaluacion_drop_box)

    jsonFinal = {}
    jsonFinal.update({'body': json_evaluacion_drop_box})

    time.sleep(2)

    webdriver_ux_test.close()
    webdriver_ux_test.quit()

    print(json.dumps(jsonFinal))


main()
