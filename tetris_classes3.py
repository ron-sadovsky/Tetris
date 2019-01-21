#########################################
# Programmer: Mrs.G
# Date: 04/12/2016
# File Name: tetris_classes3.py
# Description: These classes form the third and final class template for our Tetris game.
#########################################
import pygame
pygame.mixer.init()

BLACK     = (  0,  0,  0)                       
RED       = (255,  0,  0)                     
GREEN     = (  0,255,  0)                     
BLUE      = (  0,  0,255)                     
ORANGE    = (255,127,  0)               
CYAN      = (  0,183,235)                   
MAGENTA   = (255,  0,255)                   
YELLOW    = (255,255,  0)
WHITE     = (255,255,255) 
COLOURS   = [ BLACK,  RED,  GREEN,  BLUE,  ORANGE,  CYAN,  MAGENTA,  YELLOW,  WHITE ]
CLR_names = ['black','red','green','blue','orange','cyan','magenta','yellow','white']
FIGURES   = [  None , 'Z' ,  'S'  ,  'J' ,  'L'   ,  'I' ,   'T'   ,   'O'  , None  ]

blockPimage = pygame.image.load("blockPimage.png")
blockPimage = pygame.transform.scale(blockPimage,(25,25))

blockYimage = pygame.image.load("blockYimage.png")
blockYimage = pygame.transform.scale(blockYimage,(25,25))

blockGimage = pygame.image.load("blockGimage.png")
blockGimage = pygame.transform.scale(blockGimage,(25,25))

blockRimage = pygame.image.load("blockRimage.png")
blockRimage = pygame.transform.scale(blockRimage,(25,25))

blockOimage = pygame.image.load("blockOimage.png")
blockOimage = pygame.transform.scale(blockOimage,(25,25))

blockBimage = pygame.image.load("blockBimage.png")
blockBimage = pygame.transform.scale(blockBimage,(25,25))

blockLPimage = pygame.image.load("blockLPimage.png")
blockLPimage = pygame.transform.scale(blockLPimage,(25,25))

clearline = pygame.mixer.Sound("clearline.wav")
clearline.set_volume(0.8)
    
class Block(object):                    
    """ A square - basic building block
        data:               behaviour:
            col - column        move left/right/up/down
            row - row           draw
            clr - colour
    """
    def __init__(self, col = 1, row = 1, clr = 1):
        self.col = col                  
        self.row = row                  
        self.clr = clr

    def __str__(self):                  
        return '('+str(self.col)+','+str(self.row)+') '+CLR_names[self.clr]

    def draw(self, surface, gridsize=20):                     
        x = self.col * gridsize        
        y = self.row * gridsize
        CLR = COLOURS[self.clr]
        
        if CLR == WHITE or CLR == BLACK:
            pygame.draw.rect(surface,CLR,(x,y,gridsize,gridsize), 2)
            pygame.draw.rect(surface, WHITE,(x,y,gridsize+1,gridsize+1), 2)
            
        if CLR == MAGENTA:
            surface.blit(blockPimage,(x,y))
        if CLR == YELLOW:
            surface.blit(blockYimage,(x,y))
        if CLR == GREEN:
            surface.blit(blockGimage,(x,y))
        if CLR == RED:
            surface.blit(blockRimage,(x,y))
        if CLR == ORANGE:
            surface.blit(blockOimage,(x,y))
        if CLR == CYAN:
            surface.blit(blockBimage,(x,y))
        if CLR == BLUE:
            surface.blit(blockLPimage,(x,y))

    def move_down(self):                
        self.row = self.row + 1   
               
#######################################################################################################################
# 1. Delete the move_left, move_right and move_up,since they are no longer used (we use the Shape methods instead)
#    LEAVE the MOVE_DOWN method since we need it for movind individual blocks inside the obstacles.    
#######################################################################################################################        

    def move_left(self):                
        self.col = self.col - 1    
        
    def move_right(self):               
        self.col = self.col + 1   
        
    def move_up(self):                  
        self.row = self.row - 1  

#---------------------------------------#
class Cluster(object):
    """ Collection of blocks
        data:
            col - column where the anchor block is located
            row - row where the anchor block is located
            blocksNo - number of blocks
    """
    def __init__(self, col = 1, row = 1, blocksNo = 1):
        self.col = col                    
        self.row = row                   
        self.clr = 0                          
        self.blocks = [Block()]*blocksNo      
        self._colOffsets = [0]*blocksNo  
        self._rowOffsets = [0]*blocksNo
        
