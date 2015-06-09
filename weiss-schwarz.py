import random
from mazo import Mazo
from tablero import TableroJuego, WEISS, SCHWARZ, POSICIONES_CAMPO_FRONTAL
from interfaz import Interfaz_Ventana

MAZO_SCHWARZ = "schwarz.csv"
MAZO_WEISS = "weiss.csv"

CANTIDAD_CARTAS_INICIALES = 5

TURNO = [SCHWARZ, WEISS]


def fase_clock(tablero, interfaz, jugador, mano_jugador):
    """
    Resuelve una fase de clock, interactuando con el usuario y descartando y robando cartas segun corresponda
    :param tablero: Tablero de juego. Es un objeto de clase TableroJuego ya inicializado.
    :param interfaz: Referencia a la interfaz grafica.
    :param jugador: Jugador actual, a cuyo turno corresponde la fase de clock que se esta resolviendo. Debe ser una de
                    las constantes SCHWARZ o WEISS de tablero.py.
    :param mano_jugador: Lista de cartas que corresponde a la mano del jugador actual.
    :return: No tiene valor de retorno.
    """
    if not interfaz.preguntar_si_no("Desea aumentar el clock descartando una carta?", "Fase de clock"):
        return
    string_mano_jugador = "Mano del jugador:\n\n"
    for i in range(len(mano_jugador)):
        string_mano_jugador += "[" + str(i + 1) + "]" + str(mano_jugador[i]) + "\n"

    carta_a_descartar = None
    while not carta_a_descartar:
        i = interfaz.obtener_entero(string_mano_jugador, "Elija una carta para descartar", [1, len(mano_jugador)])
        if (not i):
            return
        interfaz.mostrar_carta(mano_jugador[i - 1])
        if not interfaz.preguntar_si_no("Descartar " + str(mano_jugador[i - 1]) + "?", "Aumentar clock"):
            continue
        carta_a_descartar = mano_jugador[i - 1]
        mano_jugador.remove(carta_a_descartar)

    cartas_robadas = tablero.aumentar_clock(jugador, carta_a_descartar)
    for i in range(len(cartas_robadas)):
        interfaz.mostrar_carta(cartas_robadas[i], "Carta robada numero " + str(i + 1))
        mano_jugador.append(cartas_robadas[i])

    interfaz.actualizar_tablero(tablero)


def fase_principal(tablero, interfaz, fase, jugador, mano_jugador):
    """
    Resuelve una fase principal.
    :param tablero: Tablero de juego. Es un objeto de clase TableroJuego ya inicializado.
    :param interfaz: Referencia a la interfaz grafica.
    :param fase: String que contiene que fase principal es la que se esta resolviendo.
    :param jugador: Jugador actual, a cuyo turno corresponde la fase principal que se esta resolviendo. Debe ser una de
                    las constantes tablero.SCHWARZ o tablero.WEISS.
    :param mano_jugador: Lista de cartas que corresponde a la mano del jugador actual.
    :return: No tiene valor de retorno.
    """
    string_mano_jugador = "Mano del jugador:\n\n"
    for i in range(len(mano_jugador)):
        string_mano_jugador += str(mano_jugador[i]) + "\n"
    while interfaz.preguntar_si_no(string_mano_jugador + "\nDesea jugar una carta?", fase):
        string_mano_jugador = "Mano del jugador:\n\n"
        for i in range(len(mano_jugador)):
            string_mano_jugador += "[" + str(i + 1) + "]" + str(mano_jugador[i]) + "\n"

        carta_a_jugar = None
        while not carta_a_jugar:
            i = interfaz.obtener_entero(string_mano_jugador, "Elija una carta a jugar", [1, len(mano_jugador)])
            if (not i):
                break
            if not tablero.puede_jugar_carta(jugador, mano_jugador[i - 1]):
                interfaz.mostrar_informacion("No se puede jugar: " + str(mano_jugador[i - 1]))
                continue
            interfaz.mostrar_carta(mano_jugador[i - 1], "Carta a jugar")
            if not interfaz.preguntar_si_no("Jugar " + str(mano_jugador[i - 1]) + "?", "Carta a jugar"):
                continue
            carta_a_jugar = mano_jugador[i - 1]
            if tablero.jugar_carta(jugador, carta_a_jugar):
                mano_jugador.remove(carta_a_jugar)
                interfaz.actualizar_tablero(tablero)

        string_mano_jugador = "Mano del jugador:\n\n"
        for i in range(len(mano_jugador)):
            string_mano_jugador += str(mano_jugador[i]) + "\n"


