from habilidad import Habilidad
from random import randrange
import tablero as imp_t
NOMBRE_HABILIDAD = "Destruir carta por dado"
#A6 Lanza un dado; destruye un personaje en la zona frontal segun el numero
#que salga. 1, 2, 3 corresponden al campo propio; 4, 5, 6 al enemigo.
class Habilidad_DestruirCartaPorDado(Habilidad):
    """ Habilidad que lanza un dado y destruye una carta de alguna de las zonas frontales. 
    1, 2, 3 corresponden al campo propio; 4, 5, 6 al enemigo."""

    def __init__(self):
        pass

    def aplicar_en_tablero(self, tablero, jugador):
        """
        Aplica la habilidad en el tablero pasado por parametro, a todas las cartas del campo frontal y la retaguardia.
        :param tablero: TableroJuego sobre el que se aplica la habilidad.
        :param jugador: Jugador que jugo la carta con la habilidad. Debe ser una de las constantes WEISS o SCHWARZ de
                        tablero.py.
        :return: No tiene valor de retorno.
        """
        
        resultado_dado = tablero.obtener_interfaz().lanzar_dado()

        if resultado_dado < 4:
            victima = tablero.obtener_oponente(jugador)
        else:
            victima = jugador
            
        cartas = tablero.obtener_cartas_campo_frontal(victima)
        for carta in cartas:
            if carta != None:
                tablero.remover_carta(victima, imp_t.CAMPO_FRONTAL ,cartas.index(carta))
                tablero.obtener_interfaz().mostrar_informacion(str(carta), "Carta destruida")
                break
        if carta == None:
            tablero.obtener_interfaz()).mostrar_informacion("No hay cartas.", "Carta destruida")

    def obtener_texto(self):
        """
        Devuelve el texto completo de la descripcion de la habilidad.
        :return: String que contiene la descripcion de la habilidad.
        """
        texto = self._obtener_texto_base()
        texto += "Lanza un dado. Si se obtiene 1, 2 o 3 destruye carta de su campo; 4, 5 o 6 del campo enemigo."
        return texto

    def obtener_nombre(self):
        """
        Devuelve el nombre completo de la habilidad, que corresponde a la constante NOMBRE_HABILIDAD.
        :return: String que contiene el nombre de la habilidad.
        """
        return NOMBRE_HABILIDAD


def obtener_habilidad():
    """
    Devuelve una instancia de la habilidad ReducirPoder1000.
    :return: Una nueva instancia de la clase Habilidad_DestruirCartaPorDado.
    """
    return Habilidad_DestruirCartaPorDado()
