import construct_transition_probability_matrix as tpm
import math
import numpy as np
import random
import pandas as pd


which_video="z4" #must stay here
#idd="5" #must stay here


class Fish_Track_Estimator:
    
    def __init__(self,  n, x, alpha, width, height, fish_positions_path, to_store, idf):
        

        self.alpha=alpha
        
        self.direction=""
        
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
        
        self.prev_state=0 #this will change
        
        self.dict_trans_prob_matrix=arg.dict_trans_prob_matrix
        
        self.estimations=[] #this stores the predicted next positions of the fish
        
        self.to_store=to_store
 
        
        
    
    

    def possible_states(self, state):
        
        #finds the possible states that the fish can go given its current position 
        
        possible_states=[st for st in self.dict_trans_prob_matrix[state] if st !=0]
        
        return possible_states
        
        
    
    def find_direction(self, frame):
        
        # this functions finds the previous direction of the fish
        #there are four possible directions: up, down, right, left
        
        #d_y=(-1*self.fish_positions[frame][1])-(-1*self.fish_positions[frame-1][1])
        d_y=self.fish_positions[frame][1]-self.fish_positions[frame-1][1]
        d_x=self.fish_positions[frame][0]-self.fish_positions[frame-1][0]
        
        #print(f"d_x: {self.fish_positions[frame][0]}-{self.fish_positions[frame-1][0]}")
        #print(f"d_y: {self.fish_positions[frame-1][1]}-{self.fish_positions[frame][1]}")
        
        if d_x == 0: #this if-else case written to prevent the division by zero error
            if d_y >=0.0:
                return "down"
            else:
                return "up"
            
        slope_v=d_y/d_x
        
        #print(f"slope: {slope_v}")
        
        angle_v=math.degrees(math.atan(slope_v)) #finding the angle by artan() function
        
        #print(f"angle: {angle_v}")
        
        
        if angle_v<0:
            angle_v= 360.0 + angle_v
        
        if 0.0 <= angle_v and angle_v < 45.0:
            return "left"
        elif 45.0 <= angle_v and angle_v < 135.0:
            return "down"
        elif 135.0 <= angle_v and angle_v < 225.0:
            return "right"
        elif 225.0<= angle_v and angle_v < 315.0:
            return "up"
        elif 315.0<= angle_v and angle_v <= 360.0:
            return "left"
        
        else: # this is unnecessery
            print(f"slope: {slope_v}")
            print(f"angle: {angle_v}")
            raise ValueError("SOMETHING WRONG with the slope!")
            
        
            
    def associated_states(self, state, frame):
        
        #this function gives the associated states given teh direction the fish.
        #for example if the fish goes down. then this function finds the downward states.
        # for more detail visit the report.
            
        direction=self.find_direction(frame)
        possible_states=self.possible_states(state)
        associated_states=[]
        
        #print(f"direction: {direction}")
        
        for st in possible_states:
            
            if direction == "up":
                if st <= state + 1: #state + 1 could exceed the max state number. but no harm. 
                    associated_states +=[st]
            elif direction == "down":
                if st >= state -1:
                    associated_states += [st]
            elif direction == "right":
                if st == state -1-self.width or st == state -1 or st == state -1+self.width:
                    continue
                else:
                    associated_states += [st]
            else: # direction ==  "left"
                if st == state +1-self.width or st == state +1 or st == state +1+self.width:
                    continue                
                else:
                    associated_states += [st]
                    
        return associated_states
    
    
    def alphaf(self, state, frame):
        
        # this function favors the probabilities by alpha. and then normalizes the new probabilies.
        
        new_probs=[]
        associated_states = self.associated_states(state, frame)
        
        #print(f"associated_states: {associated_states}")
        
        state_probs=list(self.dict_trans_prob_matrix[state].values())
        keys=list(self.dict_trans_prob_matrix[state].keys())
        
        #favor the associated states according to the previous direction of the fish by alpha
        
        for st in range(len(keys)):
            if keys[st] in associated_states:
                new_probs += [self.alpha*state_probs[st]]
            else:
                new_probs += [state_probs[st]]
                
        
        # now need to normalize the probs
        
        normalized_probs=[]
        sum_new_probs=sum(new_probs)
        
        for prob in new_probs:
            normalized_probs += [prob/sum_new_probs]
            
            
        return normalized_probs
    
    def alphaf1(self, state, frame, alp):
        
        # this function favors the probabilities by alpha. and then normalizes the new probabilies.
        
        new_probs=[]
        associated_states = self.associated_states(state, frame)
        
        #print(f"associated_states: {associated_states}")
        
        state_probs=list(self.dict_trans_prob_matrix[state].values())
        keys=list(self.dict_trans_prob_matrix[state].keys())
        
        #favor the associated states according to the previous direction of the fish by alpha
        
        for st in range(len(keys)):
            if keys[st] in associated_states:
                new_probs += [alp*state_probs[st]]
            else:
                new_probs += [state_probs[st]]
                
        
        # now need to normalize the probs
        
        normalized_probs=[]
        sum_new_probs=sum(new_probs)
        
        for prob in new_probs:
            normalized_probs += [prob/sum_new_probs]
            
            
        return normalized_probs
    
    
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
            possible_states_probs=self.alphaf(self.prev_state,t)
            
            
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
                #break
            
            #num+=1
            
        
        #accuracy= num_correct/(len(self.fish_positions)-1)
            
        df=pd.DataFrame(columns=["predictions"])
        
        df["predictions"]=predictions
        
        to_write=f"rmse: {r}"
        
        f=open(self.to_store+"results_model1_"+which_video+"_"+"id"+str(idf)+"_x"+str(self.x)+"_"+str(int(self.alpha))+".txt","w")
        f.write(to_write)
        f.close()
        
        df.to_csv(self.to_store+which_video+"_predictions_model1_"+"id"+str(idf)+"_x"+str(self.x)+"_"+str(int(self.alpha))+".csv")
        
        
    def find_best_alpha(self):
        
        r=0 #residual
        predictions=[]
        self.prev_state=self.find_state(self.fish_positions[0])
        
        alpha_values=[2,3,4,5,6,7,8,9,10]
        rmses={2:0, 3:0, 4:0,5:0,6:0,7:0,8:0,9:0,10:0}
        
        
        for a in alpha_values:
            
            r=0 #residual
            predictions=[]
            self.prev_state=self.find_state(self.fish_positions[0])
            
            for t in range(1,len(self.fish_positions)):
            
                possible_states=list(self.dict_trans_prob_matrix[self.prev_state].keys())
                possible_states_probs=self.alphaf1(self.prev_state,t,a)

            
                pred_state=random.choices(possible_states, weights=possible_states_probs,k=1)[0]
            
            
                predictions +=[pred_state] 
            
                r += self.rmse(self.fish_positions[t], self.give_centroids(pred_state))
            
                real_position=self.fish_positions[t]
                self.prev_state=self.find_state(real_position)
                
            rmses[a] += r
            
            
        return rmses
        
    
    
    
