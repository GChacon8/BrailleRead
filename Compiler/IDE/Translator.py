import sys
sys.path.append("..")


# Class in charge of translating the code
class Translator(object):
    def __init__(self, output) -> None:
        self.output = output
        self.code = ""

    def Translate(self):
        for instruction in self.output:
            data = instruction.split(";")
            if data[0] == "Write":
                self.code += data[1]
            elif data[0] == "Signal":
                self.code += data[1]
            elif data[0] == "EndSignal":
                self.code += data[1]
            else:
                print("Error in output " + data[0]+ " not recognized")
            self.code += "~"
        return self.code
