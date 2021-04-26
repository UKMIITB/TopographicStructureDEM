#!/usr/bin/env python
# coding: utf-8

# In[613]:


import numpy as np
import copy
import math
import pandas as pd


# In[614]:


#A function to return neighbours of a given position in a given matrix. Output is a list of values
#Order is topright, right, bottomright, bottom, bottomleft, left, topleft, top
def return_neighbours(rowindex, colindex, matrix):
    '''This takes input(rowindex, colindex, matrix) and returns a list of neighbour values from given matrix in 
    clockwise direction starting from topright and finally to top'''
    neighbour_values = []
    
    neighbour_values.append(matrix[rowindex-1][colindex+1])
    neighbour_values.append(matrix[rowindex][colindex+1])
    neighbour_values.append(matrix[rowindex+1][colindex+1])
    neighbour_values.append(matrix[rowindex+1][colindex])
    neighbour_values.append(matrix[rowindex+1][colindex-1])
    neighbour_values.append(matrix[rowindex][colindex-1])
    neighbour_values.append(matrix[rowindex-1][colindex-1])
    neighbour_values.append(matrix[rowindex-1][colindex])
    
    return neighbour_values


# In[615]:


#To return the value of row,col based on the above order
def return_neighbours_location(row, col, index):
    '''This function takes input as (row, col, index) and returns (row,col) tuple of neighbour for given index
    It is indexed in clockwise direction starting from topright to top'''
    if index==0:               #topright,
        return (row-1,col+1)
    
    elif index==1:             #right, 
        return (row,col+1)
    
    elif index==2:             #bottomright, 
        return (row+1,col+1)
    
    elif index==3:             #bottom, 
        return (row+1,col)
    
    elif index==4:             #bottomleft, 
        return (row+1,col-1)
    
    elif index==5:             #left, 
        return (row,col-1)
    
    elif index==6:             #topleft, 
        return (row-1,col-1)
    
    else:                      #top
        return (row-1,col)


# In[616]:


#To return the value of major flow direction based on index 
#Order is topright, right, bottomright, bottom, bottomleft, left, topleft, top
def return_major_flowdir(index):
    '''This function takes input as index and return major flow direction value corresponding to that index'''
    if index==0:    #Topright
        return 1
    
    elif index==1:  #Right 
        return 2
    
    elif index==2:  #Bottomright
        return 4
    
    elif index==3:  #Bottom
        return 8
    
    elif index==4:  #Bottomleft
        return 16
    
    elif index==5:  #Left
        return 32
    
    elif index==6:  #Topleft
        return 64
    
    else:
        return 128  #Top


# In[617]:


#dem = np.zeros((12,12))
dem = np.zeros((10,10))


# In[618]:


#hello ="778 765 750 740 747 759 765 766 769 776 786 795 770 758 745 737 741 751 753 761 777 789 802 814 777 763 747 736 735 743 750 767 787 806 820 832 786 767 750 737 729 739 752 769 785 797 808 822 794 773 756 741 730 732 744 759 772 779 789 806 799 782 763 750 737 728 732 745 757 767 782 801 802 788 771 761 751 736 729 738 751 764 779 798 799 790 780 772 762 746 733 737 754 770 784 794 811 799 787 771 757 741 728 730 745 765 779 783 823 807 790 774 762 748 733 724 733 750 764 763 830 814 801 787 776 761 743 728 725 737 748 751 822 818 811 801 791 776 757 739 726 725 735 751"
hello ="07 07 06 07 07 07 07 05 07 07 09 09 08 09 09 09 09 07 09 09 11 11 10 11 11 11 11 09 11 11 12 12 08 12 12 12 12 10 12 12 13 12 07 12 13 13 13 11 13 13 14 07 06 11 14 14 14 12 14 14 15 07 07 08 09 15 15 13 15 15 15 08 08 08 07 16 16 14 16 16 15 11 11 11 11 17 17 06 17 17 15 15 15 15 15 18 18 15 18 18"


# In[619]:


#Forming the DEM from the given data
index=0
for row in range(0,10):
    for col in range(0,10):
        #num=hello[index]+hello[index+1]+hello[index+2]
        num=hello[index]+hello[index+1]
        storenum=int(num,10)
        #index=index+4
        index=index+3
        dem[row][col]=storenum


# In[620]:


dem


# In[621]:


