'''
#####DrawSim#####
A drawing simulator to set dots on a canvas
and know its cartesian coordinates.

Version: 1.0
Author: user_Kito
date: 15/09/2021
'''

from tkinter import *
from tkinter.colorchooser import askcolor

CANVAS_WIDTH=1036
CANVAS_HEIGHT=692
WINDOW_SIZE="1300x700"
DOT_COLOR="black" #default
OFFSET=4 #number of pixels on each side of the pixel's square (OFFSET**2 pixels in the square) (default 4 -> square of 16 pixels)

class DrawSim():

    #create a DrawSim object which instances a tkinter window
    def __init__(self):
        #---dots---#
        #cartesian coordinates
        self.dot_coord=[[]]
        #coordinates refered to the top left corner
        self.dot_screen_coord=[[]]
        self.dots=[]
        self.dot_count=0
        #---lines---#
        #cartesian coordinates
        self.line_coord=[[]]
        #coordinates refered to the top left corner
        self.line_screen_coord=[[]]
        self.lines=[[]]
        self.line_count=0
        #canvas size
        self.canvas_width=CANVAS_WIDTH
        self.canvas_height=CANVAS_HEIGHT
        #instance of tkinter window
        self.win=Tk()
        self.win.title("DrawSim1.0")
        #set size of the window
        self.win.geometry(WINDOW_SIZE)
        #set the dot color (default black)
        self.dot_color=DOT_COLOR
        #set the offset
        self.offset=OFFSET

    #set a canvas on tkinter window on x y coordinates
    def set_canvas(self,x,y):
        #set canvas
        self.canvas=Canvas(self.win,width=self.canvas_width,height=self.canvas_height,relief=RAISED,bd=2,bg="white",cursor="dot")
        #assign click to draw_dot
        self.canvas.bind('<Button-1>',self.draw_dot)
        self.canvas.place(x=x,y=y)

    #set a button on the gui on x y coordinates
    def set_button(self,name,command,x,y):
        button=Button(self.win,text=str(name),command=command,height=1,width=10)
        button.place(x=x,y=y)
        return button

    #set a label on the gui on x y coordinates
    def set_label(self,content,x,y):
        label=Label(self.win,text=str(content),font=(None, 15))
        label.place(x=x,y=y)
        return label

    #set text box on gui on x y coordinates
    def set_text(self,text,x,y,h,w):
        t=Text(self.win,height=h,width=w)
        t.place(x=x,y=y)
        t.insert(1.0,text)
        return t

    #function to draw a dot (fill pixels) in canvas at mouse click and save its coordinates
    def draw_dot(self,event):
        x=event.x
        y=event.y
        #Draw a dot in the given coordinates
        #second x is the actual x, width is the actual y (for how many pixels you want)
        self.dots.insert(self.dot_count,self.canvas.create_line(x,y,x+self.offset,y,fill=str(self.dot_color),width=self.offset))
        #print("dot:"+str(self.dot_count)+"->"+str(dot))
        #obtain cartesian coordinates (preprocessing)
        canvas_x=(x-self.canvas_width/2)+self.offset/2;
        canvas_y=-y+self.canvas_height/2;
        #append new coordinates
        self.dot_coord.insert(self.dot_count,[canvas_x,canvas_y])
        self.dot_screen_coord.insert(self.dot_count,[x,y])
        #enable coordinates text box editing
        self.coordinates_box['state']='normal'
        #show coordinates
        self.coordinates_box.insert(INSERT,"Dot:"+str(self.dot_count)+" x:"+str(self.dot_coord[self.dot_count][0])+" y:"+str(self.dot_coord[self.dot_count][1])+"\n")
        self.coordinates_box.see("end-2l")
        #disable coordinates text box editing
        self.coordinates_box['state']='disabled'
        self.dot_count+=1;

    #Draw line using Direct Scan Conversion
    def draw_line1(self):
        if self.dot_count>1:
            #start
            x1=self.dot_screen_coord[self.dot_count-2][0]
            y1=self.dot_screen_coord[self.dot_count-2][1]
            #end
            x2=self.dot_screen_coord[self.dot_count-1][0]
            y2=self.dot_screen_coord[self.dot_count-1][1]
            #draw the line
            #dy=y2-y1;
            #dx=x2-x1;
            line=[]
            line_coord=[]
            line_screen_coord=[]
            m=(y2-y1)/(x2-x1);
            b=y1-m*x1;
            x=x1;
            i=0;
            while x<=x2:
                y=int(m*x+b)
                #self.dots.insert(self.dot_count,self.canvas.create_line(x,y,x+self.offset,y,fill=str(self.dot_color),width=self.offset))
                line.insert(i,self.canvas.create_line(x,y,x+self.offset,y,fill=str(self.dot_color),width=self.offset))
                #obtain cartesian coordinates (preprocessing)
                canvas_x=(x-self.canvas_width/2)+self.offset/2;
                canvas_y=-y+self.canvas_height/2;
                #append new coordinates
                line_coord.insert(i,[canvas_x,canvas_y])
                line_screen_coord.insert(i,[x,y])
                i+=1;
                x+=1;
            if i>1:
                self.line_coord.insert(self.line_count,line_coord)
                self.line_screen_coord.insert(self.line_count,line_screen_coord)
                self.lines.insert(self.line_count,line)
                print("line "+str(self.line_count)+":"+str(self.line_coord[self.line_count]))
                self.line_count+=1;

    #Draw line using Digital Diferencial Analyzer (DDA)
    def draw_line2(self):
        return None

    #Draw line using Bresenham's Algorithm
    def draw_line3(self):
        return None


    #display a text box to show dot coordinates
    def display_coordinates(self,x,y,h,w):
        #set text box for Coordinates
        self.coordinates_box=self.set_text("",x,y,h,w)
        yscrollbar=Scrollbar(self.win,orient=VERTICAL,command=self.coordinates_box.yview)
        yscrollbar.place(x=x+203,y=y,height=h+304,width=w-7)
        self.coordinates_box["yscrollcommand"]=yscrollbar.set


    #display a text box to retrieve new dot size
    def display_dot_size_box(self,x,y,h,w):
        #set text box to get new size
        self.dot_size_box=self.set_text("",x,y,h,w)

    #display x y axis
    def display_axis(self):
        for x in range(self.canvas_width):
            self.canvas.create_line(x,self.canvas_height/2,x+1,self.canvas_height/2,fill="grey",width=1)
        for y in range(self.canvas_height):
            self.canvas.create_line(self.canvas_width/2,y,self.canvas_width/2+1,y,fill="grey",width=1)


    #change the dot color
    def change_dot_color(self):
        color=askcolor(title="Choose dot color")
        if color[1]!=None:
            self.dot_color=color[1]

    #change the dot size
    def change_dot_size(self):
        size=self.dot_size_box.get(0.0,END)
        if size!="\n":
            self.offset=int(size)

    #clear the drawing area (canvas)
    def clear_canvas(self):
        self.canvas.delete(ALL)
        self.display_axis() #XD
        self.coordinates_box['state']='normal'
        self.coordinates_box.delete(0.0,"end-1c")
        self.coordinates_box['state']='disabled'
        self.dot_count=0

    #delete the last dot drawn
    def delete_last_dot(self):
        if self.dot_count>0:
            self.canvas.delete(self.dots[self.dot_count-1])
            self.coordinates_box['state']='normal'
            self.coordinates_box.delete("end-2l","end-1l")
            self.coordinates_box['state']='disabled'
            self.dot_coord.pop(self.dot_count-1)
            self.dots.pop(self.dot_count-1)
            self.dot_count-=1;

    #delete the las line drawn
    def delete_last_line(self):
        if self.line_count>0:
            for i in range(len(self.lines[self.line_count-1])):
                self.canvas.delete(self.lines[self.line_count-1][i])
            self.lines.pop(self.line_count-1)
            self.line_count-=1;

    #end simulation
    def close(self):
        self.win.destroy()

    #execute simulator
    def run(self):
        self.win.mainloop()

    def create_DrawSim_Gui(self):
        #place canvas on top left corner of tkinter window
        self.set_canvas(0,0)
        #axis in canvas
        self.display_axis()
        #label -coordinates-
        label2=self.set_label("Coordinates",1060,5)
        #display text box for coordinates
        self.display_coordinates(1060,35,20,25)
        #button -change dot color-
        self.set_button("Dot color",self.change_dot_color,1060,380)
        #button -change dot size-
        self.set_button("Dot size",self.change_dot_size,1060,420)
        #display text box for dot size change
        self.display_dot_size_box(1150,423,1,2)
        #button -delete last dot-
        self.set_button("Delete dot",self.delete_last_dot,1060,460)
        #button -delete last line-
        self.set_button("Delete line",self.delete_last_line,1060,500)
        #button -clear canvas-
        self.set_button("Delete all",self.clear_canvas,1060,540)
        #button -line 1- Draw line using Direct Scan Conversion
        self.set_button("Line 1",self.draw_line1,1198,380)
        #button -line 2- Draw line using Digital Diferencial Analyzer (DDA)
        self.set_button("Line 2",self.draw_line2,1198,420)
        #button -line 3- Draw line using Bresenham's Algorithm
        self.set_button("Line 3",self.draw_line3,1198,460)
        #button -close-
        self.set_button("Exit",self.close,1130,650)
        #run simulator
        self.run()

    '''
    --Convert screen(canvas) coordinates to cartesian
    cartesianx = screenx - screenwidth / 2;
    cartesiany = -screeny + screenheight / 2;
    '''

if __name__=="__main__":

    ds=DrawSim()

    ds.create_DrawSim_Gui()
