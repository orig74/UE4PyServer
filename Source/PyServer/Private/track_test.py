# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
from Wrappers import phandlers as ph
import time
import traceback,sys
import os,shutil
import cv2,imp
import optical_flow
from optical_flow import optical_flow_track

imp.reload(optical_flow)

cvshow=True

keep_running=True


case_params1={\
'name':'low_wind_low_alt',
'camera_height': 5,
'wind_speed':0.00,
'iterations':2,
'iteration_frame_cnt': 500,
'camera_speed':2,
'frames_in_cycle':400,
}

case_params2=case_params1.copy()
case_params2['name']='high_wind_low_alt'
case_params2['wind_speed']=0.1

case_params3=case_params1.copy()
case_params3['name']='low_wind_high_alt'
case_params3['camera_height']=13

case_params4=case_params2.copy()
case_params4['name']='high_wind_high_alt'
case_params4['camera_height']=13

case_params_list=[case_params1,case_params3,case_params4,case_params2]
#case_params_list=[case_params1]

save_path='/local/tmp/out_ue4'


from queue import Queue
imgq=Queue()

def cv_loop(imgq):
    global keep_running
    save_data_path=None
    of=optical_flow_track()
    if cvshow:
        cv2.destroyAllWindows()
        cv2.waitKey(1)
    img_cnt=0
    while keep_running:
        if imgq.empty():
            yield
            continue
        img=imgq.get()
        if img is None:
            break
        if type(img)==str: #command
            print('got command: ',img)
            if img=='reset':
                save_data_path=None
                of=optical_flow_track()
                img_cnt=0
            if img.startswith('init'):
                save_data_path=img.split(',')[1]
                of=optical_flow_track()
                img_cnt=0
            if img.startswith('save_last'):
                cv2.imwrite(save_data_path+'/last.png',retimg)
                of.save_final_state(save_data_path)
            continue
            #retimg=img
        try:
            retimg=of.feed(img.copy())
        except:
            if img_cnt%50==0:
                print('-'*60)
                traceback.print_exc(file=sys.stdout)
        if save_data_path is not None and img_cnt==0: #write first image to disk
            cv2.imwrite(save_data_path+'/first.png',retimg)
        if cvshow:
            cv2.imshow('opencv window',retimg)
            cv2.waitKey(1)
        img_cnt+=1
    if cvshow:
        cv2.destroyAllWindows()
        for _ in range(10): cv2.waitKey(1)


cv_loop_itr=None
proc=None

def main_loop(gworld):
    global cv_loop_itr,proc
    
    cv_loop_itr=cv_loop(imgq)
    next(cv_loop_itr)

    if save_path is not None:
        if os.path.isdir(save_path):
            shutil.rmtree(save_path)
        os.makedirs(save_path)
    camera_actor=ph.FindActorByName(gworld,'CameraActor_2',1) 
    if camera_actor is None:
        print('could not find CameraActor_2 yeilding forever')
        while 1:
            yield
    tick_actor=ph.FindActorByName(gworld,'PyServerTickActor_0')
    wind_actor=ph.FindActorByName(gworld,'WindDirectionalSource1') 
    for case_params in case_params_list:
        if save_path is not None:
            case_path=save_path+'/'+case_params['name']
            os.mkdir(case_path)
        for interation_num in range(case_params['iterations']): 
            camera_initial_location=(-370-1000,-2920,case_params['camera_height']*100) #centimeters
            ph.SetActorLocation(camera_actor,camera_initial_location)
            ph.SetActorRotation(camera_actor,(-0,-180,-0))
            ph.SetWindParams(wind_actor,case_params['wind_speed'])
            
            #move wind actor otherwize change wind speed doesn't work (https://answers.unrealengine.com/questions/35478/possible-to-change-wind-strength-in-level-blueprin.html)    
            loc=ph.GetActorLocation(wind_actor)
            ph.SetActorLocation(wind_actor,(loc[0],loc[1],loc[2]+1000))
            
            ph.MoveToCameraActor(tick_actor,camera_actor)
            
            if save_path is not None:
                iter_path=case_path+'/%d'%interation_num
                os.mkdir(iter_path)
                imgq.put('init,'+iter_path)
            else:
                imgq.put('reset')
        

            for _ in range(300): #adjustment frames...
                yield
            for cnt in range(case_params['iteration_frame_cnt']):
                yield
                tic=time.time()
                speed=case_params['camera_speed']
                cycle=case_params['frames_in_cycle']
                img=ph.TakeScreenshot() 
                #img=cv2.resize(img,(640,480))
                if cnt>=cycle:
                    direction=0
                elif (cnt%cycle) >= cycle/2:
                    direction=-1
                else:
                    direction=1
                loc=ph.GetActorLocation(camera_actor)
                ph.SetActorLocation(camera_actor,(direction*speed+loc[0],direction*speed+loc[1],loc[2]))
                if img is None:
                    print('got None im')
                else:
                    imgq.put(img)
                    next(cv_loop_itr)
                print('case:',case_params['name'],'iter=',interation_num,r'cnt=',cnt,direction,img.shape,imgq.qsize(),(time.time()-tic)*100,'ms')
            if save_path is not None:
                print('---saving last----')
                imgq.put('save_last')
                next(cv_loop_itr)


    print('Done experiment!')
    while 1:
        yield

def kill():
    global keep_running
    keep_running=False
    try:
        for _ in range(1000):
            next(cv_loop_itr) 
    except StopIteration:
        pass
