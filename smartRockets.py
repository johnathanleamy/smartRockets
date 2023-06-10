# imports every file form tkinter and tkinter.ttk
import math
import random
from tkinter import *
from tkinter.ttk import *
 
class GFG:

    startX = 0
    startY = 0
    frameCount = 0

    def __init__(self, master = None):
        
        self.master = master
         
        # to take care movement in x direction
        self.x = 1
        # to take care movement in y direction
        self.y = 0
 
        # canvas object to create shape
        self.canvas = Canvas(master,width= 680,height = 920)


        self.gen_size = 10
        self.rockets = []
        for i in range(0, self.gen_size):
            # creating rectangle                        CHANGE TO CREATING IN OBJECT
            self.rectangle = self.canvas.create_rectangle(
                             300, 500, 325, 525, fill = "black")
            dirs = [random.randint(0, 360) for _ in range(60)]

            self.rock = rocket(self.rectangle,dirs)
            self.rockets.append(self.rock)
            self.canvas.pack()
 

        
        #rocket_list = [Rocket("Falcon 9") for _ in range(100)]
        # calling class's movement method to
        # move the rectangle
        self.movement()
        self.canvas.bind("<Button-1>", self.start_click)
        self.canvas.bind("<ButtonRelease-1>", self.add_rectangle)
        

    def start_click(self,event):
        global startX
        global startY
        startX= event.x
        startY = event.y

    def add_rectangle(self,event):
        x = event.x
        y = event.y
        

        # Create the rectangle on the canvas
        self.canvas.create_rectangle(startX, startY, x, y , fill="black")

    def movement(self):
    
        for i in self.rockets:
            fit = i.move_object(self.canvas,10)
            print(i.framecount)
            if fit != None:
                i.reset(self.canvas)

        if fit == None:
                self.canvas.after(100, self.movement)
        else:
                print(fit)
               
                self.new_gen()

    def new_gen(self):
        self.rockets.sort(key=lambda x: x.get_fittnes())
        self.rockets[0].directions = self.rockets[1].create_offspring()
        for i in self.rockets:
            i.framecount = 0
        self.movement()



        
        

class rocket:
    def __init__(self,object,dir):
        self.lifetime = 60
        self.directions = dir
        self.framecount = 0
        self.posX = 0
        self.posY = 0
        self.obj = object
    
    def get_direction(self):
        if self.framecount < self.lifetime-1:
            self.framecount += 1
            return self.directions[self.framecount]
        return -1
    def get_fittnes(self):
        return self.posX
    def move_object(self, canvas, distance):
        angle = self.get_direction()
        # Convert angle from degrees to radians
        angle_rad = math.radians(angle)
        
        # Calculate the change in x and y coordinates
        delta_x = distance * math.cos(angle_rad)
        delta_y = distance * math.sin(angle_rad)
        self.posX += delta_x
        self.posY += delta_y

        # Move the object on the canvas
        canvas.move(self.obj, delta_x, delta_y)
        if angle == -1:
            return self.get_fittnes()
    def create_offspring(self):
        #create a similar rocket with a slighty different set of directions
        #for now just go through the direction and change each by a random number up to a constant
        maxoff = 30
        newdir = []
        for i in self.directions:
            random_number = random.uniform(-maxoff, maxoff)
            newdir.append(i + random_number)
        return newdir
    def reset(self,canvas):
        canvas.move(self.obj, -self.posX, -self.posY)
        self.posX = 0
        self.posY = 0
        

    

    

if __name__ == "__main__":
 
    # object of class Tk, responsible for creating
    # a tkinter toplevel window
    master = Tk()
    gfg = GFG(master)
 
    # Infinite loop breaks only by interrupt
    mainloop()