import cv2 as cv
import numpy as np
import pandas as pd
import ast


class KalmanFilter:
    def __init__(self):
        self.kf = cv.KalmanFilter(4, 2)
        self.kf.measurementMatrix = np.array([[1, 0, 0, 0], [0, 1, 0, 0]], np.float32)
        self.kf.transitionMatrix = np.array([[1, 0, 1, 0], [0, 1, 0, 1], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32)
        
        self.kf.processNoiseCov = np.array([[1, 0, 0, 0], [0, 1, 0, 0], [0, 0, 1, 0], [0, 0, 0, 1]], np.float32) 
        self.kf.measurementNoiseCov = np.array([[1, 0], [0, 1]], np.float32) * 0.1 #COULD BE SMALLER LIKE 0.01
        
        #Setting initial state estimate closer to the true initial state
        self.kf.statePre = np.array([[0], [0], [0], [0]], np.float32)

    def predict(self, cx, cy):
        measured = np.array([[np.float32(cx)], [np.float32(cy)]])
        self.kf.predict()
        estimated = self.kf.correct(measured)
        x, y = int(estimated[0]), int(estimated[1])
        return x, y
    
    

def rmse(point1, point2):
       
        
       point1 = np.array(point1)
       point2 = np.array(point2)
    
       # Calculate squared differences
       squared_diff = (point1 - point2) ** 2
    
       # Calculate mean squared error
       mse = np.mean(squared_diff)
    
       # Calculate RMSE
       rmse = np.sqrt(mse)
    
       return rmse
   
    
   
def give_fish_positions(path, idf):
        
    dff = pd.read_csv(path)
    fish_positions_=list(dff['id'+str(idf)].values)
        
    return [ast.literal_eval(string) for string in fish_positions_]
    
   

kf= KalmanFilter()

path3="/Users/canerozer/Desktop/BU/SPRING2024/CS585/final_project/dataset/z3/z3_fish_positions_frame1.csv"
path4="/Users/canerozer/Desktop/BU/SPRING2024/CS585/final_project/dataset/z4/z4_fish_positions_frame1.csv"


to_store="/Users/canerozer/Desktop/BU/SPRING2024/CS585/final_project/results/"
idf=5
predictions=[]
r=0
which_video="z4"

path=path4


fish_positions=give_fish_positions(path, idf)

prev_point=fish_positions[0]



for t in range(1,len(fish_positions)):
    
    predicted=kf.predict(prev_point[0], prev_point[1])
    
    predictions +=[predicted]
    
    r +=rmse(prev_point, predicted)
    
    prev_point=fish_positions[t]
    
    
    
df=pd.DataFrame(columns=["predictions"])

df["predictions"]=predictions

df.to_csv(to_store+which_video+"_kalman_"+"id"+str(idf)+".csv")

to_write=f"rmse: {r}"
        
f=open(to_store+"results_"+which_video+"_"+"id"+str(idf)+".txt","w")
f.write(to_write)
f.close()
        


    
    
    
    
    
    
    
    
    
    







