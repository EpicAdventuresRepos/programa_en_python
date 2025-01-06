from casa_encantada.datos import Resultado, Global, Localizacion, ObjetoAventura, LocalizacionPuerta
from casa_encantada.lexico import comando
from casa_encantada.user_interfaces import ConsoleOutput

"""
El parser comprueba que la segunda palabra sea un nombre registrado, por eso no puedo usar save nombre_partida
ya que daría error.

"""


def load_data():
    loc1 = Localizacion("01", "Localización 01")
    loc2 = Localizacion("02", "Localización 02")
    loc3 = Localizacion("03", "Localización 03")
    loc4 = LocalizacionPuerta("04", "Localización 04")
    loc1.conectar(0, loc2)
    loc2.conectar(2, loc3)
    loc3.conectar(1, loc4)
    loc4.conectar(3, loc1)

    estado = Global.get_instance()
    estado.set_localizacion(loc1)
    estado._output = ConsoleOutput()

    loc2.agregar_objeto("LLAVE",
                        ObjetoAventura("LLAVE", "Llave oxidada que nadie sabe qué abre.", "LLAVE", "Una llave"))



def procesar_cadena(cadena):

    palabras = cadena.split()  # Divide la cadena en palabras
    palabras_procesadas = [palabra[:6] if len(palabra) > 6 else palabra for palabra in palabras]
    return palabras_procesadas


def main_game():
    global output
    # Cargar datos iniciales
    load_data()

    estado = Global.get_instance()
    output = estado.output()

    resultado = None
    while resultado != Resultado.FIN_JUEGO:
        resultado = None
        estado = Global.get_instance()
        loc_actual = estado.localizacion()
        output.print('\n'+loc_actual.descripcion)

        while resultado != Resultado.REINICIA and resultado != Resultado.FIN_JUEGO:
            user_input = input(">> ")
            palabras = procesar_cadena(user_input)
            if len(palabras) == 1:
                user_command = comando(palabras[0])
            else:
                user_command = comando(palabras[0], palabras[1])

            # Ver si existen
            if user_command.token_verbo is None:
                output.print("Verbo no encontrado.")
                continue

            if user_command.token_nombre is None:
                output.print("Nombre no encontrado.")
                continue

            # Procesar comando en la loc en al que estoy
            loc_actual = estado.localizacion()
            resultado = loc_actual.run_command(user_command)
            if resultado != Resultado.NO_HECHO:
                continue

            # Procesar comando en los comandos por defecto.
            c_comunes = comandos_comunes()
            command_method = None
            if user_command.token_verbo in c_comunes:
                verbs = c_comunes[user_command.token_verbo]
                if user_command.token_nombre in verbs:
                    command_method = verbs[user_command.token_nombre]
                elif "*" in verbs:
                    command_method = verbs["*"]

            if command_method is not None:
                resultado = command_method(user_command)

            # Si no hay un HECHO es que no puedes hacerlo
            if resultado == Resultado.NO_HECHO or command_method is None:
                output.print("no puedes hacerlo.")
    output.print("Bye.")


# Verbos genéricos

def cmd_ver(comando):
    # borrar pantalla
    return Resultado.REINICIA


def cmd_inventario(comando):
    output.print("Llevas:")
    estado = Global.get_instance()
    for obj in estado.inventario.values():
        output.print(obj.breve_descripcion)
    return Resultado.HECHO


def cmd_fin(comando):
    return Resultado.FIN_JUEGO


def cmd_examinar_inventario(comando):

    if comando.verbo == "lee" or comando.verbo == "leer":
        output.print("No hay nada que leer de aquí.")
        return Resultado.HECHO

    if comando.token_nombre == "*":
        output.print("Indica qué examinar.")
        return Resultado.HECHO
    # To-Do
    # Mira si el objeto a examinar está en el inventario y muestra su descripción
    output.print("No puedes examinar eso.")
    return Resultado.HECHO


def cmd_guardar(comando):
    import pickle
    with open("save_game.pck", "wb") as save_file:
        pickle.dump(Global.get_instance(), save_file)
    output.print("Guardado.")
    return Resultado.HECHO


def cmd_cargar(comando):
    import pickle
    with open("save_game.pck", "rb") as save_file:
        save_data = pickle.load(save_file)
    Global._instance = save_data
    output.print("Cargado.")
    # Pulsa una tecla.
    return Resultado.REINICIA


def cmd_debug(comando):
    estado = Global.get_instance()
    output.print(estado)
    return Resultado.HECHO

def comandos_comunes():
    comandos = {
        "VER": {"*": cmd_ver},
        "INV": {"*": cmd_inventario},
        "EXAMINAR": {"*": cmd_examinar_inventario},
        "FIN_JUEGO": {"*": cmd_fin},
        "GUARDAR_PARTIDA": {"*": cmd_guardar},
        "CARGAR_PARTIDA": {"*": cmd_cargar},
        "DEBUG": {"*": cmd_debug},
    }
    return comandos


if __name__ == '__main__':
    main_game()
