'''
####################################################################################
####################################···DrawSim···###################################
####################################################################################

A drawing simulator to set dots and draw lines
on a canvas and display their cartesian coordinates.

It can also perform various transformations on lines.

Version: 2.0
Author: Nicolás Rodrigo Pérez
Date: 14/10/2021
'''

from tkinter import *
from tkinter.colorchooser import askcolor
from tkinter.filedialog import asksaveasfile
import math as mt

CANVAS_WIDTH=1086
CANVAS_HEIGHT=646
WINDOW_SIZE="1350x700"
DOT_COLOR="black" #default
OFFSET=3 #pixels on each side of the pixel's square (OFFSET**2 pixels in the square) (default 3 -> 9 pixel square)

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
        self.dot_order=0
        self.dot_coord_box=None
        #---lines---#
        #cartesian coordinates
        self.line_coord=[]
        #coordinates refered to the top left corner
        self.line_screen_coord=[]
        self.lines=[]
        self.selected_lines=[]
        self.line_count=0
        self.line_coord_box=None
        #---Shapes---#
        #cartesian coordinates
        self.shape_coord=[]
        #coordinates refered to the top left corner
        self.shape_screen_coord=[]
        self.shapes=[]
        self.shape_count=0
        #canvas size
        self.canvas_width=CANVAS_WIDTH
        self.canvas_height=CANVAS_HEIGHT
        #instance of tkinter window
        self.win=Tk()
        self.win.title("DrawSim2.0")
        self.win.resizable(True,True)
        #main window shortcuts
        self.win.bind("<Control-s>",self.save_e)
        self.win.bind("<Control-x>",self.close_e)
        #set size of the window
        self.win.geometry(WINDOW_SIZE)
        #set the dot color (default black)
        self.dot_color=DOT_COLOR
        #set the offset
        self.offset=OFFSET
        #scale variable
        self.scale=IntVar()
        #rotation
        self.ccw=IntVar()
        #reflexion
        self.x=IntVar()
        self.y=IntVar()
        self.r=IntVar()

    #offset getter
    def get_offset(self):
        return self.offset

    #dot count getter
    def get_dot_count(self):
        return self.dot_count

    #scale getter
    def get_scale(self):
        return self.scale.get()

    #ccw getter
    def get_ccw(self):
        return self.ccw.get()

    #x getter
    def get_x(self):
        return self.x.get()

    #y getter
    def get_y(self):
        return self.y.get()

    #r getter
    def get_r(self):
        return self.r.get()

    #translate canvas coordinates to cartesian
    def preprocess(self,x,y):
        cart_x,cart_y=x-self.canvas_width/2,-y+self.canvas_height/2
        return cart_x,cart_y

    #activate a square of side offset pixels with center x y on canvas
    def dot(self,x,y):
        return self.canvas.create_line(x-self.offset/2,y,x+self.offset/2,y,fill=str(self.dot_color),width=self.offset)

    #draw and add a new dot to the system and display its coordinates
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

    #draw a dot given its coordinates
    def draw_dot_coordinated(self):
        x=int(self.box_x.get(0.0,END))
        y=int(self.box_y.get(0.0,END))
        self.add_dot(x+self.canvas_width/2,-y+self.canvas_height/2)
        self.box_x.delete(0.0,END)
        self.box_y.delete(0.0,END)

    #get the coordinates of the last two dots in the canvas
    def line(self):
        #start
        x1,y1=self.dot_screen_coord[self.dot_count-2][0],self.dot_screen_coord[self.dot_count-2][1]
        #end
        x2,y2=self.dot_screen_coord[self.dot_count-1][0],self.dot_screen_coord[self.dot_count-1][1]
        return x1,y1,x2,y2

    #add a new line to the system and display its coordinates
    def add_line(self,line,line_coord,line_screen_coord):
        self.lines.insert(self.line_count,line)
        self.line_coord.insert(self.line_count,line_coord)
        self.line_screen_coord.insert(self.line_count,line_screen_coord)
        #enable coordinates text box editing
        self.line_coord_box["state"]="normal"
        #delete last line shown
        self.line_coord_box.delete("end-1l","end")
        #display line coordinates
        self.line_coord_box.insert(INSERT,"line "+str(self.line_count)+": "+str(self.line_coord[self.line_count]))
        #disable coordinates text box editing
        self.line_coord_box["state"]="disabled"
        #if scale enabled we need to delete start and endig points for great visualization
        if self.get_scale()==1:
            self.delete_last_dot()
            self.delete_last_dot()
        self.line_count+=1

    def add_shape(self):
        if self.line_count!=0:
            shape=[]
            shape_coord=[]
            shape_screen_coord=[]
            i=0
            for line in self.selected_lines:
                for dot in self.line_screen_coord[line]:
                    shape.insert(i,self.dot(dot[0],dot[1]))
                    canvas_x,canvas_y=self.preprocess(dot[0],dot[1])
                    shape_coord.insert(i,[canvas_x,canvas_y])
                    shape_screen_coord.insert(i,[dot[0],dot[1]])
                    i+=1
            for line in self.selected_lines:
                #delete lines which conform the shape
                self.delete_last_line()

                self.delete_last_dot()
                self.delete_last_dot()

            #to perform 2d transforms on shapes we need to add them as lines
            self.lines.append(shape)
            self.line_coord.append(shape_coord)
            self.line_screen_coord.append(shape_screen_coord)
            self.line_count+=1
            self.shapes.append(shape)
            self.shape_coord.append(shape_coord)
            self.shape_screen_coord.append(shape_screen_coord)
            #enable coordinates text box editing
            self.line_coord_box["state"]="normal"
            #delete last line shown
            self.line_coord_box.delete("end-1l","end")
            #display line coordinates
            self.line_coord_box.insert(INSERT,"Shape "+str(self.shape_count)+": "+str(self.shape_coord[self.shape_count]))
            #disable coordinates text box editing
            self.line_coord_box["state"]="disabled"
            print("New shape of lines: "+str(self.selected_lines)+" shape count: "+str(self.shape_count))
            self.shape_count+=1

    #select a line and delete it (or whatever)
    def select_line(self,event):
        x,y=event.x,event.y
        index=0
        if self.line_count>0:
            for i in range(len(self.line_screen_coord)):
                for j in range(len(self.line_screen_coord[i])):
                    x0,y0=self.line_screen_coord[i][j][0],self.line_screen_coord[i][j][1]
                    p=0
                    while p<self.offset*3:
                        if x0==x and y0==y or x0==x and y0==y+p or x0==x+p and y0==y or x0==x+p and y0==y+p or x0==x and y0==y-p or x0==x-p and y0==y or x0==x-p and y0==y-p:
                            for k in range(len(self.lines[i])):
                                #line=self.lines[i][k]
                                index=i
                        p+=1
            self.selected_lines.append(index)
            print("line "+str(index)+" selected")
            print("lines "+str(self.selected_lines))

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
    def set_label(self,content,x,y,size):
        label=Label(self.win,text=str(content),font=(None, size))
        label.place(x=x,y=y)
        return label

    #set text box on gui on x y coordinates
    def set_text(self,text,x,y,h,w):
        t=Text(self.win,height=h,width=w)
        t.place(x=x,y=y)
        t.insert(1.0,text)
        return t

    #set checkbox on gui on x y coordinates63
    def set_checkbox(self,text,variable,x,y):
        checkbox=Checkbutton(self.win,text=text,variable=variable,onvalue=1,offvalue=0)
        checkbox.place(x=x,y=y)
        return checkbox

    #display dot coordinates in a text box
    def display_dot_coordinates(self,x,y,h,w):
        #set text box for dot Coordinates
        self.dot_coord_box=self.set_text("",x,y,h,w)
        yscrollbar=Scrollbar(self.win,orient=VERTICAL,command=self.dot_coord_box.yview)
        yscrollbar.place(x=x+203,y=y,height=h+79,width=w-7)
        self.dot_coord_box["yscrollcommand"]=yscrollbar.set
        self.dot_coord_box["state"]="disabled"

    #display a text box to show line coordinates
    def display_line_coordinates(self,x,y,h,w):
        #set text box for line Coordinates
        self.line_coord_box=self.set_text("",x,y,h,w)
        xscrollbar=Scrollbar(self.win,orient=HORIZONTAL,command=self.line_coord_box.xview)
        xscrollbar.place(x=x,y=y+19,height=h+10,width=w+1159)
        self.line_coord_box["xscrollcommand"]=xscrollbar.set
        self.line_coord_box["wrap"]="none"
        self.line_coord_box["state"]="disabled"

    #get the start and end points of the line
    def display_dot_coordinated_boxes(self,x,y,h,w):
        self.set_label("x:",x,y,10)
        self.box_x=self.set_text("",x+15,y,h,w)
        self.set_label("y:",x+45,y,10)
        self.box_y=self.set_text("",x+60,y,h,w)
        #move from x coord box to y coord box using tab
        self.box_x.bind("<Tab>",self.move_cursor_y)
        #move from y coord box to x coord box using tab
        self.box_y.bind("<Tab>",self.move_cursor_x)

    #get the traslation quanntity in x and y
    def display_tras_coord_boxes(self,x,y,h,w):
        self.set_label("x:",x,y,10)
        self.box_tras_x=self.set_text("",x+15,y,h,w)
        self.set_label("y:",x+45,y,10)
        self.box_tras_y=self.set_text("",x+60,y,h,w)
        #move from x coord box to y coord box using tab
        self.box_tras_x.bind("<Tab>",self.move_cursor_y)
        #move from y coord box to x coord box using tab
        self.box_tras_y.bind("<Tab>",self.move_cursor_x)

    #get the traslation quanntity in x and y
    def display_esc_coord_boxes(self,x,y,h,w):
        self.set_label("x:",x,y,10)
        self.box_esc_x=self.set_text("",x+15,y,h,w)
        self.set_label("y:",x+45,y,10)
        self.box_esc_y=self.set_text("",x+60,y,h,w)
        #move from x coord box to y coord box using tab
        self.box_esc_x.bind("<Tab>",self.move_cursor_y)
        #move from y coord box to x coord box using tab
        self.box_esc_y.bind("<Tab>",self.move_cursor_x)

    #get the traslation quanntity in x and y
    def display_rot_coord_box(self,x,y,h,w):
        self.set_label("\u03B1:",x,y,10)
        self.box_rot=self.set_text("",x+15,y,h,w)

    #get the shearing details in x and y
    def display_ciz_coord_boxes(self,x,y,h,w):
        self.set_label("x:",x,y,10)
        self.box_ciz_x=self.set_text("",x+15,y,h,w)
        self.set_label("y:",x+45,y,10)
        self.box_ciz_y=self.set_text("",x+60,y,h,w)
        #move from x coord box to y coord box using tab
        self.box_ciz_x.bind("<Tab>",self.move_cursor_y)
        #move from y coord box to x coord box using tab
        self.box_ciz_y.bind("<Tab>",self.move_cursor_x)

    #get the reflexion details
    def display_ref_coord_boxes(self,x,y,h,w):
        self.set_label("m:",x,y,10)
        self.box_m=self.set_text("",x+18,y,h,w)
        self.set_label("b:",x+45,y,10)
        self.box_b=self.set_text("",x+60,y,h,w)
        #move from x coord box to y coord box using tab
        self.box_m.bind("<Tab>",self.move_cursor_y)
        #move from y coord box to x coord box using tab
        self.box_b.bind("<Tab>",self.move_cursor_x)

    #move from x coord box to y coord box
    def move_cursor_y(self,event):
        event.widget.tk_focusNext().focus()
        return("break")

    #move from y coord box to x coord box
    def move_cursor_x(self,event):
        event.widget.tk_focusPrev().focus()
        return("break")

    #display a text box to retrieve new dot size
    def display_dot_size_box(self,x,y,h,w):
        #set text box to get new size
        self.dot_size_box=self.set_text(str(self.offset),x,y,h,w)

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
        self.prev_offset=self.offset
        size=self.dot_size_box.get(0.0,END)
        if size!="\n":
            self.offset=int(size)

    #clear the drawing area (canvas)
    def clear_canvas(self):
        self.canvas.delete(ALL)
        self.display_axis() #XD
        self.dot_coord_box["state"]="normal"
        self.dot_coord_box.delete(0.0,END)
        self.dot_coord_box["state"]="disabled"
        self.line_coord_box["state"]="normal"
        self.line_coord_box.delete(0.0,END)
        self.line_coord_box["state"]="disabled"
        self.dot_size_box["state"]="normal"
        self.box_x.delete(0.0,END)
        self.box_y.delete(0.0,END)
        self.box_tras_x.delete(0.0,END)
        self.box_tras_y.delete(0.0,END)
        self.box_esc_x.delete(0.0,END)
        self.box_esc_y.delete(0.0,END)
        self.box_rot.delete(0.0,END)
        self.lines.clear()
        self.line_coord.clear()
        self.line_screen_coord.clear()
        self.dots.clear()
        self.dot_coord.clear()
        self.dot_screen_coord.clear()
        self.selected_lines.clear()
        self.dot_count=0
        self.line_count=0
        self.shape_count=0

    #delete a dot drawn
    def delete_dot(self,index):
        if self.dot_count>0:
            self.canvas.delete(self.dots[index])
            self.dot_coord_box["state"]="normal"
            self.dot_coord_box.delete("end-"+str(index-1)+"l","end-"+str(index+1)+"l")
            self.dot_coord_box["state"]="disabled"
            self.dots.pop(index)
            self.dot_coord.pop(index)
            self.dot_screen_coord.pop(index)
            self.dot_count-=1

    #delete the last dot drawn
    def delete_last_dot(self):
        if self.dot_count>0:
            self.canvas.delete(self.dots[self.dot_count-1])
            self.dot_coord_box["state"]="normal"
            self.dot_coord_box.delete("end-2l","end-1l")
            self.dot_coord_box["state"]="disabled"
            self.dots.pop(self.dot_count-1)
            self.dot_coord.pop(self.dot_count-1)
            self.dot_screen_coord.pop(self.dot_count-1)
            self.dot_count-=1

    #delete the las line drawn
    def delete_last_line(self):
        if self.line_count>0:
            for i in range(len(self.lines[self.line_count-1])):
                self.canvas.delete(self.lines[self.line_count-1][i])
            self.line_coord_box["state"]="normal"
            self.line_coord_box.delete(0.0,"end-1c")
            self.lines.pop(self.line_count-1)
            self.line_coord.pop(self.line_count-1)
            self.line_screen_coord.pop(self.line_count-1)
            #display, if exists, previous line coordinates
            if self.line_count>1:
                self.line_coord_box.insert(INSERT,"line "+str(self.line_count-2)+": "+str(self.line_coord[self.line_count-2]))
            self.line_coord_box["state"]="disabled"
            self.line_count-=1

    #delete the las shape drawn
    def delete_last_shape(self):
        if self.shape_count>0:
            for i in range(len(self.shapes[self.shape_count-1])):
                self.canvas.delete(self.shapes[self.shape_count-1][i])
            self.line_coord_box["state"]="normal"
            self.line_coord_box.delete(0.0,"end-1c")
            self.shapes.pop(self.shape_count-1)
            self.shape_coord.pop(self.shape_count-1)
            self.shape_screen_coord.pop(self.shape_count-1)
            #display, if exists, previous line coordinates
            if self.line_count>1:
                self.line_coord_box.insert(INSERT,"line "+str(self.line_count-2)+": "+str(self.line_coord[self.line_count-2]))
            self.line_coord_box["state"]="disabled"
            self.selected_lines.clear()
            self.shape_count-=1

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

    #main function to create DrawSim gui
    def create_DrawSim_Gui(self):
        #place canvas on top left corner of tkinter window
        self.set_canvas(1,1)
        #axis in canvas
        self.display_axis()
        #display text box for coordinates
        self.display_dot_coordinates(1110,10,5,25)
        #display text box for line Coordinates
        self.display_line_coordinates(10,662,1,165)
        #display boxes to get line details
        self.display_dot_coordinated_boxes(1106,103,1,3)
        #button -draw dot coordinated-
        self.set_button("Dot",self.draw_dot_coordinated,1110,130,1,10)
        #display text box for dot size change
        self.display_dot_size_box(1110,173,1,2)
        #button -change dot size-
        self.set_button("Size",self.change_dot_size,1138,170,1,6)
        #button -change dot color-
        self.set_button("Dot color",self.change_dot_color,1110,210,1,10)
        #button -delete last dot-
        self.set_button("Delete dot",self.delete_last_dot,1110,250,1,10)
        #button -delete last line-
        self.set_button("Delete line",self.delete_last_line,1110,290,1,10)
        #button -clear canvas-
        self.set_button("Delete all",self.clear_canvas,1110,330,1,10)
        #button -save as file-
        self.set_button("Save lines",self.save,1110,370,1,10)
        #button -add new shape-
        self.set_button("Shape",self.add_shape,1110,410,1,10)
        #button -delete last shape-
        self.set_button("Delete shape",self.delete_last_shape,1110,450,1,10)
        #label line algorithms
        self.set_label("Line Algorithms",1239,102,10)
        #button -line 1- Draw line using Direct Scan Conversion (Normal Slope intercept)
        self.set_button("Line 1",self.draw_line1,1248,130,1,10)
        #button -line 2- Draw line using Direct Scan Conversion (Modified Slope intercept)
        self.set_button("Line 2",self.draw_line2,1248,170,1,10)
        #button -line 3- Draw line using Digital Diferencial Analyzer (DDA)
        self.set_button("Line 3",self.draw_line3,1248,210,1,10)
        #button -line 4- Draw line using Bresenham's Algorithm
        self.set_button("Line 4",self.draw_line4,1248,250,1,10)
        #label line algorithms
        self.set_label("2D Transforms",1239,282,10)
        #display boxes to get traslation details
        self.display_tras_coord_boxes(1244,308,1,3)
        #button -traslacion-
        self.set_button("Traslacion",self.traslacion,1248,332,1,10)
        #display boxes to get traslation details
        self.display_esc_coord_boxes(1244,368,1,3)
        #button -traslacion-
        self.set_button("Escalado",self.escalado,1248,392,1,10)
        #display boxes to get traslation details
        self.display_rot_coord_box(1244,428,1,3)
        #display checkbox to set rotation mode
        self.set_checkbox("ccw",self.ccw,1288,426)
        #button -traslacion-
        self.set_button("Rotacion",self.rotacion,1248,452,1,10)
        #display boxes to get shearing details
        self.display_ciz_coord_boxes(1244,488,1,3)
        #button -cizalla (shearing)-
        self.set_button("Cizalla",self.cizalla,1248,512,1,10)
        #display boxes to get reflexion details
        self.display_ref_coord_boxes(1244,548,1,3)
        #display checkbox to set x reflexion
        self.set_checkbox("x",self.x,1248,590)
        #display checkbox to set y reflexion
        self.set_checkbox("y",self.y,1288,590)
        #button -reflexion-
        self.set_button("Reflexion",self.reflexion,1248,572,1,10)
        #display checkbox to set view mode
        self.set_checkbox("Scale",self.scale,1105,625)
        #button -close-
        self.set_button("Exit",self.close,1180,625,1,10)
        #run simulator
        self.run()

