from __future__ import division
import numpy as np 
import matplotlib 
matplotlib.use('TkAgg') 
import matplotlib.pyplot as plt 
from matplotlib import animation
import random
from random import randint
from random import shuffle 
shuffle = np.random.shuffle
random_choice = random.choice 
import datetime 

def makeDictionaryOfNeighborLists(nRow, nCol):
    """
    Builds the dictionary of neighbor position lists. nRow is number of rows and nCol is  number of columns
    """
    
    allPositions = [(r, c) for r in np.arange(0, nRow) for c in np.arange(0, nCol)] #(R,C) is defined as a position coordinate point

    #np.arange returns evenly spaced values in the interval. 
    #This will create a list of every possible coordinates (cells) in the environment

    dictionaryOfNeighborLists = {position: makeNeighborLists(position, nRow, nCol) for position in allPositions} 
	#makeNeighborLists(pos, n_row, n_col) is defined below
    
    #This will create a dictionary with a central position (pos is the key) and a corresponding list of neighboring positions 
    #It is a dictionary with positions and a list of their neighbors. 

    return dictionaryOfNeighborLists 

def makeNeighborLists(position, nRow, nCol):
    """
    Build a neighbor list for each cell
    This will create a list of all positions in a cell's Moore neighborhood. 
    Pos is the cell's position, nRow is the maximum width, nCol is the maximum height
    """
    
    r, c = position 

    neighborList = [(r+a, c+b) 
         for a in [-1, 0, 1]
         for b in [-1, 0, 1]
         if 0 <= r + a <= nRow
         if 0 <= c + b <= nCol
         if not (a == 0 and b == 0)]
    return neighborList

#neighborList is a list of neighboring positions around each position with coordinates (r, c). 

def pDivide(): 
    """
    Create a function to generate a number that will be used to determine if the cell will divide or not. 
    """

    randomNumber = random.randint(0,9) #Create a new variable called randomNumber. It is a random integer between 0 and 9. 
    return randomNumber

###CLASS FOR NORMAL CELLS###
class NormalCell(object): 

    def __init__(self, position, dictionaryOfNeighborLists): 
        self.position = position #Pos is the position of the cell
        self.remainingDivisions = 5 #Each normal cell can divide a maximum of 5 times
        self.listOfNeighborPositions = dictionaryOfNeighborLists[self.position] #listOfNeighborPositions will be the value in the dictionary for the current cell's position. Self.pos (the position of the cell) is used to look up a list of its neighbors in the dictionary of lists. 
        self.PLOT_ID = 2 #PLOT_ID is used when visualizing the results
        
    def locateEmptyNeighborPosition(self, agentDictionary):
    
    #Create a new function to locate an empty position in the cell's Moore neighborhood
    #One paramater will be 'agentDictionary' which is a dictionary of agents with key=position and value=cell. Later in the main program agentDictionary will be replaced by normalCellDictionary and cancerCellDictionary
    
        listOfEmptyNeighborPositions = []
        
        for position in self.listOfNeighborPositions:
            if position not in agentDictionary: 
                listOfEmptyNeighborPositions.append(position)
                
        if len(listOfEmptyNeighborPositions) > 1:
            emptyPosition = random_choice(listOfEmptyNeighborPositions) #then randomly select an empty position
            return emptyPosition #Return the value of the empty position 
            
        else:
            return None

    def division(self, agentDictionary, dictionaryOfNeighborLists): 
    #Create a function for cell division

        divide = pDivide()
        if 0<= divide <= 3: #If pDivide is between 4 and 9 (giving it a 60% chance of division)
            emptyPosition = self.locateEmptyNeighborPosition(agentDictionary) #Call the method to locate an empty neighbor position. 
            if emptyPosition is not None:  #If there is an empty position available (the list isn't completely empty)

                    daughterCell = NormalCell(emptyPosition, dictionaryOfNeighborLists) #Create a daughter cell. Also looks up its neighbor list. 
                    agentDictionary[emptyPosition] = daughterCell #Daughter cell added to the agent dictionary 
                    
                    self.remainingDivisions -= 1 #Reduce the number of possible cell divisions by 1 for each division

        if self.remainingDivisions <= 0: #If the cell has divided 5 times
            del agentDictionary[self.position] #Apoptosis
        
