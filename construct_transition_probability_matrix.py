import math 
import pandas as pd
from tqdm import tqdm
from os.path import exists
import json
import ast


#THIS FILE CONSTRUCTS THE TRANSITION PROBABILITY MATRIX

#determine the n, x before here. formula n*x^2=area

# determine width, height

#determine fish_positions


#delta_distance=4 ## CHANGE THIS PLACE

#OPEN UP THE fish_positions. make it a list. 

#fish_positions=[....]
#path_z4="/Users/canerozer/Desktop/BU/SPRING2024/CS585/final_project/dataset/z4/z4_fish_positions_frame2.csv"

#df = pd.read_csv(path_z4)

#fish_positions_z4_id1=list(df['id1'].values)
#fish_positions_z4_id2=list(df['id2'].values)
#fish_positions_z4_id3=list(df['id3'].values)
#fish_positions_z4_id4=list(df['id4'].values)
#fish_positions_z4_id5=list(df['id5'].values)

#n=28054
#x=4
#width=166
#height=169


class construct_matrix:
    
    def __init__(self, n,x, width, height, fish_positions_path, idf):
        
        self.n=n #number of total states
        self.x=x #width and height of the area of a state.
        self.width=width #the number of states in the width 
        self.height=height #the number of states in the height
        self.idf=idf
        
        self.fish_positions_path=fish_positions_path
        
        self.fish_positions=[] #(x.y) coordinates of the fish. is a list
        
        self.dict_adjacent_matrix={key:[] for key in range(n)} #gives the neighbors of each state
        
        self.dict_trans_prob_matrix={key:dict() for key in range(n)} #the transition probability matrix
        
        self.dict_x_y_ranges={state:[] for state in range(n)} # gives the range
        #of the corresponding area of a state
        
        #self.ground_truth=[] #takes an arbitrary (x,y) and gives the corresponding state
        
    
        
    
    def give_fish_positions(self):
        
        dff = pd.read_csv(self.fish_positions_path)
        fish_positions_=list(dff['id'+str(self.idf)].values)
        
        self.fish_positions= [ast.literal_eval(string) for string in fish_positions_]
        
    
    
    def corner_border_middle(self):
        
        #this function categorizes each state according to its position in the image frame
       
        #There are four corner states in the image. upper-left, upper-right, lower-left, lower-right.
        
        l_u_corner=[0]
        r_u_corner=[self.width -1]
        
        
        l_b_corner=[self.n  - self.width]
        r_b_corner=[self.n -1]
        
        corner= l_u_corner + l_b_corner + r_u_corner + r_b_corner
        
        #There are self.width*2 + self.height*2 - 4 border states other than the corner states.
        
        l_border=[] #left borders
        r_border=[] #right borders
        u_border=[] #upper borders
        b_border=[] #bottom borders
        
        for i in range(1, (self.height-2)+1):
            
            l_border += [self.width*i]
            r_border += [self.width*i + (self.width-1)]
            
        for i in range(1, (self.width - 2)+1):
            
            u_border += [i]
            b_border += [i + (self.height - 1)*self.width]
            
            
        border= l_border + r_border + u_border + b_border
        
        #And the states that are not on the corner and border are on the middle
        
        middle=[]
        
        border_corner= border + corner
        
        for i in range(self.n):
            if i not in border_corner:
                middle+=[i]
                
        
        return ((l_u_corner, l_b_corner, r_u_corner, r_b_corner),(l_border,r_border,u_border,b_border),middle)
    
        
        
    
    
    def fill_adjacent_matrix(self):
        
        #this function determines the neighbors of all states.
        #this is a kind of helper function for self.fill_trans_prob_matrix
        
        corners, borders, middle=self.corner_border_middle()
        
        
        l_u_corner=corners[0]
        l_b_corner=corners[1]
        r_u_corner=corners[2]
        r_b_corner=corners[3]
        
        l_border=borders[0]
        r_border=borders[1]
        u_border=borders[2]
        b_border=borders[3]
        
        
        #Finding the neighbors of corner states
        l_u_c=l_u_corner[0]
        
        self.dict_adjacent_matrix[l_u_c] += [l_u_c, l_u_c+1, l_u_c+self.width, l_u_c+1+self.width]
        
        l_b_c=l_b_corner[0]
        
        self.dict_adjacent_matrix[l_b_c] += [l_b_c, l_b_c+1, l_b_c-self.width, l_b_c + 1- self.width]
        
        r_u_c=r_u_corner[0]
        
        self.dict_adjacent_matrix[r_u_c] += [r_u_c-1, r_u_c, r_u_c-1+self.width, r_u_c +self.width]
        
        
        r_b_c=r_b_corner[0]
        
        self.dict_adjacent_matrix[r_b_c] += [r_b_c-1, r_b_c, r_b_c-1-self.width, r_b_c-self.width]
        
        
        #Finding the neighbors of border states
        for l_b in l_border:
            self.dict_adjacent_matrix[l_b] += [l_b-self.width,l_b+1-self.width,l_b, l_b+1, l_b+ self.width, l_b+1+self.width]
            
        for r_b in r_border:
            self.dict_adjacent_matrix[r_b] += [r_b-1-self.width, r_b-self.width, r_b-1, r_b, r_b-1+self.width, r_b+self.width]   
            
        for u_b in u_border:
            self.dict_adjacent_matrix[u_b] += [u_b-1, u_b, u_b+1, u_b-1+self.width, u_b+self.width, u_b+1+self.width]
            
        for b_b in b_border:
            self.dict_adjacent_matrix[b_b] += [b_b-1-self.width,b_b-self.width,b_b+1-self.width, b_b-1,b_b,b_b+1]

        
        for m in middle:
            self.dict_adjacent_matrix[m]=[m-1-self.width,m-self.width,m+1-self.width,m-1,m,m+1,m-1+self.width,m+self.width,m+1+self.width]
        
        #end of the method
            
        
            
    def fill_trans_prob_matrix1(self):
        
        #this function fills the trans_prob_matrix
        
        #THIS IS TOO INEFFICIENT!!!
        
        json_file_path = '/Users/canerozer/Desktop/BU/SPRING2024/CS585/final_project/transition_probability_matrix.json'
        
        
        if exists('/Users/canerozer/Desktop/BU/SPRING2024/CS585/final_project/transition_probability_matrix.json'):
            
            with open(json_file_path, 'r') as json_file:
                self.dict_trans_prob_matrix = json.load(json_file)


            print("Loaded dictionary!")
            
            
        else:           
                  
            for key in tqdm(range(self.n)):
                values=self.dict_adjacent_matrix[key]
            
                for value in range(self.n):
                    if value in values:
                        self.dict_trans_prob_matrix[key] += [1/len(values)]
                    else:
                        self.dict_trans_prob_matrix[key] += [0]
                                                
                        
            with open(json_file_path, 'w') as json_file:
                json.dump(self.dict_trans_prob_matrix, json_file)
                
            print("Dictionary saved as JSON file:", json_file_path)
            
            
            
    def fill_trans_prob_matrix(self):
        
        #this function fills the trans_prob_matrix
        
        #THIS IS MORE EFFICIENT 
        

           for key in tqdm(range(self.n)):
               values=self.dict_adjacent_matrix[key]
            
               for value in values:
                   self.dict_trans_prob_matrix[key][value] = 1/len(values)
                   
                   


        
    def fill_dict_x_y_ranges(self):
        
        #fills the self.dict_x_y_ranges
        #this function gives the starting and ending coordinates of each state
        
        for state in range(self.n):
        
            up_c=((math.floor(state/self.width))*self.x, (state-(math.floor(state/self.width)*self.width))*self.x)
            down_c=(up_c[0]+self.x, up_c[1]+self.x)
        
            self.dict_x_y_ranges[state] =[up_c,down_c]
            
    
    def give_centroids(self, state):
        
        
        #((math.floor(state/self.width))*self.x, state-(math.floor(state/self.width)*self.width))
        
        up_c0=(math.floor(state/self.width))*self.x
        
        up_c1=(state*self.x) - (up_c0*self.width)
        
        
        
        return (up_c0 + (self.x // 2), up_c1 + (self.x //2))
    
    
    """def give_state(self, point):
        
        # given a point:(x,y), this function gives the corresponding state of the poin
        #this is a helper function for fill_ground_truth()
        #an inefficient implementation. but still it works...
        
        
        for state in range(self.n):
            u_l, d_r= self.dict_x_y_ranges[state]
            
            if u_l[0] < point[0] and point[0] <= d_r[0] and u_l[1] < point[1] and point[1] <= d_r[1]:
                return state
            
        
        raise ValueError("YOU HAVE A MISTAKE IN fill_dict_x_y_ranges()")
        
        
    def give_state1(self, point):
        
            
        # given a point:(x,y), this function gives the corresponding state of the poin
        #this is a helper function for fill_ground_truth()
        #an inefficient implementation. but still it works...
            
        row_index = point[1] // self.x
        col_index = point[0] // self.x

        # Calculate the number of squares in a row
        num_squares_in_row = self.width // self.x

        # Calculate the square number
        state= row_index * num_squares_in_row + col_index

        return state
        
        
        
        
    
    def fill_ground_truth(self):
        
        #this function fills the ground_truth
        #given the (x,y) coordinates of the fish, it deterimines which state the fish is at
        
        self.give_fish_positions()
        
        
        for position in self.fish_positions:
            
            self.ground_truth +=[self.give_state(position)]"""
            
            
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
            
            
        
                




















