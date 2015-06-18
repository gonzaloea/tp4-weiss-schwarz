import random

from tablero import TableroJuego
import tablero
import creador_cartas
from mazo import Mazo
MAZO_SCHWARZ = "schwarz.csv"
MAZO_WEISS = "weiss.csv"

def clocking(gameboard, player_hand , side):
    print "Choose a card to play:"
    for i in range(len(player_hand)):
        creador_cartas.mostrar_carta(player_hand[i],"Hand: "+player_hand[i].obtener_nombre())

    print player_hand

    card_to_play = int(raw_input("Card number:"))-1
    card = player_hand.pop(card_to_play)

    print "DEBUG: Before clocking"
    print "DEBUG: Clock level:", gameboard.obtener_cantidad_clock(side)

    print "DEBUG: During clocking"
    creador_cartas.mostrar_carta(card,"Card to clock",4)
    print "DEBUG: Card to clock:", card

    cards = gameboard.aumentar_clock(side, card)

    print "Drew cartas: ",cards
    for card in cards:
        creador_cartas.mostrar_carta(card,"Drew cartas")

    print "DEBUG: After clocking"
    print "DEBUG: Clock level:", gameboard.obtener_cantidad_clock(side)

    return cards

def play_character(gameboard, player_hand, side):
    print "Choose a card to play:"
    for i in range(len(player_hand)):
        creador_cartas.mostrar_carta(player_hand[i],"Hand: "+player_hand[i].obtener_nombre())

    print player_hand

    card_to_play = int(raw_input("Card number:"))-1
    card = player_hand.pop(card_to_play)

    if gameboard.puede_jugar_carta(side, card):
        creador_cartas.mostrar_carta(card,"Can play:",4)
        gameboard.jugar_personaje(side, card, tablero.CAMPO_FRONTAL, tablero.FRONTAL_IZQUIERDA)
        return []
    else:
        creador_cartas.mostrar_carta(card,"Can't play:",4)
        return [card]


def simulate_game():
    """  """
    # Board creation
    gameboard = TableroJuego(None, Mazo(MAZO_WEISS), Mazo(MAZO_SCHWARZ))

    # Init
    player1_hand = gameboard.robar_cartas(tablero.WEISS, 5)
    player2_hand = gameboard.robar_cartas(tablero.SCHWARZ, 5)

    print "Opening hand"
    print player1_hand
    print player2_hand

    # first turn
    print "Weiss first turn"
    print "Weiss clocking"
    player1_hand += clocking(gameboard, player1_hand, tablero.WEISS)

    print "Weiss play"
    player1_hand += play_character(gameboard, player1_hand, tablero.WEISS)

    print "Before attack"
    print "Schwarz clock level:", gameboard.obtener_cantidad_clock(tablero.SCHWARZ)

    triggered_card = gameboard.atack(tablero.WEISS, tablero.FRONTAL_IZQUIERDA, tablero.FRONTAL_DERECHA)
    creador_cartas.mostrar_carta(triggered_card,"Triggered")

    print "After attack"
    print "Schwarz clock level:", gameboard.obtener_cantidad_clock(tablero.SCHWARZ)


simulate_game()
