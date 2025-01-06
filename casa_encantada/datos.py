#Asocia una dirección a un token de movimiento.
# N = 0, S = 1, etc.
movimiento = ("N", "S", "E", "O")
movimiento_doble_sentido = (1, 0, 3, 2)

class Resultado:
    """
    """
    HECHO    = "Éxito"
    NO_HECHO = "Fallo"
    REINICIA = "Indeterminado"
    FIN_JUEGO = "Salir del juego"


class Localizacion:
    def __init__(self, nombre, descripcion, oscura=False):
        self.nombre = nombre
        self.descripcion = descripcion
        self.oscura = oscura  # Estado de iluminación de la localización
        # Cambiar a mapa token: objeto
        self.objetos = {}  # Objetos visibles en la localización Token : Objeto
        self.objetos_ocultos = []  # Lista de objetos no visibles
        self.conexiones = {}  # Diccionario para las conexiones con otras localizaciones {dirección: Localizacion}
        self.examinables = {} # Cosas examinables que no son objetos.

        self.comandos = {
            "N": {"*": self.mover_norte},
            "S": {"*": self.mover_sur},
            "E": {"*": self.mover_este},
            "O": {"*": self.mover_oeste},
            "COGER": {"*": self.coger},
            "DEJAR": {"*": self.dejar},
            # No puedo tener 2 porque uno sobrescribe al otro.
            "EXAMINAR": {"*": self.examinar},
            #"EXAMINAR": {"*": self.ex_objetos},   # Si el anterior nod evuelve HECGHO, se ejecuta este.
        }

    def __str__(self):
        return str(self.nombre) + " / Conexiones: " + str(self.conexiones)

    def agregar_objeto(self, token, objeto, visible=True):
        if visible:
            self.objetos[token] = objeto
        else:
            self.objetos_ocultos.append(objeto)

    def hay_objetos_visibles(self):
        return len(self.objetos) > 0

    def conectar(self, direccion, otra_localizacion, doble_sentido = True):
        self.conexiones[direccion] = otra_localizacion
        if not doble_sentido:
            return
        direccion_conraria = movimiento_doble_sentido[direccion]
        otra_localizacion.conectar(direccion_conraria, self, False)


    def agregar_examinable(self, token, descripción):
        self.examinables[token] = descripción

    def mostrar_descripcion(self):
        """
        Devuelve una descripción detallada de la localización, incluyendo objetos visibles y direcciones.
        """
        if self.oscura:
            return f"Te encuentras en {self.nombre}. Está completamente a oscuras. Necesitas una fuente de luz para ver algo.\n"

        descripcion = f"Te encuentras en {self.nombre}. {self.descripcion}\n"
        if self.objetos:
            descripcion += f"Objetos visibles: {', '.join(self.objetos)}.\n"
        if self.conexiones:
            descripcion += f"Puedes ir hacia: {', '.join(self.conexiones.keys())}.\n"
        return descripcion

    def run_command(self, comando):
        if comando.token_verbo not in self.comandos:
            return Resultado.NO_HECHO
        verbs = self.comandos[comando.token_verbo]
        if comando.token_nombre not in verbs:
            if "*" not in verbs:
                return Resultado.NO_HECHO
            else:
                names = verbs["*"]
        else:
            names = verbs[comando.token_nombre]
        return names(comando)

    def _mover(self, direccion):
        if direccion not in self.conexiones:
            print("No hay salida.")
            return Resultado.HECHO
        estado = Global.get_instance()
        estado.set_localizacion(self.conexiones[direccion])
        return Resultado.REINICIA

    def mover_norte(self, command):
        return self._mover(0)

    def mover_sur(self, command):
        return self._mover(1)

    def mover_este(self, command):
        return self._mover(2)

    def mover_oeste(self, command):
        return self._mover(3)

    def coger(self, command):
        if command.token_nombre == "*":
            print("Indica qué coger.")
            return Resultado.HECHO
        if command.token_nombre not in self.objetos:
            print("No está aquí.")
            return Resultado.HECHO
        estado = Global.get_instance()
        estado.añade_inventario(command.token_nombre, self.objetos[command.token_nombre])
        del self.objetos[command.token_nombre]
        print("Ok.")

        return Resultado.HECHO

    def dejar(self, command):
        # To-Do
        return Resultado.HECHO

    def examinar(self, command):
        if command.token_nombre in self.examinables:
            print(self.examinables[command.token_nombre])
            return Resultado.HECHO
        if command.token_nombre in self.objetos:
            print(self.objetos[command.token_nombre].descripcion)
            return Resultado.HECHO

        return Resultado.NO_HECHO


###########


class LocalizacionPuerta(Localizacion):
    def __init__(self, nombre, descripcion, oscura=False):
        super().__init__(nombre, descripcion, oscura)
        self.puerta_cerrada = True
        self.direccion_puerta = 3 # Oeste
        self.comandos["ABRIR"] = {"PUERTA": self.abrir_puerta}
        self.examinables["PUERTA"] = "Tiene una cerradura para una llave."

    def mover_oeste(self, command):
        # Asumo que hay salida
        if (self.puerta_cerrada):
            print("La puerta está cerrada")
            return Resultado.HECHO
        return self._mover(2)

    def abrir_puerta(self, comando):
        estado = Global.get_instance()
        if estado.en_inventario("LLAVE") and self.puerta_cerrada:
            print("Abres la puerta con la llave.")
            self.puerta_cerrada = True
        else:
            print("No puedes hacer eso") # Mensajes más cocnretos.
        return Resultado.HECHO


###########

class ObjetoAventura:
    def __init__(self, nombre, descripcion, token, breve_descripcion):
        self.nombre = nombre
        self.descripcion = descripcion
        self._token = token  # El atributo `token` es privado para hacer que sea de solo lectura
        self.breve_descripcion = breve_descripcion
        self.en_inventario = False  # Indica si el objeto está en el inventario del jugador.


    @property
    def token(self):
        return self._token

    def examinar(self):
        return f"{self.nombre}: {self.descripcion}"

    def mostrar_breve_descripcion(self):
        return self.breve_descripcion or f"No hay descripción breve para el {self.nombre}."

    def __repr__(self):
        """
        Representación en texto del objeto.
        """
        return f"ObjetoAventura(nombre='{self.nombre}', token='{self.token}')"


###########


class Global:

    _instance = None

    @staticmethod
    def get_instance():
        """
        Devuelve la única instancia del Singleton.
        Si no existe, la crea.
        """
        if Global._instance is None:
            Global._instance = Global()
        return Global._instance

    def __init__(self):
        self.localizacion_actual = None
        self.inventario = {}
        self._sve_dt = None
        self._output = None

    def __str__(self):
        return f"Localización {self.localizacion_actual} / Inventario: {self.inventario}"

    def set_localizacion(self, localizacion_actual):
        self.localizacion_actual = localizacion_actual

    def localizacion(self):
        return self.localizacion_actual

    def añade_inventario(self, token, objeto):
        self.inventario[token] = objeto

    def en_inventario(self, token):
        return token in self.inventario

    def saca_inventario(self, token):
        objeto = self.inventario[token]
        del self.inventario[token]
        return objeto

    def output(self):
        return self._output


