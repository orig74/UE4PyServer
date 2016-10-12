# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
from Wrappers import phandlers as ph
import time
import cv2,imp
import optical_flow
from optical_flow import optical_flow_track

imp.reload(optical_flow)

cvshow=True

keep_running=True

threaded=True
if threaded:
    import multiprocessing as mp
    imgq=mp.Queue()
else:    
    from queue import Queue
    imgq=Queue()

def cv_loop(imgq):
    global keep_running
    of=optical_flow_track()
    if cvshow:
        cv2.destroyAllWindows()
        cv2.waitKey(1)
    while keep_running:
        if imgq.empty():
            yield
            continue
        img=imgq.get()
        if img is None:
            break
        
        #retimg=img
        retimg=of.feed(img)
        if cvshow:
            cv2.imshow('opencv window',retimg)
            cv2.waitKey(1)
    if cvshow:
        cv2.destroyAllWindows()
        for _ in range(10): cv2.waitKey(1)

if threaded:
    def proc_fun(imgq):
        cv_loop_itr=cv_loop(imgq)
        while 1:
            try:
                next(cv_loop_itr)
            except StopIteration:
                break
            time.sleep(0)  


cv_loop_itr=None
proc=None

def main_loop(gworld):
    global cv_loop_itr,proc
    if not threaded:
        cv_loop_itr=cv_loop(imgq)
        next(cv_loop_itr)
    else:
        print('starting new thread')
        #ret=_thread.start_new_thread(cv_loop,())
        #cv_loop_thread(imgq).start()
        proc=mp.Process(target=proc_fun,args=(imgq,))
        proc.start()
        print('after starting new thread')

 
    cnt=0
    print('-------> start main_loop 2')
    #cv2.destroyAllWindows()
    camera_actor=ph.FindActorByName(gworld,'CameraActor_2',1) 
    if camera_actor is None:
        print('could not find CameraActor_2 yeilding forever')
        while 1:
            yield
    tick_actor=ph.FindActorByName(gworld,'PyServerTickActor_0',1)
    camera_initial_location=(-370-1000,-2920,510+300)
    ph.SetActorLocation(camera_actor,camera_initial_location)
    ph.SetActorRotation(camera_actor,(-0,-180,-0))
    yield
    ph.MoveToCameraActor(tick_actor,camera_actor)
    #ph.SetScreenResolution(640,480)

    for _ in range(100): #adjustment frames...
        yield
 
    while 1:
        #print('-------> main_loop',cnt)
        tic=time.time()
        yield
        speed=2.0
        cycle=400
        #ph.GetCvScreenshot()
        #img=cv2.resize(ph.GetCvScreenshot2(gworld),(640,480))
        img=ph.TakeScreenshot() 
        #img=None
        #continue
        #if cnt==0:
        #    import ipdb;ipdb.set_trace()
        #img=cv2.resize(img,(640,480))
        #img=cv2.resize(ph.GetCvScreenshot(),(640,480))
        #img=None#img=ph.GetCvScreenshot()
        if cnt>cycle:
            direction=0
        elif (cnt%cycle) > cycle/2:
            direction=-1
        else:
            direction=1
            
        #import ipdb;ipdb.set_trace()
        loc=ph.GetActorLocation(camera_actor)
        ph.SetActorLocation(camera_actor,(direction*speed+loc[0],direction*speed+loc[1],loc[2]))
        if img is None:
            print('got None im')
        else:
            imgq.put(img)
            if not threaded:
                next(cv_loop_itr)
        print('cnt=',cnt,direction,img.shape,imgq.qsize())
            #if cnt<6:
            #    import pdb;pdb.set_trace()
        cnt+=1

def kill():
    global keep_running
    keep_running=False
    if not threaded:
        try:
            for _ in range(1000):
                next(cv_loop_itr) 
        except StopIteration:
            pass
    else:
        imgq.put(None)
        print('---sending None')
        for _ in range(10):
            if imgq.qsize()==0:
                break
            time.sleep(1)
        time.sleep(1) 
        #proc.join()
        print('---Done kill')