#LEARN ABOUT... auxiliary attributes(attributes that are not accessible from the game template, but exist only inside the class)
#           _colOffsets - list of horizontal offsets for each block, in reference to the anchor block
#           _rowOffsets - list of vertical offsets for each block, in reference to the anchor block
#    In this template I have renamed blockXOffset and blockYOsset into _colOffsets into _rowOffsets. 
#    2. In addition renamed update(self) method to _update(self) to show that it is private.
#       Make the necessary changes THROUGHOUT THE WHOLE TEMPLATE by replacing self.update() with self._update()
##########################################################################################################################################

    def _update(self):
        for i in range(len(self.blocks)):
            blockCOL = self.col+self._colOffsets[i] 
            blockROW = self.row+self._rowOffsets[i] 
            blockCLR = self.clr
            self.blocks[i] = Block(blockCOL, blockROW, blockCLR)

    def draw(self, surface, gridsize):                     
        for block in self.blocks:
            block.draw(surface, gridsize)

    def collides(self, other):
        """ Compare each block from a cluster to all blocks from another cluster.
            Return True only if there is a location conflict.
        """
        for block in self.blocks:
            for obstacle in other.blocks:
                if block.col == obstacle.col and block.row == obstacle.row:
                    return True
        return False
    
    def append(self, other): 
        """ Append all blocks from another cluster to this one.
        """

        for i in other.blocks:
            self.blocks.append(i)
###########################################################################################
# 9.  Add code here that appends the blocks of the other object to the self.blocks list.
#     Use a for loop to take each individual block from the other.blocks list 
############################################################################################
        

#---------------------------------------#
class Obstacles(Cluster):
    """ Collection of tetrominoe blocks on the playing field, left from previous shapes.
        
    """        
    def __init__(self, col = 0, row = 0, blocksNo = 0):
        Cluster.__init__(self, col, row, blocksNo)      # initially the playing field is empty(no shapes are left inside the field)

    def show(self):
        print("\nObstacle: ")
        for block in self.blocks:
            print (block)

    def findFullRows(self, top, bottom, columns):
        fullRows = []
        rows = []
        for block in self.blocks:                       
            rows.append(block.row)                      # make a list with only the row numbers of all blocks
            
        for row in range(top, bottom):                  # starting from the top (row 0), and down to the bottom
            if rows.count(row) == columns:              # if the number of blocks with certain row number
                fullRows.append(row)                    # equals to the number of columns -> the row is full
                clearline.play()
        return fullRows                                 # return a list with the full rows' numbers


    def removeFullRows(self, fullRows):
        for row in fullRows:                            # for each full row, STARTING FROM THE TOP (fullRows are in order)
            for i in reversed(range(len(self.blocks))): # check all obstacle blocks in REVERSE ORDER,
                                                        # so when popping them the index doesn't go out of range !!!
                if self.blocks[i].row == row:
                    self.blocks.pop(i)                  # remove each block that is on this row
                elif self.blocks[i].row < row:
                    self.blocks[i].move_down()          # move down each block that is above this row
        
#---------------------------------------#
class Shape(Cluster):                     
    """ A tetrominoe in one of the shapes: Z,S,J,L,I,T,O; consists of 4 x Block() objects
        data:               behaviour:
            col - column        move left/right/up/down
            row - row           draw
            clr - colour        rotate
                * figure/shape is defined by the colour
            rot - rotation             
    """
    def __init__(self, col = 1, row = 1, clr = 1):
        Cluster.__init__(self, col, row, 4)
        self.clr = clr
############################################################################################
# 3.  Protect(Rename) variable rot to _rot, as there is no need to access it from outside. 
#     The entire rotation process should be handled INSIDE the object ONLY
############################################################################################
        self._rot = 1
        self._colOffsets = [-1, 0, 0, 1] 
        self._rowOffsets = [-1,-1, 0, 0] 
        self._rotate() # private
        
    def __str__(self):                  
        return FIGURES[self.clr]+' ('+str(self.col)+','+str(self.row)+') '+CLR_names[self.clr]

