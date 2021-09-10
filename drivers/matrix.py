import drivers.matrix_ezmx42hs

class Matrix():
    def __init__(self, name, model, *args, **kwargs):
        self.name  = name
        self.model = model
        if self.model == "ezmx42hs": self.__matrix__ = drivers.matrix_ezmx42hs.MatrixEzmx42hs(**kwargs)
        else: raise Exception("Invalid Matrix Model Type '{}'".format(model))

    def connect(self):
        self.__matrix__.connect()

    def disconnect(self):
        self.__matrix__.disconnect()

    def isConnected(self):
        return self.__matrix__.isConnected()

    def version(self):
        return self.__matrix__.version()

    def setOuputScaler(self, output, mode):
        self.__matrix__.setOutputScalar(output, mode)

    def getOuputScaler(self, output):
        return self.__matrix__.getOutputScalar(output)

    def setOutputSource(self, output, input):
        self.__matrix__.setOutputSource(output, input)

    def getOutputSource(self, output):
        return self.__matrix__.getOutputSource(output)

    def setInputEDID(self, input, mode):
        self.__matrix__.setInputEDID(input, mode)

    def getInputEDID(self, input):
        return self.__matrix__.getInputEDID(input)
    


