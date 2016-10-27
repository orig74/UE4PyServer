# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
from Wrappers import phandlers as ph
import time
import traceback,sys
import os,shutil
import cv2,imp

def main_loop(gworld):
    camera_actor=ph.FindActorByName(gworld,'Sphere_16',1)
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
       
        #this the RGB image 
        img1=cv2.resize(ph.GetTextureImg(),(512,512),cv2.INTER_LINEAR)
        
        #this is the depth image its 8 bit and will be recived in the red channel
        img2=ph.GetTextureImg(1,channels=[2])
        print('tic==',time.time()-start)
        start=time.time()
        cv2.imshow('camera 1',img1)
        cv2.imshow('camera 2',img2)
        
        cv2.waitKey(1)
        cnt+=1


def kill():
    cv2.destroyAllWindows()
    for _ in range(10):
        cv2.waitKey(10)
