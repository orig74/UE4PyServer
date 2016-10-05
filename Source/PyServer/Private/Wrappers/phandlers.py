# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
from Wrappers import libc
from ctypes import *
libc.StrToPtr.argtypes=[c_wchar_p]
libc.StrToPtr.restype=c_void_p
def _StrToPtr(worldstr):
    ret=c_wchar_p(worldstr)
    ret=libc.StrToPtr(ret)
    return ret

libc.GetCurrentLevel.argtypes=[c_void_p]
libc.GetCurrentLevel.restype=c_void_p
def GetCurrentLevel(uworld):
    return libc.GetCurrentLevel(uworld)

libc.GetNumberOfLevelBluePrints.argtypes=[c_void_p]
libc.GetNumberOfLevelBluePrints.restype=c_int
def GetNumberOfLevelBluePrints(ulevel):
    return libc.GetNumberOfLevelBluePrints(ulevel)