#newdem will store the 1st correction 
newdem = copy.copy(dem)
rowlength, collength=dem.shape


# In[622]:


#this is used to fill single cell depression by raising it to minimum neighbour value and store in newdem variable
#border values are excluded
def depressionlessdem():
    '''This function performs depressionless dem calculation by raising centre pixel value to minimum of 
    neighbour values and returns False if none of the values were altered else True if any single pixel value was 
    updated'''
    isfound=False
    for row in range(1,rowlength-1):
        for col in range(1,collength-1):
            
            centre=newdem[row][col]
            neighbour_values = return_neighbours(row, col, newdem)
            
            if(centre<min(neighbour_values)):
                newdem[row][col]=min(neighbour_values)
                isfound=True
                
            else:
                newdem[row][col]
                
    return isfound


# In[623]:


isfound = True
while(isfound==True):
    isfound =depressionlessdem()


# In[624]:


newdem


# In[625]:


#flowdir is used to store flow direction and in this block the edge pixel value is stored
flowdir = np.zeros((rowlength,collength))

for row in range(0,rowlength):
    for col in range(0,collength):
        
        if col==0:
            flowdir[row][col]=32
            continue
            
        if col==collength-1:
            flowdir[row][col]=2
            continue
            
        if row==0:
            flowdir[row][col]=128
            continue
            
        if row==rowlength-1:
            flowdir[row][col]=8
            continue
flowdir


# In[626]:


weighteddropmatrix=[[0]*collength for i in range(rowlength)]
weighteddropmatrix


# In[627]:


#In this block we find the neighbour drop and assign values as per Table3 step3
#weighteddropmatrix stores weighteddrop values of neighbours for each pixel except the edge pixel for later purpose
weighteddropmatrix=[[0]*collength for i in range(rowlength)]
for row in range(0,rowlength):
    for col in range(0,collength):
        
        if flowdir[row][col]!=0:    #These are the edge pixels so we donot need to compute for it
            continue
            
        else:
            
            weighteddrop=[]
            
            topright=(newdem[row][col]-newdem[row-1][col+1])/math.sqrt(2)
            right=newdem[row][col]-newdem[row][col+1]
            bottomright=(newdem[row][col]-newdem[row+1][col+1])/math.sqrt(2)
            bottom=newdem[row][col]-newdem[row+1][col]
            bottomleft=(newdem[row][col]-newdem[row+1][col-1])/math.sqrt(2)
            left=newdem[row][col]-newdem[row][col-1]
            topleft=(newdem[row][col]-newdem[row-1][col-1])/math.sqrt(2)
            top=newdem[row][col]-newdem[row-1][col]
            
            weighteddrop.append(topright)
            weighteddrop.append(right)
            weighteddrop.append(bottomright)
            weighteddrop.append(bottom)
            weighteddrop.append(bottomleft)
            weighteddrop.append(left)
            weighteddrop.append(topleft)
            weighteddrop.append(top)
            
            weighteddropmatrix[row][col]=weighteddrop
            largest=max(weighteddrop)
            largestindex = weighteddrop.index(largest)
            largestcount=weighteddrop.count(largest)
            
            
            if largest<0:                      #undefined flow so random negative number is assigned
                flowdir[row][col]=-20
                
            if largest>=0 and largestcount==1: #flow direction is along the largest drop
                flowdir[row][col] = return_major_flowdir(largestindex)
                
            if largest>0 and largestcount>1:       #flow direction should be according to lookup table.
                #case where largest count=3 and in order then picking the central value
                if largestcount==3:
                    indices = [ind for ind,val in enumerate(weighteddrop) if val==largest]
                    indices.sort()
                    if indices==[0,1,2] or indices==[1,2,3] or indices==[2,3,4] or indices==[3,4,5] or indices==[4,5,6] or indices==[5,6,7] or indices==[6,7,0] or indices==[7,0,1]:
                        flowdir[row][col] = return_major_flowdir(indices[1]) #Assigning central value
                    else:
                        flowdir[row][col] = return_major_flowdir(largestindex) #Randomly assigning value
                else:
                    flowdir[row][col] = return_major_flowdir(largestindex) #Randomly assigning value 
                
            if largest==0 and largestcount>1:  #summing their neighbours location code 
                directionsum=0
                
                indices = [ind for ind,val in enumerate(weighteddrop) if val==largest] 
                for ind in indices:
                    directionsum +=return_major_flowdir(ind)
                    
                flowdir[row][col]=directionsum
    


