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
        if img=='reset':
            of=optical_flow_track()
            continue
        
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

save_data=True

case_params1={\
'name':'nowind_low',
'camera_height': 5,
'wind_speed':0.00,
'iterations':2,
'iteration_frame_cnt': 500,
'camera_speed':2,
'frames_in_cycle':400,
}

case_params2=case_params1.copy()
case_params2['name']='wind_low'
case_params2['wind_speed']=0.1

case_params3=case_params1.copy()
case_params3['name']='nowind_heigh'
case_params3['camera_height']=13

case_params4=case_params2.copy()
case_params4['name']='wind_heigh'
case_params4['camera_height']=13

case_params_list=[case_params1,case_params2,case_params3,case_params4]

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

    

 
    print('-------> start main_loop 2')
    #cv2.destroyAllWindows()
    camera_actor=ph.FindActorByName(gworld,'CameraActor_2',1) 
    if camera_actor is None:
        print('could not find CameraActor_2 yeilding forever')
        while 1:
            yield
    tick_actor=ph.FindActorByName(gworld,'PyServerTickActor_0')
    wind_actor=ph.FindActorByName(gworld,'WindDirectionalSource1') 
    for case_params in case_params_list:
        for interation_num in range(case_params['iterations']): 
            camera_initial_location=(-370-1000,-2920,case_params['camera_height']*100) #centimeters
            ph.SetActorLocation(camera_actor,camera_initial_location)
            ph.SetActorRotation(camera_actor,(-0,-180,-0))
            
            #if 1:
            #    ph.ActivateActor(wind_actor)
            #else:
            #    ph.DeactivateActor(wind_actor)
            ph.SetWindParams(wind_actor,case_params['wind_speed'])
            
            #move wind actor otherwize change wind speed doesn't work (https://answers.unrealengine.com/questions/35478/possible-to-change-wind-strength-in-level-blueprin.html)    
            loc=ph.GetActorLocation(wind_actor)
            ph.SetActorLocation(wind_actor,(loc[0],loc[1],loc[2]+1000))
            
            ph.MoveToCameraActor(tick_actor,camera_actor)
            
            imgq.put('reset')
            #ph.SetScreenResolution(640,480)

            for _ in range(100): #adjustment frames...
                yield
            for cnt in range(case_params['iteration_frame_cnt']):
                tic=time.time()
                yield
                speed=case_params['camera_speed']
                cycle=case_params['frames_in_cycle']
                img=ph.TakeScreenshot() 
                #img=cv2.resize(img,(640,480))
                if cnt>cycle:
                    direction=0
                elif (cnt%cycle) > cycle/2:
                    direction=-1
                else:
                    direction=1
                loc=ph.GetActorLocation(camera_actor)
                ph.SetActorLocation(camera_actor,(direction*speed+loc[0],direction*speed+loc[1],loc[2]))
                if img is None:
                    print('got None im')
                else:
                    imgq.put(img)
                    if not threaded:
                        next(cv_loop_itr)
                print('case:',case_params['name'],'iter=',interation_num,r'cnt=',cnt,direction,img.shape,imgq.qsize())

    print('Done experiment!')
    while 1:
        yield

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
