from habilidades.habilidad import Habilidad

NOMBRE_HABILIDAD = "Reducir Poder Nivel 1"

class Habilidad_ReducirPoderNivel1(Habilidad):
    """ Habilidad que reduce el poder de todas las cartas nivel 1 hasta el final del turno. """

    def __init__(self):
        self.modificador = 1000

    def aplicar_en_carta(self, carta):
        """
        Aplica el modificador restando al poder de la carta pasada por parametro, si esta es nivel 1.
        :param carta: Carta a la que se quiere aplicar el modificador.
        :return: No tiene valor de retorno.
        """
        if carta.obtener_nivel() == 1:
            carta.establecer_poder(carta.obtener_poder() - self.modificador)

    def aplicar_en_tablero(self, tablero, jugador, interfaz):
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

    def obtener_texto(self):
        """
        Devuelve el texto completo de la descripcion de la habilidad.
        :return: String que contiene la descripcion de la habilidad.
        """
        texto = self._obtener_texto_base()
        texto += "Reduce los puntos de ataque de los personajes nivel 1 en " + str(self.modificador) + \
                 " hasta el final del turno."
        return texto

    def obtener_nombre(self):
        """
        Devuelve el nombre completo de la habilidad, que corresponde a la constante NOMBRE_HABILIDAD.
        :return: String que contiene el nombre de la habilidad.
        """
        return NOMBRE_HABILIDAD

    def revertir_en_carta(self, carta):
        """
        Revierte el efecto, aumentando el poder de la carta pasada por parametro.
        :param carta: Carta sobre la que se desea revertir el efecto de la habilidad.
        :return: No tiene valor de retorno.
        """
        if carta.obtener_nivel() == 1:
            carta.establecer_poder(carta.obtener_poder() + self.modificador)

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


def obtener_habilidad():
    """
    Devuelve una instancia de la habilidad ReducirPoder1000.
    :return: Una nueva instancia de la clase Habilidad_ReducirPoderNivel1.
    """
    return Habilidad_ReducirPoderNivel1()