# In[628]:


flowdir


# In[629]:


#For each cell not already encoded as negative, 0, 1, 2, 4, 8, 16, 32, 64, or 128, examine the neighbor cells 
#with the largest drop. If a neighbor is encountered that has a flow direction of 1, 2, 4, 8, 16, 32, 64, or 128, 
#and the neighbor does not flow to the center cell, assign the center cell a flow direction which
#flows to this neighbor.
#Table 3 step 4
for row in range(0,rowlength):
    for col in range(0,collength):
        if flowdir[row][col]<0 or flowdir[row][col]==0 or flowdir[row][col]==1 or flowdir[row][col]==2 or flowdir[row][col]==4 or flowdir[row][col]==8 or flowdir[row][col]==16 or flowdir[row][col]==32 or flowdir[row][col]==64 or flowdir[row][col]==128:
            continue
        else:
            weighteddrop=weighteddropmatrix[row][col]
            maxweighteddrop=max(weighteddrop)
            maxweighteddroplist = [ind for (ind,val) in enumerate(weighteddrop) if val==maxweighteddrop]
            
            for maxweighteddropindex in maxweighteddroplist:
                
                rowval, colval = return_neighbours_location(row, col, maxweighteddropindex)
            
                if flowdir[rowval][colval]==1 or flowdir[rowval][colval]==2 or flowdir[rowval][colval]==4 or flowdir[rowval][colval]==8 or flowdir[rowval][colval]==16 or flowdir[rowval][colval]==32 or flowdir[rowval][colval]==64 or flowdir[rowval][colval]==128:
                    neighbourtocentre=False #checking if it flows to centre
                
                    if maxweighteddropindex==0 and flowdir[rowval][colval]==16:   #topright neighbour
                        neighbourtocentre=True
                    elif maxweighteddropindex==1 and flowdir[rowval][colval]==32: #right neighbour
                        neighbourtocentre=True
                    elif maxweighteddropindex==2 and flowdir[rowval][colval]==64: #bottomright neighbour
                        neighbourtocentre=True
                    elif maxweighteddropindex==3 and flowdir[rowval][colval]==128: #bottom neighbour
                        neighbourtocentre=True
                    elif maxweighteddropindex==4 and flowdir[rowval][colval]==1: #bottomleft neighbour
                        neighbourtocentre=True
                    elif maxweighteddropindex==5 and flowdir[rowval][colval]==2: #left neighbour
                        neighbourtocentre=True
                    elif maxweighteddropindex==6 and flowdir[rowval][colval]==4: #topleft neighbour
                        neighbourtocentre=True
                    else:                         #top neighbour
                        if flowdir[rowval][colval]==8:
                            neighbourtocentre=True

                    if neighbourtocentre==False:    #neighbour doesnot flow to centre then centre flows to this neighbour 
                        flowdir[row][col] = return_major_flowdir(maxweighteddropindex)
                        break


# In[630]:


flowdir


# In[631]:


#For directions that are not along the standard 8 directions are marked as negative
for row in range(0,rowlength):
    for col in range(0,collength):
        if flowdir[row][col]!=1 and flowdir[row][col]!=2 and flowdir[row][col]!=4 and flowdir[row][col]!=8 and flowdir[row][col]!=16 and flowdir[row][col]!=32 and flowdir[row][col]!=64 and flowdir[row][col]!=128:
            flowdir[row][col]=flowdir[row][col]*-1
        else:
            continue


# In[632]:


flowdir


# In[633]:


#Creating unique watershed labels
watershedlabel=np.zeros((rowlength,collength))
unique_values = 1
for row in range(0,rowlength):
    for col in range(0,collength):
        
        if flowdir[row][col]<0:
            watershedlabel[row][col]=unique_values
            unique_values = unique_values+1
            
        else:
            continue


# In[634]:


watershedlabel


# In[635]:


#Allocating spatially connected groups of cell as one unique labels which is minimum of the connected cells
#Excluding the border cells
def unique_watershed_label():
    '''Allocating spatially connected groups of cell as one unique labels which is minimum of the connected cells
    excluding the border cells.Returns False if no value was updated'''
    isfound = False
    for row in range(1,rowlength-1):
        for col in range(1,collength-1):
            
            neighbour_values = return_neighbours(row, col, watershedlabel)
            neighbour_values = list(filter(lambda val:val!=0, neighbour_values)) #removed occurence of 0
            
            if len(neighbour_values)==0:
                continue
                
            else:
                min_neighbour_val = min(neighbour_values)
                if(min_neighbour_val<watershedlabel[row][col]):
                    isfound = True
                    watershedlabel[row][col] = min_neighbour_val
    return isfound


