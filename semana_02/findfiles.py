from pathlib import Path

def files_in_folder(folder):
    r_ficheros = list()
    r_directorios=list()
    p = Path(folder)
    try:
        for x in p.iterdir():
            if x.is_dir():
                r_directorios.append(str(x))
            else:
                r_ficheros.append(str(x))
        return r_ficheros, r_directorios
    except:
        print("Acceso denegado para", folder)
        return [], []


def find_files(ficheros, extensiones):
    resultado = list()
    for fichero in ficheros:
        for extension in extensiones:
            if fichero.endswith(extension):
                resultado.append(fichero)
    return  resultado


def mostrar_ficheros(ficheros):
    if len(ficheros) > 0:
        print(ficheros)


def busqueda_recursiva(directorio_busqueda, extensiones):
    ficheros, directorios = files_in_folder(directorio_busqueda)
    mostrar_ficheros(find_files(ficheros, extensiones))
    for directorio in directorios:
        #print("Entrando en ", directorio)
        busqueda_recursiva(directorio, extensiones)



# Press the green button in the gutter to run the script.
if __name__ == '__main__':
   pass


#extensiones = [".txt", ".jpg", ".doc", ".avi", ".mpg", ".mpeg", ".png", ".mkv"]
extensiones = [".avi", ".mpg", ".mpeg", ".mkv", ".mp4", ".ogv", ".flv", ".wmv", ".webm"]
#busqueda_recursiva('D:/Recovery_20210224_220558', extensiones)
busqueda_recursiva('D:/Recovery_20210226_110340', extensiones)
print("Fin.")



