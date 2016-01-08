/********************************************************************
*  Author: James Chapman
*  License: BSD
*  Date: 13/03/2014
*  Description:
*********************************************************************/

#include <iostream>

#include "intadd.hpp"

using namespace PythonDLL;

//
// Static class members
//
int IntAdd::s_resultValue;
PythonCallbackFunction IntAdd::s_callbackFn;

/**
* Constructor
*/
IntAdd::IntAdd()
{
    s_resultValue = 0;
}

/**
* Destructor
*/
IntAdd::~IntAdd()
{}

/**
* Set callback function
*/
void IntAdd::setCallBackFunction(PythonCallbackFunction _fn)
{
    s_callbackFn = _fn;
}

/**
* Add 2 integers
*/
void IntAdd::add(int _a, int _b)
{
    s_resultValue = _a + _b;
    std::cout << "DLL: " << s_resultValue << std::endl;
    s_callbackFn(s_resultValue);
}