# In[636]:


isfound = True
while(isfound==True):
    isfound = unique_watershed_label()


# In[637]:


watershedlabel


# In[638]:


#creating distinct watershed label values for spatially connected groups
label_set = []
for row in range(1,rowlength-1):
    for col in range(1, collength-1):
        if watershedlabel[row][col]!=0:
            if watershedlabel[row][col] not in label_set:
                label_set.append(watershedlabel[row][col])
            watershedlabel[row][col] = label_set.index(watershedlabel[row][col])+1
watershedlabel


# In[639]:


class pour_point_table(object):
    def __init__(self, pair, elevation, location):
        self.pair = pair
        self.elevation = elevation
        self.location = location
        
    def get_pair(self):
        return self.pair
    def get_elevation(self):
        return self.elevation
    def get_location(self):
        return self.location
    def set_elevation(self, newelevation):
        self.elevation = newelevation
    def set_location(self, newlocation):
        self.location = newlocation


# In[640]:


def is_pair_present(pair, pour_point_list):
    for obj in pour_point_list:
        obj_pair = obj.get_pair()
        if obj_pair==pair:
            return True
    return False


# In[641]:


def pair_present_location(pair, pour_point_list):
    for (ind,obj) in enumerate(pour_point_list):
        if obj.get_pair()==pair:
            return ind


# In[642]:


pour_point_list = []
def prepare_pour_points():
    for row in range(1,rowlength-1):
        for col in range(1,collength-1):

            neighbour_values = return_neighbours(row, col, watershedlabel)
            for val in neighbour_values:
                if watershedlabel[row][col]!=val:
                    index = neighbour_values.index(val)
                    row_neighbour, col_neighbour = return_neighbours_location(row, col, index)
                    elevation = max(newdem[row][col], newdem[row_neighbour][col_neighbour])
                    pair = (min(watershedlabel[row][col],watershedlabel[row_neighbour][col_neighbour]), 
                            max(watershedlabel[row][col],watershedlabel[row_neighbour][col_neighbour]))
                    if is_pair_present(pair,pour_point_list)==True:
                        index_pour_point_list = pair_present_location(pair, pour_point_list)
                        obj = pour_point_list[index_pour_point_list]
                        original_elevation = obj.get_elevation()
                        if elevation<original_elevation:
                            obj.set_elevation(elevation)
                            obj.set_location((row,col))
                            pour_point_list[index_pour_point_list] = obj
                    else:
                        obj = pour_point_table(pair, elevation, (row,col))
                        pour_point_list.append(obj)


# In[643]:


prepare_pour_points()


# In[644]:


df_table = pd.DataFrame(data=None, columns=['Pair', 'Elevation', 'Location(row,col)']) 


# In[645]:


for obj in pour_point_list:
    df_table = df_table.append({'Pair': obj.get_pair(), 'Elevation':obj.get_elevation(),
                                'Location(row,col)':obj.get_location()},ignore_index=True)


# In[646]:


df_table.set_index('Pair', inplace=True)


# In[647]:


df_table


# In[648]:


label_set


# In[649]:


class watershed_data(object):
    def __init__(self, row, col):
        self.row = row
        self.col = col
        self.dem_val = newdem[row][col]
        self.watershed_label = watershedlabel[row][col]
    def get_row(self):
        return int(self.row)
    def get_col(self):
        return int(self.col)
    def get_dem_val(self):
        return self.dem_val
    def get_watershed_label(self):
        return int(self.watershed_label)


# In[650]:


#Preparing an array of all pour/sinks
all_pour_point = []
for row in range(rowlength):
    for col in range(collength):
        if watershedlabel[row][col] in label_set:
            all_pour_point.append(watershed_data(row,col))


# In[560]:


def return_neighbours_coordinate(row,col):
    ''' This returns a list of tuple values of the neighbours in clockwise direction 
    starting from topright and finally to top'''
    neighbours_coordinate = []
    for ind in range(0,8):
        neighbours_coordinate.append(return_neighbours_location(row,col,ind))
    
    return neighbours_coordinate


