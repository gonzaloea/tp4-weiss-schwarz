from time import sleep
from carta import CartaPersonaje, CartaClimax, CartaEvento
import pygame

pygame.init()
ANCHO_CARTA = 448
ALTO_CARTA = 626

ANCHO_CLIMAX = 626
ALTO_CLIMAX = 448


def generar_imagen_personaje(carta):
    """
    Genera la imagen para una carta de personaje y la devuelve.
    :param carta: Carta para la que se desea generar la imagen.
    :return: Surface de pygame, que es la imagen generada para la carta.
    """
    resultado = pygame.Surface((ANCHO_CARTA, ALTO_CARTA))
    resultado.fill((255, 255, 255))

    archivo_imagen = carta.obtener_nombre().replace(' ', '_') + ".png"

    archivo_layout = carta.obtener_color()[0] + str(carta.obtener_puntos_alma()) + "s.png"

    if carta.obtener_nivel() != 0:
        archivo_nivel = carta.obtener_color()[0] + "l" + str(carta.obtener_nivel()) + ".png"
    else:
        archivo_nivel = "l0.png"

    archivo_costo = "c" + str(carta.obtener_costo()) + ".png"
    imagen = pygame.image.load("resources/card_images/" + archivo_imagen)
    i_w, i_h = imagen.get_size()
    if i_w > i_h:
        i_w = ALTO_CARTA * i_w / i_h
        i_h = ALTO_CARTA
        if i_w < ANCHO_CARTA:
            i_h = ANCHO_CARTA * i_h / i_w
            i_w = ANCHO_CARTA

    else:
        i_h = ANCHO_CARTA * i_h / i_w
        i_w = ANCHO_CARTA
        if i_h < ALTO_CARTA:
            i_w = ALTO_CARTA * i_w / i_h
            i_h = ALTO_CARTA

    imagen = pygame.transform.scale(imagen, (i_w, i_h))
    ajuste_horizontal = (ANCHO_CARTA - i_w) / 2
    ajuste_vertical = (ALTO_CARTA - i_h) / 2

    resultado.blit(imagen, (ajuste_horizontal, ajuste_vertical))

    imagen = pygame.image.load("resources/card_layouts/character/" + archivo_layout)
    resultado.blit(imagen, (0, 0))

    imagen = pygame.image.load("resources/card_layouts/level/" + archivo_nivel)
    resultado.blit(imagen, (0, 0))

    imagen = pygame.image.load("resources/card_layouts/cost/" + archivo_costo)
    resultado.blit(imagen, (0, 60))

    efecto_extra = carta.obetener_puntos_efecto_extra()
    if efecto_extra == 0:
        imagen = pygame.image.load("resources/card_layouts/triggers/none.png")
        resultado.blit(imagen, (ANCHO_CARTA - imagen.get_size()[0], 0))
    else:
        imagen = pygame.image.load("resources/card_layouts/triggers/soul.png")
        resultado.blit(imagen, (ANCHO_CARTA - imagen.get_size()[0], 0))

        if efecto_extra == 2:
            resultado.blit(imagen, (ANCHO_CARTA - imagen.get_size()[0] * 2, 0))

    fuente = pygame.font.Font("resources/agfarotissemiserif.ttf", 27)

    label = fuente.render(str(carta.obtener_nombre()), 1, (255, 255, 255))
    centro_horizontal = 115 + ((435 - 155) - label.get_size()[0]) / 2
    resultado.blit(label, (centro_horizontal, 554))  # Min 155 - Max 350 || #Min 555 - Max 575

    label = fuente.render(str(carta.obtener_poder()), 1, (255, 255, 255))
    centro_horizontal = 32 + ((116 - 32) - label.get_size()[0]) / 2
    resultado.blit(label, (centro_horizontal, 567))  # Min 32 - Max 116

    fuente = pygame.font.Font("resources/agfarotissemiserif.ttf", 11)
    subtipo_x = 212
    for trait in carta.obtener_subtipos():
        label = fuente.render(trait, 1, (0, 0, 0))
        centro_horizontal = subtipo_x + (90 - label.get_size()[0]) / 2
        resultado.blit(label, (centro_horizontal, 587))
        subtipo_x += 100

    fuente = pygame.font.Font("resources/agfarotissemiserif.ttf", 16)

    lineas = []
    for linea in carta.obtener_texto_decorativo().split('\n'):
        lineas.append(fuente.render(linea, 1, (0, 0, 0)))

    alto_linea = lineas[0].get_size()[1]

    caja_de_texto = pygame.Surface((ANCHO_CARTA - ANCHO_CARTA / 8, alto_linea * len(lineas)), pygame.SRCALPHA)
    caja_de_texto.fill((255, 255, 255, 150))
    posicion = 550
    resultado.blit(caja_de_texto, (ANCHO_CARTA / 16, posicion - caja_de_texto.get_size()[1]))

    for label in lineas[::-1]:
        posicion -= alto_linea
        resultado.blit(label, (ANCHO_CARTA / 16, posicion))

    if (carta.obtener_habilidad()):
        lineas = []
        for linea in carta.obtener_habilidad().obtener_texto().split('\n'):
            lineas.append(fuente.render(linea, 1, (0, 0, 0)))

        alto_linea = lineas[0].get_size()[1]

        caja_de_texto = pygame.Surface((ANCHO_CARTA - ANCHO_CARTA / 8, alto_linea * len(lineas)), pygame.SRCALPHA)
        caja_de_texto.fill((255, 255, 255, 150))
        posicion -= 5
        resultado.blit(caja_de_texto, (ANCHO_CARTA / 16, posicion - caja_de_texto.get_size()[1]))

        for label in lineas[::-1]:
            posicion -= alto_linea
            resultado.blit(label, (ANCHO_CARTA / 16, posicion))

    return resultado


