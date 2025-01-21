from templates import *


class Objeto(object):
    def __init__(self, name, s_desc=None, desc="", loc="NOTCREATED"):
        self._name = name.upper()
        self._loc = loc
        self._desc=desc
        self._short_desc = s_desc
        if s_desc is None:
            self._short_desc = "An " + name + "."

plantilla = """
; Palabra
% for obj in objetos:
{{obj._name}} {{contadores[0]}}
% contadores[0] += 1
% end

; Descripción corta
% for obj in objetos:
#define o{{obj._name}} {{contadores[1]}}
/o{{obj._name}} "{{obj._short_desc}}"
% contadores[1] += 1
% end

; Declaración de objeto
% for obj in objetos:
/o{{obj._name}}      {{obj._loc}} 1       _ _  _ _ _ _ _ _ _ _ _ _ _ _ _ _ _ Y    {{obj._name}}   _ 
% end

; Examinar
% for obj in objetos:
> EX  HAMMER     PRESENT o{{obj._name}}  
                 MESSAGE "{{obj._desc}}"
                 DONE                
% end
"""

objetos = (
    Objeto("Hammer", "A blacksmith's hammer", "A weapon made for everyday use.#n6 points of damage."),
    Objeto("Anchor", desc="From a ship that was shipwrecked long ago.#n10 points of damage."),
    Objeto("Egg", desc="Bigger than your head.", loc="10")
)
contadores = [200, 0]
tpl = SimpleTemplate(plantilla)
print(tpl.render(contadores=contadores, objetos=objetos))