# In[561]:


def unique_neighbour_coordinate(neighbours_coordinate, label_pour_point):
    '''This function takes neighbours_coordinate as list and label_pour_point list and 
    remove those neighbour coordinate which are already present on label_pour_point.
    As this is mutable so change is also reflected in the original called function'''
    label_pour_point_coordinate_list = []      #List containing all coordinates of label_pour_points
    for obj in label_pour_point:
        label_pour_point_coordinate_list.append((obj.get_row(), obj.get_col()))
        
    neighbours_coordinate = [coordinate for coordinate in neighbours_coordinate if coordinate not in label_pour_point_coordinate_list]


# In[562]:


def return_min_label_pour_point(label_pour_point):
    '''This function returns the object whose cell value has the lowest dem value'''
    
    min_demval = label_pour_point[0].get_dem_val()
    label_pour_point_min = label_pour_point[0]
    
    for ind,obj in enumerate(label_pour_point):
        if obj.get_dem_val()<min_demval:
            min_demval = obj.get_dem_val()
            label_pour_point_min = label_pour_point[ind]
    
    return label_pour_point_min


# In[563]:


def is_borderpixel(row,col):
    '''Return true/false based on the whether that row,col lies on border or not'''
    if row==0 or row==rowlength-1 or col==0 or col==collength-1:
        return True
    else:
        return False


# In[564]:


def return_min_neighbours_coordinate(neighbours_coordinate):
    '''This function returns the location of minimum value of dem and preference to non boundary pixel is given'''
    #Initialising everything with the first value
    min_row = neighbours_coordinate[0][0]
    min_col = neighbours_coordinate[0][1]
    min_dem = newdem[min_row][min_col]
    
    for cells in neighbours_coordinate:
        row = cells[0]
        col = cells[1]
        if newdem[row][col]<min_dem:           #Lower dem value found, so updating all the variables
            min_dem = newdem[row][col]
            min_row = row
            min_col = col
        elif newdem[row][col]==min_dem:
            if is_borderpixel(min_row,min_col):  #Update in hope of getting a non-border cell value 
                min_row = row
                min_col = col
        else:
            continue
    return (min_row,min_col)


# In[565]:


def update_data(label_pour_point, row, col, label_val):
    watershedlabel[row][col] = label_val
    for obj in label_pour_point:
        if newdem[obj.get_row()][obj.get_col()] < newdem[row][col]:
            newdem[obj.get_row()][obj.get_col()] = newdem[row][col]


# In[566]:


#Starting the raising watershed process
remaining_label_set = copy.deepcopy(label_set)    #All different label values

while(len(remaining_label_set)>0): 
    
    label_val = remaining_label_set.pop()   #Picked one label for processing and removed that from the list
    label_pour_point = []                   #To store all pixels which has label value==label_val

    label_pour_point = [obj for obj in all_pour_point if obj.get_watershed_label()==label_val]
    all_pour_point = [obj for obj in all_pour_point if obj not in label_pour_point] #Updating all_pour_point
            
    while(True):
        neighbours_coordinate = []
        for val in label_pour_point:
            row = val.get_row()
            col = val.get_col()
            neighbours_coordinate += return_neighbours_coordinate(row,col) #We have all neighbours of cell in N
        neighbours_coordinate = list(set(neighbours_coordinate)) #Removing duplicate instances
        unique_neighbour_coordinate(neighbours_coordinate, label_pour_point) #Removing inside neighbours (Array M)
        
        #finding minimum for label_pour_point
        label_pour_point_min = return_min_label_pour_point(label_pour_point)
        
        #finding minimum dem for neighbours_coordinate
        neighbour_row_min,neighbour_col_min = return_min_neighbours_coordinate(neighbours_coordinate)
        
        if is_borderpixel(neighbour_row_min,neighbour_col_min):
            break
        if newdem[neighbour_row_min][neighbour_col_min] < newdem[label_pour_point_min.get_row()][label_pour_point_min.get_col()]:
            break
        else:    #Neighbour is either greater or equal so we need to update the values
            label_pour_point.append(watershed_data(neighbour_row_min, neighbour_col_min))
            update_data(label_pour_point, neighbour_row_min, neighbour_col_min, label_val) #To update dem values


# In[657]:


newdem


# In[ ]:




