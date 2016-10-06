# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
from Wrappers import phandlers as ph
def main_loop(gworld):
    iter=0
    #print('-------> start main_loop 2')
    while 1:
        #print('-------> main_loop',iter)
        yield
        iter+=1
        if iter==100:
            #import ipdb;ipdb.set_trace()
            print('got to iter 100')

def kill():
    print('tracker_test killed')
