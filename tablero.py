# coding=utf-8
import random
from carta import CartaClimax, CartaPersonaje, CartaEvento

BENEFICIO_AUMENTAR_CLOCK = 2

NIVEL_MAX = 4
CLOCK_PARA_NIVEL = 7

RETAGUARDIA = 2
CAMPO_FRONTAL = 1
ZONAS = [RETAGUARDIA, CAMPO_FRONTAL]

FRONTAL_IZQUIERDA = -1
FRONTAL_CENTRO = 0
FRONTAL_DERECHA = 1
POSICIONES_CAMPO_FRONTAL = [FRONTAL_IZQUIERDA, FRONTAL_CENTRO, FRONTAL_DERECHA]

RETAGUARDIA_IZQUIERDA = 0
RETAGUARDIA_DERECHA = 1
POSICIONES_RETAGUARDIA = [RETAGUARDIA_IZQUIERDA, RETAGUARDIA_DERECHA]

SCHWARZ = "Schwarz"
WEISS = "Weiss"
JUGADORES = [WEISS,SCHWARZ]

SIN_GANADOR = ""

EFECTO_CONTINUO = 0
EFECTO_TEMPORAL = 1

POSICION_DESTRUIR_DEFENSOR = 1
POSICION_DESTRUIR_ATACANTE = 0


