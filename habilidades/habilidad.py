# Nombre de la habilidad. Debe ser un identificador unico, que sirva como clave para distinguir la habilidad de otras.
NOMBRE_HABILIDAD = " "

class Habilidad(object):
    """ Clase base para todas las habilidades.
        Las habilidades puede tener uno o mas objetivos, no tener ninguno o ser un efecto general. Pueden interactuar
        con las cartas, los jugadores, las distintas areas del tablero, los mazos, etc. Sus efectos pueden ser
        inmediatos (suceden en el momento, como robar cartas extra o destruir un personaje), temporales (un efecto que
        dura hasta el final del turno) o permanentes (su efecto nunca se deshace). Ademas de aplicar los efectos y
        modificaciones, las habilidades deben ser capaz de revertirlos (cuando corresponda)."""

    def __init__(self):
        pass

    def aplicar_en_carta(self, carta):
        """
        Aplica el efecto de la habilidad en la carta pasada por parametro. Si la habilidad no se aplica a cartas, no
        es necesario implementar este metodo.
        :param carta: Carta sobre la que se aplica el efecto.
        :return: No tiene valor de retorno.
        """
        pass

    def aplicar_en_tablero(self, tablero, jugador):
        """
        Aplica el efecto de la habilidad de la carta del jugador pasado por parametro en el tablero de juego dado.
        Este metodo es llamado al jugar la carta que tiene la habilidad, por lo que siempre debe implementarse.
        :param tablero: TableroJuego sobre el que se desarrolla el juego, y sobre el que se quiere aplicar la habilidad.
        :param jugador: Jugador que juega la carta que tiene la habilidad. Es una de las constantes WEISS o SCHWARZ de
                        tablero.py.
        :return: No tiene valor de retorno.
        """
        pass

    def revertir_en_carta(self, carta):
        """
        Revierte el efecto aplicado en la carta pasada por parametro. Si la habilidad no se aplica a cartas, no es
        necesario implementar este metodo.
        :param carta: Carta sobre la que se desea revertir el efecto aplicado por la habilidad.
        :return: No tiene valor de retorno.
        """
        pass

    def revertir_en_tablero(self, tablero, jugador):
        """
        Revierte el efecto aplicado por la habilidad, cuando y como corresponda.
        :param tablero: TableroJuego sobre el que se desarrolla el juego, y sobre el que se quiere aplicar la habilidad.
        :param jugador: Jugador que juega la carta que tiene la habilidad. Es una de las constantes WEISS o SCHWARZ de
                        tablero.py.
        :return: No tiene valor de retorno.
        """
        pass

    def _obtener_texto_base(self):
        return "HABILIDAD: [{0}]\n".format(self.obtener_nombre())

    def resetear_habilidad(self):
        """
        Si la habilidad posee algun estado interno, este metodo debe resetaerlo como si fuese recien construida.
        :return: No tiene valor de retorno
        """
        pass

    def obtener_nombre(self):
        """
        Devuelve el nombre de la habilidad.
        :return: String con el contenido de NOMBRE_HABILIDAD
        """
        return NOMBRE_HABILIDAD

    def obtener_texto(self):
        """
        Devuelve el texto completo de la habilidad. El mismo debe contener el nombre, describir el efecto de la
        habilidad y cualquier informacion que se considere necesaria. Este texto se usa para mostrar el nombre y
        descripcion de la habilidad en la interfaz.
        :return: String con el texto completo de la habilidad.
        """
        pass

def obtener_habilidad():
    """
    Devuelve una nueva instancia de la habilidad.
    :return: Un nuevo objeto de una clase que hereda de Habilidad.
    """
    return None