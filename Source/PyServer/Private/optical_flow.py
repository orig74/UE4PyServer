# vim: tabstop=8 expandtab shiftwidth=4 softtabstop=4
import numpy as np
import cv2

class optical_flow_track(object):
    def __init__(self):
    # params for ShiTomasi corner detection
        self.feature_params = dict( maxCorners = 100,
                        qualityLevel = 0.3,
                        minDistance = 7,
                        blockSize = 7 )

        # Parameters for lucas kanade optical flow
        self.lk_params = dict( winSize  = (15,15),
                   maxLevel = 2,
                   criteria = (cv2.TERM_CRITERIA_EPS | cv2.TERM_CRITERIA_COUNT, 10, 0.03))

        # Create some random colors
        self.color = np.random.randint(0,255,(100,3))
        self.old_gray=None
        self.old_frame=None
        self.p0=self.p1=None

    def feed(self,frame):
        if self.old_gray is None:
            self.old_frame=frame
            self.old_gray=cv2.cvtColor(self.old_frame, cv2.COLOR_BGR2GRAY)
            self.p0 = cv2.goodFeaturesToTrack(self.old_gray, mask = None, **feature_params)
            self.mask=np.zeros_like(self.old_frame)

        self.frame_gray = cv2.cvtColor(self.frame, cv2.COLOR_BGR2GRAY)
        p1, st, err = cv2.calcOpticalFlowPyrLK(self.old_gray, self.frame_gray, self.p0, None, **lk_params)

        # Select good points
        good_new = p1[st==1]
        good_old = p0[st==1]

        # draw the tracks
        for i,(new,old) in enumerate(zip(good_new,good_old)):
             a,b = new.ravel()
             c,d = old.ravel()
             mask = cv2.line(mask, (a,b),(c,d), color[i].tolist(), 2)
             ret_frame = cv2.circle(frame,(a,b),5,color[i].tolist(),-1)
        img = cv2.add(ret_frame,self.mask)

        # Now update the previous frame and previous points
        old_gray = frame_gray.copy()
        p0 = good_new.reshape(-1,1,2)