class _CampoJugador(object):
    """ Campo de un jugador. Mantiene el estado de su campo de juego, ejecuta y resuelve las acciones efectuadas por el
        jugador y las fases del juego (robar cartas, poner en el campo, combate, etc.)."""

    def __init__(self, nombre, mazo):
        """
        :param nombre: Nombre del jugador.
        :param mazo: Mazo del jugador
        :return: No tiene valor de retorno.
        """
        self.area_clock = []
        self.area_recursos = []
        self.area_nivel = []
        self.area_climax = None
        self.area_espera = []
        self.campo_frontal = [None, None, None]
        self.retaguardia = [None, None]

        self.mazo = mazo
        self.nombre = nombre

    def recibir_ataque(self, posicion_atacante, posicion_defensor, campo_oponente, interfaz):
        """
        Resuelve el combate entre la carta en posicion_atacante en el campo frontal del jugador y la carta en
        posicion_defensor del campo frontal del oponente. Devuelve el resultado del ataque, indicando que carta/s
        deben destruirse.
        :param posicion_atacante: Posicion en el campo del atacante de la carta atacante. Debe ser una de las
                                  constantes FRONTAL_IZQUIERDA,FRONTAL_CENTRO o FRONTAL_DERECHA.
        :param posicion_defensor: Posicion en el campo del defensor de la carta defensora. Debe ser una de las
                                  constantes FRONTAL_IZQUIERDA,FRONTAL_CENTRO o FRONTAL_DERECHA.
        :param campo_oponente: Referencia a un objeto de clase _CampoJugador, que corresponde al campo del oponente.
        :param interfaz: Referencia a la interfaz grafica.
        :return: Lista de la forma [destruir_atacante, destruir_defensora]. Cada posicion es True si la carta debe ser
        destruida, False en caso contrario.
        """
        numero_carta_atacante = POSICIONES_CAMPO_FRONTAL.index(posicion_atacante)
        numero_carta_defensor = POSICIONES_CAMPO_FRONTAL.index(posicion_defensor)
        carta_atacante = self.campo_frontal[numero_carta_atacante]
        carta_defensora = campo_oponente.campo_frontal[numero_carta_defensor]
        resultado = [False, False]

        # Si el atacante tiene poder igual o menor al defensor, el combate resulta en empate o derrota
        if carta_defensora and carta_atacante.poder <= carta_defensora.poder:
            # Em ambos casos se destruye el atacante
            resultado[POSICION_DESTRUIR_ATACANTE] = True
            # Si tienen el mismo poder, es un empate y se destruye también el defensor
            if carta_atacante.poder == carta_defensora.poder:
                resultado[POSICION_DESTRUIR_DEFENSOR] = True
            return resultado

        # Si se gana el combate (haya o no defensor), se activa el efecto extra del ataque
        carta_efecto_extra = self.mazo.robar_carta()
        puntos_efecto_extra = carta_efecto_extra.obetener_puntos_efecto_extra()
        puntos_alma = carta_atacante.puntos_alma + puntos_efecto_extra

        # Si no hay defensor, es un ataque directo y suma bono a los puntos de alma
        if not carta_defensora:
            puntos_alma += 1
        # Si hay defensor y su poder es menor que el atacante, se destruye
        elif carta_atacante.poder > carta_defensora.poder:
            resultado[POSICION_DESTRUIR_DEFENSOR] = True

        # Se muestra la carta del efecto extra y el bono que suma en la interfaz
        interfaz.mostrar_carta(carta_efecto_extra, "Carta efecto extra: +" + str(puntos_efecto_extra) + " puntos de alma")
        # Se aplica el daño al oponente
        campo_oponente.resolver_ataque(puntos_alma, interfaz)
        # La carta de efecto extra se guarda como recurso
        self.area_recursos.append(carta_efecto_extra)

        return resultado

    def subir_nivel(self, interfaz):
        """
        Sube el nivel del jugador. Vacia el area de clock, colocando una carta aleatoria en el area de nivel y el resto
        en el area de espera.
        :param interfaz: Referencia a la interfaz grafica.
        :return: No tiene valor de retorno.
        """
        # Eleccion de la carta a mover de zona
        carta_seleccionada = random.choice(self.area_clock)
        self.area_clock.remove(carta_seleccionada)
        self.area_nivel.append(carta_seleccionada)
        # Vacia el area de clock
        self.area_espera += self.area_clock
        self.area_clock = []

        interfaz.mostrar_informacion("Jugador: " + self.nombre + " subio de nivel\n\nNivel actual:" + str(self.obtener_nivel()),
                           "Aumento de nivel")

    def resolver_ataque(self, puntos_alma, interfaz):
        """
        Aplica un daño igual a la cantidad de puntos de alma recibidos por parametro. Roba del mazo esa cantidad de
        cartas y las envia al area de clock, salvo que el daño sea cancelado por una carta de Climax. En ese caso, se
        dejan de robar cartas, y las ya tomadas se envian al area de espera.
        :param puntos_alma: Puntos de alma de la carta que esta haciendo el daño. Debe ser un entero mayor a 0.
        :param interfaz: Referencia a la interfaz grafica.
        :return: No tiene valor de retorno.
        """
        # Se envian al area de clock tantas cartas como puntos de daño se reciba
        cartas_a_descartar = []
        for c in xrange(puntos_alma):
            cartas_a_descartar.append(self.mazo.robar_carta())
            # Si la carta es una carta de climax, se cancela el daño y las cartas ya robadas van al area de espera
            if isinstance(cartas_a_descartar[-1], CartaClimax):
                interfaz.mostrar_informacion("Sacada carta: {0}\n Daño cancelado".format(str(cartas_a_descartar[-1])),
                                   "Daño cancelado")
                for carta in cartas_a_descartar:
                    self.area_espera.append(carta)
                return
        self.area_clock += cartas_a_descartar

        interfaz.mostrar_informacion("El jugador " + self.nombre + " recibio " + str(puntos_alma) + " puntos de daño",
                           "Daño recibido")

        # Si la cantidad de cartas en el area de clock es suficiente para subir de nivel, se sube
        if len(self.area_clock) >= CLOCK_PARA_NIVEL:
            self.subir_nivel(interfaz)

    def remover_carta(self, zona_campo, posicion_carta):
        """
        Remueve la carta del campo y la envia a la zona de espera.
        :param zona_campo: Zona en la que se encuentra la carta a remover. Debe ser una de las constantes CAMPO_FRONTAL
                           o RETAGUARDIA.
        :param posicion_carta: Posicion en la zona del campo de la carta. Debe ser una de las constantes
                               FRONTAL_IZQUIERDA,FRONTAL_CENTRO o FRONTAL_DERECHA si es del campo frontal, o
                               RETAGUARDIA_IZQUIERDA o RETAGUARDIA_DERECHA si es de la retaguardia.
        :return: La carta removida.
        """
        numero_de_carta = POSICIONES_CAMPO_FRONTAL.index(posicion_carta)
        if zona_campo == CAMPO_FRONTAL:
            carta_removida = self.campo_frontal[numero_de_carta]
            self.campo_frontal[numero_de_carta] = None
        elif zona_campo == RETAGUARDIA:
            carta_removida = self.retaguardia[numero_de_carta]
            self.retaguardia[numero_de_carta] = None
        self.area_espera.append(carta_removida)
        return carta_removida

    def robar_cartas(self, cantidad):
        """
        Roba del mazo la cantidad de cartas especificada. Si el mazo contiene menos cartas que las que se quieren
        robar, se toman todas las que haya y se recarga el mazo.
        :param cantidad: Cantidad de cartas a remover. Debe ser un entero mayor o igual a 0.
        :return: Lista con las cartas que se robaron del mazo.
        """
        cartas_robadas = []
        
        if self.mazo.esta_vacio():
            self.recargar_mazo()
        
        while (not self.mazo.esta_vacio()) and (cantidad > len(cartas_robadas)):
            cartas_robadas.append(self.mazo.robar_carta())
            if self.mazo.esta_vacio():
                self.recargar_mazo()

        return cartas_robadas

    def recargar_mazo(self):
        """
        Saca todas las cartas del area de espera y las coloca mezcladas en el mazo (tenga o no otras cartas).
        :return: No tiene valor de retorno.
        """
        self.mazo.agregar_cartas(self.area_espera)
        self.mazo.mezclar()
        self.area_espera = []

    def obtener_cantidad_clock(self):
        """
        Devuelve la cantidad de cartas en el area de clock.
        :return: Entero mayor o igual a 0, igual a la cantidad de cartas en el area de clock.
        """
        return len(self.area_clock)

    def obtener_nivel(self):
        """
        Devuelve el nivel del jugador, que es igual a la cantidad de cartas en el area de nivel.
        :return: Entero mayor o igual a 0, igual a la cantidad de cartas en el area de nivel.
        """
        return len(self.area_nivel)

    def aumentar_clock(self, carta):
        """
        Coloca la carta pasada por parametro en el area de clock, y roba del mazo una cantidad de cartas igual a la
        constante BENEFICIO_AUMENTAR_CLOCK.
        :param carta: Carta a poner en el area de clock.
        :return: Lista de las cartas robadas del mazo.
        """
        self.area_clock.append(carta)
        return self.robar_cartas(BENEFICIO_AUMENTAR_CLOCK)

    def obtener_colores_clock(self):
        """
        Devuelve una lista con todos los colores de cartas que hay en el area de clock.
        :return: Lista de strings.
        """
        colores = {}
        for carta in self.area_clock:
            colores[carta.obtener_color()] = 0
        return colores.keys()

    def obtener_colores_nivel(self):
        """
        Devuelve una lista con todos los colores de cartas que hay en el area de nivel.
        :return: Lista de strings.
        """
        colores = {}
        for carta in self.area_nivel:
            colores[carta.obtener_color()] = 0
        return colores.keys()

    def obtener_colores_recursos(self):
        """
        Devuelve una lista con todos los colores de cartas que hay en el area de recursos.
        :return: Lista de strings.
        """
        colores = {}
        for carta in self.area_recursos:
            colores[carta.obtener_color()] = 0
        return colores.keys()

    def puede_jugar_carta(self, carta):
        """
        Devuelve si la carta pasada por parametro pueda ser jugada o no.
        :param carta: Carta que se quiere jugar.
        :return: Booleano que indica si la carta pasada puede jugarse o no.
        """
        # Se chequea si hay lugar en el campo
        if None not in self.campo_frontal + self.retaguardia:
            return False
        # Se chequea si el nivel del jugador es mayor o igual que el de la carta
        if carta.obtener_nivel() > self.obtener_nivel():
            return False
        # Se chequea si la cantidad de cartas en el area de recursos alcanzan para pagar el costo de la carta
        if carta.obtener_costo() > len(self.area_recursos):
            return False
        # Se chequea si se pueden jugar cartas de ese color
        playable_colors = self.obtener_colores_clock()
        playable_colors += self.obtener_colores_nivel()
        if carta.obtener_color() not in playable_colors:
            if carta.obtener_nivel() != 0:
                return False

        return True

    def pagar_costo(self, costo_a_pagar):
        """
        Desapila del area de recursos una cantidad de cartas igual al costo pasado por parametro, y las mueve al area
        de espera.
        :param costo_a_pagar: Entero mayor o igual a 0, que indica el costo a pagar (cantidad de cartas a mover).
        :return: No tiene valor de retorno.
        """
        for c in xrange(costo_a_pagar):
            carta = self.area_recursos.pop()
            self.area_espera.append(carta)

    def jugar_personaje(self, carta, interfaz):
        """
        Coloca, si se puede, la carta de personaje pasada por parametro en el campo. Despliega menues para seleccionar
        en que zona del campo y posicion jugar la carta. Devuelve si la carta se pudo jugar o no.
        :param carta: Carta de personaje que se quiere jugar.
        :param interfaz: Referencia a la interfaz grafica.
        :return: Booleano que indica si la carta fue colocada en el campo o no.
        """
        if not self.puede_jugar_carta(carta):
            return False

        while True:
            seleccion_zona = interfaz.obtener_entero("Ingrese la zona del campo donde jugar la carta:\n\n"
                                                  "[1] Campo frontal\n[2] Retaguardia",
                                                  titulo="Seleccion de zona del campo", intervalo=[1, len(ZONAS)])
            if not seleccion_zona:
                return False
            zona_campo = None
            posicion = None

            if seleccion_zona == CAMPO_FRONTAL:
                posicion = interfaz.obtener_entero(
                    "Ingrese la posicion dentro de la zona del campo:\n\n"
                    "Posiciones: [1-" + str(len(POSICIONES_CAMPO_FRONTAL)) + "]",
                    titulo="Seleccion de posicion", intervalo=[1, len(POSICIONES_CAMPO_FRONTAL)])
                zona_campo = self.campo_frontal
            elif seleccion_zona == RETAGUARDIA:
                posicion = interfaz.obtener_entero(
                    "Ingrese la posicion dentro de la zona del campo:\n\n"
                    "Posiciones: [1-" + str(len(POSICIONES_RETAGUARDIA)) + "]",
                    titulo="Seleccion de posicion", intervalo=[1, len(POSICIONES_RETAGUARDIA)])
                zona_campo = self.retaguardia

            if not posicion:
                return False

            posicion -= 1
            if zona_campo[posicion]:
                interfaz.mostrar_informacion("No se puede jugar en esa posicion, esta ocupada", titulo="")
                if not interfaz.preguntar_si_no("Elegir otra posicion?", titulo=""):
                    return False
            else:
                zona_campo[posicion] = carta
                self.pagar_costo(carta.obtener_costo())
                return True

    def puede_jugar_carta_climax(self, carta):
        """
        Devuelve si la carta de climax pasada por parametro pueda ser jugada o no.
        :param carta: Carta de climax que se quiere jugar.
        :return: Booleano que indica si la carta de climax pasada puede jugarse o no.
        """
        # Si hay una carta en el area de climax no puede jugarse otra
        if self.area_climax:
            return False

        colores_jugables = self.obtener_colores_clock()
        colores_jugables += self.obtener_colores_nivel()
        if carta.obtener_color() not in colores_jugables:
            return False

        return True

    def jugar_evento(self, carta, interfaz):
        """
        Juega, si se puede, la carta de evento pasada por parametro. Devuelve si la carta se pudo jugar o no.
        :param carta: Carta de evento que se quiere jugar.
        :param interfaz: Referencia a la interfaz grafica.
        :return: Booleano que indica si la carta fue jugada o no.
        """
        if not self.puede_jugar_carta(carta):
            return False
        self.pagar_costo(carta.obtener_costo())
        self.area_espera.append(carta)
        return True

    def jugar_climax(self, carta, interfaz):
        """
        Coloca, si se puede, la carta de climax pasada por parametro en el campo. Devuelve si la carta se pudo jugar.
        :param carta: Carta de climax que se quiere jugar.
        :param interfaz: Referencia a la interfaz grafica.
        :return: Booleano que indica si la carta fue jugada o no.
        """
        if not self.puede_jugar_carta_climax(carta):
            return False
        self.area_climax = carta
        return True

    def remover_climax(self):
        """
        Remueve la carta del area de climax, si hay alguna, y la coloca en el area de espera.
        :return: No tiene valor de retorno.
        """
        if not self.area_climax:
            return
        self.area_espera.append(self.area_climax)
        self.area_climax = None

    def obtener_mazo(self):
        """
        Devuelve el mazo
        """
        return self.mazo

    def descartar_carta(self, carta):
        """
        Agrega una carta al tope de la zona de espera
        :param carta: Carta que se quiere descartar
        :return: No tiene valor de retorno
        """
        self.area_espera.append(carta)

    def remover_carta_clock(self):
        """
        Saca la ultima carta del area de clock
        :return: Carta la ultima carta del area de clock
        """
        return self.area_clock.pop()


    def obtener_cantidad_recursos(self):
        """
        Devuelve la cantidad de cartas en el area de recursos.
        :return: Entero mayor o igual a 0, igual a la cantidad de cartas en el area de recursos.
        """
        return len(self.area_recursos)

    def obtener_area_nivel(self):
        """
        Devuelve el area de nivel
        :return: Lista con las cartas del area de nivel
        """
        return self.area_nivel


