# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import numpy as np
import cv2

class optical_flow_track(object):
    def __init__(self):

        # Parameters for lucas kanade optical flow
        self.lk_params = dict( winSize  = (15,15),
                   maxLevel = 2,
                   criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.08))

        # Create some random colors
        self.color = np.random.randint(0,255,(2000,3))
        self.old_gray=None
        self.old_frame=None
        self.p0=self.p1=None

    def feed(self,frame):
        if self.old_gray is None:
            self.old_frame=frame
            self.old_gray=cv2.cvtColor(self.old_frame, cv2.COLOR_BGR2GRAY)
            marg=30
            self.p0 = np.array([(i,j) for i in range(marg,frame.shape[1]-marg,30) for j in range(marg,frame.shape[0]-marg,30)],dtype='float32').reshape(-1,1,2)

        #import ipdb;ipdb.set_trace()
        frame_gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        p1, st, err = cv2.calcOpticalFlowPyrLK(self.old_gray, frame_gray, self.p0, None, **self.lk_params)

        # Select good points
        good_new = p1[st==1]
        good_old = self.p0[st==1]

        # draw the tracks
        for i,(new,old) in enumerate(zip(good_new,good_old)):
             a,b = new.ravel()
             c,d = old.ravel()
             frame = cv2.circle(frame,(a,b),2,self.color[i].tolist(),-1)

        # Now update the previous frame and previous points
        self.old_gray = frame_gray.copy()
        self.p0 = good_new.reshape(-1,1,2)
        return frame 

if __name__=="__main__":
    frame=cv2.imread('/tmp/screenshot.png')
    of=optical_flow_track()
    out=of.feed(frame)
    cv2.imshow('cv window',out)
    cv2.waitKey(0)
        