###CLASS FOR CANCER CELLS###
class CancerCell(object): 

    def __init__(self, position, dictionaryOfNeighborLists):

        self.position = position #Pos is the position of the cancer cell (a tuple)
        self.listOfNeighborPositions = dictionaryOfNeighborLists[self.position] #neighbor.pos.list will be the value in the dictionary for the current cell's position. The position of the cell is used to look up a list of its neighbors in the dictionary of lists. 
        self.PLOT_ID = 1 #PLOT_ID is used when visualizing the results 

    def locateEmptyNeighborPosition(self, agentDictionary): 
    #Create a new function to locate an empty position in the cell's Moore neighborhood
    #One paramater will be 'agentDictionary' which is a dictionary of agents with key=position and value=cell. Later in the main program agentDictionary will be replaced by normalCellDictionary and cancerCellDictionary
        
        listOfEmptyNeighborPositions = []
        
        for position in self.listOfNeighborPositions:
            if position not in agentDictionary: 
                listOfEmptyNeighborPositions.append(position)
                
        if len(listOfEmptyNeighborPositions) > 1:  
            emptyPosition = random_choice(listOfEmptyNeighborPositions) #then randomly select an empty position
            return emptyPosition #Return the value of the empty position 
            
        else:
            return None

    def division(self, agentDictionary, dictionaryOfNeighborLists): #Create a function for cell division

        divide = pDivide()
        if 3<= divide <= 9: #If pDivide is between 0 and 3 (giving it a 40% chance of division)
            emptyPosition = self.locateEmptyNeighborPosition(agentDictionary) #Call the method to locate an empty neighbor position. 

            if emptyPosition is not None:  #If there is an empty position available (the list isn't completely empty)

                    daughterCell = CancerCell(emptyPosition, dictionaryOfNeighborLists) #Create a daughter cell. Also looks up its neighbor list. 
                    agentDictionary[emptyPosition] = daughterCell #Daughter cell added to the agent dictionary 

                
###START THE SIMULATION###     
if __name__ == "__main__": #Tell the interpreter to execute this program. 
    import time
    startTime = time.time() #Mark the start time of the program
    
    nRow = 1000 #1000 rows
    nCol = 1000 #1000 columns
    maxRepeats  = 100 #Maximum number of iterations
    print(maxRepeats)
    
    dictionaryOfNeighborLists = makeDictionaryOfNeighborLists(nRow, nCol) #Call the function to build the dictionary of neighbor position lists

    center_r = int(nRow/2.0) #Find the r component of the center of the plot 
    center_c = int(nCol/2.0) #Find the c component of the center of the plot 
    cancerPosition = (center_r, center_c) #Define the center position using the above components 
    normalPosition = (((center_r)+1), (center_c))
    print (cancerPosition)
    print (normalPosition)

    FirstNormalCell = NormalCell(normalPosition, dictionaryOfNeighborLists) #Create the first cancer cell at the center position 
    normalCellDictionary = {normalPosition:FirstNormalCell} #Create a new definition in the cell dictionary for the first normal cell 
    
    FirstCancerCell = CancerCell(cancerPosition, dictionaryOfNeighborLists) #Create the first cancer cell at the center position 
    cancerCellDictionary = {cancerPosition:FirstCancerCell} #Create a new definition in the cell dictionary for the first cancer cell
    
    for rep in range(maxRepeats): #Call the replicate function in a FOR loop; run for 400 times
        normalCellList = normalCellDictionary.values() #Copy the cells in a cell dictionary to a list
        
        shuffle(normalCellList) #Shuffle/randomize the list 
        for cell in normalCellList: 
                cell.division(normalCellDictionary, dictionaryOfNeighborLists) 
                #Loop through the randomly ordered cells and call the growth function
                #normalCellDictionary is this particular agentDictionary.

    for rep in range(maxRepeats): 
        cancerCellList = cancerCellDictionary.values() #Copy the cells in the cell dictionary to a list
        
        shuffle(cancerCellList)
        for cell in cancerCellList:
                cell.division(cancerCellDictionary, dictionaryOfNeighborLists) #Loop through the list of randomly ordered cells
                #cancerCellDictionary is this particular agentDictionary.

    matrix = np.zeros((nRow, nCol)) #np.zeros creates a matrix with row and column dimensions specified


    for cell in cancerCellDictionary.values():
        matrix[cell.position] = cell.PLOT_ID #2
        
    for cell in normalCellDictionary.values():
        matrix[cell.position] = cell.PLOT_ID #1. The PLOT_ID ints create the cells in different colors 
    


    plt.imshow(matrix, interpolation='none', cmap='coolwarm', vmin=0, vmax=2) #Paint an image on the model)

    endTime = time.time() #Define the end time of the program 
    totalTime = round((endTime-startTime), 2) #Calculate the change in time 
    print('Time: ' + str(totalTime)) #Print the time elapsed
    
    number_of_cancer_cells = len(cancerCellDictionary) #Find the length of cancerCellDictionary
    print('Cancer cells: ' + str(number_of_cancer_cells)) #Print out this number
    
    number_of_normal_cells = len(normalCellDictionary) #Find the length of normalCellDictionary
    print('Normal cells: ' + str(number_of_normal_cells)) #Print out this number 
    
    number_of_total_cells = number_of_cancer_cells + number_of_normal_cells #Calculate the total number of cells (normal+cancer)
    print('Total cells: ' + str(number_of_total_cells)) #Print out this number
    
    percent_normal = round(float(100*(number_of_normal_cells/number_of_total_cells)),2) #Calculate the number of normal cells as a percent of the total
    percent_cancer = round(float(100*(number_of_cancer_cells/number_of_total_cells)),2) #Calculate the number of cancer cells as a percent of the total
    print('Percent Normal: ' + str(percent_normal) + '%') #Print out number of normal cells
    print('Percent Cancer: ' + str(percent_cancer) + '%') #Print out number of cancer cells 

plt.show() #Show the matrix
