"""Minimal ctypes bridge to the locally installed Z3 shared library.
All mathematical constraints are supplied as inspectable SMT-LIB 2 text.
"""
import ctypes as C
import ctypes.util
import os
class Solver:
    def __init__(self):
        name=os.environ.get('Z3_LIBRARY') or C.util.find_library('z3') or 'libz3.so.4'
        self.lib=C.CDLL(name)
        z=self.lib
        z.Z3_mk_config.restype=C.c_void_p
        z.Z3_del_config.argtypes=[C.c_void_p]
        z.Z3_mk_context.argtypes=[C.c_void_p];z.Z3_mk_context.restype=C.c_void_p
        z.Z3_del_context.argtypes=[C.c_void_p]
        z.Z3_eval_smtlib2_string.argtypes=[C.c_void_p,C.c_char_p];z.Z3_eval_smtlib2_string.restype=C.c_char_p
        z.Z3_get_full_version.restype=C.c_char_p
        cfg=z.Z3_mk_config();self.ctx=z.Z3_mk_context(cfg);z.Z3_del_config(cfg)
    def eval(self,text):
        return self.lib.Z3_eval_smtlib2_string(self.ctx,text.encode()).decode()
    def version(self):return self.lib.Z3_get_full_version().decode()
    def close(self):
        if self.ctx:self.lib.Z3_del_context(self.ctx);self.ctx=None