###########################################################################################
################################  LINE ALGORITHMS  ########################################
###########################################################################################

    #Draw line using Direct Scan Conversion (original Slope intercept)
    def draw_line1(self):
        if self.get_dot_count()>1:
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
                if self.get_scale()==1:
                    if i%self.get_offset()==0:
                        line.insert(i,self.dot(x,y))
                else:
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
        if self.get_dot_count()>1:
            line=[]
            line_coord=[]
            line_screen_coord=[]
            #get the start and end points
            x1,y1,x2,y2=self.line()
            #mod4
            if x2<x1:
                #swap start and end points
                aux=x1
                x1=x2
                x2=aux
                aux=y1
                y1=y2
                y2=aux
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
            dx,dy=x2-x1,y2-y1
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
                dx=-1 if dx<0 else 1
                while x1!=x2:
                    x1+=dx
                    y=mt.floor(m*x1+b)
                    if self.get_scale()==1:
                        if i%self.get_offset()==0:
                            line.insert(i,self.dot(x1,y))
                    else:
                        line.insert(i,self.dot(x1,y))
                    canvas_x,canvas_y=self.preprocess(x1,y)
                    line_coord.insert(i,[canvas_x,canvas_y])
                    line_screen_coord.insert(i,[x1,y])
                    i+=1
            #slope > 1
            elif dy!=0:
                m=dx/dy
                b=x1-m*y1
                dy=-1 if dy<0 else 1
                while y1!=y2:
                    y1+=dy
                    x=mt.floor(m*y1+b)
                    if self.get_scale()==1:
                        if i%self.get_offset()==0:
                            line.insert(i,self.dot(x,y1))
                    else:
                        line.insert(i,self.dot(x,y1))
                    canvas_x,canvas_y=self.preprocess(x,y1)
                    line_coord.insert(i,[canvas_x,canvas_y])
                    line_screen_coord.insert(i,[x,y1])
                    i+=1
            if i>1:
                self.add_line(line,line_coord,line_screen_coord)

    #Draw line using Digital Diferencial Analyzer (DDA)
    def draw_line3(self):
        if self.get_dot_count()>1:
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
                if self.get_scale()==1:
                    if i%self.get_offset()==0:
                        line.insert(i,self.dot(mt.floor(x),mt.floor(y)))
                else:
                    line.insert(i,self.dot(mt.floor(x),mt.floor(y)))
                canvas_x,canvas_y=self.preprocess(x,y)
                line_coord.insert(i,[mt.floor(canvas_x),mt.floor(canvas_y)])
                line_screen_coord.insert(i,[mt.floor(x),mt.floor(y)])
                x+=dxx
                y+=dyy
                i+=1
            if i>1:
                self.add_line(line,line_coord,line_screen_coord)

    #Draw line using Bresenham's Algorithm modified
    def draw_line4(self):
        if self.get_dot_count()>1:
            t=False
            line=[]
            line_coord=[]
            line_screen_coord=[]
            #get the start and end points
            x1,y1,x2,y2=self.line()
            #mod 4
            if x2<x1:
                t=True
                #swap start and end points
                aux=x1
                x1=x2
                x2=aux
                aux=y1
                y1=y2
                y2=aux
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
            dx,dy=abs(x2-x1),abs(y2-y1)
            x,y=x1,y1
            #increment or decrement x and y due to line position
            if self.get_scale()==1:
                #increment or decrement x and y due to line position
                dxx,dyy=-self.get_offset() if dx<0 else self.get_offset(),-self.get_offset() if dy>0 else self.get_offset()
                if t==True and y1<y2:
                    dyy=-self.get_offset() if dy<0 else self.get_offset()
                elif y1<y2:
                    dyy=-self.get_offset() if dy<0 else self.get_offset()
            else:
                dxx,dyy=-1 if dx<0 else 1,-1 if dy>0 else 1
                if t==True and y1<y2:
                    dyy=-1 if dy<0 else 1
                elif y1<y2:
                    dyy=-1 if dy<0 else 1
            i=0
            #slope < 1
            if dx>dy:
                e=2*dy-dx
                while i<=dx:
                    if self.get_scale()==1:
                        if i%self.get_offset()==0:
                            line.insert(i,self.dot(x,y))
                            canvas_x,canvas_y=self.preprocess(x,y)
                            line_coord.insert(i,[canvas_x,canvas_y])
                            line_screen_coord.insert(i,[x,y])
                            while e>0:
                                y+=dyy
                                e-=2*dx
                            x+=dxx
                            e+=2*dy
                    else:
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
            #slope > 1
            elif dy!=0:
                e=2*dx-dy
                while i<=dy:
                    if self.get_scale()==1:
                        if i%self.get_offset()==0:
                            line.insert(i,self.dot(x,y))
                            canvas_x,canvas_y=self.preprocess(x,y)
                            line_coord.insert(i,[canvas_x,canvas_y])
                            line_screen_coord.insert(i,[x,y])
                            while e>0:
                                x+=dxx
                                e-=2*dy
                            y+=dyy
                            e+=2*dx
                    else:
                        line.insert(i,self.dot(x,y))
                        canvas_x,canvas_y=self.preprocess(x,y)
                        line_coord.insert(i,[canvas_x,canvas_y])
                        line_screen_coord.insert(i,[x,y])
                        while e>0:
                            x+=dxx
                            e-=2*dy
                        y+=dyy
                        e+=2*dx
                    i+=1
            if i>1:
                self.add_line(line,line_coord,line_screen_coord)

