import time
from os import path
from pathlib import Path

from selenium.common.exceptions import ElementClickInterceptedException
from selenium.common.exceptions import ElementNotInteractableException
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import StaleElementReferenceException
from selenium.common.exceptions import TimeoutException
from selenium.common.exceptions import WebDriverException
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.remote.webdriver import WebDriver
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.support.ui import WebDriverWait
from src.webdriver_actions.html_actions import HtmlActions

from src.step_evaluaciones import constantes_evaluaciones_claro_drive
from src.utils.utils_evaluaciones import UtilsEvaluaciones
from src.utils.utils_format import FormatUtils
from src.utils.utils_html import ValidacionesHtml
from src.utils.utils_temporizador import Temporizador


class EvaluacionesDropBoxDriveSteps:

    def ingreso_pagina_principal_dropbox(self, webdriver_test_ux: WebDriver, json_eval, url_login):
        tiempo_step_inicio = Temporizador.obtener_tiempo_timer()
        fecha_inicio = Temporizador.obtener_fecha_tiempo_actual()

        try:
            webdriver_test_ux.get(url_login)

            HtmlActions.webdriver_wait_presence_of_element_located(webdriver_test_ux, 10, name='login_email')
            HtmlActions.webdriver_wait_presence_of_element_located(webdriver_test_ux, 10, name='login_password')

            json_eval = UtilsEvaluaciones.establecer_output_status_step(
                json_eval, 0, 0, True, constantes_evaluaciones_claro_drive.MSG_OUTPUT_INGRESO_PAGINA_PRINCIPAL_EXITOSO)

        except ElementNotInteractableException as e:
            msg_output = constantes_evaluaciones_claro_drive.MSG_OUTPUT_INGRESO_PAGINA_PRINCIPAL_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 0, 0, False, msg_output)

        except NoSuchElementException as e:
            msg_output = constantes_evaluaciones_claro_drive.MSG_OUTPUT_INGRESO_PAGINA_PRINCIPAL_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 0, 0, False, msg_output)

        except TimeoutException as e:
            msg_output = constantes_evaluaciones_claro_drive.MSG_OUTPUT_INGRESO_PAGINA_PRINCIPAL_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 0, 0, False, msg_output)

        except ElementClickInterceptedException as e:
            msg_output = constantes_evaluaciones_claro_drive.MSG_OUTPUT_INGRESO_PAGINA_PRINCIPAL_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 0, 0, False, msg_output)

        except WebDriverException as e:
            msg_output = constantes_evaluaciones_claro_drive.MSG_OUTPUT_INGRESO_PAGINA_PRINCIPAL_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 0, 0, False, msg_output)

        json_eval = UtilsEvaluaciones.finalizar_tiempos_en_step(json_eval, 0 ,tiempo_step_inicio, fecha_inicio)

        return json_eval


    def inicio_sesion_dropbox(self, webdriver_test_ux: WebDriver, json_eval, json_args, url_login):
        intentos_ingreso_password_gmail = 0
        tiempo_step_inicio = None
        fecha_inicio = Temporizador.obtener_fecha_tiempo_actual()

        if not UtilsEvaluaciones.se_ingreso_correctamente_a_la_pagina_principal(json_eval):
            json_eval = UtilsEvaluaciones.generar_json_inicio_de_sesion_incorrecta(
                json_eval, tiempo_step_inicio, fecha_inicio, 1,
                constantes_evaluaciones_claro_drive.MSG_INICIO_SESION_FALLIDA_POR_INGRESO_DE_PAGINA)

            return json_eval

        try:
            btn_inicio_sesion = HtmlActions.webdriver_wait_element_to_be_clickable(
                webdriver_test_ux, 6, xpath='//button[@class="auth-google button-primary"]')

            HtmlActions.click_html_element(btn_inicio_sesion, xpath='//button[@class="auth-google button-primary"]')

            if ValidacionesHtml.se_encuentran_mas_ventanas_en_sesion(webdriver_test_ux, 6):
                ventana_padre = webdriver_test_ux.window_handles[0]
                ventana_hija = webdriver_test_ux.window_handles[1]

                webdriver_test_ux.switch_to.window(ventana_hija)

            modo_no_grafico = FormatUtils.lector_archivo_ini().getboolean('Driver', 'headless')

            if modo_no_grafico:

                input_correo_gmail = HtmlActions.webdriver_wait_element_to_be_clickable(
                    webdriver_test_ux, 6, id='Email')

                HtmlActions.enviar_data_keys(input_correo_gmail, json_args['user'], id='Email')

                btn_next_gmail_sec_email = HtmlActions.webdriver_wait_element_to_be_clickable(
                    webdriver_test_ux, 6, id='next')

                HtmlActions.click_html_element(btn_next_gmail_sec_email, id='next')

                input_pass_gmail = HtmlActions.webdriver_wait_presence_of_element_located(
                    webdriver_test_ux, 6, id='password')

                HtmlActions.enviar_data_keys(input_pass_gmail, json_args['password'], id='password')

                btn_next_gmail_sec_password = HtmlActions.webdriver_wait_element_to_be_clickable(
                    webdriver_test_ux, 6, id='submit')

                HtmlActions.click_html_element(btn_next_gmail_sec_password, id='submit')

            else:

                input_correo_gmail = HtmlActions.webdriver_wait_presence_of_element_located(
                    webdriver_test_ux, 10, id='identifierId')

                HtmlActions.webdriver_wait_element_to_be_clickable(webdriver_test_ux, 10, id='identifierId')
                HtmlActions.click_html_element(input_correo_gmail, id='identifierId')
                HtmlActions.enviar_data_keys(input_correo_gmail, json_args['user'], id='identifierId')

                btn_next_gmail_sec_email = HtmlActions.webdriver_wait_presence_of_element_located(
                    webdriver_test_ux, 10, id='identifierNext')

                HtmlActions.webdriver_wait_element_to_be_clickable(webdriver_test_ux, 10, id='identifierNext')
                HtmlActions.click_html_element(btn_next_gmail_sec_email, id='identifierNext')

                div_form = HtmlActions.webdriver_wait_presence_of_element_located(webdriver_test_ux, 10, id='password')

                input_pass_gmail = HtmlActions.webdriver_wait_presence_of_element_located(div_form, 10, name='password')

                while intentos_ingreso_password_gmail < 6:

                    if input_pass_gmail.is_displayed() and input_pass_gmail.is_enabled():
                        HtmlActions.enviar_data_keys(input_pass_gmail, json_args['password'], name='password')
                    else:
                        intentos_ingreso_password_gmail = intentos_ingreso_password_gmail + 1

                    valor_input_password = input_pass_gmail.get_attribute('value')

                    if len(valor_input_password) > 0:
                        break

                    time.sleep(1)

                btn_next_gmail_sec_password = HtmlActions.webdriver_wait_element_to_be_clickable(
                    webdriver_test_ux, 10, id='passwordNext')
                HtmlActions.click_html_element(btn_next_gmail_sec_password, id='passwordNext')


            tiempo_step_inicio = Temporizador.obtener_tiempo_timer()

            webdriver_test_ux.switch_to.window(ventana_padre)

            HtmlActions.webdriver_wait_element_to_be_clickable(
                webdriver_test_ux, 10, class_name='maestro-nav__contents')

            json_eval = UtilsEvaluaciones.establecer_output_status_step(
                json_eval, 1, 0, True, constantes_evaluaciones_claro_drive.MSG_OUTPUT_INICIO_SESION_EXITOSO)

        except ElementNotInteractableException as e:
            msg_output = constantes_evaluaciones_claro_drive.MSG_OUTPUT_INICIO_SESION_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 1, 0, False, msg_output)

        except NoSuchElementException as e:
            msg_output = constantes_evaluaciones_claro_drive.MSG_OUTPUT_INICIO_SESION_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 1, 0, False, msg_output)

        except TimeoutException as e:
            msg_output = constantes_evaluaciones_claro_drive.MSG_OUTPUT_INICIO_SESION_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 1, 0, False, msg_output)

        except ElementClickInterceptedException as e:
            msg_output = constantes_evaluaciones_claro_drive.MSG_OUTPUT_INICIO_SESION_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 1, 0, False, msg_output)

        json_eval = UtilsEvaluaciones.finalizar_tiempos_en_step(json_eval, 1, tiempo_step_inicio, fecha_inicio)

        return json_eval

    def cargar_archivo_dropbox(self, webdriver_test_ux: WebDriver, json_eval, json_args, nombre_archivo_sin_ext,
                               nombre_archivo_con_ext):
        tiempo_step_inicio = Temporizador.obtener_tiempo_timer()
        fecha_inicio = Temporizador.obtener_fecha_tiempo_actual()

        if not UtilsEvaluaciones.se_ingreso_correctamente_a_la_sesion(json_eval):
            json_eval = UtilsEvaluaciones.generar_json_inicio_de_sesion_incorrecta(
                json_eval, tiempo_step_inicio, fecha_inicio, 2,
                constantes_evaluaciones_claro_drive.MSG_CARGA_ARCHIVO_FALLIDA_POR_INICIO_DE_SESION)

            return json_eval

        try:
            ValidacionesHtml.verificar_remover_ventana_configuracion(webdriver_test_ux)
            ValidacionesHtml.verificar_archivo_ya_existente_en_portal(webdriver_test_ux, nombre_archivo_sin_ext)

            input_carga_de_archivo = HtmlActions.webdriver_wait_presence_of_element_located(
                webdriver_test_ux, 10, xpath='//body/div/div/input[1]')

            HtmlActions.enviar_data_keys(input_carga_de_archivo, dataKey=json_args['pathImage'],
                                         xpath='//body/div/div/input[1]')

            HtmlActions.webdriver_wait_presence_of_element_located(
                webdriver_test_ux, 12, xpath='//div[@class="ReactModal__Content ReactModal__Content--after-open '
                                             'dig-Modal folder-picker-modal"]')

            btn_cargar = HtmlActions.webdriver_wait_presence_of_element_located(
                webdriver_test_ux, 12, xpath='//button[@class="dig-Button dig-Button--primary dig-Button--standard"]')

            HtmlActions.webdriver_wait_until_not_presence_of_element_located(
                webdriver_test_ux, 12, class_name='folder-picker__empty-message')

            WebDriverWait(webdriver_test_ux, 12).until(
                EC.presence_of_element_located((By.CLASS_NAME, 'folder-picker__empty-message')))

            HtmlActions.click_html_element(btn_cargar, xpath='//button[@class="dig-Button dig-Button--primary '
                                                             'dig-Button--standard"]')

            HtmlActions.webdriver_wait_presence_of_element_located(
                webdriver_test_ux, 720, xpath='//span[@class="dig-Snackbar-message "][text()="Se carg\u00F3 {}."]'.format(
                    nombre_archivo_con_ext))

            btn_cerrar_progreso_carga = HtmlActions.webdriver_wait_presence_of_element_located(
                webdriver_test_ux, 10, xpath='//span[@class="dig-Button-content"][text()="Cerrar"]')

            HtmlActions.click_html_element(btn_cerrar_progreso_carga,
                                           xpath='//span[@class="dig-Button-content"][text()="Cerrar"]')

            json_eval = UtilsEvaluaciones.establecer_output_status_step(
                json_eval, 2, 0, True, constantes_evaluaciones_claro_drive.MSG_OUTPUT_CARGA_ARCHIVO_EXITOSO)

        except ElementNotInteractableException as e:
            msg_output = constantes_evaluaciones_claro_drive.MSG_OUTPUT_CARGA_ARCHIVO_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 2, 0, False, msg_output)

        except NoSuchElementException as e:
            msg_output = constantes_evaluaciones_claro_drive.MSG_OUTPUT_CARGA_ARCHIVO_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 2, 0, False, msg_output)

        except TimeoutException as e:
            msg_output = constantes_evaluaciones_claro_drive.MSG_OUTPUT_CARGA_ARCHIVO_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 2, 0, False, msg_output)

        except ElementClickInterceptedException as e:
            msg_output = constantes_evaluaciones_claro_drive.MSG_OUTPUT_CARGA_ARCHIVO_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 2, 0, False, msg_output)

        json_eval = UtilsEvaluaciones.finalizar_tiempos_en_step(json_eval, 2, tiempo_step_inicio, fecha_inicio)

        return json_eval

    def descargar_archivo_dropbox(self, webdriver_test_ux: WebDriver, json_eval, nombre_archivo_con_ext):

        extension_del_archivo = path.splitext(nombre_archivo_con_ext)[1]
        nombre_del_archivo_sin_extension = Path(nombre_archivo_con_ext).stem

        tiempo_step_inicio = Temporizador.obtener_tiempo_timer()
        fecha_inicio = Temporizador.obtener_fecha_tiempo_actual()

        if not UtilsEvaluaciones.se_ingreso_correctamente_a_la_sesion(json_eval):
            json_eval = UtilsEvaluaciones.generar_json_inicio_de_sesion_incorrecta(
                json_eval, tiempo_step_inicio, fecha_inicio, 3,
                constantes_evaluaciones_claro_drive.MSG_DESCARGA_ARCHIVO_FALLIDA_POR_CARGA_ARCHIVO_FALLIDA)

            return json_eval

        try:
            ValidacionesHtml.verificar_remover_ventana_configuracion(webdriver_test_ux)

            search_bar = HtmlActions.webdriver_wait_element_to_be_clickable(
                webdriver_test_ux, 20, class_name='search__input')

            HtmlActions.enviar_data_keys(search_bar, nombre_archivo_con_ext, class_name='search__input')
            #time.sleep(1)
            HtmlActions.enviar_data_keys(search_bar, Keys.RETURN, class_name='search__input')

            archivo_por_descargar = HtmlActions.webdriver_wait_element_to_be_clickable(
                webdriver_test_ux, 20, xpath='//tr[@data-filename="{}"]'.format(nombre_archivo_con_ext))

            HtmlActions.click_html_element(archivo_por_descargar, xpath='//tr[@data-filename="{}"]')

            btn_mas_acciones = HtmlActions.webdriver_wait_element_to_be_clickable(
                archivo_por_descargar, 20, xpath='//button[@data-testid="action-bar-overflow"]')

            HtmlActions.click_html_element(btn_mas_acciones, xpath='//button[@data-testid="action-bar-overflow"]')

            btn_descargar = HtmlActions.webdriver_wait_element_to_be_clickable(
                webdriver_test_ux, 20, xpath='//div[@class="dig-Menu-row-title"][text()="Descargar"]')

            HtmlActions.click_html_element(btn_descargar,
                                           xpath='//div[@class="dig-Menu-row-title"][text()="Descargar"]')

            UtilsEvaluaciones.verificar_descarga_en_ejecucion(nombre_del_archivo_sin_extension, extension_del_archivo)

            json_eval = UtilsEvaluaciones.establecer_output_status_step(
                json_eval, 3, 0, True, constantes_evaluaciones_claro_drive.MSG_OUTPUT_DESCARGA_ARCHIVO_EXITOSO)

        except ElementNotInteractableException as e:
            msg_output = constantes_evaluaciones_claro_drive.MSG_OUTPUT_DESCARGA_ARCHIVO_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 3, 0, False, msg_output)

        except NoSuchElementException as e:
            msg_output = constantes_evaluaciones_claro_drive.MSG_OUTPUT_DESCARGA_ARCHIVO_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 3, 0, False, msg_output)

        except TimeoutException as e:
            msg_output = constantes_evaluaciones_claro_drive.MSG_OUTPUT_DESCARGA_ARCHIVO_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 3, 0, False, msg_output)

        except ElementClickInterceptedException as e:
            msg_output = constantes_evaluaciones_claro_drive.MSG_OUTPUT_DESCARGA_ARCHIVO_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 3, 0, False, msg_output)

        except StaleElementReferenceException as e:
            msg_output = constantes_evaluaciones_claro_drive.MSG_OUTPUT_DESCARGA_ARCHIVO_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 3, 0, False, msg_output)

        json_eval = UtilsEvaluaciones.finalizar_tiempos_en_step(json_eval, 3, tiempo_step_inicio, fecha_inicio)

        return json_eval

    def eliminar_archivo_dropbox(self, webdriver_test_ux: WebDriver, json_eval, nombre_archivo_con_ext):
        tiempo_step_inicio = Temporizador.obtener_tiempo_timer()
        fecha_inicio = Temporizador.obtener_fecha_tiempo_actual()

        if not UtilsEvaluaciones.se_ingreso_correctamente_a_la_sesion(json_eval):
            json_eval = UtilsEvaluaciones.generar_json_inicio_de_sesion_incorrecta(
                json_eval, tiempo_step_inicio, fecha_inicio, 4,
                constantes_evaluaciones_claro_drive.MSG_ELIMINACION_ARCHIVO_FALLIDA_POR_CARGA_ARCHIVO_FALLIDA)

            return json_eval

        try:

            archivo_por_eliminar = HtmlActions.webdriver_wait_element_to_be_clickable(
                webdriver_test_ux, 20, xpath='//tr[@data-filename="{}"]'.format(nombre_archivo_con_ext))

            HtmlActions.click_html_element(archivo_por_eliminar, xpath='//tr[@data-filename="{}"]')

            btn_mas_acciones = HtmlActions.webdriver_wait_element_to_be_clickable(
                archivo_por_eliminar, 20, xpath='//button[@data-testid="action-bar-overflow"]')

            HtmlActions.click_html_element(btn_mas_acciones, xpath='//button[@data-testid="action-bar-overflow"]')

            btn_eliminar = HtmlActions.webdriver_wait_element_to_be_clickable(
                webdriver_test_ux, 20, xpath='//div[@class="dig-Menu-row-title"][text()="Eliminar"]')

            HtmlActions.click_html_element(btn_eliminar,
                                           xpath='//div[@class="dig-Menu-row-title"][text()="Eliminar"]')

            btn_eliminar_modal = HtmlActions.webdriver_wait_element_to_be_clickable(
                webdriver_test_ux, 20, xpath='//span[@class="dig-Button-content"][text()="Eliminar"]')

            HtmlActions.click_html_element(
                btn_eliminar_modal, xpath='//span[@class="dig-Button-content"][text()="Eliminar"]')

            HtmlActions.webdriver_wait_presence_of_element_located(
                webdriver_test_ux, 30,
                xpath='//span[@class="dig-Snackbar-message "][text()="Se elimin\u00F3 1 elemento."]')

            json_eval = UtilsEvaluaciones.establecer_output_status_step(
                json_eval, 4, 0, True, constantes_evaluaciones_claro_drive.MSG_OUTPUT_BORRADO_ARCHIVO_EXITOSO)

        except ElementNotInteractableException as e:
            msg_output = constantes_evaluaciones_claro_drive.MSG_OUTPUT_BORRADO_ARCHIVO_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 4, 0, False, msg_output)

        except NoSuchElementException as e:
            msg_output = constantes_evaluaciones_claro_drive.MSG_OUTPUT_BORRADO_ARCHIVO_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 4, 0, False, msg_output)

        except TimeoutException as e:
            msg_output = constantes_evaluaciones_claro_drive.MSG_OUTPUT_BORRADO_ARCHIVO_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 4, 0, False, msg_output)

        except ElementClickInterceptedException as e:
            msg_output = constantes_evaluaciones_claro_drive.MSG_OUTPUT_BORRADO_ARCHIVO_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 4, 0, False, msg_output)

        json_eval = UtilsEvaluaciones.finalizar_tiempos_en_step(json_eval, 4, tiempo_step_inicio, fecha_inicio)

        return json_eval

    def cerrar_sesion_dropbox(self, webdriver_test_ux: WebDriver, json_eval):
        tiempo_step_inicio = Temporizador.obtener_tiempo_timer()
        fecha_inicio = Temporizador.obtener_fecha_tiempo_actual()

        if not UtilsEvaluaciones.se_ingreso_correctamente_a_la_sesion(json_eval):
            json_eval = UtilsEvaluaciones.generar_json_inicio_de_sesion_incorrecta(
                json_eval, tiempo_step_inicio, fecha_inicio, 5,
                constantes_evaluaciones_claro_drive.MSG_CIERRE_SESION_FALLIDA_POR_INICIO_DE_SESION)

            return json_eval

        try:
            boton_imagen_perfil = HtmlActions.webdriver_wait_element_to_be_clickable(
                webdriver_test_ux, 12, class_name='account-menu-v2__avatar')

            HtmlActions.click_html_element(boton_imagen_perfil, class_name='account-menu-v2__avatar')

            boton_salir_sesion = HtmlActions.webdriver_wait_element_to_be_clickable(
                webdriver_test_ux, 12, xpath='//div[@class="dig-Menu-row-title"][text()="Salir"]')

            HtmlActions.click_html_element(boton_salir_sesion, xpath='//div[@class="dig-Menu-row-title"][text()="Salir')

            HtmlActions.webdriver_wait_presence_of_element_located(webdriver_test_ux, 10, name='login_email')
            HtmlActions.webdriver_wait_presence_of_element_located(webdriver_test_ux, 10, name='login_password')

            json_eval = UtilsEvaluaciones.establecer_output_status_step(
                json_eval, 5, 0, True, constantes_evaluaciones_claro_drive.MSG_OUTPUT_CIERRE_SESION_EXITOSO)

        except ElementNotInteractableException as e:
            msg_output = constantes_evaluaciones_claro_drive.MSG_OUTPUT_CIERRE_SESION_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 5, 0, False, msg_output)

        except NoSuchElementException as e:
            msg_output = constantes_evaluaciones_claro_drive.MSG_OUTPUT_CIERRE_SESION_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 5, 0, False, msg_output)

        except TimeoutException as e:
            msg_output = constantes_evaluaciones_claro_drive.MSG_OUTPUT_CIERRE_SESION_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 5, 0, False, msg_output)

        except ElementClickInterceptedException as e:
            msg_output = constantes_evaluaciones_claro_drive.MSG_OUTPUT_CIERRE_SESION_SIN_EXITO.format(e.msg)
            json_eval = UtilsEvaluaciones.establecer_output_status_step(json_eval, 5, 0, False, msg_output)

        json_eval = UtilsEvaluaciones.finalizar_tiempos_en_step(json_eval, 5, tiempo_step_inicio, fecha_inicio)

        return json_eval
