import cv2 as cv
import math
import pandas as pd
import ast



def give_centroids(state):
    
        
        
    #((math.floor(state/self.width))*self.x, state-(math.floor(state/self.width)*self.width))
        
    up_c0=(math.floor(state/width))*x
        
    up_c1=(state*x) - (up_c0*width)

    
    return (up_c0 + (x // 2), up_c1 + (x //2))


video_file3='/Users/canerozer/Desktop/BU/SPRING2024/CS585/final_project/dataset/z3/z3_cropped.mp4'
to_store3='/Users/canerozer/Desktop/BU/SPRING2024/CS585/final_project/dataset/z3/'
pred_path="/Users/canerozer/Desktop/BUDUR.csv"
real_path='/Users/canerozer/Desktop/BU/SPRING2024/CS585/final_project/dataset/z3/z3_fish_positions_frame2.csv'


idf=1

x=4
width=169
height=166

which="z3"


cap = cv.VideoCapture(video_file3)

vidwrite = cv.VideoWriter(to_store3 + which+'_pred.mp4', cv.VideoWriter_fourcc(*'MP4V'), 30, (664, 676))

state_predictions=[]

dff = pd.read_csv(pred_path)
fish_positions_=list(dff['predictions'].values)


fish_positions= [give_centroids(int(state)) for state in fish_positions_]


dfff = pd.read_csv(real_path)
real_positions=list(dfff['id'+str(idf)].values)

real_positions = [ast.literal_eval(string) for string in real_positions]




num=1
check=1

stop=0

while True:
    
    ret, image = cap.read()
    
    #if stop==20:
        #break
    
    #stop +=1
    
    if ret == False:
        break
    
    check+=1
    
    if check % 2==0:
        continue
    
    image = cv.resize(image, (664, 676))

    
    #cv.line(image, (first_point[0],first_point[1]), (last_point[0],last_point[1]), (255,0,0),2)
    
    #for x in range(count+1):
    pos_x,pos_y = fish_positions[num] 
    
    #pos_x,pos_y = real_positions[num] !!!
    
    #print(fish_positions[num])
    
    if pos_x>=664 or pos_y>=676:
        print(f"OVERFLOW: {(pos_x,pos_y)}")
    
    #image = cv.circle(image, (int(pos_x),int(pos_y)), 1, (0,0,255), 2)
    
    for yaxis in range(height):
        
    
        image= cv.line(image, (0, yaxis*x), (width*x, yaxis*x), (255, 0, 0), 1)
        
    for xaxis in range(width):
        
    
        image= cv.line(image, (xaxis*x, 0), (xaxis*x, height*x), (255, 0, 0), 1)
    
    
        
        #image= cv.line(image, (xaxis, 0), (image.shape[1], 100), (255, 0, 0), 1)
        
        
    vidwrite.write(image)
        
    break

    
    #image = cv.circle(image, (int(pos_x),int(pos_y)), 1, (0,0,255), 2) !!!
        
    vidwrite.write(image)
    num +=1
    #count+=1   
    if num>=len(fish_positions):
        break

vidwrite.release()








