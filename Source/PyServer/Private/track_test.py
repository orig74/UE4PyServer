# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
from Wrappers import phandlers as ph
import cv2
print('---- track_test imported ----')
print('---- destroy cv windows ----')
cv2.destroyAllWindows()
#cv2.namedWindow('opencv window', cv2.WINDOW_NORMAL)
cv2.waitKey(1)

def main_loop(gworld):
    iter=0
    print('-------> start main_loop 2')
    #cv2.destroyAllWindows()
    while 1:
        #print('-------> main_loop',iter)
        yield
        iter+=1
        if iter==100:
            import imp; imp.reload(ph)
            #import ipdb;ipdb.set_trace()
            aname='PlayerController_0'
            tick_actor=ph.FindActorByName(gworld,'PyServerTickActor_0',1)
            camera_actor=ph.FindActorByName(gworld,'CameraActor_1')
            print('------',tick_actor,camera_actor)
            ph.MoveToCameraActor(tick_actor,camera_actor)
            #aname='CameraActor_0'
            #aname='CameraActor_0'
            #actor=ph.FindActorByName(gworld,aname,1)
            #actor1=ph.FindActorByName(gworld,'FirstPersonCharacter',1)
            #loc=ph.GetActorLocation(cameraactor)
            #print('-----',loc)
            #ph.SetActorLocation(actor,((iter/100)*10,0,0))

        if iter>100 and (iter%1)==0:
            #import ipdb;ipdb.set_trace()
            camera_actor=ph.FindActorByName(gworld,'CameraActor_1')
            loc=ph.GetActorLocation(camera_actor)
            ph.SetActorLocation(camera_actor,(((iter/100)%20)*1+loc[0],loc[1],loc[2]))
            img=ph.GetCvScreenshot()
            if img is None:
                print('got None im')
            else:
                print('got img',img.shape)
                cv2.imshow('opencv window',img)
                cv2.waitKey(1)

def kill():
    print('tracker_test killed')
