"""
SPDX-License-Identifier: BSD-2
"""

from ._libtpm2_pytss import lib, ffi
from .TCTI import TCTI
from .utils import _chkrc


class TctiLdr(TCTI):
    def __init__(self, name=None, conf=None):

        self._ctx_pp = ffi.new("TSS2_TCTI_CONTEXT **")

        if name is None:
            name = ffi.NULL
        elif isinstance(name, str):
            name = name.encode()

        if conf is None:
            conf = ffi.NULL
        elif isinstance(conf, str):
            conf = conf.encode()

        if not isinstance(name, (bytes, type(ffi.NULL))):
            raise TypeError(f"name must be of type bytes, got {type(name)}")

        if not isinstance(conf, (bytes, type(ffi.NULL))):
            raise TypeError(f"conf must be of type bytes, got {type(name)}")

        _chkrc(lib.Tss2_TctiLdr_Initialize_Ex(name, conf, self._ctx_pp))
        super().__init__(self._ctx_pp[0])

        self._name = name.decode() if name else ""
        self._conf = conf.decode() if conf else ""

    def __enter__(self):
        return self

    def __exit__(self, _type, value, traceback):
        self.close()

    def close(self):
        lib.Tss2_TctiLdr_Finalize(self._ctx_pp)
        self._ctx = ffi.NULL

    @property
    def name(self):
        return self._name

    @property
    def conf(self):
        return self._conf
