#ifndef TESTING_ONLY
#include "PyServerPrivatePCH.h"
#else
#include "PythonProxy.h"

int main()
{
    LoadPythonInterperter();
    return 0;
}
#endif