###########################################################################################
#################################  2D TRANSFORMS  #########################################
###########################################################################################

    def traslacion(self):
        if len(self.selected_lines)>0:
            line=[]
            line_coord=[]
            line_screen_coord=[]
            index=self.selected_lines[-1]
            add_x,add_y=int(self.box_tras_x.get(0.0,END)),int(self.box_tras_y.get(0.0,END))
            #borramos la linea original
            for i in range(len(self.lines[index])):
                self.canvas.delete(self.lines[index][i])
            self.lines.pop(index)
            #la pintamos trasladada
            for dot in self.line_screen_coord[index]:
                dot[0]+=add_x
                dot[1]-=add_y
                line.append(self.dot(dot[0],dot[1]))
                canvas_x,canvas_y=self.preprocess(dot[0],dot[1])
                line_coord.append([canvas_x,canvas_y])
                line_screen_coord.append([dot[0],dot[1]])
            self.line_screen_coord.pop(index)
            self.lines.append(line)
            self.line_coord.append(line_coord)
            self.line_screen_coord.append(line_screen_coord)
            #enable coordinates text box editing
            self.line_coord_box["state"]="normal"
            #delete last line shown
            self.line_coord_box.delete("end-1l","end")
            #display line coordinates
            self.line_coord_box.insert(INSERT,"line "+str(index)+": "+str(self.line_coord[-1]))
            #disable coordinates text box editing
            self.line_coord_box["state"]="disabled"
            self.box_tras_x.delete(0.0,END)
            self.box_tras_y.delete(0.0,END)


    def escalado(self):
        if len(self.selected_lines)>0:
            line=[]
            line_coord=[]
            line_screen_coord=[]
            index=self.selected_lines[-1]
            add_x,add_y=float(self.box_esc_x.get(0.0,END)),float(self.box_esc_y.get(0.0,END))
            #borramos la linea original
            for i in range(len(self.lines[index])):
                self.canvas.delete(self.lines[index][i])
            self.lines.pop(index)
            #la pintamos trasladada
            for dot in self.line_screen_coord[index]:
                dot[0]*=add_x
                dot[1]*=add_y
                line.append(self.dot(dot[0],dot[1]))
                canvas_x,canvas_y=self.preprocess(dot[0],dot[1])
                line_coord.append([canvas_x,canvas_y])
                line_screen_coord.append([dot[0],dot[1]])
            self.line_screen_coord.pop(index)
            self.lines.append(line)
            self.line_coord.append(line_coord)
            self.line_screen_coord.append(line_screen_coord)
            #enable coordinates text box editing
            self.line_coord_box["state"]="normal"
            #delete last line shown
            self.line_coord_box.delete("end-1l","end")
            #display line coordinates
            self.line_coord_box.insert(INSERT,"line "+str(index)+": "+str(self.line_coord[-1]))
            #disable coordinates text box editing
            self.line_coord_box["state"]="disabled"
            self.box_esc_x.delete(0.0,END)
            self.box_esc_y.delete(0.0,END)

    def rotacion(self):
        if len(self.selected_lines)>0:
            line=[]
            line_coord=[]
            line_screen_coord=[]
            index=self.selected_lines[-1]
            angle=int(self.box_rot.get(0.0,END))
            angle=angle*(mt.pi/180)
            for i in range(len(self.lines[index])):
                self.canvas.delete(self.lines[index][i])
            self.lines.pop(index)
            #la pintamos trasladada
            for dot in self.line_screen_coord[index]:
                if self.get_ccw()==1:
                    dot[0]=int(dot[0]*mt.cos(angle)+dot[1]*mt.sin(angle))
                    dot[1]=-int(dot[0]*mt.sin(angle)-dot[1]*mt.cos(angle))
                else:
                    dot[0]=int(dot[0]*mt.cos(angle)-dot[1]*mt.sin(angle))
                    dot[1]=int(dot[0]*mt.sin(angle)+dot[1]*mt.cos(angle))
                line.append(self.dot(dot[0],dot[1]))
                canvas_x,canvas_y=self.preprocess(dot[0],dot[1])
                line_coord.append([canvas_x,canvas_y])
                line_screen_coord.append([dot[0],dot[1]])
            self.line_screen_coord.pop(index)
            self.lines.append(line)
            self.line_coord.append(line_coord)
            self.line_screen_coord.append(line_screen_coord)
            #enable coordinates text box editing
            self.line_coord_box["state"]="normal"
            #delete last line shown
            self.line_coord_box.delete("end-1l","end")
            #display line coordinates
            self.line_coord_box.insert(INSERT,"line "+str(index)+": "+str(self.line_coord[-1]))
            #disable coordinates text box editing
            self.line_coord_box["state"]="disabled"
            self.box_rot.delete(0.0,END)

    def cizalla(self):
        if len(self.selected_lines)>0:
            line=[]
            line_coord=[]
            line_screen_coord=[]
            index=self.selected_lines[-1]
            add_x,add_y=float(self.box_ciz_x.get(0.0,END)),float(self.box_ciz_y.get(0.0,END))
            #borramos la linea original
            for i in range(len(self.lines[index])):
                self.canvas.delete(self.lines[index][i])
            self.lines.pop(index)
            #la pintamos trasladada
            for dot in self.line_screen_coord[index]:
                #x shearing
                if add_y==0 and add_x>0:
                    dot[0]=int(dot[0]+dot[1]*add_x)
                #y shearing
                elif add_x==0 and add_y>0:
                    dot[1]=int(dot[0]*add_y+dot[1])
                #normal shearing
                elif add_x>0 and add_y>0:
                    dot[0]=int(dot[0]+dot[1]*add_x)
                    dot[1]=int(dot[0]*add_y+dot[1])
                line.append(self.dot(dot[0],dot[1]))
                canvas_x,canvas_y=self.preprocess(dot[0],dot[1])
                line_coord.append([canvas_x,canvas_y])
                line_screen_coord.append([dot[0],dot[1]])
            self.line_screen_coord.pop(index)
            self.lines.append(line)
            self.line_coord.append(line_coord)
            self.line_screen_coord.append(line_screen_coord)
            #enable coordinates text box editing
            self.line_coord_box["state"]="normal"
            #delete last line shown
            self.line_coord_box.delete("end-1l","end")
            #display line coordinates
            self.line_coord_box.insert(INSERT,"line "+str(index)+": "+str(self.line_coord[-1]))
            #disable coordinates text box editing
            self.line_coord_box["state"]="disabled"
            self.box_ciz_x.delete(0.0,END)
            self.box_ciz_y.delete(0.0,END)

    def reflexion(self):
        if len(self.selected_lines)>0:
            line=[]
            line_coord=[]
            line_screen_coord=[]
            index=self.selected_lines[-1]
            #m,b=float(self.box_m.get(0.0,END)),float(self.box_b.get(0.0,END))
            #borramos la linea original
            for i in range(len(self.lines[index])):
                self.canvas.delete(self.lines[index][i])
            self.lines.pop(index)
            #la pintamos trasladada
            for dot in self.line_screen_coord[index]:
                if self.get_x()==1:
                    if dot[1]>self.canvas_height/2:
                        dot[1]=self.canvas_height-dot[1]
                    else:
                        dot[1]+=dot[1]
                elif self.get_y()==1:
                    if dot[0]>self.canvas_width/2:
                        dot[0]=self.canvas_width-dot[0]
                    else:
                        dot[0]+=dot[0]
                #falta respecto de recta
                line.append(self.dot(dot[0],dot[1]))
                canvas_x,canvas_y=self.preprocess(dot[0],dot[1])
                line_coord.append([canvas_x,canvas_y])
                line_screen_coord.append([dot[0],dot[1]])
            self.line_screen_coord.pop(index)
            self.lines.append(line)
            self.line_coord.append(line_coord)
            self.line_screen_coord.append(line_screen_coord)
            #enable coordinates text box editing
            self.line_coord_box["state"]="normal"
            #delete last line shown
            self.line_coord_box.delete("end-1l","end")
            #display line coordinates
            self.line_coord_box.insert(INSERT,"line "+str(index)+": "+str(self.line_coord[-1]))
            #disable coordinates text box editing
            self.line_coord_box["state"]="disabled"
            self.box_m.delete(0.0,END)
            self.box_b.delete(0.0,END)


#main
ds=DrawSim()

ds.create_DrawSim_Gui()