def mostrar_mano(interfaz, jugador, mano_jugador):
    """
    Muestra, a traves de la interfaz, la mano del jugador.
    :param interfaz: Referencia a la interfaz grafica.
    :param jugador: Jugador al que le pertenece la mano a mostrar. Debe ser una de las constantes tablero.SCHWARZ o tablero.WEISS.
    :param mano_jugador: Lista de cartas que corresponde a la mano del jugador actual.
    :return: No tiene valor de retorno.
    """
    string_mano_jugador = "Mano del jugador:\n\n"
    for i in range(len(mano_jugador)):
        string_mano_jugador += str(mano_jugador[i]) + "\n"
    interfaz.mostrar_informacion(string_mano_jugador, "Mano del jugador " + jugador)


def fase_combate(tablero, interfaz, jugador):
    """
    Resuelve una fase de combate.
    :param tablero: Tablero de juego. Es un objeto de clase TableroJuego ya inicializado.
    :param interfaz: Referencia a la interfaz grafica.
    :param jugador: Jugador actual, a cuyo turno corresponde la fase de combate que se esta resolviendo. Debe ser una de
                    las constantes tablero.SCHWARZ o tablero.WEISS.
    :return: No tiene valor de retorno.
    """
    campo_frontal = tablero.obtener_cartas_campo_frontal(jugador)
    while interfaz.preguntar_si_no("Desea atacar con alguna carta?", "Fase de ataque"):
        posicion = interfaz.obtener_entero("Elija carta con la que atacar:", "Seleccion de atacante",
                                        [1, len(POSICIONES_CAMPO_FRONTAL)])
        if not posicion:
            continue
        if not campo_frontal[posicion - 1]:
            interfaz.mostrar_informacion("No es una carta valida para atacar", "No se puede atacar")
            continue
        interfaz.mostrar_carta(campo_frontal[posicion - 1], "Carta atacante")
        campo_frontal[posicion - 1] = None
        tablero.declarar_ataque(jugador, POSICIONES_CAMPO_FRONTAL[posicion - 1])
        interfaz.actualizar_tablero(tablero)


def main():
    interfaz = Interfaz_Ventana()
    # Manos de los jugadores
    manos = [[], []]
    # Create decks
    mazo_weiss = Mazo(MAZO_WEISS)
    mazo_schwarz = Mazo(MAZO_SCHWARZ)
    # Decidir quien empieza
    indice_jugador = random.choice([0, 1])
    # Inicializacion del tablero
    tablero = TableroJuego(interfaz, mazo_weiss, mazo_schwarz)
    # Generacion de las manos de los jugadores
    manos[indice_jugador] = tablero.robar_cartas(TURNO[indice_jugador], CANTIDAD_CARTAS_INICIALES - 1)
    manos[(indice_jugador + 1) % 2] = tablero.robar_cartas(TURNO[(indice_jugador + 1) % 2], CANTIDAD_CARTAS_INICIALES)

    interfaz.actualizar_tablero(tablero)

    # Game loop
    while not tablero.obtener_ganador():
        jugador = TURNO[indice_jugador % 2]
        mano_jugador = manos[indice_jugador % 2]
        # Comienzo del turno
        interfaz.mostrar_informacion("Comienza el turno del jugador " + str(jugador), "Turno jugador")
        tablero.iniciar_turno()
        interfaz.actualizar_tablero(tablero)
        # Fase de robar (el primer turno se saltea esta fase)
        drew_card = tablero.robar_cartas(jugador)[0]
        mano_jugador.append(drew_card)
        interfaz.mostrar_informacion("Carta robada:\n" + str(drew_card), "Fase de robar")
        mostrar_mano(interfaz, jugador, mano_jugador)
        # Fase de clock
        fase_clock(tablero, interfaz, jugador, mano_jugador)
        interfaz.actualizar_tablero(tablero)
        mostrar_mano(interfaz, jugador, mano_jugador)
        # Primer fase principal
        fase_principal(tablero, interfaz, "Primer fase principal", jugador, mano_jugador)
        interfaz.actualizar_tablero(tablero)
        # Fase de combate
        fase_combate(tablero, interfaz, jugador)
        interfaz.actualizar_tablero(tablero)
        mostrar_mano(interfaz, jugador, mano_jugador)
        # Segunda fase principal
        fase_principal(tablero, interfaz, "Segunda fase principal", jugador, mano_jugador)
        interfaz.actualizar_tablero(tablero)
        # Fin del turno
        indice_jugador += 1
        interfaz.mostrar_informacion("Finaliza el turno del jugador " + str(jugador), "Fin turno jugador")
        tablero.terminar_turno()
    # Final del juego
    interfaz.mostrar_informacion("Gano el jugador " + tablero.obtener_ganador(), "Fin del juego")


main()
