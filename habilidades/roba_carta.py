from habilidades.habilidad import Habilidad
import interfaz

NOMBRE_HABILIDAD = "Robar carta lanzando una moneda"


class Habilidad_RobaCarta(Habilidad):
    """Lanza una moneda; mientras que sea cara, saca una carta del mazo del enemigo y la envia a su zona de descarte. 
    Se detiene cuando sale cruzo o el mazo enemigo esta vacio."""
    def __init__(self):
        pass
    
    def aplicar_en_tablero(self, tablero, jugador):
        """
        Aplica la habilidad en el tablero pasado por parametro a todas las cartas del mazo del oponente
        :param tablero: TableroJuego sobre el que se aplica la habilidad.
        :param jugador: Jugador que jugo la carta con la habilidad. Debe ser una de las constantes WEISS o SCHWARZ de tablero.py.
        :return: No tiene valor de retorno.
        """
        oponente = tablero.obtener_oponente(jugador)
        campo_oponente = tablero.obtener_campo_jugador(oponente)
        mazo_oponente = campo_oponente.obtener_mazo()
        while  tablero.obtener_interfaz().lanzar_moneda() == interfaz.CARA and not mazo_oponente.esta_vacio():
                carta_robada = tablero.robar_cartas(oponente)
                tablero.obtener_interfaz().mostrar_informacion(str(carta_robada[0]), "Carta descartada")
                campo_oponente.descartar_carta(carta_robada[0])
                tablero.obtener_interfaz().actualizar_tablero(tablero)
            
    def obtener_nombre(self):
        """
        Devuelve el nombre completo de la habilidad, que corresponde a la constante NOMBRE_HABILIDAD.
        :return
        """
        return NOMBRE_HABILIDAD

    def obtener_texto(self):
        """
        Devuelve el texto completo de la descripcion de la habilidad.
        :return: String que contiene la descripcion de la habilidad.
         """
        texto = self._obtener_texto_base()
        texto += "Lanza una moneda. Si sale cara roba una carta del mazo\n del oponente y la tira a su zona de descarte. Se detiene\n cuando sale cruz o el mazo del oponente esta vacio"
        return texto


def obtener_habilidad():
    """ 
    Devuelve una instancia de la habilidad_RobaCarta
    :return: Una nueva instancia de la clase Habilidad_RobaCarta.
    """
    return Habilidad_RobaCarta()
