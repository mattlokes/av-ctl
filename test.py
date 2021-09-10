from matrix import *

kwargs = {
          'serial' : {
              'port'    : '/dev/ttyUSB0',
              'baudrate': 57600,
              'timeout' : 0.1,

          }
         }

matrix = Matrix(name="test_matrix", model="ezmx42hs", **kwargs)

if matrix.isConnected():
    print("Found EZ-MX42HS Version: {}".format(matrix.version()))
    route1 = matrix.getOutputSource(1)
    edid1  = matrix.getInputEDID(route1)
    route2 = matrix.getOutputSource(2)
    edid2  = matrix.getInputEDID(route2)
    print("  Routes: ")
    print("    {}  - > 1   [EDID: {}]".format(route1, edid1))
    print("    {}  - > 2   [EDID: {}]".format(route2, edid2))
else:
    print("No Matrix Found!")
