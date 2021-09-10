from drivers.matrix_base import *

import serial
import re

class MatrixEzmx42hs(MatrixBase):
    def __init__(self, *args, **kwargs):
        
        super().__init__( inputs       =4, 
                          outputs      =2,
                          scalar_modes = {
                                          "BYPASS": 1,
                                          "4K->2K": 2
                                         },
                          edid_modes   = {
                                          "EDID_BYPASS"            :  0,
                                          "1080P_2CH_HDR"          :  1,
                                          "1080P_6CH_HDR"          :  2,
                                          "1080P_8CH_HDR"          :  3,
                                          "1080P_3D_2CH_HDR"       :  4,
                                          "1080P_3D_6CH_HDR"       :  5,
                                          "1080P_3D_8CH_HDR"       :  6,
                                          "4K30HZ_3D_2CH_HDR"      :  7,
                                          "4K30HZ_3D_6CH_HDR"      :  8,
                                          "4K30HZ_3D_8CH_HDR"      :  9,
                                          "4K60HzY420_3D_2CH_HDR"  : 10,
                                          "4K60HzY420_3D_6CH_HDR"  : 11,
                                          "4K60HzY420_3D_8CH_HDR"  : 12,
                                          "4K60HZ_3D_2CH_HDR"      : 13,
                                          "4K60HZ_3D_6CH_HDR"      : 14,
                                          "4K60HZ_3D_8CH_HDR"      : 15,
                                          "H4K_DOLBY_VISION_ATMOS" : 16,
                                         }
                        )

        # Create Scalar Cache as we cant retrive the information from the device.
        self.__output_scalar_cache__ = {
                                         1: self.__encodeScalar__("BYPASS"),
                                         2: self.__encodeScalar__("BYPASS"),
                                       }

        # Setup Serial Comms
        self.serial = serial.Serial( **kwargs['serial'] )
        self.connect()

    ### Serial Interfacing Functions
    def __serial_flush__(self):
        self.serial.flush()

    def __serial_tx__(self, string):
        return self.serial.write(string.encode('utf-8'))

    def __serial_rx__(self,length=None):
        if length is None:
            return self.serial.readall().decode()
        else:
            return self.serial.read(length).decode()

    def __getStatus__(self):
        status = {
                  'output_source':{},
                  'input_edid':   {},
                 }

        self.__serial_flush__()
        self.__serial_tx__("EZG STA\r")

        #rx = self.__serial_rx__(length=150)
        rx = self.__serial_rx__()
        lines = rx.split("\n")
        for l in lines:

            route = re.search(r'OUT(?P<output>\d+) VS IN(?P<input>\d+)', l)
            if route:
                route = route.groupdict()
                status['output_source'][int(route['output'])] = int(route['input'])
                continue

            edid = re.search(r'IN(?P<input>\d+) EDID (?P<edid>\d+)', l)
            if edid:
                edid = edid.groupdict()
                status['input_edid'][int(edid['input'])] = self.__decodeEDID__(int(edid['edid']))
                continue

        return status

    ###  Matrix Interface
    def connect(self):
        self.serial.close()
        self.serial.open()
        self.serial.write(b'\r\r')
        self.__serial_flush__()

    def disconnect(self):
        self.__serial_flush__()
        self.serial.close()

    def isConnected(self):
        return self.version() is not None

    def version(self):
        self.__serial_flush__()
        self.__serial_tx__("EZSTA\r")

        #rx = self.__serial_rx__(length=500)
        rx = self.__serial_rx__()

        m = re.search(r'F/W Version : ([0-9.]+)',rx) 
        if m: return m.group(1)
        else: return None

    def setOuputScaler(self, output, mode):
        self.__checkOutput__(output)
        self.__checkScalar__(mode)
        mode = self.__encodeScalar__( mode)
        self.__serial_tx__("EZS OUT{} VIDEO{}\r".format(output, mode))
        self.__output_scalar_cache__[output] = mode
    
    def getOuputScalar(self, output):
        self.__checkOutput__(output)
        return self.__decodeScalar__(self.__output_scalar_cache__[output])

    def setInputEDID(self, input, mode):
        self.__checkInput__(input)
        self.__checkEDID__(mode)
        mode = self.__encodeEDID__( mode)
        self.__serial_tx__("EZS IN{} EDID {}\r".format(input, mode))

    def getInputEDID(self, input):
        self.__checkInput__(input)
        status = self.__getStatus__()
        return status['input_edid'][input]
    
    def setOutputSource(self, output, input):
        self.__checkOutput__(output)
        self.__checkInput__(input)
        self.__serial_tx__("EZS OUT{} VS IN{}\r".format(output, input))

    def getOutputSource(self, output):
        self.__checkOutput__(output)
        status = self.__getStatus__()
        return status['output_source'][output]