#idf=5


x=4
width=676//x
height=664//x

n=(676*664)//(x**2)

alpha=10

path_z4="/Users/canerozer/Desktop/BU/SPRING2024/CS585/final_project/dataset/z4/z4_fish_positions_frame1.csv"
path_z3="/Users/canerozer/Desktop/BU/SPRING2024/CS585/final_project/dataset/z3/z3_fish_positions_frame1.csv"

to_store="/Users/canerozer/Desktop/BU/SPRING2024/CS585/final_project/results/"



#fte=Fish_Track_Estimator(n=n, x=x, width=width,alpha=alpha, height=height, fish_positions_path=path_z4, to_store=to_store, idf=idf)
            
#fte.estimate()            
            
#print(fte.find_best_alpha())


if which_video=="z3":

    for idf in range(1,3):

        fte=Fish_Track_Estimator(n=n, x=x, width=width,alpha=alpha, height=height, fish_positions_path=path_z3, to_store=to_store, idf=idf)
            
        fte.estimate()
        
else:
    
    for idf in range(1,6):
        
        fte=Fish_Track_Estimator(n=n, x=x, width=width,alpha=alpha, height=height, fish_positions_path=path_z4, to_store=to_store, idf=idf)
            
        fte.estimate()
    



        
        
        
        
        
        
    
