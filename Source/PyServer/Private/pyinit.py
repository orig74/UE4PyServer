# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
print('pyinit imported')
cnt=0
import os,imp
import Wrappers
from Wrappers import phandlers
import entry_point


main_loop_iter=None

def PyInit(gworld):
    import track_test
    imp.reload(track_test)
    print('In PyInit, gworld=',gworld)
    #phandlers.SetScreenResolution(640,480)

def PyBeginPlay(gworld):
    global main_loop_iter
    print('In PyBeginPlay, gworld=',gworld,type(gworld))
    imp.reload(entry_point)
    if main_loop_iter is not None: #already running!
        entry_point.kill()
    #imp.reload(entry_point.main_module)
    entry_point.reload()
    imp.reload(phandlers)
    #import ipdb;ipdb.set_trace()
    main_loop_iter=entry_point.main_loop(phandlers._StrToPtr(gworld))
    next(main_loop_iter)

def PyEndPlay(gworld):
    global main_loop_iter
    print('In PyEndPlay, gworld=',gworld,type(gworld))
    entry_point.kill()


def PyTick():
    global cnt,main_loop_iter
    if main_loop_iter is not None:
        #if cnt==10:
        #    import pdb;pdb.set_trace()
        try:
            next(main_loop_iter)
        except StopIteration:
            main_loop_iter=None
            print("ending main loop!!")
    #if (cnt%1000)==0:
    #    print('in pytick')
    #    Wrappers.libc.calledfrompython()
    #    print('in pytick 2')
    cnt+=1


if __name__=="__main__":
    PyTick()
