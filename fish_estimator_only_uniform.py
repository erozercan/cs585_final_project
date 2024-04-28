import construct_transition_probability_matrix as tpm
import math
import random
import numpy as np
import pandas as pd


which_video="z4" #must stay here
#idd="1" #must stay here


class Fish_Track_Estimator:
    
    def __init__(self,  n, x, width, height, fish_positions_path, to_store, idf):
        
        self.n=n
        self.x=x
        self.r=0 #this is residual 
        
        self.idf=idf
        
        self.states=list(range(n))
        
        self.width=width
        self.height=height
        
        
        arg=tpm.construct_matrix(n, x, width, height, fish_positions_path, idf)
        
        arg.fill_adjacent_matrix()
        arg.fill_trans_prob_matrix()
        
        arg.fill_dict_x_y_ranges()
        #arg.fill_ground_truth()
        arg.give_fish_positions()
        
        self.fish_positions=arg.fish_positions #ground truth positions of the fish
        
        #self.ground_truth_states= arg.ground_truth
        
        self.prev_state=0
        
        self.dict_trans_prob_matrix=arg.dict_trans_prob_matrix
        
        self.estimations=[] #this stores the predicted next positions of the fish
        
        self.to_store=to_store
        


    def give_centroids(self, state):
        
        
        #((math.floor(state/self.width))*self.x, state-(math.floor(state/self.width)*self.width))
        
        up_c0=(math.floor(state/self.width))*self.x
        
        up_c1=(state*self.x) - (up_c0*self.width)
        
        
        
        return (up_c0 + (self.x // 2), up_c1 + (self.x //2))
        
        
    
    
    def rmse(self, point1, point2):
       
        
        point1 = np.array(point1)
        point2 = np.array(point2)
    
        # Calculate squared differences
        squared_diff = (point1 - point2) ** 2
    
        # Calculate mean squared error
        mse = np.mean(squared_diff)
    
        # Calculate RMSE
        rmse = np.sqrt(mse)
    
        return rmse
    
    
    def find_state(self,point):
        
        if point[0]%self.x==0 and point[1]%self.x==0:
            
            
            new_point=point
            
            
        
        elif point[0]%self.x!=0 and point[1]%self.x==0:
            
            new_x=point[0]
            
            while new_x%self.x!=0:
                
                new_x -=1
                
            new_point=(new_x,point[1])
            
            
                
        
        elif point[0]%self.x==0 and point[1]%self.x!=0:
            
            new_y=point[1]
            
            while new_y%self.x!=0:
                
                new_y -=1
                
                
            new_point=(point[0],new_y)
                
            
            
        else:
            
            new_x=point[0]
            new_y=point[1]
            
            while new_x%self.x!=0:
                
                new_x -=1
  
            while new_y%self.x!=0:
                
                new_y -=1
                
            
            new_point=(new_x,new_y)
            
            
        if new_point[0]==self.x*self.height:
            
            
            new_point=(new_point[0]-self.x, new_point[1])
            
        if new_point[1]==self.x*self.width:
            
            new_point=(new_point[0],new_point[1]-self.x)
            
        
        #return ((new_point[0]*self.width) + new_point[1])//self.x
        return (new_point[0]//self.x)*self.width + (new_point[1]//self.x)
    
    
    

    def estimate(self):
        
        r=0 #residual
        predictions=[]
        #num_correct=0 #number of correct predictions
        self.prev_state=self.find_state(self.fish_positions[0])
        
        #num =1
        
        
        for t in range(1,len(self.fish_positions)):
            
            possible_states=list(self.dict_trans_prob_matrix[self.prev_state].keys())
            possible_states_probs=list(self.dict_trans_prob_matrix[self.prev_state].values())
            
            #print(f"{num})")
            #print(f"t:{t},")
            
            
            
            #print(f"fish_position:{self.fish_positions[t-1]},")
            #print(self.prev_state)
            #print(possible_states)
            #print(possible_states_probs)
            
            
            
            pred_state=random.choices(possible_states, weights=possible_states_probs,k=1)[0]
            
            #print(f"pred:{pred_state}")
            
            predictions +=[pred_state] 
            
            
            r += self.rmse(self.fish_positions[t], self.give_centroids(pred_state))
            
            #print(f"pred centroid:{self.give_centroids(pred_state)}")
            
            #if pred_state==self.ground_truth_states[t]:
                
                #num_correct +=1
            
            #self.prev_state=self.ground_truth_states[t]
            real_position=self.fish_positions[t]
            self.prev_state=self.find_state(real_position)
            
            #if num==10:
            #    break
            
            #num+=1
            
        
        #accuracy= num_correct/(len(self.fish_positions)-1)
            
        df=pd.DataFrame(columns=["predictions"])
        
        df["predictions"]=predictions
        
        to_write=f"rmse: {r}"
        
        f=open(self.to_store+"results_"+which_video+"_"+"id"+str(idf)+"_x"+str(self.x)+".txt","w")
        f.write(to_write)
        f.close()
        
        df.to_csv(self.to_store+which_video+"_predictions_model0_"+"id"+str(idf)+"_x"+str(self.x)+".csv")
                
        

#idf=1
        

#(h:664, w:676)

x=4
width=676//x
height=664//x

n=(676*664)//(x**2)

path_z4="/Users/canerozer/Desktop/BU/SPRING2024/CS585/final_project/dataset/z4/z4_fish_positions_frame1.csv"
path_z3="/Users/canerozer/Desktop/BU/SPRING2024/CS585/final_project/dataset/z3/z3_fish_positions_frame1.csv"

to_store="/Users/canerozer/Desktop/BU/SPRING2024/CS585/final_project/results/"

if which_video=="z3":

    for idf in range(1,3):

        fte=Fish_Track_Estimator(n=n, x=x, width=width, height=height, fish_positions_path=path_z3, to_store=to_store, idf=idf)
            
        fte.estimate()
        
else:
    
    for idf in range(1,6):
        
        fte=Fish_Track_Estimator(n=n, x=x, width=width, height=height, fish_positions_path=path_z4, to_store=to_store, idf=idf)
            
        fte.estimate()
    
            


        




