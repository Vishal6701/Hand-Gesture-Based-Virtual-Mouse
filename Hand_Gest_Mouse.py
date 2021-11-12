'''---------------------Import Packages------------------------'''
import cv2
import time
import pyautogui 
import Hand_Tracking_Module as htm
import math 
import numpy as np
from pynput.mouse import Button , Controller
import imutils
import autopy


''' -------------------ALL Variables Declaration ----------------------------------'''
mouse=Controller()
pyautogui.FAILSAFE=False

Red_Frame=100
smooth=30
Prev_loc_X,Prev_loc_Y=0,0
clocX,clocY=0,0
wScr,hScr=autopy.screen.size()

'''----------------------Camera Setting For Capturing Real Time Motion-------------------------'''

wCam=640
hCam=480
cap=cv2.VideoCapture(0,cv2.CAP_DSHOW)
cap.set(3,wCam)
cap.set(4,hCam)

'''----------------------Variable for Frame Per Second Calculations---------------------------'''


pTime=0
cTime=0





"""-----------------------Create object Of Hand Detection---------------------------------------"""

detector=htm.handDetector(detectionCon=0.6)

'''-----------------------infinite  Loop For Capturing Video and Hand Gesture-------------------------'''

while True:
    success,img=cap.read()
    img=cv2.flip(img,+1)
    img=detector.findHands(img)
    Lmlist,bbox=detector.findPosition(img,draw=False)
    
    
  

    


    
    
     
    if len(Lmlist)!=0:
        
        x1,y1=Lmlist[8][1:]
        x2,y2=Lmlist[12][1:]
        x4,y4=Lmlist[20][1:]

       
        
        

        

        ''' -------------------------Finger_UP Detection------------------------------------'''
        finger=detector.fingerUp()




        


        ''' -------------------------------Pointer Of mouse(index finger) ------------------------------------'''

        if finger[1]==1 and finger[2]==0 :

            cv2.rectangle(img,(Red_Frame,Red_Frame),(wCam-Red_Frame,hCam-Red_Frame),(255,0,255),2)
            x3=np.interp(x1,(Red_Frame,wCam-Red_Frame),(0,wScr))
            y3=np.interp(y1,(Red_Frame,hCam-Red_Frame),(0,hScr))

            clocX=Prev_loc_X + (x3-Prev_loc_X)/smooth
            clocY=Prev_loc_Y + (y3-Prev_loc_Y)/smooth

            
            

            autopy.mouse.move(x3,y3)

            cv2.circle(img,(x1,y1),10,(255,0,255),cv2.FILLED)

            Prev_loc_X,Prev_loc_Y=clocX,clocY

            cv2.rectangle(img,(500,10),(630,70),(255,255,255),2)
            cv2.putText(img,'Pointer',(510,50),cv2.FONT_HERSHEY_COMPLEX,0.7,(255,117,89),3)

                      
          


        '''--------------------Right Click with Up index and middle finger together------------------- '''

        
        if finger[0]==0:

             if finger[1]==1 and finger[2]==1:
                    x2,y2=Lmlist[12][1],Lmlist[12][2]
                    x1,y1=Lmlist[8][1],Lmlist[8][2]
                    
                    cv2.rectangle(img,(Red_Frame,Red_Frame),(wCam-Red_Frame,hCam-Red_Frame),(255,0,255),2)
                    x3=np.interp(x1,(Red_Frame,wCam-Red_Frame),(0,wScr))
                    y3=np.interp(y1,(Red_Frame,hCam-Red_Frame),(0,hScr))

                    clocX=Prev_loc_X + (x3-Prev_loc_X)/smooth
                    clocY=Prev_loc_Y + (y3-Prev_loc_Y)/smooth

                    
                    
                    autopy.mouse.move(x3,y3)

                    cv2.circle(img,(x1,y1),10,(255,0,255),cv2.FILLED)

                    Prev_loc_X,Prev_loc_Y=clocX,clocY




                    
                    cx,cy=(x1+x2)//2 ,(y1+y2)//2
                    cv2.circle(img,(x1,y1),10,(170,255,25),cv2.FILLED)
                    cv2.circle(img,(x2,y2),10,(0,255,255),cv2.FILLED)
                    cv2.line(img,(x1,y1),(x2,y2),(255,255,255),3)
                    cv2.circle(img,(cx,cy),5,(120,0,25),cv2.FILLED)
                    
                    
                    length=math.hypot(x2-x1 , y2-y1)
                    #cv2.putText(img,f"Distance:{str(length)}",(10,120),cv2.FONT_HERSHEY_COMPLEX,1,(255,117,89),2)

                    

                    
                            
                    if length<40:
                        pyautogui.rightClick()
                        cv2.putText(img,f"Right-Click",(10,460),cv2.FONT_HERSHEY_COMPLEX,1,(255,117,89),2)
                    

                       
     
                

                
                    

        '''---------------------------left_Click with thumb at screen--------------------------------''' 

        if finger[0]==1: 
          if finger[1]==1:  
            x2,y2=Lmlist[4][1],Lmlist[4][2]
            x1,y1=Lmlist[8][1],Lmlist[8][2]


            
            cv2.rectangle(img,(Red_Frame,Red_Frame),(wCam-Red_Frame,hCam-Red_Frame),(255,0,255),2)
            x3=np.interp(x1,(Red_Frame,wCam-Red_Frame),(0,wScr))
            y3=np.interp(y1,(Red_Frame,hCam-Red_Frame),(0,hScr))

            clocX=Prev_loc_X + (x3-Prev_loc_X)/smooth
            clocY=Prev_loc_Y + (y3-Prev_loc_Y)/smooth

            

            autopy.mouse.move(x3,y3)

            cv2.circle(img,(x1,y1),10,(255,0,255),cv2.FILLED)

            Prev_loc_X,Prev_loc_Y=clocX,clocY


            
            
            length=math.hypot(x2-x1 , y2-y1)
            cv2.putText(img,f"Left-Click",(10,460),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)
         
            
            
   
                   


            
            if length<140:
                    #cv2.circle(img,(Cx,Cy),7,(0,255,0),cv2.FILLED)
                    pyautogui.leftClick()
                    cv2.putText(img,f"Left-Click",(10,460),cv2.FONT_HERSHEY_COMPLEX,1,(0,0,255),2)


        


        '''---------------------------Scroll on Screen using last finger---------------------------'''
        if finger[0]==1:

                x5,y5=Lmlist[17][1:]
                length=detector.Distance(img,20,17,draw=True)
                #cv2.circle(img,(x5,y5),10,(255,0,255),cv2.FILLED)
                #print(length)

            
                x4,y4=Lmlist[20][1:]
                cv2.circle(img,(x4,y4),7,(255,255,255),cv2.FILLED)
                if length>40:
                    pyautogui.scroll(x1,y1)
                if length<40:
                    pyautogui.scroll(-x1,-y1)

        
        '''--------------------------Zoom Function (1st and 4th finger )----------------------------'''
        if finger[0]==0:

            if finger[1]==1 and finger[4]:
                length=detector.Distance(img,8,20,draw=True)
                #print(length)
                if length<90:
                    zoom=pyautogui.hotkey('ctrl','+')
                    pyautogui.press('zoom',int(1/2),1)

                    
    
                
                

            
                    

            

            

    '''---------------------------Frame rate Per Second ----------------------------------''' 

    cTime=time.time()
    deno=(cTime-pTime)
    if(deno==0): 
        deno=deno+1
    fps=1/deno
    pTime=cTime

    cv2.putText(img,f'FPS {int(fps)}',(10,70),cv2.FONT_HERSHEY_COMPLEX,2,(0,0,255),2)

    '''----------------------------OutPut Screen --------------------------------------------'''
   

    cv2.imshow("output",img)

    if(cv2.waitKey(1)==27):
        break

    '''----------------------------Destroy ALL window After Closing -----------------------------'''

cap.release()
cv2.destroyAllWindows()


