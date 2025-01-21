from templates import *


class Objeto(object):
    def __init__(self, name, s_desc=None, desc="", loc="NOTCREATED"):
        self._name = name.upper()
        self._loc = loc
        self._desc=desc
        self._short_desc = s_desc
        if s_desc is None:
            self._short_desc = "An " + name + "."


plantilla_html = """
<HTML>

<HEAD> </HEAD>
<BODY>

% for obj in objetos:
<P> <BOLD> {{obj._name}} </BOLD> </P>
<P> Está en: {{obj._name}}      </P>
<P> {{obj._desc}}      </P>
<HR/>
% end

</BODY>

</HTML>
"""


objetos = (
    Objeto("Hammer", "A blacksmith's hammer", "A weapon made for everyday use.#n6 points of damage."),
    Objeto("Anchor", desc="From a ship that was shipwrecked long ago.#n10 points of damage."),
    Objeto("Egg", desc="Bigger than your head.", loc="10")
)
contadores = [200, 0]
tpl = SimpleTemplate(plantilla_html)
print(tpl.render(contadores=contadores, objetos=objetos))



