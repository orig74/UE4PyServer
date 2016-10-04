# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
print('pyinit imported')
cnt=0
from ctypes import *
import os

pluginpath=os.path.abspath(os.path.dirname(__file__)+'/../../../')
libfile=pluginpath+'/Binaries/Linux/libUE4Editor-PyServer.so'
libc=CDLL(libfile)
libc.calledfrompython.argtypes=[]
libc.calledfrompython.restype=c_int


def PythonButtonClicked():
    print('PythonButtonClicked inside python!!!')

def PyInit(gworld):
    print('In PyInit, gworld=',gworld)

def PyTick():
    global cnt
    if (cnt%10)==0:
        print('in pytick')
        libc.calledfrompython()
        print('in pytick 2')


if __name__=="__main__":
    PyTick()
