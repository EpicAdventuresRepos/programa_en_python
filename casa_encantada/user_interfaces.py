
class ConsoleOutput(object):

    def print(self, msg):
        print(msg)

    @staticmethod
    def s_print(msg):
        print(msg)


class ConsoleInput(object):

        def press_intro(self):
            ConsoleOutput.s_print("Pulsa Enter...")
            input()