def generar_imagen_evento(carta):
    """
    Genera la imagen para una carta de evento y la devuelve.
    :param carta: Carta para la que se desea generar la imagen.
    :return: Surface de pygame, que es la imagen generada para la carta.
    """
    resultado = pygame.Surface((ANCHO_CARTA, ALTO_CARTA))
    resultado.fill((255, 255, 255))

    archivo_imagen = carta.obtener_nombre().replace(' ', '_') + ".png"

    archivo_layout = carta.obtener_color() + ".png"

    if carta.obtener_nivel() != 0:
        archivo_nivel = carta.obtener_color()[0] + "l" + str(carta.obtener_nivel()) + ".png"
    else:
        archivo_nivel = "l0.png"

    archivo_costo = "c" + str(carta.obtener_costo()) + ".png"
    imagen = pygame.image.load("resources/card_images/" + archivo_imagen)
    i_w, i_h = imagen.get_size()
    if i_w > i_h:
        i_w = ALTO_CARTA * i_w / i_h
        i_h = ALTO_CARTA
        if i_w < ANCHO_CARTA:
            i_h = ANCHO_CARTA * i_h / i_w
            i_w = ANCHO_CARTA

    else:
        i_h = ANCHO_CARTA * i_h / i_w
        i_w = ANCHO_CARTA
        if i_h < ALTO_CARTA:
            i_w = ALTO_CARTA * i_w / i_h
            i_h = ALTO_CARTA

    imagen = pygame.transform.scale(imagen, (i_w, i_h))
    ajuste_horizontal = (ANCHO_CARTA - i_w) / 2
    ajuste_vertical = (ALTO_CARTA - i_h) / 2

    resultado.blit(imagen, (ajuste_horizontal, ajuste_vertical))

    imagen = pygame.image.load("resources/card_layouts/event/" + archivo_layout)
    resultado.blit(imagen, (0, 0))

    imagen = pygame.image.load("resources/card_layouts/level/" + archivo_nivel)
    resultado.blit(imagen, (0, 0))

    imagen = pygame.image.load("resources/card_layouts/cost/" + archivo_costo)
    resultado.blit(imagen, (0, 60))

    efecto_extra = carta.obetener_puntos_efecto_extra()
    if efecto_extra == 0:
        imagen = pygame.image.load("resources/card_layouts/triggers/none.png")
        resultado.blit(imagen, (ANCHO_CARTA - imagen.get_size()[0], 0))
    else:
        imagen = pygame.image.load("resources/card_layouts/triggers/soul.png")
        resultado.blit(imagen, (ANCHO_CARTA - imagen.get_size()[0], 0))

        if efecto_extra == 2:
            resultado.blit(imagen, (ANCHO_CARTA - imagen.get_size()[0] * 2, 0))

    fuente = pygame.font.Font("resources/agfarotissemiserif.ttf", 25)

    label = fuente.render(str(carta.obtener_nombre()), 1, (255, 255, 255))
    center_horizontal = 115 + ((435 - 155) - label.get_size()[0]) / 2
    resultado.blit(label, (center_horizontal, 570))  # Min 155 - Max 350 || #Min 555 - Max 575

    fuente = pygame.font.Font("resources/agfarotissemiserif.ttf", 16)

    lineas = []
    for line in carta.obtener_texto_decorativo().split('\n'):
        lineas.append(fuente.render(line, 1, (0, 0, 0)))

    alto_linea = lineas[0].get_size()[1]

    caja_de_texto = pygame.Surface((ANCHO_CARTA - ANCHO_CARTA / 8, alto_linea * len(lineas)), pygame.SRCALPHA)
    caja_de_texto.fill((255, 255, 255, 150))
    posicion = 565
    resultado.blit(caja_de_texto, (ANCHO_CARTA / 16, posicion - caja_de_texto.get_size()[1]))

    for label in lineas[::-1]:
        posicion -= alto_linea
        resultado.blit(label, (ANCHO_CARTA / 16, posicion))

    if (carta.obtener_habilidad()):
        lineas = []
        for line in carta.obtener_habilidad().obtener_texto().split('\n'):
            lineas.append(fuente.render(line, 1, (0, 0, 0)))

        alto_linea = lineas[0].get_size()[1]

        caja_de_texto = pygame.Surface((ANCHO_CARTA - ANCHO_CARTA / 8, alto_linea * len(lineas)), pygame.SRCALPHA)
        caja_de_texto.fill((255, 255, 255, 150))
        posicion -= 5
        resultado.blit(caja_de_texto, (ANCHO_CARTA / 16, posicion - caja_de_texto.get_size()[1]))

        for label in lineas[::-1]:
            posicion -= alto_linea
            resultado.blit(label, (ANCHO_CARTA / 16, posicion))

    return resultado


