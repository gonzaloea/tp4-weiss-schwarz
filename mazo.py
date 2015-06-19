import random
from carta import CartaPersonaje, CartaEvento, CartaClimax
import habilidades
from habilidades import *

LIMITE_CARTAS_MAZO = 50
LIMITE_COPIAS_CARTA = 4
LIMITE_CARTAS_CLIMAX = 8

TIPO_CARTA = 0
NOMBRE_CARTA = 1
COLOR = 2
EFECTO_EXTRA = 3
HABILIDAD = 4
TEXTO_DECORATIVO = 5
NIVEL = 6
COSTE = 7
PODER = 8
PUNTOS_DE_ALMA = 9
SUBTIPOS = 10


def generar_diccionario_habilidades():
    """
    Genera y devuelve un diccionario con todas las habilidades que se usan. La clave es el nombre de la habilidad,
    obtenido de la constante NOMBRE_HABILIDAD de cada una, y el valor asociado es una referencia a la funcion
    obtener_habilidad de la misma.
    :return: Diccionario con la forma descripta.
    """
    lista_habilidades = {}
    for modulo in [habilidades.__getattribute__(x) for x in dir(habilidades) if x[0] != "_"]:
        lista_habilidades[modulo.NOMBRE_HABILIDAD] = modulo.obtener_habilidad

    return lista_habilidades


class Mazo(object):
    """ Clase que mantiene y emula el mazo de los jugadores. """

    def _cargar_mazo(self, archivo_mazo):
        """
        Genera las cartas y las carga en el mazo a partir del archivo pasado por parametro. El archivo debe tener un
        formato acorde a las especificaciones.
        :param archivo_mazo: String con la ruta al archivo de mazo a cargar.
        :return: No tiene valor de retorno.
        """
        try:
            mazo = open(archivo_mazo)
        except IOError:
            raise ValueError, "El archivo no se puede abrir"

        lista_habilidades = generar_diccionario_habilidades()

        cartas_totales = 0
        cartas_climax = 0
        cartas_cargadas = {}

        for linea in mazo:
            cartas_totales += 1
            if cartas_totales > LIMITE_CARTAS_MAZO:
                mazo.close()
                raise ValueError, "El archivo contiene mas de {0} cartas".format(str(LIMITE_CARTAS_MAZO))

            linea = linea.rstrip()
            campos = linea.split("|")

            tipo_carta = campos[TIPO_CARTA]
            nombre_carta = campos[NOMBRE_CARTA]
            color = campos[COLOR]
            efecto_extra = int(campos[EFECTO_EXTRA])
            habilidad = None

            if lista_habilidades.has_key(campos[HABILIDAD]):
                habilidad = lista_habilidades[campos[HABILIDAD]]()
                
            texto_decorativo = campos[TEXTO_DECORATIVO].replace("$", "\n")

            cartas_cargadas[nombre_carta] = cartas_cargadas.get(nombre_carta, 0) + 1

            if cartas_cargadas[nombre_carta] > LIMITE_COPIAS_CARTA:
                mazo.close()
                raise ValueError, "El archivo contiene mas de {0} copias de: {1}".format(str(LIMITE_COPIAS_CARTA),
                                                                                         nombre_carta)

            if tipo_carta == "CLIMAX":
                cartas_climax += 1

                if cartas_climax > LIMITE_CARTAS_CLIMAX:
                    mazo.close()
                    raise ValueError, "El archivo contiene mas de {0} cartas climax".format(str(LIMITE_CARTAS_CLIMAX),
                                                                                        nombre_carta)

                self.cartas.append(CartaClimax(nombre_carta, color, efecto_extra, habilidad, texto_decorativo))
                continue

            nivel = int(campos[NIVEL])
            coste = int(campos[COSTE])

            if tipo_carta == "EVENT":
                self.cartas.append(
                    CartaEvento(nombre_carta, color, efecto_extra, habilidad, texto_decorativo, nivel, coste))
                continue

            poder = int(campos[PODER])
            puntos_de_alma = int(campos[PUNTOS_DE_ALMA])
            tipos = campos[SUBTIPOS].split(",")

            if tipo_carta == "CHARACTER":
                self.cartas.append(
                    CartaPersonaje(nombre_carta, color, efecto_extra, habilidad, texto_decorativo, nivel, coste, poder,
                                   puntos_de_alma, tipos))

        mazo.close()

        if cartas_totales < LIMITE_CARTAS_MAZO:
            mazo.close()
            raise ValueError, "El archivo contiene menos de {0} cartas".format(str(LIMITE_CARTAS_MAZO))

    def __init__(self, archivo_mazo):
        self.cartas = []
        self._cargar_mazo(archivo_mazo)
        self.mezclar()

    def robar_carta(self):
        """
        Roba la carta del tope del mazo y la devuelve.
        :return: Carta robada del mazo, o None si esta vacio.
        """
        if self.esta_vacio():
            return None
        return self.cartas.pop()

    def apilar_carta(self, carta):
        """
        Apila la carta pasada por parametro, dejandola en el tope del mismo.
        :param carta: Carta a apilar.
        :return: No tiene valor de retorno.
        """
        self.cartas.append(carta)

    def agregar_cartas(self, lista_cartas):
        """
        Agrega las cartas de la lista pasada por parametro al mazo, en el orden en el que se pasan, al tope del mazo.
        :param lista_cartas: Lista con las cartas que se desean agregar al mazo.
        :return: No tiene valor de retorno.
        """
        self.cartas += lista_cartas

    def mezclar(self):
        """
        Mezcla las cartas del mazo, dejandolas en un orden aleatorio.
        :return: No tiene valor de retorno.
        """
        random.shuffle(self.cartas)

    def esta_vacio(self):
        """
        Devuelve True si no quedan mas cartas en el mazo, False en caso contrario.
        :return: Booleano que indica si quedan o no cartas en el mazo.
        """
        return len(self.cartas) == 0