############################################################################################
# 4.  Protect(Rename) method rotate to _rotate, as there is no need to invoke it from outside 
#     the space bar action will be eventually removed
############################################################################################# 

    def _rotate(self):
        """ offsets are assigned starting from the farthest (most distant) block in reference to the anchor block """
        if self.clr == 1:    #           (default rotation)    
                             #   o             o o                o              
                             # o x               x o            x o          o x
                             # o                                o              o o
            _colOffsets = [[-1,-1, 0, 0], [-1, 0, 0, 1], [ 1, 1, 0, 0], [ 1, 0, 0,-1]] #
            _rowOffsets = [[ 1, 0, 0,-1], [-1,-1, 0, 0], [-1, 0, 0, 1], [ 1, 1, 0, 0]] #       
        elif self.clr == 2:  #
                             # o                 o o           o              
                             # o x             o x             x o             x o
                             #   o                               o           o o
            _colOffsets = [[-1,-1, 0, 0], [ 1, 0, 0,-1], [ 1, 1, 0, 0], [-1, 0, 0, 1]] #
            _rowOffsets = [[-1, 0, 0, 1], [-1,-1, 0, 0], [ 1, 0, 0,-1], [ 1, 1, 0, 0]] #
        elif self.clr == 3:  # 
                             #   o             o                o o              
                             #   x             o x o            x           o x o
                             # o o                              o               o
            _colOffsets = [[-1, 0, 0, 0], [-1,-1, 0, 1], [ 1, 0, 0, 0], [ 1, 1, 0,-1]] #
            _rowOffsets = [[ 1, 1, 0,-1], [-1, 0, 0, 0], [-1,-1, 0, 1], [ 1, 0, 0, 0]] #            
        elif self.clr == 4:  #  
                             # o o                o             o              
                             #   x            o x o             x           o x o
                             #   o                              o o         o
            _colOffsets = [[-1, 0, 0, 0], [-1, 0, 1, 1], [0, 0, 0, 1], [-1, -1, 0, 1]]
            _rowOffsets = [[-1,-1, 0, 1], [0,0,0, -1], [-1, 0, 1, 1], [1,0, 0, 0]] #
        elif self.clr == 5:  #   o                              o
                             #   o                              x              
                             #   x            o x o o           o          o o x o
                             #   o                              o              
            _colOffsets = [[ 0, 0, 0, 0], [ 2, 1, 0,-1], [ 0, 0, 0, 0], [-2,-1, 0, 1]] #
            _rowOffsets = [[-2,-1, 0, 1], [ 0, 0, 0, 0], [ 2, 1, 0,-1], [ 0, 0, 0, 0]] #           
        elif self.clr == 6:  #
                             #   o              o                o              
                             # o x            o x o              x o         o x o
                             #   o                               o             o 
            _colOffsets = [[ 0,-1, 0, 0], [-1, 0, 0, 1], [ 0, 1, 0, 0], [ 1, 0, 0,-1]] #
            _rowOffsets = [[ 1, 0, 0,-1], [ 0,-1, 0, 0], [-1, 0, 0, 1], [ 0, 1, 0, 0]] #
        elif self.clr == 7:  # 
                             # o o            o o               o o          o o
                             # o x            o x               o x          o x
                             # 
            _colOffsets = [[-1,-1, 0, 0], [-1,-1, 0, 0], [-1,-1, 0, 0], [-1,-1, 0, 0]] #@@
            _rowOffsets = [[ 0,-1, 0,-1], [ 0,-1, 0,-1], [ 0,-1, 0,-1], [ 0,-1, 0,-1]] #@@
        self._colOffsets = _colOffsets[self._rot] 
        self._rowOffsets = _rowOffsets[self._rot] 
        self._update() # private

    def move_left(self):                
        self.col = self.col - 1                   
        self._update() # private
        
    def move_right(self):               
        self.col = self.col + 1                   
        self._update() # private
        
    def move_down(self):                
        self.row = self.row + 1                   
        self._update() # private
        
    def move_up(self):                  
        self.row = self.row - 1                   
        self._update() # private

    def rotateClkwise(self):
        self._rot = (self._rot + 1)%4  
        self._rotate()
###################################################################################################################
# 5.  Add code here that rotates the shape one step clockwise. Use the rotation section from class template #1
###################################################################################################################

    def rotateCntclkwise(self):
        self._rot = (self._rot - 1)%4
        self._rotate()
        
    def shapeRot(self):
        return self._rot
        
    def shadowRot(self,rotation):
        self._rot=rotation
        self._rotate()

    def setClr(self):
        self.clr = 8
        
    
##########################################################################################################################
# 6.  Add code here that rotates the shape one step counterclockwise. Use the rotation section from class template #1
##########################################################################################################################
   
        
#---------------------------------------#
class Floor(Cluster):
    """ Horizontal line of blocks
        data:
            col - column where the anchor block is located
            row - row where the anchor block is located
            blocksNo - number of blocks 
    """
    def __init__(self, col = 1, row = 1, blocksNo = 1):
        Cluster.__init__(self, col, row, blocksNo)
        for i in range(blocksNo):
            self._colOffsets[i] = i 
        self._update() # private       
            
#---------------------------------------#
class Wall(Cluster):
    """ Vertical line of blocks
        data:
            col - column where the anchor block is located
            row - row where the anchor block is located
            blocksNo - number of blocks 
    """
    def __init__(self, col = 1, row = 1, blocksNo = 1):
        Cluster.__init__(self, col, row, blocksNo)
        for i in range(blocksNo):
            self._rowOffsets[i] = i 
        self._update() # private Make sure all the methods marked as private have an underscore before its name
