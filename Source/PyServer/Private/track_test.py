# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
from Wrappers import phandlers as ph
def main_loop(gworld):
    iter=0
    #print('-------> start main_loop 2')
    while 1:
        #print('-------> main_loop',iter)
        yield
        iter+=1
        if iter%100==0:
            import imp; imp.reload(ph)
            import ipdb;ipdb.set_trace()
            actor=ph.FindActorByName(gworld,'CameraActor_0',1)
            actor1=ph.FindActorByName(gworld,'FirstPersonCharacter',1)
            loc=ph.GetActorLocation(actor1)
            print('-----',loc)
            ph.SetActorLocation(actor,loc)

def kill():
    print('tracker_test killed')
