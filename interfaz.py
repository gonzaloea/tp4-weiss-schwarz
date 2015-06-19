from Tkinter import Tk, Label
import pygame
import random
from time import sleep
import tkMessageBox
import tkSimpleDialog
from tablero import WEISS, SCHWARZ

import creador_cartas

CRUZ = "cruz"
CARA = "cara"

RESOLUCION = (800, 500)

ANCHO_PUNTO = 20

ALTO_CARTA_TABLERO = 10 * ANCHO_PUNTO
ANCHO_CARTA_TABLERO = 7 * ANCHO_PUNTO

LADO_AREA_CARTA = 12 * ANCHO_PUNTO

ALTO_BACKGROUND = LADO_AREA_CARTA * 5
ANCHO_BACKGROUND = LADO_AREA_CARTA * 8

POSICION_ANCHO_LABEL_PODER = ANCHO_CARTA_TABLERO / 4
POSICION_ALTO_LABEL_PODER = ALTO_CARTA_TABLERO / 2

class Interfaz_Ventana(object):
    """ Interfaz grafica del juego. """
    
    def __init__(self):
        pygame.init()
        self.tk_window = Tk()
        self.label_imagen = Label()

        self.surface_cartas = {}

    def obtener_entero(self, mensaje, titulo="", intervalo=[]):
        """
        Pide al usuario que ingrese un numero entero, mostrando el mensaje pasado por parametro. Si se recibe un 
        intervalo, el numero debe pertenecer al mismo.
        :param mensaje: Mensaje a mostrar en la ventana al pedir el numero.
        :param titulo: Titulo de la ventana.
        :param intervalo: Lista de dos numeros, de la forma [min, max]. Si se recibe, el numero que se pida debe ser 
                          mayor o igual a min y menor o igual a max. Se seguira pidiendo al usuario que ingrese un 
                          numero hasta que se cumplan las condiciones.
        :return: Numero entero ingresado por el usuario.
        """
        if not intervalo:
            return tkSimpleDialog.askinteger(titulo, mensaje, parent=self.tk_window)
        return tkSimpleDialog.askinteger(titulo, mensaje, parent=self.tk_window, minvalue=intervalo[0],
                                         maxvalue=intervalo[1])

    def mostrar_informacion(self, mensaje, titulo=""):
        """
        Muestra una ventana con el mensaje pasado por parametro.
        :param mensaje: Mensaje que se mostrara en la ventana.
        :param titulo: Titulo de la ventana.
        :return: No tiene valor de retorno.
        """
        tkMessageBox.askquestion(titulo, mensaje, type=tkMessageBox.OK, icon="info")

    def preguntar_si_no(self, mensaje, titulo=""):
        """
        Muestra el mensaje recibido por parametro y pide que se conteste si o no. Devuelve True si se contesto si, 
        False si se contesto no.
        :param mensaje: Mensaje a mostrar en la ventana.
        :param titulo: Titulo de la ventana.
        :return: Booleano que indica si se contesto si.
        """
        resultado = tkMessageBox.askquestion(titulo, mensaje, type=tkMessageBox.YESNO)
        return resultado == "yes"

    def mostrar_carta(self, carta, titulo=""):
        """
        Muestra una ventana con la imagen que corresponde a la carta pasada por parametro.
        :param carta: Carta que se quiere mostrar su imagen correspondiente.
        :param titulo: Titulo de la ventana.
        :return: No tiene valor de retorno.
        """
        self.label_imagen.destroy()

        c = self.__obtener_surface_carta(carta)
        from PIL import Image, ImageTk

        imagen = Image.fromstring('RGBA', c.get_rect()[2:], pygame.image.tostring(c, "RGBA"))
        foto = ImageTk.PhotoImage(imagen)

        self.label_imagen = Label(image=foto)
        self.label_imagen.image = foto  # keep a reference!
        self.label_imagen.pack()
        self.tk_window.title(titulo)

        self.tk_window.update()
        sleep(2)

    def __obtener_surface_carta(self, carta):
        """
        Devuelve la imagen correspondiente a la carta pasada por parametro. Si la imagen no esta guardada, se genera y 
        se guarda.
        :param carta: Carta que se quiere mostrar su imagen. 
        :return: Surface con la imagen correspondiente a la carta.
        """
        str_carta = str(carta)
        if not self.surface_cartas.has_key(str_carta):
            self.surface_cartas[str_carta] = creador_cartas.generar_imagen_carta(carta)

        return self.surface_cartas[str_carta]

    def __dibujar_cartas_personaje(self, background, zona_campo, posicion, rotacion):
        for carta in zona_campo:
            fuente = pygame.font.Font("resources/agfarotissemiserif.ttf", 30)

            if carta:
                surface_carta = self.__obtener_surface_carta(carta)
                surface_carta = pygame.transform.scale(surface_carta, (ANCHO_CARTA_TABLERO, ALTO_CARTA_TABLERO))

                label_poder = fuente.render(str(carta.obtener_poder()), 1, (0, 0, 0))
                surface_carta.blit(label_poder, (POSICION_ANCHO_LABEL_PODER, POSICION_ALTO_LABEL_PODER))

                surface_carta = pygame.transform.rotate(surface_carta, rotacion)
                background.blit(surface_carta, posicion)

            posicion[1] += LADO_AREA_CARTA

    def __dibujar_campo_frontal(self, background, posicion_frontal_izquierda, rotacion, campo_frontal):
        posicion = [posicion_frontal_izquierda + LADO_AREA_CARTA / 12, LADO_AREA_CARTA + (5 * LADO_AREA_CARTA) / 24]

        self.__dibujar_cartas_personaje(background, campo_frontal, posicion, rotacion)

    def __dibujar_retaguardia(self, background, posicion_frontal_izquierda, rotacion, retaguardia):
        posicion = [posicion_frontal_izquierda + LADO_AREA_CARTA / 12,
                    (3 * LADO_AREA_CARTA) / 2 + (5 * LADO_AREA_CARTA) / 24]

        self.__dibujar_cartas_personaje(background, retaguardia, posicion, rotacion)

    def __dibujar_climax(self, background, posicion_frontal_izquierda, rotacion, carta_climax):
        posicion = [posicion_frontal_izquierda + (5 * LADO_AREA_CARTA) / 24, 2 * LADO_AREA_CARTA + LADO_AREA_CARTA / 12]

        if not carta_climax:
            return

        self.__dibujar_carta_individual(background, carta_climax, posicion, rotacion)

    def __dibujar_carta_individual(self, background, discard_top, posicion, rotacion):
        surface_carta = self.__obtener_surface_carta(discard_top)
        surface_carta = pygame.transform.scale(surface_carta, (ANCHO_CARTA_TABLERO, ALTO_CARTA_TABLERO))
        surface_carta = pygame.transform.rotate(surface_carta, rotacion)
        background.blit(surface_carta, posicion)

    def __dibujar_descarte_weiss(self, background, posicion_frontal_izquierda, rotacion, discard_top):
        posicion = [posicion_frontal_izquierda + LADO_AREA_CARTA / 12, 4 * LADO_AREA_CARTA + (5 * LADO_AREA_CARTA) / 24]

        if not discard_top:
            return

        self.__dibujar_carta_individual(background, discard_top, posicion, rotacion)

    def __dibujar_descarte_schwarz(self, background, posicion_frontal_izquierda, rotacion, discard_top):
        posicion = [posicion_frontal_izquierda + LADO_AREA_CARTA / 12, (5 * LADO_AREA_CARTA) / 24]

        if not discard_top:
            return

        self.__dibujar_carta_individual(background, discard_top, posicion, rotacion)

    def __dibujar_clock_weiss(self, background, posicion_frontal_izquierda, rotacion, clock):
        posicion = [posicion_frontal_izquierda + LADO_AREA_CARTA / 12, LADO_AREA_CARTA + (3 * LADO_AREA_CARTA) / 24]

        for carta in clock:
            if carta:
                self.__dibujar_carta_individual(background, carta, posicion, rotacion)

            posicion[1] += (3 * ANCHO_CARTA_TABLERO) / 4

    def __dibujar_clock_schwarz(self, background, posicion_frontal_izquierda, rotacion, clock):
        posicion = [posicion_frontal_izquierda + LADO_AREA_CARTA / 12,
                    4 * LADO_AREA_CARTA - (3 * LADO_AREA_CARTA) / 24 - ANCHO_CARTA_TABLERO]

        for carta in clock:
            if carta:
                self.__dibujar_carta_individual(background, carta, posicion, rotacion)

            posicion[1] -= (3 * ANCHO_CARTA_TABLERO) / 4

    def __dibujar_nivel_weiss(self, background, posicion_frontal_izquierda, rotacion, nivel):
        posicion = [posicion_frontal_izquierda + LADO_AREA_CARTA / 12, LADO_AREA_CARTA / 12]

        for carta in nivel:
            if carta:
                self.__dibujar_carta_individual(background, carta, posicion, rotacion)

            posicion[0] += ANCHO_CARTA_TABLERO / 3

    def __dibujar_nivel_schwarz(self, background, posicion_frontal_izquierda, rotacion, nivel):
        posicion = [posicion_frontal_izquierda + LADO_AREA_CARTA / 3, 4 * LADO_AREA_CARTA + LADO_AREA_CARTA / 12]

        for carta in nivel:
            if carta:
                self.__dibujar_carta_individual(background, carta, posicion, rotacion)

            posicion[0] -= ANCHO_CARTA_TABLERO / 3

    def __dibujar_recursos_weiss(self, background, posicion_frontal_izquierda, rotacion, recursos):
        posicion = [posicion_frontal_izquierda + LADO_AREA_CARTA / 4, LADO_AREA_CARTA / 12]

        for carta in recursos:
            if carta:
                self.__dibujar_carta_individual(background, carta, posicion, rotacion)

            posicion[0] -= ANCHO_CARTA_TABLERO / 3

    def __dibujar_recursos_schwarz(self, background, posicion_frontal_izquierda, rotacion, recursos):
        posicion = [posicion_frontal_izquierda + LADO_AREA_CARTA / 5, 4 * LADO_AREA_CARTA + LADO_AREA_CARTA / 12]

        for carta in recursos:
            if carta:
                self.__dibujar_carta_individual(background, carta, posicion, rotacion)

            posicion[0] += ANCHO_CARTA_TABLERO / 3

    def __generar_tablero(self, tablero):
        background = pygame.image.load("resources/background.png")
        background = pygame.transform.scale(background, (ANCHO_BACKGROUND, ALTO_BACKGROUND))

        campo_frontal = tablero.obtener_todas_campo_frontal()

        posicion_frontal_izquierda = 0
        self.__dibujar_clock_weiss(background, posicion_frontal_izquierda, -90,
                                   tablero.obtener_cartas_clock(WEISS))
        self.__dibujar_nivel_weiss(background, posicion_frontal_izquierda, 0, tablero.obtener_cartas_nivel(WEISS))

        posicion_frontal_izquierda += LADO_AREA_CARTA
        self.__dibujar_climax(background, posicion_frontal_izquierda, 0, tablero.obtener_climax(WEISS))
        self.__dibujar_descarte_weiss(background, posicion_frontal_izquierda, -90,
                                     tablero.obtener_tope_espera(WEISS))

        posicion_frontal_izquierda += LADO_AREA_CARTA
        self.__dibujar_retaguardia(background, posicion_frontal_izquierda, -90,
                                  tablero.obtener_cartas_retaguardia(WEISS))

        posicion_frontal_izquierda += LADO_AREA_CARTA
        self.__dibujar_recursos_weiss(background, posicion_frontal_izquierda, 0, tablero.obtener_cartas_recursos(WEISS))
        self.__dibujar_campo_frontal(background, posicion_frontal_izquierda, -90,
                                   tablero.obtener_cartas_campo_frontal(WEISS))

        posicion_frontal_izquierda += LADO_AREA_CARTA
        self.__dibujar_campo_frontal(background, posicion_frontal_izquierda, 90,
                                   tablero.obtener_cartas_campo_frontal(SCHWARZ)[::-1])
        self.__dibujar_recursos_schwarz(background, posicion_frontal_izquierda, 180,
                                     tablero.obtener_cartas_recursos(SCHWARZ))

        posicion_frontal_izquierda += LADO_AREA_CARTA
        self.__dibujar_retaguardia(background, posicion_frontal_izquierda, 90,
                                  tablero.obtener_cartas_retaguardia(SCHWARZ)[::-1])

        posicion_frontal_izquierda += LADO_AREA_CARTA
        self.__dibujar_descarte_schwarz(background, posicion_frontal_izquierda, 90,
                                       tablero.obtener_tope_espera(SCHWARZ))
        self.__dibujar_climax(background, posicion_frontal_izquierda, 180,
                                   tablero.obtener_climax(SCHWARZ))

        posicion_frontal_izquierda += LADO_AREA_CARTA
        self.__dibujar_clock_schwarz(background, posicion_frontal_izquierda, 90,
                                     tablero.obtener_cartas_clock(SCHWARZ))
        self.__dibujar_nivel_schwarz(background, posicion_frontal_izquierda, 180,
                                     tablero.obtener_cartas_nivel(SCHWARZ))

        return pygame.transform.scale(background, RESOLUCION)

    def actualizar_tablero(self, tablero):
        """
        Actualiza y muestra el tablero de juego.
        :param tablero: TableroJuego del que se quiere mostrar el estado.
        :return: No tiene valor de retorno.
        """
        surface_tablero = self.__generar_tablero(tablero)
        pantalla = pygame.display.set_mode(surface_tablero.get_size())
        pantalla.blit(surface_tablero, (0, 0))
        pygame.display.set_caption("Tablero")
        pygame.display.flip()

    def lanzar_dado(self):
        """
        Simula el lanzamiento de un dado de 6 caras y muestra en una ventana informativa el resultado obtenido.
        :return: Entero de 1 a 6, que es el resultado de la tirada de dado.
        """
        resultado = random.randrange(1, 6)
        self.mostrar_informacion("Salio: " + str(resultado), "Dado lanzado")
        return resultado

    def lanzar_moneda(self):
        """
        Simula el lanzamiento de una moneda y muestra el resultado en una ventana informativa.
        :return: String con las contantes CARA o CRUZ, que es el resultado del lanzamiento de la moneda.
        """
        resultado = random.choice([CARA, CRUZ])
        self.mostrar_informacion("Salio: " + resultado, "Moneda lanzada")
        return resultado
