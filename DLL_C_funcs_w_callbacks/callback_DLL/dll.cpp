/********************************************************************
*  Author: James Chapman
*  License: BSD
*  Date: 13/03/2014
*  Description:
*********************************************************************/

#include <functional>
#include <Windows.h>

#include "intadd.hpp"
#include "dll.hpp"

#ifdef __cplusplus
extern "C"
{
#endif

    /**
    * Entry point into DLL
    */
    DLL_EXPORT BOOL APIENTRY DllMain(HINSTANCE hinstDLL, DWORD fdwReason, LPVOID lpvReserved)
    {
        switch (fdwReason)
        {
        case DLL_PROCESS_ATTACH:
            // attach to process
            // return FALSE to fail DLL load
            break;

        case DLL_PROCESS_DETACH:
            // detach from process
            break;

        case DLL_THREAD_ATTACH:
            // attach to thread
            break;

        case DLL_THREAD_DETACH:
            // detach from thread
            break;
        }
        return TRUE; // succesful
    }

    /**
    * Set callback function
    */
    DLL_EXPORT void __cdecl setCallBackFunction(PythonCallbackFunction _fn)
    {
        PythonDLL::IntAdd::setCallBackFunction(_fn);
    }

    /**
    * Add 2 integers
    */
    DLL_EXPORT void __cdecl add(int _a, int _b)
    {
        PythonDLL::IntAdd::add(_a, _b);
    }

#ifdef __cplusplus
}
#endif
