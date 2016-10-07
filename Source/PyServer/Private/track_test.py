# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
from Wrappers import phandlers as ph
import cv2,imp
import optical_flow
from optical_flow import optical_flow_track
imp.reload(optical_flow)

print('---- track_test imported ----')
print('---- destroy cv windows ----')
cv2.destroyAllWindows()
#cv2.namedWindow('opencv window', cv2.WINDOW_NORMAL)
cv2.waitKey(1)

def main_loop(gworld):
    iter=0
    print('-------> start main_loop 2')
    of=optical_flow_track()
    #cv2.destroyAllWindows()
    camera_actor=ph.FindActorByName(gworld,'CameraActor_2',1) 
    if camera_actor is None:
        print('could not find CameraActor_2 yeilding forever')
        while 1:
            yield
    tick_actor=ph.FindActorByName(gworld,'PyServerTickActor_0',1)
    ph.MoveToCameraActor(tick_actor,camera_actor)
    while 1:
        #print('-------> main_loop',iter)
        yield
        iter+=1
            #aname='CameraActor_0'
            #aname='CameraActor_0'
            #actor=ph.FindActorByName(gworld,aname,1)
            #actor1=ph.FindActorByName(gworld,'FirstPersonCharacter',1)
            #loc=ph.GetActorLocation(cameraactor)
            #print('-----',loc)
            #ph.SetActorLocation(actor,((iter/100)*10,0,0))

        img=cv2.resize(ph.GetCvScreenshot(),(640,480))
        if iter>10 and (iter%1)==0:
            #import ipdb;ipdb.set_trace()
            loc=ph.GetActorLocation(camera_actor)
            ph.SetActorLocation(camera_actor,(((iter/100)%20)*1+loc[0],loc[1],loc[2]))
            if img is None:
                print('got None im')
            else:
                print('got img',img.shape)
                #import pdb;pdb.set_trace()
                retimg=of.feed(img)
                cv2.imshow('opencv window',retimg)
                cv2.waitKey(1)

def kill():
    print('tracker_test killed')
