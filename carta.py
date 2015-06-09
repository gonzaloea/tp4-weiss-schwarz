class Carta(object):
    """ Clase que define atributos y metodos basicos de las cartas. Se usa como base para los distintos tipos
        de carta. """

    def __init__(self, nombre, color, efecto_extra, habilidad, texto_decorativo):
        """
        :param nombre: Nombre de la carta. Debe ser un string.
        :param color: Color de la carta. Debe ser un string que representa el color.
        :param efecto_extra: Puntos de efecto extra de la carta. Debe ser un numero entero entre 0 y 2, inclusive.
        :param habilidad: Habilidad de la carta. La misma debe ser una instancia de una clase que herede de Habilidad.
        :param texto_decorativo:Texto adicional de la carta. Debe ser un string.
        """
        self.nombre = nombre
        self.color = color
        self.efecto_extra = efecto_extra
        self.habilidad = habilidad
        self.texto_decorativo = texto_decorativo

    def obtener_color(self):
        """
        Devuelve el color de la carta
        :return: String que representa el color
        """
        return self.color

    def obetener_puntos_efecto_extra(self):
        """
        Devuelve los puntos de efecto extra de la carta
        :return: Numero entero entre 0 y 2 inclusive
        """
        return self.efecto_extra

    def obtener_nombre(self):
        """
        Devuelve el nombre de la carta
        :return: String con el nombre
        """
        return self.nombre

    def obtener_texto_decorativo(self):
        """
        Devuelve el texto adicional de la carta
        :return: String con el texto adicional
        """
        return self.texto_decorativo

    def obtener_habilidad(self):
        """
        Devuelve la referencia de la habilidad que posee la carta
        :return: Una referencia a un objeto de una clase que herede de Habilidad
        """
        return self.habilidad


class CartaPersonaje(Carta):
    """ Clase que representa a las cartas de tipo Personaje. """

    def __init__(self, nombre, color, efecto_extra, habilidad, texto_decorativo, nivel, costo, poder, puntos_alma, subtipos):
        """
        :param nombre: Nombre de la carta. Debe ser un string.
        :param color: Color de la carta. Debe ser un string que representa el color.
        :param efecto_extra: Puntos de efecto extra de la carta. Debe ser un numero entero entre 0 y 2, inclusive.
        :param habilidad: Habilidad de la carta. La misma debe ser una instancia de una clase que herede de Habilidad.
        :param texto_decorativo:Texto adicional de la carta. Debe ser un string.
        :param nivel: Nivel de la carta. Debe ser un numero entero igual o mayor a 0.
        :param costo: Costo para jugar la carta. Debe ser un numero entero igual o mayor a 0.
        :param poder: Poder de la carta. Debe ser un numero entero igual o mayor a 0.
        :param puntos_alma: Puntos de alma de la carta. Debe ser un numero entero, y valer 1 o 2.
        :param subtipos: Subtipos de la carta de personaje. Debe ser una tupla que contenga 2 string.
        """
        super(self.__class__, self).__init__(nombre, color, efecto_extra, habilidad, texto_decorativo)
        self.nivel = nivel
        self.costo = costo
        self.poder = poder
        self.puntos_alma = puntos_alma
        self.subtipos = subtipos

    def obtener_nivel(self):
        """
        Devuelve el nivel de la carta
        :return: Numero entero igual o mayor a 0
        """
        return self.nivel

    def obtener_costo(self):
        """
        Devuelve el costo de la carta
        :return: Numero entero igual o mayor a 0
        """
        return self.costo

    def obtener_poder(self):
        """
        Devuelve la fuerza de la carta
        :return: Numero entero igual o mayor a 0
        """
        return self.poder

    def obtener_puntos_alma(self):
        """
        Devuelve los puntos de alma de la carta
        :return: Numero entero mayor a 0
        """
        return self.puntos_alma

    def obtener_subtipos(self):
        """
        Devuelve los subtipos de la carta
        :return: Tupla que contiene 2 string
        """
        return self.subtipos

    def establecer_poder(self, poder):
        """
        Establece el poder de la carta al valor pasado por parametro. El poder de una carta nunca puede ser menor que 0.
        :param poder: Numero entero cuyo valor sera establecido como poder de la carta.
        :return: No tiene valor de retorno.
        """
        self.poder = round(poder)
        if self.poder < 0:
            self.poder = 0

    def __str__(self):
        return self.nombre + " (" + str(self.nivel) + "," + str(self.costo) + " " + self.color + ")"

    def __repr__(self):
        return self.nombre + " (" + str(self.nivel) + "," + str(self.costo) + " " + self.color + ")"


class CartaEvento(Carta):
    """ Clase que representa a las cartas de tipo Evento. """

    def __init__(self, nombre, color, efecto_extra, habilidad, texto_decorativo, nivel, costo):
        """
        :param nombre: Nombre de la carta. Debe ser un string.
        :param color: Color de la carta. Debe ser un string que representa el color.
        :param efecto_extra: Puntos de efecto extra de la carta. Debe ser un numero entero entre 0 y 2, inclusive.
        :param habilidad: Habilidad de la carta. La misma debe ser una instancia de una clase que herede de Habilidad.
        :param texto_decorativo:Texto adicional de la carta. Debe ser un string.
        :param nivel: Nivel de la carta. Debe ser un numero entero igual o mayor a 0.
        :param costo: Costo para jugar la carta. Debe ser un numero entero igual o mayor a 0.
        """
        super(self.__class__, self).__init__(nombre, color, efecto_extra, habilidad, texto_decorativo)
        self.nivel = nivel
        self.costo = costo

    def obtener_nivel(self):
        """
        Devuelve el nivel de la carta
        :return: Numero entero igual o mayor a 0
        """
        return self.nivel

    def obtener_costo(self):
        """
        Devuelve el costo de la carta
        :return: Numero entero igual o mayor a 0
        """
        return self.costo

    def __str__(self):
        return self.nombre + " (" + str(self.nivel) + "," + str(self.costo) + " " + self.color + ")"

    def __repr__(self):
        return self.nombre + " (" + str(self.nivel) + "," + str(self.costo) + " " + self.color + ")"


class CartaClimax(Carta):
    """ Clase que representa a las cartas de tipo climax. """

    def __str__(self):
        return self.nombre + " (" + self.color + " CLIMAX)"

    def __repr__(self):
        return self.nombre + " (" + self.color + " CLIMAX)"
