from habilidades.habilidad import Habilidad

NOMBRE_HABILIDAD = "nombre"


class TemplateHabilidad(Habilidad):

    def __init__(self):
        pass

    def aplicar_en_carta(self, carta):
        raise NotImplementedError

    def aplicar_en_tablero(self, tablero, jugador):
        raise NotImplementedError

    def revertir_en_carta(self, carta):
        raise NotImplementedError

    def revertir_en_tablero(self, tablero, jugador):
        raise NotImplementedError

    def resetear_habilidad(self):
        pass

    def obtener_nombre(self):
        return NOMBRE_HABILIDAD

    def obtener_texto(self):
        return ""


def obtener_habilidad():
    return TemplateHabilidad()