'''
#####DrawSim#####

A drawing simulator to set dots and draw lines
on a canvas and display their cartesian coordinates.

Version: 1.0
Author: user_Kito
Date: 15/09/2021
'''

#filedialog.asksaveasfile/askopenfile

from tkinter import *
from tkinter.colorchooser import askcolor
import math as mt

CANVAS_WIDTH=1036
CANVAS_HEIGHT=680
WINDOW_SIZE="1300x730"
DOT_COLOR="black" #default
OFFSET=4 #number of pixels on each side of the pixel's square (OFFSET**2 pixels in the square) (default 4 -> 16 pixel square)

class DrawSim():

    #create a DrawSim object which instantiates a tkinter window
    def __init__(self):
        #---dots---#
        #cartesian coordinates
        self.dot_coord=[]
        #coordinates refered to the top left corner
        self.dot_screen_coord=[]
        self.dots=[]
        self.dot_count=0
        self.dot_coord_box=None
        #---lines---#
        #cartesian coordinates
        self.line_coord=[]
        #coordinates refered to the top left corner
        self.line_screen_coord=[]
        self.lines=[]
        self.line_count=0
        self.line_coord_box=None
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
        self.canvas.bind("<Button-1>",self.draw_dot)
        self.canvas.bind("<Button-3>",self.select_line)
        self.canvas.place(x=x,y=y)

    #set a button on the gui on x y coordinates
    def set_button(self,name,command,x,y,h,w):
        button=Button(self.win,text=str(name),command=command,height=h,width=w)
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
        x,y=event.x,event.y
        #Draw a dot in the given coordinates
        #second x is the actual x, width is the actual y (for how many pixels you want)
        self.dots.insert(self.dot_count,self.canvas.create_line(x,y,x+self.offset,y,fill=str(self.dot_color),width=self.offset))
        #obtain cartesian coordinates (preprocessing)
        canvas_x,canvas_y=(x-self.canvas_width/2)+self.offset/2,-y+self.canvas_height/2
        #append new coordinates
        self.dot_coord.insert(self.dot_count,[canvas_x,canvas_y])
        self.dot_screen_coord.insert(self.dot_count,[x,y])
        #enable coordinates text box editing
        self.dot_coord_box["state"]="normal"
        #show coordinates
        self.dot_coord_box.insert(INSERT,"Dot:"+str(self.dot_count)+" x:"+str(self.dot_coord[self.dot_count][0])+" y:"+str(self.dot_coord[self.dot_count][1])+"\n")
        self.dot_coord_box.see("end-2l")
        #disable coordinates text box editing
        self.dot_coord_box["state"]="disabled"
        self.dot_count+=1

    #Draw line using Direct Scan Conversion (original Slope intercept)
    def draw_line1(self):
        if self.dot_count>1:
            line=[]
            line_coord=[]
            line_screen_coord=[]
            #start
            x1,y1=self.dot_screen_coord[self.dot_count-2][0],self.dot_screen_coord[self.dot_count-2][1]
            #end
            x2,y2=self.dot_screen_coord[self.dot_count-1][0],self.dot_screen_coord[self.dot_count-1][1]
            #draw the line
            dx,dy=x2-x1,y2-y1
            m=dy/dx
            b=y1-m*x1
            x,y=x1,y1
            i=0
            while x<=x2:
                line.insert(i,self.canvas.create_line(x,y,x+self.offset,y,fill=str(self.dot_color),width=self.offset))
                #obtain cartesian coordinates (preprocessing)
                canvas_x,canvas_y=(x-self.canvas_width/2)+self.offset/2,-y+self.canvas_height/2
                #append new coordinates
                line_coord.insert(i,[canvas_x,canvas_y])
                line_screen_coord.insert(i,[x,y])
                i+=1
                x+=self.offset
                y=int(m*x+b)
            if i>1:
                self.line_coord.insert(self.line_count,line_coord)
                self.line_screen_coord.insert(self.line_count,line_screen_coord)
                self.lines.insert(self.line_count,line)
                #enable coordinates text box editing
                self.line_coord_box["state"]="normal"
                #delete last line shown
                self.line_coord_box.delete("end-1l","end")
                #display line coordinates
                self.line_coord_box.insert(INSERT,"line "+str(self.line_count)+": "+str(self.line_coord[self.line_count]))
                #disable coordinates text box editing
                self.line_coord_box["state"]="disabled"
                self.line_count+=1


    #Draw line using Direct Scan Conversion (Modified Slope intercept)
    def draw_line21(self):
        if self.dot_count>1:
            t=True
            line=[]
            line_coord=[]
            line_screen_coord=[]
            #start
            x1,y1=self.dot_screen_coord[self.dot_count-2][0],self.dot_screen_coord[self.dot_count-2][1]
            #end
            x2,y2=self.dot_screen_coord[self.dot_count-1][0],self.dot_screen_coord[self.dot_count-1][1]
            #mod4
            if x2<x1:
                print("x2 < x1")
                #swap start and end points
                aux=x1
                x1=x2
                x2=aux
                aux=y1
                y1=y2
                y2=aux
            #obtain cartesian coordinates of starting point (preprocessing)
            x11,y11=(x1-self.canvas_width/2)+self.offset/2,-y1+self.canvas_height/2
            #obtain cartesian coordinates of ending point (preprocessing)
            x22,y22=(x2-self.canvas_width/2)+self.offset/2,-y2+self.canvas_height/2
            #draw the line
            dx,dy=x2-x1,y2-y1
            dxx,dyy=x22-x11,y22-y11
            x,y=x1,y1
            #mod2
            if x2==x1:
                if y1>y2:
                    #draw vertical line downwards
                    for y in range(y2,y1):
                        self.canvas.create_line(x2,y,x2+self.offset,y,fill=str(self.dot_color),width=self.offset) ###MAL###
                    return
                else:
                    #draw vertical line upwards
                    for y in range(y1,y2):
                        self.canvas.create_line(x2,y,x2+self.offset,y,fill=str(self.dot_color),width=self.offset) ###MAL###
                    return
            else:
                #m1 -> slope with cartesian coordinates (real one for checks)
                m,m1=dy/dx,dyy/dxx
            #mod3 m>1
            if abs(dx)<abs(dy) and dy!=0:
                print("m > 1")
                t=False
                #set new m
                m=1/m
            b=y-m*x
            i=0
            dy=-self.offset if dy<0 else self.offset
            dx=-self.offset if dx<0 else self.offset
            while x<=x2:
                #if t==False:
                #    line.insert(i,self.canvas.create_line(y,x,y+self.offset,x,fill=str(self.dot_color),width=self.offset))
                #else:
                line.insert(i,self.canvas.create_line(x,y,x+self.offset,y,fill=str(self.dot_color),width=self.offset))
                print(i)
                #obtain cartesian coordinates (preprocessing)
                canvas_x,canvas_y=(x-self.canvas_width/2)+self.offset/2,-y+self.canvas_height/2
                #append new coordinates
                line_coord.insert(i,[canvas_x,canvas_y])
                line_screen_coord.insert(i,[x,y])
                i+=1
                if t==False:
                    y+=dy
                    x=int(m*y+b)
                else:
                    x+=dx
                    y=int(m*x+b)
            if i>1:
                self.line_coord.insert(self.line_count,line_coord)
                self.line_screen_coord.insert(self.line_count,line_screen_coord)
                self.lines.insert(self.line_count,line)
                #enable coordinates text box editing
                self.line_coord_box["state"]="normal"
                #delete last line shown
                self.line_coord_box.delete("end-1l","end")
                #display line coordinates
                self.line_coord_box.insert(INSERT,"line "+str(self.line_count)+": "+str(self.line_coord[self.line_count]))
                #disable coordinates text box editing
                self.line_coord_box["state"]="disabled"
                self.line_count+=1



    #Draw line using Direct Scan Conversion (Modified Slope intercept)
    def draw_line22(self):
        if self.dot_count>1:
            t=True
            line=[]
            line_coord=[]
            line_screen_coord=[]
            #start
            x1,y1=self.dot_screen_coord[self.dot_count-2][0],self.dot_screen_coord[self.dot_count-2][1]
            #end
            x2,y2=self.dot_screen_coord[self.dot_count-1][0],self.dot_screen_coord[self.dot_count-1][1]
            #mod4
            if x2<x1:
                print("x2 < x1")
                t=False
                #swap start and end points
                aux=x1
                x1=x2
                x2=aux
                aux=y1
                y1=y2
                y2=aux
            dx,dy=x2-x1,y2-y1
            #mod2
            if x2==x1:
                if y1>y2:
                    #draw vertical line downwards
                    for y in range(y2,y1):
                        self.canvas.create_line(x2,y,x2+self.offset,y,fill=str(self.dot_color),width=self.offset) ###MAL###
                    return
                else:
                    #draw vertical line upwards
                    for y in range(y1,y2):
                        self.canvas.create_line(x2,y,x2+self.offset,y,fill=str(self.dot_color),width=self.offset) ###MAL###
                    return
            i=0
            #starting point
            line.insert(i,self.canvas.create_line(x1,y1,x1+self.offset,y1,fill=str(self.dot_color),width=self.offset))
            canvas_x,canvas_y=(x1-self.canvas_width/2)+self.offset/2,-y1+self.canvas_height/2
            line_coord.insert(i,[canvas_x,canvas_y])
            line_screen_coord.insert(i,[x1,y1])
            i+=1
            #slope < 1
            if abs(dx)>abs(dy):
                m=dy/dx
                print(m)
                b=y1-m*x1
                dx=-self.offset if dx<0 else self.offset
                while x1<x2:
                    x1+=dx
                    y=mt.floor(m*x1+b)
                    line.insert(i,self.canvas.create_line(x1,y,x1+self.offset,y,fill=str(self.dot_color),width=self.offset))
                    canvas_x,canvas_y=(x1-self.canvas_width/2)+self.offset/2,-y+self.canvas_height/2
                    line_coord.insert(i,[canvas_x,canvas_y])
                    line_screen_coord.insert(i,[x1,y])
                    i+=1
            #slope > 1
            elif dy!=0:
                print("m > 1")
                m=dx/dy
                print(m)
                b=x1-m*y1
                dy=-self.offset if dy<0 else self.offset
                while y1>y2:
                    #print("y1: "+str(y1)+" y2: "+str(y2))
                    y1+=dy
                    x=mt.floor(m*y1+b)
                    line.insert(i,self.canvas.create_line(x,y1,x+self.offset,y1,fill=str(self.dot_color),width=self.offset))
                    canvas_x,canvas_y=(x-self.canvas_width/2)+self.offset/2,-y1+self.canvas_height/2
                    line_coord.insert(i,[canvas_x,canvas_y])
                    line_screen_coord.insert(i,[x,y1])
                    i+=1
            if i>1:
                self.line_coord.insert(self.line_count,line_coord)
                self.line_screen_coord.insert(self.line_count,line_screen_coord)
                self.lines.insert(self.line_count,line)
                #enable coordinates text box editing
                self.line_coord_box["state"]="normal"
                #delete last line shown
                self.line_coord_box.delete("end-1l","end")
                #display line coordinates
                self.line_coord_box.insert(INSERT,"line "+str(self.line_count)+": "+str(self.line_coord[self.line_count]))
                #disable coordinates text box editing
                self.line_coord_box["state"]="disabled"
                self.line_count+=1


    #Draw line using Digital Diferencial Analyzer (DDA)
    def draw_line3(self):
        if self.dot_count>1:
            line=[]
            line_coord=[]
            line_screen_coord=[]
            #start
            x1,y1=self.dot_screen_coord[self.dot_count-2][0],self.dot_screen_coord[self.dot_count-2][1]
            #end
            x2,y2=self.dot_screen_coord[self.dot_count-1][0],self.dot_screen_coord[self.dot_count-1][1]
            #draw the line
            dx,dy=x2-x1,y2-y1
            m=max(abs(dx),abs(dy))
            dxx=(dx/m)
            dyy=(dy/m)
            x,y=x1,y1
            i=0
            while i<=m:
                line.insert(i,self.canvas.create_line(mt.floor(x),mt.floor(y),mt.floor(x)+self.offset,mt.floor(y),fill=str(self.dot_color),width=self.offset))
                #obtain cartesian coordinates (preprocessing)
                canvas_x,canvas_y=(x-self.canvas_width/2)+self.offset/2,-y+self.canvas_height/2
                #append new coordinates
                line_coord.insert(i,[mt.floor(canvas_x),mt.floor(canvas_y)])
                line_screen_coord.insert(i,[mt.floor(x),mt.floor(y)])
                x+=dxx
                y+=dyy
                i+=1
            if i>1:
                self.line_coord.insert(self.line_count,line_coord)
                self.line_screen_coord.insert(self.line_count,line_screen_coord)
                self.lines.insert(self.line_count,line)
                #enable coordinates text box editing
                self.line_coord_box["state"]="normal"
                #delete last line shown
                self.line_coord_box.delete("end-1l","end")
                #display line coordinates
                self.line_coord_box.insert(INSERT,"line "+str(self.line_count)+": "+str(self.line_coord[self.line_count]))
                #disable coordinates text box editing
                self.line_coord_box["state"]="disabled"
                self.line_count+=1

    #Draw line using Bresenham's Algorithm
    def draw_line4(self):
        return None


    #select a line and display its coordinates
    def select_line(self,event):
        x=event.x
        y=event.y
        if self.line_count>0:
            for i in range(len(self.line_screen_coord)):
                print(i)
                for j in range(len(self.line_screen_coord[i])):
                    x0,y0=self.line_screen_coord[i][j][0],self.line_screen_coord[i][j][1]
                    print(j,x0,y0)
                    print(x,y)
                    if x0==x and y0==y:
                        for k in range(len(self.lines[i])):
                            self.canvas.delete(self.lines[i][k])
                    elif x0==x and y0==y+1:
                        for k in range(len(self.lines[i])):
                            self.canvas.delete(self.lines[i][k])
                    elif x0==x+1 and y0==y:
                        for k in range(len(self.lines[i])):
                            self.canvas.delete(self.lines[i][k])
                    elif x0==x+1 and y0==y+1:
                        for k in range(len(self.lines[i])):
                            self.canvas.delete(self.lines[i][k])
                    elif x0==x and y0==y-1:
                        for k in range(len(self.lines[i])):
                            self.canvas.delete(self.lines[i][k])
                    elif x0==x-1 and y0==y:
                        for k in range(len(self.lines[i])):
                            self.canvas.delete(self.lines[i][k])
                    elif x0==x-1 and y0==y-1:
                        for k in range(len(self.lines[i])):
                            self.canvas.delete(self.lines[i][k])

    #display a text box to show dot coordinates
    def display_dot_coordinates(self,x,y,h,w):
        #set text box for dot Coordinates
        self.dot_coord_box=self.set_text("",x,y,h,w)
        yscrollbar=Scrollbar(self.win,orient=VERTICAL,command=self.dot_coord_box.yview)
        yscrollbar.place(x=x+203,y=y,height=h+304,width=w-7)
        self.dot_coord_box["yscrollcommand"]=yscrollbar.set

    #display a text box to show line coordinates
    def display_line_coordinates(self,x,y,h,w):
        #set text box for line Coordinates
        self.line_coord_box=self.set_text("",x,y,h,w)
        xscrollbar=Scrollbar(self.win,orient=HORIZONTAL,command=self.line_coord_box.xview)
        xscrollbar.place(x=x,y=y+19,height=h+10,width=w+1124)
        self.line_coord_box["xscrollcommand"]=xscrollbar.set
        self.line_coord_box["wrap"]="none"

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
        self.dot_coord_box["state"]="normal"
        self.dot_coord_box.delete(0.0,"end-1c")
        self.dot_coord_box["state"]="disabled"
        self.line_coord_box["state"]="normal"
        self.line_coord_box.delete(0.0,"end-1c")
        self.line_coord_box["state"]="disabled"
        self.dot_size_box["state"]="normal"
        self.dot_size_box.delete(0.0,"end-1c")
        self.dot_color=DOT_COLOR
        self.offset=OFFSET
        self.dot_count=0
        self.line_count=0

    #delete the last dot drawn
    def delete_last_dot(self):
        if self.dot_count>0:
            self.canvas.delete(self.dots[self.dot_count-1])
            self.dot_coord_box["state"]="normal"
            self.dot_coord_box.delete("end-2l","end-1l")
            self.dot_coord_box["state"]="disabled"
            self.dot_coord.pop(self.dot_count-1)
            self.dots.pop(self.dot_count-1)
            self.dot_count-=1

    #delete the las line drawn
    def delete_last_line(self):
        if self.line_count>0:
            for i in range(len(self.lines[self.line_count-1])):
                self.canvas.delete(self.lines[self.line_count-1][i])
            self.line_coord_box["state"]="normal"
            self.line_coord_box.delete(0.0,"end-1c")
            #display, if exists, previous line coordinates
            if self.line_count>1:
                self.line_coord_box.insert(INSERT,"line "+str(self.line_count-2)+": "+str(self.line_coord[self.line_count-2]))
            self.line_coord_box["state"]="disabled"
            self.lines.pop(self.line_count-1)
            self.line_count-=1

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
        self.set_label("Coordinates",1060,5)
        #display text box for coordinates
        self.display_dot_coordinates(1060,35,20,25)
        #display text box for line Coordinates
        self.display_line_coordinates(10,693,1,160)
        #button -change dot color-
        self.set_button("Dot color",self.change_dot_color,1060,380,1,10)
        #button -change dot size-
        self.set_button("Dot size",self.change_dot_size,1060,420,1,10)
        #display text box for dot size change
        self.display_dot_size_box(1150,423,1,2)
        #button -delete last dot-
        self.set_button("Delete dot",self.delete_last_dot,1060,460,1,10)
        #button -delete last line-
        self.set_button("Delete line",self.delete_last_line,1060,500,1,10)
        #button -clear canvas-
        self.set_button("Delete all",self.clear_canvas,1060,540,1,10)
        #button -line 1- Draw line using Direct Scan Conversion (Normal Slope intercept)
        self.set_button("Line 1",self.draw_line1,1198,380,1,10)
        #button -line 2- Draw line using Direct Scan Conversion (Modified Slope intercept)
        self.set_button("Line 2",self.draw_line22,1198,420,1,10)
        #button -line 3- Draw line using Digital Diferencial Analyzer (DDA)
        self.set_button("Line 3",self.draw_line3,1198,460,1,10)
        #button -line 4- Draw line using Bresenham's Algorithm
        self.set_button("Line 4",self.draw_line4,1198,500,1,10)
        #button -close-
        self.set_button("Exit",self.close,1130,650,1,10)
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
