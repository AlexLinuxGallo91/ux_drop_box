import src.validaciones_json.constantes_json as const

class GeneradorJsonBaseEvaluacion:

    @staticmethod
    def establecer_estructura_principal_json(correo, cuerpo_principal_json):
        raiz = {}
        raiz.update({'node': correo})
        raiz.update({'body': cuerpo_principal_json})

        return raiz

    @staticmethod
    def establecer_raiz_json():
        raiz = {}
        raiz.update({"start": ""})
        raiz.update({"end": ""})
        raiz.update({"status": ""})
        raiz.update({"time": 0})
        raiz.update({"steps": []})

        return raiz

    @staticmethod
    def generar_nodo_padre(order, name='', status='', output=None, start="", end=""):
        if output is None:
            output = []

        nodo_padre = {}
        nodo_padre.update({"order": order})
        nodo_padre.update({"name": name})
        nodo_padre.update({"status": status})
        nodo_padre.update({"output": output})
        nodo_padre.update({"start": start})
        nodo_padre.update({"end": end})
        nodo_padre.update({"time": 0})

        return nodo_padre

    @staticmethod
    def generar_nodo_hijo(order, name='', status='', output=""):
        nodo_hijo = {}
        nodo_hijo.update({"order": order})
        nodo_hijo.update({"name": name})
        nodo_hijo.update({"status": status})
        nodo_hijo.update({"output": output})

        return nodo_hijo

    @staticmethod
    def generar_nuevo_template_json():
        # genera el nodo raiz
        json_a_enviar = GeneradorJsonBaseEvaluacion.establecer_raiz_json()

        # establece las 3 evaluaciones principales
        json_a_enviar["steps"].append(GeneradorJsonBaseEvaluacion.generar_nodo_padre(1))
        json_a_enviar["steps"].append(GeneradorJsonBaseEvaluacion.generar_nodo_padre(2))
        json_a_enviar["steps"].append(GeneradorJsonBaseEvaluacion.generar_nodo_padre(3))
        json_a_enviar["steps"].append(GeneradorJsonBaseEvaluacion.generar_nodo_padre(4))
        json_a_enviar["steps"].append(GeneradorJsonBaseEvaluacion.generar_nodo_padre(5))

        # establece cada uno los steps de cada evaluacion
        json_a_enviar["steps"][0]["output"] = [GeneradorJsonBaseEvaluacion.generar_nodo_hijo(1)]
        json_a_enviar["steps"][1]["output"] = [GeneradorJsonBaseEvaluacion.generar_nodo_hijo(1)]
        json_a_enviar["steps"][2]["output"] = [GeneradorJsonBaseEvaluacion.generar_nodo_hijo(1)]
        json_a_enviar["steps"][3]["output"] = [GeneradorJsonBaseEvaluacion.generar_nodo_hijo(1)]
        json_a_enviar["steps"][4]["output"] = [GeneradorJsonBaseEvaluacion.generar_nodo_hijo(1)]

        json_a_enviar["steps"][0]["name"] = const.STEP_NAME_1
        json_a_enviar["steps"][1]["name"] = const.STEP_NAME_2
        json_a_enviar["steps"][2]["name"] = const.STEP_NAME_3
        json_a_enviar["steps"][3]["name"] = const.STEP_NAME_4
        json_a_enviar["steps"][4]["name"] = const.STEP_NAME_5

        json_a_enviar["steps"][0]["output"][0]["name"] = const.STEP_OUTPUT_NAME_1
        json_a_enviar["steps"][1]["output"][0]["name"] = const.STEP_OUTPUT_NAME_2
        json_a_enviar["steps"][2]["output"][0]["name"] = const.STEP_OUTPUT_NAME_3
        json_a_enviar["steps"][3]["output"][0]["name"] = const.STEP_OUTPUT_NAME_4
        json_a_enviar["steps"][4]["output"][0]["name"] = const.STEP_OUTPUT_NAME_5

        return json_a_enviar
