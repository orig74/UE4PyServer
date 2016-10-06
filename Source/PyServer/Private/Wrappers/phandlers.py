# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
from Wrappers import libc
from ctypes import *

libc.StrToPtr.argtypes=[c_char_p]
libc.StrToPtr.restype=c_void_p
def _StrToPtr(worldstr):
    worldbytes=worldstr.encode('utf-8')
    cptr=c_char_p(worldbytes)
    voidptr=libc.StrToPtr(cptr)
    return voidptr

libc.GetCurrentLevel.argtypes=[c_void_p]
libc.GetCurrentLevel.restype=c_void_p
def GetCurrentLevel(uworld):
    return libc.GetCurrentLevel(uworld)

libc.GetNumberOfLevelBluePrints.argtypes=[c_void_p]
libc.GetNumberOfLevelBluePrints.restype=c_int
def GetNumberOfLevelBluePrints(ulevel):
    return libc.GetNumberOfLevelBluePrints(ulevel)

libc.GetActorCount.argtypes=[c_void_p]
libc.GetActorCount.restype=c_int
def GetActorCount(uworld):
    return libc.GetActorCount(uworld)

libc.FindActorByName.argtypes=[c_void_p,c_char_p,c_int]
libc.FindActorByName.restype=c_void_p
def FindActorByName(uworld,name,verbose=0):
    namebytes=name.encode('utf-8')
    return libc.FindActorByName(uworld,namebytes,verbose)

float3type=c_float*3
float3type_p=POINTER(float3type)
libc.GetActorLocation.argtypes=[c_void_p,float3type_p]
def GetActorLocation(actor):
    vec=float3type()
    libc.GetActorLocation(actor,pointer(vec))
    return tuple(vec)

libc.SetActorLocation.argtypes=[c_void_p,float3type_p]
def SetActorLocation(actor,invec):
    vec=float3type(*invec)
    libc.SetActorLocation(actor,vec)


    
