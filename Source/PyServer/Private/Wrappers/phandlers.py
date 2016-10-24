# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
from Wrappers import libc
from ctypes import *
import cv2

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

libc.GetActorRotation.argtypes=[c_void_p,float3type_p]
def GetActorRotation(actor):
    vec=float3type()
    libc.GetActorRotation(actor,pointer(vec))
    return tuple(vec)

libc.SetActorRotation.argtypes=[c_void_p,float3type_p]
def SetActorRotation(actor,invec):
    vec=float3type(*invec)
    libc.SetActorRotation(actor,vec)


libc.MoveToCameraActor.argtypes=[c_void_p,c_void_p,c_int]
def MoveToCameraActor(actor,camera,index=0):
    libc.MoveToCameraActor(actor,camera,index)

int2type=c_int*2
libc.GetViewPortSize.argtypes=[POINTER(int2type)]
libc.TakeScreenshot.argtypes=[c_void_p,c_int]
import cv2
import numpy as np
tmp_capture_mem=np.array([1],dtype='uint8')
 
def TakeScreenshot():
        global tmp_capture_mem
        sz=int2type()
        libc.GetViewPortSize(pointer(sz))
        req_mem_sz=sz[0]*sz[1]*4# (RGBA)
        if len(tmp_capture_mem)<req_mem_sz:
            #tmp_capture_mem=b'\0'*req_mem_sz
            tmp_capture_mem=np.zeros(req_mem_sz,'uint8')
        ptr=tmp_capture_mem.ctypes.data_as(c_void_p)
        lsize=libc.TakeScreenshot(ptr,len(tmp_capture_mem))
        return tmp_capture_mem.reshape((sz[1],sz[0],4))[:,:,:3] 

libc.SetWindParams.argtypes=[c_void_p,c_float,c_float]

#BUG!! does not work 
def SetWindParams(awind,speed): 
    libc.SetWindParams(awind,speed,speed)

libc.DeactivateActorComponent.argtypes=[c_void_p]
def DeactivateActor(actor):
    libc.DeactivateActorComponent(actor)


libc.ActivateActorComponent.argtypes=[c_void_p,c_bool]
def ActivateActor(actor):
    libc.ActivateActorComponent(actor,False)


libc.GetTextureSize.argtypes=[POINTER(int2type),c_int,c_bool]
libc.GetTexture.argtypes=[c_void_p,c_int,c_int,c_bool]
def GetTextureImg(txt_index=0,verbose=0):
        global tmp_capture_mem
        sz=int2type()
        ret=libc.GetTextureSize(pointer(sz),txt_index,verbose)
        req_mem_sz=sz[0]*sz[1]*4# (RGBA)
        
        if len(tmp_capture_mem)<req_mem_sz:
            tmp_capture_mem=np.zeros(req_mem_sz,'uint8')
        ptr=tmp_capture_mem.ctypes.data_as(c_void_p)
        libc.GetTexture(ptr,req_mem_sz,txt_index,0)
        return tmp_capture_mem.reshape((sz[1],sz[0],4))[:,:,:3] 