class TableroJuego(object):
    """ Tablero de juego. Mantiene los campos de los dos jugadores, las habilidades aplicadas (tanto actuales como en
        turnos anteriores) y la referencia a la interfaz grafica. Ejecuta y resuelve las acciones efectuadas por los
        jugadores y las fases del juego (robar cartas, poner en el campo, combate, etc.)."""

    def __init__(self, interfaz=None, mazo_weiss=None, mazo_schwarz=None):
        """
        :param interfaz: Refencia a la interfaz grafica.
        :param mazo_*: Referencia a un mazo
        :return: No tiene valor de retorno.
        """
        # Blanco (Weiss)
        self.weiss = _CampoJugador(WEISS, mazo_weiss)
        # Negro (Schwarz)
        self.schwarz = _CampoJugador(SCHWARZ, mazo_schwarz)
        self.interfaz = interfaz
        self.habilidades=[]
    
    def obtener_oponente(self, jugador):
        """
        Devuelve el oponente del jugador pasado por parametro.
        :param jugador: Jugador del que se desea obtener el oponente. Debe ser una de las constantes WEISS o SCHWARZ.
        :return: Constante WEISS o SCHWARZ, dependiendo del jugador pasado por parametro.
        """
        if jugador == WEISS:
            return SCHWARZ
        return WEISS

    def obtener_campo_jugador(self, jugador):
        """
        Devuelve el campo de juego del jugador cuyo turno se esta jugando actualmente.
        :param jugador: Jugador actual. Debe ser una de las constantes WEISS o SCHWARZ.
        :return: _CampoJugador que corresponde al jugador actual.
        """
        if jugador == WEISS:
            return self.weiss
        return self.schwarz

    def remover_carta(self, jugador, zona_campo, posicion_carta):
        """
        Remueve la carta del campo del jugador y la envia a la zona de espera.
        :param jugador: Jugador al que se le removera la carta. Debe ser una de las constantes WEISS o SCHWARZ.
        :param zona_campo: Zona en la que se encuentra la carta a remover. Debe ser una de las constantes CAMPO_FRONTAL
                           o RETAGUARDIA.
        :param posicion_carta: Posicion en la zona del campo de la carta. Debe ser una de las constantes
                               FRONTAL_IZQUIERDA,FRONTAL_CENTRO o FRONTAL_DERECHA si es del campo frontal, o
                               RETAGUARDIA_IZQUIERDA o RETAGUARDIA_DERECHA si es de la retaguardia.
        :return: La carta removida.
        """
        campo_jugador = self.obtener_campo_jugador(jugador)
        carta_removida = campo_jugador.remover_carta(CAMPO_FRONTAL, posicion_carta)
        self.revertir_habilidades_sobre_carta(carta_removida)
        self.remover_habilidad(jugador, carta_removida.obtener_habilidad())

    def declarar_ataque(self, jugador, posicion_atacante):
        """
        Efectua y resuelve el ataque de la carta que se encuentra en la posicion pasada por parametro el campo del
        jugador pasado. Remueve las cartas que correspondan como resultado del ataque, y revierte las habilidades
        aplicadas sobre ellas (si las hay).
        :param jugador: Jugador atacante. Debe ser una de las constantes WEISS o SCHWARZ.
        :param posicion_atacante: Posicion en el campo frontal del jugador de la carta atacante. Debe ser una de las
                                  constantes FRONTAL_IZQUIERDA, FRONTAL_CENTRO o FRONTAL_DERECHA.
        :return: No tiene valor de retorno.
        """
        campo_atacante = None
        campo_defensor = None
        if jugador == WEISS:
            campo_atacante = self.weiss
            campo_defensor = self.schwarz
        elif jugador == SCHWARZ:
            campo_atacante = self.schwarz
            campo_defensor = self.weiss
        oponente = self.obtener_oponente(jugador)
        posicion_defensora = -1 * posicion_atacante
        resultado = campo_atacante.recibir_ataque(posicion_atacante, posicion_defensora, campo_defensor, self.interfaz)
        if (resultado[POSICION_DESTRUIR_ATACANTE] == True):
            self.remover_carta(jugador, CAMPO_FRONTAL, posicion_atacante)
        if (resultado[POSICION_DESTRUIR_DEFENSOR] == True):
            self.remover_carta(oponente, CAMPO_FRONTAL, posicion_defensora)

    def jugar_carta(self, jugador, carta):
        """
        Juega, si se puede, la carta pasada por parametro. Devuelve si la carta pudo jugarse o no.
        :param jugador: Jugador que juega la carta. Debe ser una de las constantes WEISS o SCHWARZ.
        :param carta: Carta que se quiere jugar.
        :return: Booleano que indica si se pudo jugar la carta o no.
        """
        if isinstance(carta, CartaPersonaje):
            if self.jugar_personaje(jugador, carta):
                self.aplicar_habilidad_sobre_tablero(jugador, carta.obtener_habilidad(), EFECTO_CONTINUO)
                return True
            return False
        elif isinstance(carta, CartaEvento):
            if self.jugar_evento(jugador, carta):
                self.aplicar_habilidad_sobre_tablero(jugador, carta.obtener_habilidad(), EFECTO_TEMPORAL)
                return True
            return False
        elif isinstance(carta, CartaClimax):
            if self.jugar_climax(jugador, carta):
                self.aplicar_habilidad_sobre_tablero(jugador, carta.obtener_habilidad(), EFECTO_TEMPORAL)
                return True
            return False
        else:
            return False

    def jugar_personaje(self, jugador, carta):
        """
        Coloca, si se puede, la carta de personaje pasada por parametro en el campo del jugador pasado. Devuelve si la
        carta de personaje se pudo jugar o no.
        :param jugador: Jugador que juega la carta. Debe ser una de las constantes WEISS o SCHWARZ.
        :param carta: Carta de personaje que se quiere jugar.
        :return: Booleano que indica si la carta fue colocada en el campo o no.
        """
        if not self.obtener_campo_jugador(jugador).jugar_personaje(carta, self.interfaz):
            return False
        self.aplicar_habilidades_en_carta(carta)
        return True

    def jugar_evento(self, jugador, carta):
        """
        Juega, si se puede, la carta de evento pasada por parametro. Devuelve si la carta se pudo jugar o no.
        :param jugador: Jugador que juega la carta. Debe ser una de las constantes WEISS o SCHWARZ.
        :param carta: Carta de evento que se quiere jugar.
        :return: Booleano que indica si la carta fue jugada o no.
        """
        return self.obtener_campo_jugador(jugador).jugar_evento(carta, self.interfaz)

    def jugar_climax(self, jugador, carta):
        """
        Coloca, si se puede, la carta de climax pasada por parametro en el campo del jugador pasado. Devuelve si la
        carta se pudo jugar.
        :param jugador: Jugador que juega la carta. Debe ser una de las constantes WEISS o SCHWARZ.
        :param carta: Carta de climax que se quiere jugar.
        :return: Booleano que indica si la carta fue jugada o no.
        """
        return self.obtener_campo_jugador(jugador).jugar_climax(carta, self.interfaz)

    def robar_cartas(self, jugador, cantidad=1):
        """
        Roba del mazo del jugador pasado por parametro la cantidad de cartas especificada. Si el mazo contiene menos
        cartas que las que se quieren robar, se toman todas las que haya y se recarga el mazo.
        :param jugador: Jugador que roba las cartas. Debe ser una de las constantes WEISS o SCHWARZ.
        :param cantidad: Cantidad de cartas a remover. Debe ser un entero mayor o igual a 0.
        :return: Lista con las cartas que se robaron del mazo.
        """
        return self.obtener_campo_jugador(jugador).robar_cartas(cantidad)

    def obtener_nivel_jugador(self, jugador):
        """
        Devuelve el nivel del jugador pasado por parametro.
        :param jugador: Debe ser una de las constantes WEISS o SCHWARZ.
        :return: Entero mayor o igual a 0 que indica el nivel del jugador.
        """
        return self.obtener_campo_jugador(jugador).obtener_nivel()

    def obtener_cantidad_clock(self, jugador):
        """
        Devuelve la cantidad de cartas en el area de clock del jugador pasado por parametro.
        :param jugador: Debe ser una de las constantes WEISS o SCHWARZ.
        :return: Entero mayor o igual a 0 que indica la cantidad de cartas en el area de clock del jugador.
        """
        return self.obtener_campo_jugador(jugador).obtener_cantidad_clock()

    def aumentar_clock(self, jugador, carta):
        """
        Coloca la carta pasada por parametro en el area de clock del jugador, y roba del mazo del mismo una cantidad de
        cartas igual a la constante BENEFICIO_AUMENTAR_CLOCK.
        :param jugador: Debe ser una de las constantes WEISS o SCHWARZ.
        :param carta: Carta a poner en el area de clock.
        :return: Lista de las cartas robadas del mazo.
        """
        return self.obtener_campo_jugador(jugador).aumentar_clock(carta)

    def puede_jugar_carta(self, jugador, carta):
        """
        Verifica si el jugador pasado por parametro puede jugar la carta pasada. Devuelve True si puede hacerlo, False
        en caso contrario.
        :param jugador: Jugador que quiere jugar la carta. Debe ser una de las constantes WEISS o SCHWARZ.
        :param carta: Carta que se quiere verificar si puede ser jugada.
        :return: Booleano que indica si se puede o no jugar la carta.
        """
        if isinstance(carta, CartaClimax):
            return self.obtener_campo_jugador(jugador).puede_jugar_carta_climax(carta)
        else:
            return self.obtener_campo_jugador(jugador).puede_jugar_carta(carta)

    def obtener_ganador(self):
        """
        Devuelve el jugador ganador si hay uno (constantes WEISS o SCHWARZ), o SIN_GANADOR si no hay uno.
        :return: Constante WEISS, SCHWARZ o SIN_SIN_GANADOR.
        """
        if self.weiss.obtener_nivel() == NIVEL_MAX:
            return SCHWARZ
        if self.schwarz.obtener_nivel() == NIVEL_MAX:
            return WEISS
        return SIN_GANADOR

    def obtener_cartas_campo_frontal(self, jugador):
        """
        Obtiene las cartas del campo frontal del jugador pasado por parametro y la devuelve.
        :param jugador: Jugador del que se quiere obtener el campo frontal. Debe ser una de las constantes WEISS o
                        SCHWARZ.
        :return: Lista de cartas.
        """
        return self.obtener_campo_jugador(jugador).campo_frontal[:]

    def obtener_cartas_nivel(self, jugador):
        """
        Obtiene las cartas del area de nivel del jugador pasado por parametro y la devuelve.
        :param jugador: Jugador del que se quiere obtener el campo frontal. Debe ser una de las constantes WEISS o
                        SCHWARZ.
        :return: Lista de cartas.
        """
        return self.obtener_campo_jugador(jugador).area_nivel[:]

    def obtener_cartas_recursos(self, jugador):
        """
        Obtiene las cartas del area de recursos del jugador pasado por parametro y la devuelve.
        :param jugador: Jugador del que se quiere obtener el campo frontal. Debe ser una de las constantes WEISS o
                        SCHWARZ.
        :return: Lista de cartas.
        """
        return self.obtener_campo_jugador(jugador).area_recursos[:]

    def obtener_cartas_clock(self, jugador):
        """
        Obtiene las cartas del area de clock del jugador pasado por parametro y la devuelve.
        :param jugador: Jugador del que se quiere obtener el campo frontal. Debe ser una de las constantes WEISS o
                        SCHWARZ.
        :return: Lista de cartas.
        """
        return self.obtener_campo_jugador(jugador).area_clock[:]

    def obtener_cartas_retaguardia(self, jugador):
        """
        Obtiene las cartas de la retaguardia del jugador pasado por parametro y la devuelve.
        :param jugador: Jugador del que se quiere obtener el campo frontal. Debe ser una de las constantes WEISS o
                        SCHWARZ.
        :return: Lista de cartas.
        """
        return self.obtener_campo_jugador(jugador).retaguardia[:]

    def obtener_todas_campo_frontal(self):
        """
        Devuelve una lista con todas las cartas que se encuentran en los campos frontales de ambos jugadores.
        :return: Lista de cartas. Las primeras tres cartas son las del jugador Weiss y las ultimas tres de Schwarz.
        """
        cartas = []
        cartas += self.weiss.campo_frontal
        cartas += self.schwarz.campo_frontal
        return cartas

    def obtener_tope_espera(self, jugador):
        """
        Devuelve la carta que se encuentra en el tope del area de espera, o None si no hay ninguna.
        :param jugador: Jugador del que se quiere obtener el tope del area de espera. Debe ser una de las constantes
                        WEISS o SCHWARZ.
        :return: Carta del tope del area de espera, o None si el area esta vacia.
        """
        if self.obtener_campo_jugador(jugador).area_espera == []:
            return None
        return self.obtener_campo_jugador(jugador).area_espera[-1]

    def obtener_climax(self, jugador):
        """
        Devuelve la carta del area de climax del jugador pasado por parametro, si hay una.
        :param jugador: Jugador del que se quiere obtener la carta del area de climax. Debe ser una de las constantes
                        WEISS o SCHWARZ.
        :return: Carta del area de climax, o None si el area esta vacia.
        """
        return self.obtener_campo_jugador(jugador).area_climax

    def iniciar_turno(self):
        """
        Inicia el turno aplicando las habilidades que quedaron en el campo durante el turno anterior
        en el mismo orden que fueron aplicado en este.
        :return: No tiene valor de retorno.
        """
        for habilidad,jugador,continuidad in self.habilidades:
            habilidad.aplicar_en_tablero(self,jugador)

    def terminar_turno(self):
        """
        Termina el turno. Revierte todos los efectos de las cartas aplicadas en el campo
        en el orden inverso en que fueron aplicadas. Las habilidades EFECTO_CONTINUO deben guardarse
        para ser aplicadas en el proximo turno (en el mismo orden en el que se aplicaron en este turno).
        :return: No tiene tipo de retorno.
        """
        index_iter = xrange(len(self.habilidades))
        for index in reversed(index_iter):
            #itero en reversa para darle efecto de pila
            habilidad_activa,jugador,continuidad = self.habilidades[index]
            habilidad_activa.revertir_en_tablero(self,jugador)
            if continuidad == EFECTO_TEMPORAL:
                #Si la habilidad es temporal, la remuevo de la lista.
                self.habilidades.remove(self.habilidades[index])

    def aplicar_habilidades_en_carta(self, card):
        """
        Aplica las habilidades activas en el campo a la carta pasada como parametro. Se deben
        aplicar en el orden que se aplicaron originalmente.
        :param carta: Carta sobre la que aplicar las habilidades.
        :return: No tiene valor de retorno.
        """
        for habilidad in self.habilidades:
            habilidad.aplicar_en_carta(card)

    def aplicar_habilidad_sobre_tablero(self, jugador, habilidad, continuidad):
        """
        Aplica la habilidad pasada por parametro al campo del jugador pasado.
        :param jugador: Jugador en el que se aplica la habilidad.
        :param habilidad: Referencia a la habilidad a aplicar. Debe ser un objeto de una clase que herede de Habilidad.
        :param continuidad: Indica si es una habilidad continua o que solo tiene efecto por un turno. Debe ser una de
                            las constantes EFECTO_CONTINUO o EFECTO_TEMPORAL.
        :return: No tiene valor de retorno.
        """
        if habilidad != None:
            self.habilidades.append(habilidad,jugador,continuidad, interfaz)
            habilidad.aplicar_en_tablero(self,jugador)

    def revertir_habilidades_sobre_carta(self, carta):
        """
        Revierte los efectos sobre la carta pasada como paramtero en el orden inverso en que fueron aplicados.
        :param carta:Carta a la que se le deben revertir las habilidades
        :return: No tiene valor de retorno.
        """
        for habilidad,jugador,continuidad in reversed(self.habilidades):
            habilidad.revertir_en_carta(card)

    def remover_habilidad(self, jugador, habilidad):
        """
        Remueve la habilidad pasada por parametro, aplicada por el jugador pasado, de la pila de habilidades aplicadas.
        :param jugador: Jugador que aplico la habilidad originalmente. Debe ser una de las constantes WEISS o SCHWARZ.
        :param habilidad: Habilidad a deshacer. Debe ser un objeto de una clase que herede de Habilidad.
        :return: No tiene valor de retorno.
        """
        #Creo el iterador de indices de acuerdo al largo de la lista
        index_iter = xrange(len(self.habilidades))
        for index in reversed(index_iter):
            #itero en reversa para darle efecto de pila
            habilidad_activa,jugador,continuidad = self.habilidades[index]
            habilidad_activa.revertir_en_tablero(self,jugador)
            if habilidad == habilidad_activa:
                #si encuentro la habilidad pasada por param, luego de revertirla, la saco de la lista.
                self.habilidades.remove(self.habilidades[index])
        #Aplico todas las habilidades nuevamente.
        for habilidad_activa,jugador,continuidad in self.habilidades:
            habilidad_activa.aplicar_en_tablero(self,jugador)
