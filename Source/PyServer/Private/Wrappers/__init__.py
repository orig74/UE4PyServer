# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import os
import ctypes
pluginpath=os.path.abspath(os.path.dirname(__file__)+'/../../../../')
libfile=pluginpath+'/Binaries/Linux/libUE4Editor-PyServer.so'
libc=ctypes.CDLL(libfile)
libc.calledfrompython.argtypes=[]
libc.calledfrompython.restype=c_int