def generar_imagen_climax(carta):
    """
    Genera la imagen para una carta de climax y la devuelve.
    :param carta: Carta para la que se desea generar la imagen.
    :return: Surface de pygame, que es la imagen generada para la carta.
    """
    resultado = pygame.Surface((ANCHO_CLIMAX, ALTO_CLIMAX))
    resultado.fill((255, 255, 255))

    archivo_imagen = carta.obtener_nombre().replace(' ', '_') + ".png"

    archivo_layout = carta.obtener_color() + ".png"

    imagen = pygame.image.load("resources/card_images/" + archivo_imagen)
    i_w, i_h = imagen.get_size()
    if i_w > i_h:
        i_w = ALTO_CLIMAX * i_w / i_h
        i_h = ALTO_CLIMAX
        if i_w < ANCHO_CLIMAX:
            i_h = ANCHO_CLIMAX * i_h / i_w
            i_w = ANCHO_CLIMAX

    else:
        i_h = ANCHO_CLIMAX * i_h / i_w
        i_w = ANCHO_CLIMAX
        if i_h < ALTO_CLIMAX:
            i_w = ALTO_CLIMAX * i_w / i_h
            i_h = ALTO_CLIMAX

    imagen = pygame.transform.scale(imagen, (i_w, i_h))
    ajuste_horizontal = (ANCHO_CLIMAX - i_w) / 2
    ajuste_vertical = (ALTO_CLIMAX - i_h) / 2

    resultado.blit(imagen, (ajuste_horizontal, ajuste_vertical))

    imagen = pygame.image.load("resources/card_layouts/climax/" + archivo_layout)
    resultado.blit(imagen, (0, 0))

    efecto_extra = carta.obetener_puntos_efecto_extra()
    if efecto_extra == 0:
        imagen = pygame.image.load("resources/card_layouts/triggers/none.png")
        imagen = pygame.transform.rotate(imagen, 90)
        resultado.blit(imagen, (0, 0))
    else:
        imagen = pygame.image.load("resources/card_layouts/triggers/soul.png")
        imagen = pygame.transform.rotate(imagen, 90)
        resultado.blit(imagen, (0, 0))

        if efecto_extra == 2:
            resultado.blit(imagen, (0, imagen.get_size()[1]))

    fuente = pygame.font.Font("resources/agfarotissemiserif.ttf", 22)

    label = fuente.render(str(carta.obtener_nombre()), 1, (255, 255, 255))
    centro_horizontal = 380 + ((580 - 380) - label.get_size()[0]) / 2
    resultado.blit(label, (centro_horizontal, 394))

    fuente = pygame.font.Font("resources/agfarotissemiserif.ttf", 16)

    lineas = []
    for line in carta.obtener_texto_decorativo().split('\n'):
        lineas.append(fuente.render(line, 1, (0, 0, 0)))

    alto_linea = lineas[0].get_size()[1]

    caja_de_texto = pygame.Surface((339, alto_linea * len(lineas)), pygame.SRCALPHA)
    caja_de_texto.fill((255, 255, 255, 150))
    posicion = 390
    resultado.blit(caja_de_texto, (ANCHO_CLIMAX - 372, posicion - caja_de_texto.get_size()[1]))

    for label in lineas[::-1]:
        posicion -= alto_linea
        resultado.blit(label, (ANCHO_CLIMAX - 372, posicion))

    fuente = pygame.font.Font("resources/agfarotissemiserif.ttf", 12)

    lineas = []

    alto_linea = 0
    if carta.obtener_habilidad():
        for line in carta.obtener_habilidad().obtener_texto().split('\n'):
            lineas.append(fuente.render(line, 1, (0, 0, 0)))

        alto_linea = lineas[0].get_size()[1]

    caja_de_texto = pygame.Surface((225, alto_linea * len(lineas)), pygame.SRCALPHA)
    caja_de_texto.fill((255, 255, 255, 150))
    posicion = 445
    resultado.blit(caja_de_texto, (8, posicion - caja_de_texto.get_size()[1]))

    for label in lineas[::-1]:
        posicion -= alto_linea
        resultado.blit(label, (10, posicion))

    return pygame.transform.rotate(resultado, -90)


