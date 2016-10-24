# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
from Wrappers import phandlers as ph
import time
import traceback,sys
import os,shutil
import cv2,imp

def main_loop(gworld):
    #render_target=ph.GetRenderTarget()
    camera_actor=ph.FindActorByName(gworld,'SceneCapture2D1',1)
    #camera_actor=ph.FindActorByName(gworld,'Sphere_2',1)
    print('---------',camera_actor) 
    if camera_actor is None:
        print('Error cannot find actor yeilding forever')
        while 1:
            yield
    start=time.time()
    loc=ph.GetActorLocation(camera_actor)
    cnt=0
    while 1:
        yield
        ph.SetActorLocation(camera_actor,(loc[0],loc[1]+1*cnt,loc[2]))
        
        img1=ph.GetTextureImg()
        print('tic!=',time.time()-start)
        cv2.imshow('camera 1',img1)
        cv2.waitKey(1)
        cnt+=1


def _main_loop(gworld):
    camera_actor1=ph.FindActorByName(gworld,'CameraActor_2',1) 
    camera_actor2=ph.FindActorByName(gworld,'CameraActor_3',1) 
    tick_actor=ph.FindActorByName(gworld,'PyServerTickActor_0')
    if camera_actor1 is None or camera_actor2 is None:
        print('could not find CameraActor_2 or CameraActor_3 yeilding forever')
        while 1:
            yield
    while 1:
        ph.MoveToCameraActor(tick_actor,camera_actor1,0)
        yield
        img1=ph.TakeScreenshot() 
        cv2.imshow('camera 1',img1)
        cv2.waitKey(1)
        ph.MoveToCameraActor(tick_actor,camera_actor2,1)
        yield
        img2=ph.TakeScreenshot() 
        cv2.imshow('camera 2',img2)
        cv2.waitKey(1)


def kill():
    cv2.destroyAllWindows()
    for _ in range(10):
        cv2.waitKey(10)
