class Codec():
    def __init__(self, encoding={}):
        self.__encodes__ = encoding
        self.__decodes__ = {v:k for k,v in self.__encodes__.items()}

    def isLegal(self, value):
        return value in self.__encodes__.keys() or value in self.__decodes__.keys()

    def values(self):
        return self.__encodes__.keys()

    def encode(self, value):
        return self.__encodes__.get(value, None)

    def decode(self, value):
        return self.__decodes__.get(value, None)
            
class MatrixBase():
    def __init__(self, *args, **kwargs):
        self.legal_inputs       = list(range(1,kwargs.get("inputs",  4)+1))
        self.legal_outputs      = list(range(1,kwargs.get("outputs", 2)+1))
        self.scalar_codec       = Codec(kwargs.get("scalar_modes", {}))
        self.edid_codec         = Codec(kwargs.get("edid_modes", {}))

    def __checkInput__(self, input):
        if input not in self.legal_inputs:
            estr = "Invalid Input '{}', device contains  inputs {}".format(input, self.legal_inputs)
            raise Exception (estr)

    def __checkOutput__(self, output):
        if output not in self.legal_outputs:
            estr = "Invalid Output '{}', device contains  Outputs {}".format(output, self.legal_outputs)
            raise Exception (estr)

    def __checkScalar__(self, mode):
        if not self.scalar_codec.isLegal(mode):
            estr  = "Invalid Scalar Mode '{}' expected one of: \n".format(mode)
            estr += "  - {}".format("\n  - ".join(self.scalar_codec.values()))
            raise Exception (estr)

    def __checkEDID__(self, mode):
        if not self.edid_codec.isLegal(mode):
            estr  = "Invalid EDID Mode '{}' expected one of: \n".format(mode)
            estr += "  - {}".format("\n  - ".join(self.edid_codec.values()))
            raise Exception (estr)

    def __decodeEDID__(self, edid):
        return self.edid_codec.decode(edid)

    def __encodeEDID__(self, edid):
        enc = self.edid_codec.encode(edid)
        return enc if enc is not None else edid

    def __decodeScalar__(self, scalar):
        return self.scalar_codec.decode(scalar)

    def __encodeScalar__(self, scalar):
        enc = self.scalar_codec.encode(scalar)
        return enc if enc is not None else scalar

    def connect(self):
        assert False, "Virtual Function - This me be overriden for this objection to be used"

    def disconnect(self):
        assert False, "Virtual Function - This me be overriden for this objection to be used"

    def isConnected(self):
        assert False, "Virtual Function - This me be overriden for this objection to be used"

    def version(self):
        assert False, "Virtual Function - This me be overriden for this objection to be used"

    def setOuputScaler(self, output, mode):
        assert False, "Virtual Function - This me be overriden for this objection to be used"

    def getOuputScaler(self, output):
        assert False, "Virtual Function - This me be overriden for this objection to be used"

    def setOutputSource(self, output, input):
        assert False, "Virtual Function - This me be overriden for this objection to be used"

    def getOutputSource(self, output):
        assert False, "Virtual Function - This me be overriden for this objection to be used"

    def setInputEDID(self, input, mode):
        assert False, "Virtual Function - This me be overriden for this objection to be used"

    def getInputEDID(self, input):
        assert False, "Virtual Function - This me be overriden for this objection to be used"
    


