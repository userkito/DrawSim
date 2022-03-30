'''
#####DrawSim#####

A drawing simulator to set dots and draw lines
on a canvas and display their cartesian coordinates.

Version: 1.0
Author: user_Kito
Date: 15/09/2021
'''

#askopenfile

from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter.filedialog import asksaveasfile
import math as mt

CANVAS_WIDTH=1086
CANVAS_HEIGHT=680
WINDOW_SIZE="1350x730"
DOT_COLOR="black" #default
OFFSET=3 #number of pixels on each side of the pixel's square (OFFSET**2 pixels in the square) (default 3 -> 9 pixel square)

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
        #shortcuts
        self.win.bind("<Control-s>",self.save_e)
        self.win.bind("<Control-x>",self.close_e)
        #set size of the window
        self.win.geometry(WINDOW_SIZE)
        #set the dot color (default black)
        self.dot_color=DOT_COLOR
        #set the offset
        self.offset=OFFSET

    #translate canvas coordinates to cartesian
    def preprocess(self,x,y):
        cart_x,cart_y=x-self.canvas_width/2,-y+self.canvas_height/2
        return cart_x,cart_y

    #activate a square of side offset pixels with center x y
    def dot(self,x,y):
        return self.canvas.create_line(x-self.offset/2,y,x+self.offset/2,y,fill=str(self.dot_color),width=self.offset)

    #draw and add a new dot and display its coordinates
    def add_dot(self,x,y):
        #Draw a dot in the given coordinates
        self.dots.insert(self.dot_count,self.dot(x,y))
        #obtain cartesian coordinates (preprocessing)
        cart_x,cart_y=self.preprocess(x,y)
        #append new coordinates
        self.dot_coord.insert(self.dot_count,[cart_x,cart_y])
        self.dot_screen_coord.insert(self.dot_count,[x,y])
        #enable coordinates text box editing
        self.dot_coord_box["state"]="normal"
        #show coordinates
        self.dot_coord_box.insert(INSERT,"Dot:"+str(self.dot_count)+" x:"+str(self.dot_coord[self.dot_count][0])+" y:"+str(self.dot_coord[self.dot_count][1])+"\n")
        self.dot_coord_box.see("end-2l")
        #disable coordinates text box editing
        self.dot_coord_box["state"]="disabled"
        self.dot_count+=1

    #function to draw a dot (fill pixels) in canvas at mouse click and save its coordinates
    def draw_dot(self,event):
        x,y=event.x,event.y
        self.add_dot(x,y)

    #get the coordinates of the last two dots in the canvas
    def line(self):
        #start
        x1,y1=self.dot_screen_coord[self.dot_count-2][0],self.dot_screen_coord[self.dot_count-2][1]
        #end
        x2,y2=self.dot_screen_coord[self.dot_count-1][0],self.dot_screen_coord[self.dot_count-1][1]
        return x1,y1,x2,y2

    #add a new line and display its coordinates
    def add_line(self,line,line_coord,line_screen_coord):
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

    #Draw line using Direct Scan Conversion (original Slope intercept)
    def draw_line1(self):
        if self.dot_count>1:
            line=[]
            line_coord=[]
            line_screen_coord=[]
            #get the start and end points
            x1,y1,x2,y2=self.line()
            dx,dy=x2-x1,y2-y1
            m=dy/dx
            b=y1-m*x1
            x,y=x1,y1
            i=0
            while x<=x2:
                line.insert(i,self.dot(x,y))
                canvas_x,canvas_y=self.preprocess(x,y)
                line_coord.insert(i,[canvas_x,canvas_y])
                line_screen_coord.insert(i,[x,y])
                x+=1
                y=int(m*x+b)
                i+=1
            if i>1:
                self.add_line(line,line_coord,line_screen_coord)

    #Draw line using Direct Scan Conversion (Modified Slope intercept)
    def draw_line2(self):
        if self.dot_count>1:
            line=[]
            line_coord=[]
            line_screen_coord=[]
            #get the start and end points
            x1,y1,x2,y2=self.line()
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
            dx,dy=x2-x1,y2-y1
            #mod2
            i=0
            if x2==x1:
                if y1>y2:
                    #draw vertical line downwards
                    for y in range(y2,y1):
                        line.insert(i,self.dot(x2,y))
                        canvas_x,canvas_y=self.preprocess(x2,y)
                        line_coord.insert(i,[canvas_x,canvas_y])
                        line_screen_coord.insert(i,[x2,y])
                        i+=1
                    if i>1:
                        self.add_line(line,line_coord,line_screen_coord)
                    return
                else:
                    #draw vertical line upwards
                    for y in range(y1,y2):
                        line.insert(i,self.dot(x2,y))
                        canvas_x,canvas_y=self.preprocess(x2,y)
                        line_coord.insert(i,[canvas_x,canvas_y])
                        line_screen_coord.insert(i,[x2,y])
                        i+=1
                    if i>1:
                        self.add_line(line,line_coord,line_screen_coord)
                    return
            i=0
            #starting point
            line.insert(i,self.dot(x1,y1))
            canvas_x,canvas_y=self.preprocess(x1,y1)
            line_coord.insert(i,[canvas_x,canvas_y])
            line_screen_coord.insert(i,[x1,y1])
            i+=1
            #slope < 1
            if abs(dx)>abs(dy):
                m=dy/dx
                b=y1-m*x1
                x=x1
                #dxx=-self.offset if dx<0 else self.offset
                dx=-1 if dx<0 else 1
                while x1!=x2:
                    #x+=dx
                    #if x%self.offset==0:
                    x1+=dx
                    y=mt.floor(m*x1+b)
                    line.insert(i,self.dot(x1,y))
                    canvas_x,canvas_y=self.preprocess(x1,y)
                    line_coord.insert(i,[canvas_x,canvas_y])
                    line_screen_coord.insert(i,[x1,y])
                    i+=1
            #slope > 1
            elif dy!=0:
                m=dx/dy
                b=x1-m*y1
                y=y1
                #dyy=-self.offset if dy<0 else self.offset
                dy=-1 if dy<0 else 1
                while y1!=y2:
                    #y+=dy
                    #if y%self.offset==0:
                    y1+=dy
                    x=mt.floor(m*y1+b)
                    line.insert(i,self.dot(x,y1))
                    canvas_x,canvas_y=self.preprocess(x,y1)
                    line_coord.insert(i,[canvas_x,canvas_y])
                    line_screen_coord.insert(i,[x,y1])
                    i+=1
            #ending point
            line.insert(i,self.dot(x2,y2))
            canvas_x,canvas_y=self.preprocess(x2,y2)
            line_coord.insert(i,[canvas_x,canvas_y])
            line_screen_coord.insert(i,[x2,y2])
            if i>1:
                self.add_line(line,line_coord,line_screen_coord)

    #Draw line using Digital Diferencial Analyzer (DDA)
    def draw_line3(self):
        if self.dot_count>1:
            line=[]
            line_coord=[]
            line_screen_coord=[]
            #get the start and end points
            x1,y1,x2,y2=self.line()
            dx,dy=x2-x1,y2-y1
            m=max(abs(dx),abs(dy))
            if m!=0:
                dxx=(dx/m)
                dyy=(dy/m)
            x,y=x1,y1
            i=0
            while i<=m:
                line.insert(i,self.dot(mt.floor(x),mt.floor(y)))
                canvas_x,canvas_y=self.preprocess(x,y)
                line_coord.insert(i,[mt.floor(canvas_x),mt.floor(canvas_y)])
                line_screen_coord.insert(i,[mt.floor(x),mt.floor(y)])
                x+=dxx
                y+=dyy
                i+=1
            if i>1:
                self.add_line(line,line_coord,line_screen_coord)

    #Draw line using Bresenham's Algorithm
    def draw_line4(self):
        if self.dot_count>1:
            t=False
            line=[]
            line_coord=[]
            line_screen_coord=[]
            #get the start and end points
            x1,y1,x2,y2=self.line()
            #mod 4
            if x2<x1:
                print("x2 < x1")
                t=True
                #swap start and end points
                aux=x1
                x1=x2
                x2=aux
                aux=y1
                y1=y2
                y2=aux
            dx,dy=abs(x2-x1),abs(y2-y1)
            #m=-(dy/dx)
            #e=m-0.5
            e=2*(dy-dx)
            x,y=x1,y1
            #increment or decrement x and y due to line position
            dxx,dyy=-1 if dx<0 else 1,-1 if dy>0 else 1
            if t==True and y1<y2:
                dyy=-1 if dy<0 else 1
            elif y1<y2:
                dyy=-1 if dy<0 else 1
            '''
            #increment or decrement x and y due to line position
            dxx,dyy=-self.offset if dx<0 else self.offset,-self.offset if dy>0 else self.offset
            if t==True and y1<y2:
                dyy=-self.offset if dy<0 else self.offset
            elif y1<y2:
                dyy=-self.offset if dy<0 else self.offset
            '''
            i=0
            while i<=dx:
                line.insert(i,self.dot(x,y))
                canvas_x,canvas_y=self.preprocess(x,y)
                line_coord.insert(i,[canvas_x,canvas_y])
                line_screen_coord.insert(i,[x,y])
                while e>0:
                    y+=dyy
                    e-=2*dx
                x+=dxx
                e+=2*dy
                i+=1
            if i>1:
                self.add_line(line,line_coord,line_screen_coord)

    #draw a line given its coordinates
    def draw_line_coordinated(self):
        #line algorithm (1-4)
        t=int(self.box_t.get(0.0,END))
        x1=int(self.box_x1.get(0.0,END))
        y1=int(self.box_y1.get(0.0,END))
        self.add_dot(x1+self.canvas_width/2,-y1+self.canvas_height/2)
        x2=int(self.box_x2.get(0.0,END))
        y2=int(self.box_y2.get(0.0,END))
        self.add_dot(x2+self.canvas_width/2,-y2+self.canvas_height/2)
        if t==1:
            self.draw_line1()
        elif t==2:
            self.draw_line2()
        elif t==3:
            self.draw_line3()
        elif t==4:
            self.draw_line4()
        else:
            return

    #set a canvas on tkinter window on x y coordinates
    def set_canvas(self,x,y):
        #set canvas
        self.canvas=Canvas(self.win,width=self.canvas_width,height=self.canvas_height,relief=RAISED,bd=2,bg="white")
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

    #select a line and delete it (or whatever)
    def select_line(self,event):
        x,y=event.x,event.y
        if self.line_count>0:
            for i in range(len(self.line_screen_coord)):
                for j in range(len(self.line_screen_coord[i])):
                    x0,y0=self.line_screen_coord[i][j][0],self.line_screen_coord[i][j][1]
                    p=0
                    while p<self.offset*2:
                        if x0==x and y0==y or x0==x and y0==y+p or x0==x+p and y0==y or x0==x+p and y0==y+p or x0==x and y0==y-p or x0==x-p and y0==y or x0==x-p and y0==y-p:
                            for k in range(len(self.lines[i])):
                                self.canvas.delete(self.lines[i][k])
                        p+=1

    #display dot coordinates in a text box
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
        xscrollbar.place(x=x,y=y+19,height=h+10,width=w+1159)
        self.line_coord_box["xscrollcommand"]=xscrollbar.set
        self.line_coord_box["wrap"]="none"

    #get the start and end points of the line
    def display_line_coordinates_boxes(self,x,y,h,w):
        self.box_t=self.set_text("",x+130,y-27,h,w-2)
        self.box_x1=self.set_text("",x+30,y,h,w)
        self.box_y1=self.set_text("",x+60,y,h,w)
        self.box_x2=self.set_text("",x+96,y,h,w)
        self.box_y2=self.set_text("",x+126,y,h,w)

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
        self.box_t.delete(0.0,"end-1c")
        self.box_x1.delete(0.0,"end-1c")
        self.box_y1.delete(0.0,"end-1c")
        self.box_x2.delete(0.0,"end-1c")
        self.box_y2.delete(0.0,"end-1c")
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
            self.lines.pop(self.line_count-1)
            self.line_count-=1
            #display, if exists, previous line coordinates
            if self.line_count>0:
                self.line_coord_box.insert(INSERT,"line "+str(self.line_count-1)+": "+str(self.line_coord[self.line_count-1]))
            self.line_coord_box["state"]="disabled"


    #save canvas as a file
    def save(self):
        if self.line_count>0:
            files=[("All Files","*.*"),("Python Files","*.py"),("Text Document","*.txt"),("Image","*.jpg"),("Image","*.png")]
            file=asksaveasfile(filetypes=files,defaultextension=files)
            for i in range(self.line_count):
                if file!=None:
                    file.write("Line "+str(i)+":\n"+str(self.line_screen_coord[i])+"\n\n")

    #save canvas as a file (shortcut version)
    def save_e(self,e):
        if self.line_count>0:
            files=[("All Files","*.*"),("Python Files","*.py"),("Text Document","*.txt"),("Image","*.jpg"),("Image","*.png")]
            file=asksaveasfile(filetypes=files,defaultextension=files)
            for i in range(self.line_count):
                if file!=None:
                    file.write("Line "+str(i)+":\n"+str(self.line_screen_coord[i])+"\n\n")

    #end simulation
    def close(self):
        self.win.destroy()

    #end simulation (shortcut version)
    def close_e(self,e):
        self.win.destroy()

    #execute simulator
    def run(self):
        self.win.mainloop()

    def create_DrawSim_Gui(self):
        #place canvas on top left corner of tkinter window
        self.set_canvas(1,1)
        #axis in canvas
        self.display_axis()
        #label -coordinates-
        self.set_label("Coordinates",1110,5)
        #display text box for coordinates
        self.display_dot_coordinates(1110,35,20,25)
        #display text box for line Coordinates
        self.display_line_coordinates(10,693,1,165)
        #button -change dot color-
        self.set_button("Dot color",self.change_dot_color,1110,380,1,10)
        #button -change dot size-
        self.set_button("Dot size",self.change_dot_size,1110,420,1,10)
        #display text box for dot size change
        self.display_dot_size_box(1196,423,1,2)
        #button -delete last dot-
        self.set_button("Delete dot",self.delete_last_dot,1110,460,1,10)
        #button -delete last line-
        self.set_button("Delete line",self.delete_last_line,1110,500,1,10)
        #button -clear canvas-
        self.set_button("Delete all",self.clear_canvas,1110,540,1,10)
        #button -save as file-
        self.set_button("Save lines",self.save,1110,580,1,10)
        #button -line 1- Draw line using Direct Scan Conversion (Normal Slope intercept)
        self.set_button("Line 1",self.draw_line1,1248,380,1,10)
        #button -line 2- Draw line using Direct Scan Conversion (Modified Slope intercept)
        self.set_button("Line 2",self.draw_line2,1248,420,1,10)
        #button -line 3- Draw line using Digital Diferencial Analyzer (DDA)
        self.set_button("Line 3",self.draw_line3,1248,460,1,10)
        #button -line 4- Draw line using Bresenham's Algorithm
        self.set_button("Line 4",self.draw_line4,1248,500,1,10)
        #button -line coordinated- draw a line given its start and end points
        self.set_button("Line",self.draw_line_coordinated,1248,540,1,8)
        #display boxes to get line details
        self.display_line_coordinates_boxes(1190,570,1,3)
        #button -close-
        self.set_button("Exit",self.close,1180,650,1,10)
        #run simulator
        self.run()

#main
ds=DrawSim()

ds.create_DrawSim_Gui()
