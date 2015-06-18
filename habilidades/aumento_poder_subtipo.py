from habilidades.habilidad import Habilidad

NOMBRE_HABILIDAD = "aumento_poder_subtipo"


class Habilidad_AumentoPoderSubtipo(Habilidad):
    """ Habilidad que aumenta el poder de todas las cartas del subtipo especificado mientras la carta permanezca en campo. """
    def __init__(self):
        self.aumento = 1500
        self.subtipo = "Luchador"

    def aplicar_en_carta(self, carta):
        """
        Aplica el aumento al poder de la carta pasada por parametro, si esta coincide con el subtipo de la haibilidad.
        :param carta: Carta a la que se quiere aplicar el aumento.
        :return: No tiene valor de retorno.
        """
        if isinstance(carta, CartaPersonaje) and self.subtipo in carta.obtener_subtipos():
            carta.establecer_poder(carta.obtener_poder() + self.aumento)

    def aplicar_en_tablero(self, tablero, jugador):
        """
        Aplica la habilidad en el tablero pasado por parametro, a todas las cartas del campo frontal y la retaguardia.
        :param tablero: TableroJuego sobre el que se aplica la habilidad.
        :param jugador: Jugador que jugo la carta con la habilidad. Debe ser una de las constantes WEISS o SCHWARZ de
                        tablero.py.
        :return: No tiene valor de retorno.
        """
        cartas = tablero.obtener_cartas_campo_frontal(jugador)
        cartas += tablero.obtener_cartas_retaguardia(jugador)
        oponente = tablero.obtener_oponente(jugador)
        cartas += tablero.obtener_cartas_campo_frontal(oponente)
        cartas += tablero.obtener_cartas_retaguardia(oponente)
        for carta in cartas:
            if not carta:
                continue
            print carta
            self.aplicar_en_carta(carta)

    def revertir_en_carta(self, carta):
        """
        Revierte el efecto, disminuyendo el poder de la carta pasada por parametro del subtipo de la clase.
        :param carta: Carta sobre la que se desea revertir el efecto de la habilidad.
        :return: No tiene valor de retorno.
        """
        if isinstance(carta, CartaPersonaje) and self.subtipo in carta.obtener_subtipos():
            carta.establecer_poder(carta.obtener_poder() - self.aumento)

    def revertir_en_tablero(self, tablero, jugador):
        """
        Revierte el efecto de la habilidad en el tablero pasado por parametro, volviendo las cartas afectadas al estado
        que tenian antes de aplicarla.
        :param tablero: TableroJuego sobre el que se aplica la habilidad.
        :param jugador: Jugador que jugo la carta con la habilidad.
        :return: No tiene valor de retorno.
        """
        cartas = tablero.obtener_cartas_campo_frontal(jugador)
        cartas += tablero.obtener_cartas_retaguardia(jugador)
        oponente = tablero.obtener_oponente(jugador)
        cartas += tablero.obtener_cartas_campo_frontal(oponente)
        cartas += tablero.obtener_cartas_retaguardia(oponente)
        for carta in cartas:
            if not carta:
                continue
            self.revertir_en_carta(carta)

    def obtener_nombre(self):
        return NOMBRE_HABILIDAD

    def obtener_texto(self):
        """
        Devuelve el texto completo de la descripcion de la habilidad.
        :return: String que contiene la descripcion de la habilidad.
        """
        texto = self._obtener_texto_base()
        texto += "Aumenta los puntos de poder de las cartas del subtipo "+str(self.subtipo)+" en "
        texto += str(self.aumento)+"puntos mientras la carta permanezca en el campo"
        return texto



def obtener_habilidad():
    """
    Devuelve una instancia de la habilidad AumentoPoderSubtipo.
    :return: Una nueva instancia de la clase Habilidad_AumentoPoderSubtipo.
    """
    return Habilidad_AumentoPoderSubtipo()