def generar_imagen_carta(carta):
    """
    Genera la imagen para la carta pasada por parametro y la devuelve.
    :param carta: Carta para la que se desea generar la imagen.
    :return: Surface de pygame, que es la imagen generada para la carta.
    """
    if isinstance(carta, CartaClimax):
        return generar_imagen_climax(carta)
    elif isinstance(carta, CartaPersonaje):
        return generar_imagen_personaje(carta)
    elif isinstance(carta, CartaEvento):
        return generar_imagen_evento(carta)
    else:
        raise TypeError, "No es una carta, no se generar una imagen"


def mostrar_carta(carta, texto="", tiempo=2):
    """
    Muestra la imagen correspondiente a la carta pasada por parametro, durante el tiempo dado. La imagen es generada
    dinamicamente al llamar a la funcion.
    :param carta: Carta para la que se quiere generar y mostrar la imagen.
    :param texto: Texto que se mostrara en la ventana en la que se muestre la imagen de la carta.
    :param tiempo: Tiempo que se mostrara la imagen.
    :return: No tiene valor de retorno.
    """
    if isinstance(carta, CartaClimax):
        pantalla = pygame.display.set_mode((ANCHO_CLIMAX, ALTO_CLIMAX))
        imagen_carta = generar_imagen_climax(carta)
    elif isinstance(carta, CartaPersonaje):
        pantalla = pygame.display.set_mode((ANCHO_CARTA, ALTO_CARTA))
        imagen_carta = generar_imagen_personaje(carta)
    elif isinstance(carta, CartaEvento):
        pantalla = pygame.display.set_mode((ANCHO_CARTA, ALTO_CARTA))
        imagen_carta = generar_imagen_evento(carta)
    else:
        raise TypeError, "Eso no es una carta, no se puede mostrar"

    pantalla.blit(imagen_carta, (0, 0))
    pygame.display.set_caption(texto)
    pygame.display.flip()
    sleep(tiempo)