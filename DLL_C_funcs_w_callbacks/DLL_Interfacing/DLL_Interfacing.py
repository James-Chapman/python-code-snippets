# -*- coding: utf-8 -*-
#####################################################################
#  Author: James Chapman
#  License: BSD
#  Date: 13/03/2014
#  Description:
#####################################################################

import ctypes

# DLL handle
g_dllHandle = None  

# Callback function type definition
# 1st param is return type
# 2nd param is function param type
CMPFUNC = ctypes.CFUNCTYPE(ctypes.c_void_p, ctypes.c_int)  

#
# Function DLL will call back to
#
def callback_function(_callback_value):
    result = ctypes.c_int(_callback_value)
    print("Callback result: %d" % (result.value))

#
# Python API binding wrapped in a class
#    
class PyIntAdd(object):

    def __init__(self, dll_file):
        global g_dllHandle
        g_dllHandle = ctypes.CDLL(dll_file)
        assert g_dllHandle is not None
    
    
    def setCallBackFn(self, callbackFn):
        """DLL_EXPORT void __cdecl setCallBackFunction(PythonCallbackFunction _fn);"""
        global g_dllHandle
        assert g_dllHandle is not None
        g_dllHandle.setCallBackFunction(callbackFn)    


    def add(self, a, b):
        """DLL_EXPORT void __cdecl add(int _a, int _b);"""
        global g_dllHandle
        assert g_dllHandle is not None
        g_dllHandle.add(ctypes.c_int(a), ctypes.c_int(b))


#
# Main method
#
def main():
    intAdd = PyIntAdd('callback_DLL.dll')
    global CMPFUNC
    callback_obj = CMPFUNC(callback_function)   
    ctypes._CFuncPtr     
    intAdd.setCallBackFn(callback_obj)
    print("Calling dll.add with values 1 and 2")
    intAdd.add(1, 2)


if __name__ == '__main__':
    main()
    