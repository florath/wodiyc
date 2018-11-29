'''
G Code Library

This is a modular GCode library.
It is written in a way that it can / must be prepended
into each NGC file.
'''
import os

class GCodeLib:

    def __init__(self, path='wodiyc/lib/gcode/glib'):
        self._path = path

    def output(self, file_descriptor):
        '''Output the complete library to the file descriptor'''
        file_descriptor.write(b"(----- GCode Library -----)\n")
        for fname in os.listdir(self._path):
            if not fname.endswith('.ngc'):
                continue
            pathname = os.path.join(self._path, fname)
            with open(pathname, "rb") as ngc_file:
                fcontent = ngc_file.read()
                file_descriptor.write(
                    ("(--- File [%s] ---)\n" % fname).encode())
                file_descriptor.write(fcontent)
        file_descriptor.write(b"(----- End GCode Library -----)\n")
