/********************************************************************
*  Author: James Chapman
*  License: BSD
*  Date: 13/03/2014
*  Description:
*********************************************************************/

#ifndef INTADD_HPP
#define INTADD_HPP

#pragma once

#include <windows.h>

typedef void(*PythonCallbackFunction)(int);

namespace PythonDLL
{
    class IntAdd
    {
    public:
        IntAdd();
        ~IntAdd();
        static void setCallBackFunction(PythonCallbackFunction _fn);
        static void add(int _a, int _b);
    private:
        static int s_resultValue;
        static PythonCallbackFunction s_callbackFn;
    };

}; // PythonDLL

#endif // INTADD_HPP
