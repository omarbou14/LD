from tkinter import Tk, Canvas, Menu, Listbox, Button, RIGHT, Entry
import PySimpleGUI as sg
import threading
import random
from math import floor, pow, sqrt
from time import sleep
from termcolor import cprint


w = 600
h = 600


n = 4

c_coord = [0, 0, 0, 0]

t1 = 0

class Noeud:
    def __init__(self, x, y, vx=0, vy=0):
        self.x = x
        self.y = y
        self.vx = vx
        self.vy = vy

    def dep(self, dx, dy):
        self.x += dx
        self.y += dy



class Line_object:
    def __init__(self, can, x1, y1, x2, y2):
        global list2
        self.p1 = Noeud(x1, y1)
        self.p2 = Noeud(x2, y2)
        self.ItemId = can.create_line(x1 , y1, x2, y2, fill='black', activefill='white', width=3, capstyle='round')
        
        self.ItemId1 = can.create_text(x1, y1, text='0', fill='blue', anchor='s', font=('Arial', -8))
        
        self.ItemId2 = can.create_text(x2, y2, text='1', fill='blue', anchor='s', font=('Arial', -8))
        
        self.ItemId3 = can.create_text((x1+x2)/2, (y1+y2)/2, text=str(len(list2)), fill='red', anchor='s', font=('Arial', -20))

    def coords(self, can, x1, y1, x2, y2):
        self.p1.x = x1
        self.p1.y = y1
        self.p2.x = x2
        self.p2.y = y2      
        can.coords(self.ItemId, x1 , y1, x2, y2)
        can.coords(self.ItemId1, x1 , y1)
        can.coords(self.ItemId2, x2 , y2)
        can.coords(self.ItemId3, (x1+x2)/2, (y1+y2)/2)

    def print_info(self, a=0, i=0):
        print("\t\tp1: x=%s, y=%s " %(self.p1.x, self.p1.y))
        print("\t\tp2: x=%s, y=%s " %(self.p2.x, self.p2.y))
        if a == 1:
            print("\tobj address: %s" %(self))        
        if i == 1:
            print("\t\tItemId: %s ItemId1: %s ItemId2: %s ItemId3: %s " %(self.ItemId, self.ItemId1, self.ItemId2, self.ItemId3))
   
class Source_object(Noeud):
    def __init__(self, can, x, y):
        super().__init__(x, y)
        self.ItemId = can.create_oval(self.x-10, self.y-10, self.x+10, self.y+10, fill='yellow')

    def print_info(self, a=0, i=0):
        print("\t\tp: x=%s, y=%s " %(self.x, self.y))
        if a == 1:
            print("\tobj address: %s" %(self))        
        if i == 1:
            print("\t\tItemId: %s" %(self.ItemId))

class Recepteur_object(Noeud):
    def __init__(self, can, x, y):
        super().__init__(x, y)
        self.ItemId = can.create_oval(self.x-10, self.y-10, self.x+10, self.y+10, fill='white')
    def print_info(self, a=0, i=0):
        print("\t\tp: x=%s, y=%s " %(self.x, self.y))
        if a == 1:
            print("\tobj address: %s" %(self))        
        if i == 1:
            print("\t\tItemId: %s" %(self.ItemId))

class point_rencontre(Noeud,):
    def __init__(self, can, x, y, c, t):
        super().__init__(x, y)
        self.ItemId = can.create_oval(self.x-3, self.y-3, self.x+3, self.y+3, fill=c)
        self.ItemId1 = can.create_text(x, y, text=t, fill='blue', anchor='s', font=('Arial', -8))
    def print_info(self, a=0, i=0):
        print("\t\tp: x=%s, y=%s " %(self.x, self.y))
        if a == 1:
            print("\tobj address: %s" %(self))        
        if i == 1:
            print("\t\tItemId: %s" %(self.ItemId))

def new_line(can, list1, list2, x1=0, y1=0, x2=0, y2=0):
    if x1 == "" or x1 == 0:
        x1 = random.randint(150,450)
    if y1 == "" or y1 == 0:
        y1 = random.randint(100,500)
    if x2 == "" or x2 == 0:
        x2 = x1 + random.randint(0, 20) - 20
    if y2 == "" or y2 == 0:
        y2 = y1 + random.randint(0, 20) - 20
    list2.append(Line_object(can, x1, y1, x2, y2))
    list1.insert(list1.size(), 'L' + str(len(list2) - 1))

def new_source(can, list1, list3, x=0, y=0):
    if x == 0 and y == 0:
        x = random.randint(200,400)
        y = random.randint(100,200)
    list3.append(Source_object(can, x, y))
    list1.insert(list1.size(), 'S' + str(len(list3) - 1))

def new_recever(can, list1, list4, x=0, y=0):
    if x == 0 and y == 0:
        x = random.randint(200,400)
        y = random.randint(400,500)
    list4.append(Recepteur_object(can, x, y))
    list1.insert(list1.size(), 'R' + str(len(list4) - 1))

def new_point_rencontre(can, x, y, c="black", t=""):
    global list5
    list5.append(point_rencontre(can, x, y, c, t))

def new_line_event(event): 
    global can
    global list1
    global list2
    new_line(can, list1, list2)

def new_line2_event(event): 
    global can
    global list1
    global list2
    global c_coord
    new_line(can, list1, list2, c_coord[0], c_coord[1], c_coord[2], c_coord[3])

def new_line3_event(event):
    global can
    global list1
    global list2


    sg.theme('dark grey 9')

    layout = [  [sg.Text('x1'), sg.Input()],
                [sg.Text('y1'), sg.Input()],
                [sg.Text('x2'), sg.Input()],
                [sg.Text('y2'), sg.Input()],
                [sg.Button('Ok')] ]
    
    windows = sg.Window('New Line 3', layout)
    event, values = windows.read(close=True)
    print("event:", event)
    if event == "Ok":
        new_line(can, list1, list2, values[0], values[1], values[2], values[3])


def new_source_event(event):
    global can
    global list1
    global list3
    new_source(can, list1, list3) 

def new_recever_event(event):
    global can
    global list1
    global list4
    new_recever(can, list1, list4)

def print_1_event(event):
    print_1()
def print_1():
    global list1
    global list2
    global list3
    global list4

    print("line list:")
    for i in range(len(list2)):
        print("\tline: %s" %(i))
        list2[i].print_info()
    print("source list:")
    for i in range(len(list3)):
        print("\tsource: %s" %(i))
        list3[i].print_info()
    print("recepteur list:")
    for i in range(len(list4)):
        print("\trecever: %s" %(i))
        list4[i].print_info()


def cursor_event(event):
    global c_coord

    c_coord[0] = c_coord[2]
    c_coord[1] = c_coord[3]
    c_coord[2] = event.x
    c_coord[3] = event.y
    print("x1=%s y1=%s x1=%s y1=%s" %(c_coord[0], c_coord[1], c_coord[2], c_coord[3]))
        

def distance_n_n(p1, p2):
    return sqrt( pow(p1.x - p2.x, 2) +  pow(p1.y - p2.y, 2))

def distance_coord(x1, y1, x2, y2):
    return sqrt( pow(x1 - x2, 2) +  pow(y1- y2, 2))


m = 0
def compteur():
    global m
    m += 1

min_max = 500
best_branche = []   
def parcours_event(event):
    parcours()
def parcours():
    global list1
    global list2
    global list3
    global list4
    global m
    global min_max
    global best_branche
    m = 0

    #list de tous les noeuds
    list_2 = []
    list_3 = []
    list_4 = []

    for obj in list2:
        list_2.append([obj.p1, obj.p2])    
    for obj in list3:
        list_3.append(obj)
    for obj in list4:
        list_4.append(obj)


    #parcours
    if len(list_2) == 0:
        print("Line list vide")
        return   
    list_line = list_2
    if len(list_3) == 0:
        print("Source list vide")
        return
    list_source = [list3[0]] #unique element pour le moment
    if len(list_4) == 0:
        print("recever list vide")
        return    
    list_recever = [list4[0]] #unique element pour le moment
    
    #parcours S-N
    for i in range(len(list_line)):
        for j in (0, 1):
            list_parent = []
            if distance_n_n(list_line[i][j], list_source[0]) < min_max:
                list_parent.append((i, j))
                parcours_n_n(list_line, list_parent, list_source, list_recever)
            else:
                #print("branche tue car la distance est grande entre S%s et L%sP%s" %(0, i, j))
                pass
                
    print(best_branche[-1])


def parcours_n_n(list_line, list_parent, list_source, list_recever):
    global min_max
    global best_branche
        
    #print("debut parcours_n_n", list_parent)
    #print("longeur list_line: %s, longeur list_parrent: %s" %(len(list_line), len(list_parent)))
    if len(list_line) == len(list_parent):
        #print("branche list_parent: %s terminer" %(list_parent))
        max = 0
        # S N
        score = distance_n_n( list_source[0] , list_line[ list_parent[0][0] ][ list_parent[0][1] ])
        #print("distance S%s -> L%sP%s = %s )" %(0, list_parent[0][0], list_parent[0][1], score))
        if score > max:
            max = score
        # N N
        for i in range(len(list_parent) - 1):
            score = 0.5 * distance_n_n(list_line[ list_parent[i][0] ][ abs(list_parent[i][1] - 1) ], list_line[ list_parent[i+1][0] ][ list_parent[i+1][1] ])
            #print("distance L%sP%s -> L%sP%s = %s )" %(list_parent[i][0], abs(list_parent[i][1] - 1), list_parent[i+1][0], list_parent[i+1][1], score))
            if score > max:
                max = score
        # N R
        score = distance_n_n(list_line[ list_parent[-1][0] ][ abs(list_parent[-1][1] - 1) ],  list_recever[0])
        #print("distance L%sP%s -> R%s = %s )" %(list_parent[-1][0], abs(list_parent[-1][1] - 1), 0, score))
        if score > max:
            max = score
        if max <= min_max:
            min_max = max
            best_branche.append((list_parent, max))
            #print(best_branche[-1])
            #print("details")
            score = distance_n_n( list_source[0] , list_line[ list_parent[0][0] ][ list_parent[0][1] ])
            #print("distance S%s -> L%sP%s = %s )" %(0, list_parent[0][0], list_parent[0][1], score))
            for i in range(len(list_parent) - 1):
                score = distance_n_n(list_line[ list_parent[i][0] ][ abs(list_parent[i][1] - 1) ], list_line[ list_parent[i+1][0] ][ list_parent[i+1][1] ])
                #print("distance L%sP%s -> L%sP%s = %s )" %(list_parent[i][0], abs(list_parent[i][1] - 1), list_parent[i+1][0], list_parent[i+1][1], score))
            score = distance_n_n(list_line[ list_parent[-1][0] ][ abs(list_parent[-1][1] - 1) ],  list_recever[0])
            #print("distance L%sP%s -> R%s = %s )" %(list_parent[-1][0], abs(list_parent[-1][1] - 1), 0, score))
        return
    
    for i in range(len(list_line)):
        t = 0
        for i2 in range(len(list_parent)):
            if i == list_parent[i2][0]:
                #print("branche tue car %s est dans la list parent" %(i))
                t = 1
        if t == 0:
            for j in (0, 1):
                if distance_n_n(list_line[i][j], list_line[list_parent[-1][0]][abs(list_parent[-1][1] - 1)]) < min_max:
                    list_parent_copy = list_parent.copy()
                    list_parent_copy.append((i, j))
                    parcours_n_n(list_line, list_parent_copy, list_source, list_recever)

def rencontre_event(event):
    global can
    global list2
    global best_branche
    if len(best_branche) == 0:
        print("list vide")
    else:
        list_line = []
        for obj in list2:
            list_line.append([obj.p1, obj.p2])
        bb_ = best_branche[-1][0].copy()
        for i in range(len(bb_) - 1):
            x = 0.5 * (list_line[ bb_[i][0] ][ abs(bb_[i][1] - 1) ].x + list_line[ bb_[i+1][0] ][ bb_[i+1][1] ].x)
            y = 0.5 * (list_line[ bb_[i][0] ][ abs(bb_[i][1] - 1) ].y + list_line[ bb_[i+1][0] ][ bb_[i+1][1] ].y)
            new_point_rencontre(can, x, y)

def verif_len_event(event):
    global list2        #list of obj
    global list3        #list of obj
    global list4        #list of obj 
    global best_branche #list of list
    global list6        #empty of results

    if len(best_branche) == 0:
        print("list vide")
    else:
        list_line = [] 
        for obj in list2:
            list_line.append([obj.p1, obj.p2])  #list2 of obj -> list_line of list of obj
        bb_ = best_branche[-1][0].copy()        #last elem of best_branche
        list_point = []                         #list of ["name", x, y]
        # S N
        list_point.append(["S", list3[0].x, list3[0].y])
        # N N
        for i in range(len(bb_) - 1):
            x = 0.5 * (list_line[ bb_[i][0] ][ abs(bb_[i][1] - 1) ].x + list_line[ bb_[i+1][0] ][ bb_[i+1][1] ].x)
            y = 0.5 * (list_line[ bb_[i][0] ][ abs(bb_[i][1] - 1) ].y + list_line[ bb_[i+1][0] ][ bb_[i+1][1] ].y)
            list_point.append([str(i), x, y])
        # N R
        list_point.append(["R", list4[0].x, list4[0].y])

        t = 0
        longueur_limit = 80
        for i in range(len(list_point) - 1):
            x1 = list_point[i][1]
            y1 = list_point[i][2]
            x2 = list_point[i+1][1]
            y2 = list_point[i+1][2]
            longueur = distance_coord(x1 , y1, x2, y2)
            print("longueur L%s :" %(i), end="")
            if longueur < longueur_limit:
                colorp = "green"
            else:
                colorp = "red"
                t = 1
            cprint(longueur, color=colorp)
        if t == 0:
            print("problem solve")
        else:

            print("correction")
            #calcule de la solution stantard
            list_point_standart = []
            # S N
            list_point_standart.append(["S", list3[0].x, list3[0].y])
            # N N
            for i in range(len(bb_)-1):
                x = (1 - (i+1)/(len(bb_))) * list3[0].x + ((i+1)/(len(bb_))) * list4[0].x
                y = (1 - (i+1)/(len(bb_))) * list3[0].y + ((i+1)/(len(bb_))) * list4[0].y
                j = bb_[i][0]
                list_point_standart.append([str(j), x, y])
                    
            # N R
            list_point_standart.append(["R", list4[0].x, list4[0].y])
            for i in range(len(list_point_standart)):
                #new_point_rencontre(can, list_point_standart[i][1], list_point_standart[i][2], "blue", list_point_standart[i][0])
                pass
            #print("list_point:", list_point)
            #print("list_point_standart:", list_point_standart)

            t = 0
            itr = 0
            itr_limit = 3000
            c1 = 0.999
            c2 = 0.001
            while(t==0 and itr < itr_limit):


                for i in range(len(list_point) - 1):
                    longueur = distance_coord(list_point[i][1], list_point[i][2], list_point[i+1][1], list_point[i+1][2])
                    if longueur >= longueur_limit:
                        #print("correction point %s (%s, %s) -> " %(i, list_point[i][1], list_point[i][2]), end=" ")
                        list_point[i][1] = c1 * list_point[i][1] + c2 * list_point_standart[i][1]
                        list_point[i][2] = c1 * list_point[i][2] + c2 * list_point_standart[i][2]
                        list_point[i+1][1] = c1 * list_point[i+1][1] + c2 * list_point_standart[i+1][1]
                        list_point[i+1][2] = c1 * list_point[i+1][2] + c2 * list_point_standart[i+1][2]
                        #print("(%s, %s)" %(list_point[i][1], list_point[i][2]))
                        #print("correction point %s (%s, %s) -> " %(i+1, list_point[i+1][1], list_point[i+1][2]), end=" ")               
                t1 = 0
                for i in range(len(list_point) - 1):
                    #longueur0 = distance_n_n(list_line[ bb_[i][0] ][0], list_line[ bb_[i][0] ][1])
                    #print("longueur L%s %s -> " %( i, longueur0), end="")
                    longueur = distance_coord(list_point[i][1], list_point[i][2], list_point[i+1][1], list_point[i+1][2])
                    
                    if longueur < longueur_limit:
                        colorp = "green"
                    else:
                        colorp = "red"
                        t1 = 1
                    #cprint(longueur, color=colorp)
                for i in range(len(list_point)):
                    #new_point_rencontre(can, list_point[i][1], list_point[i][2], "white")
                    pass
                if t1 == 0:
                    t = 1
                itr += 1
            if itr < itr_limit:
                print("problem solve, itr:%s" %itr)
                list6 = list_point.copy()       #results -> list6
                for i in range(len(list_point)):
                    #new_point_rencontre(can, list_point[i][1], list_point[i][2], "red")
                    pass
            else:
                print("no converge solution")

def simulation_event(event):
    global can
    global list2
    global list6
    global t1

    if len(list6) == 0:
        print("list vide")
    else:
        t1.start()

def simulation():
    global can
    global list2
    global best_branche
    global list6
    v = 1
    itr = 0
    itr_limit = 500
    limit1 = 1

    list_line = [] 
    for obj in list2:
        list_line.append([obj.p1, obj.p2])  #list2 of obj -> list_line of list of obj
    bb_ = best_branche[-1][0].copy()        #last elem of best_branche

    while(itr < itr_limit):
        for nn in range(len(list2)):
            # P1
            N1 = list_line[ bb_[nn][0] ][0]
            N2 = list_line[ bb_[nn][0] ][1]
            if bb_[nn][1] == 0:
                x1 = N1.x
                y1 = N1.y
            else:
                x1 = N2.x
                y1 = N2.y

            x2 = list6[nn][1]
            y2 = list6[nn][2]
            c1 = x1 - x2
            c2 = y1 - y2
            if abs(c1) > limit1:
                x = x1 - (c1/sqrt( pow(c1, 2) + pow(c2, 2) )) * v
            else:
                x = x1
            if abs(c2) > limit1:
                y = y1 - (c2/sqrt( pow(c1, 2) + pow(c2, 2) )) * v
            else:
                y = y1
            
            if bb_[nn][1] == 0:
                list2[bb_[nn][0]].coords(can, x, y, N2.x, N2.y)
            else:
                list2[bb_[nn][0]].coords(can, N1.x, N1.y, x, y)

            # P2
            if bb_[nn][1] == 1:
                x1 = N1.x
                y1 = N1.y
            else:
                x1 = N2.x
                y1 = N2.y

            x2 = list6[nn+1][1]
            y2 = list6[nn+1][2]
            c1 = x1 - x2
            c2 = y1 - y2
            if abs(c1) > limit1:
                x = x1 - (c1/sqrt( pow(c1, 2) + pow(c2, 2) )) * v
            else:
                x = x1
            if abs(c2) > limit1:
                y = y1 - (c2/sqrt( pow(c1, 2) + pow(c2, 2) )) * v
            else:
                y = y1
            
            if bb_[nn][1] == 1:
                list2[bb_[nn][0]].coords(can, x, y, N2.x, N2.y)
            else:
                list2[bb_[nn][0]].coords(can, N1.x, N1.y, x, y)
        itr += 1  

    

root = Tk()
root.geometry("900x700")
root.title("Distribution")



can = Canvas(root, width=w, height=h, bg='grey')
can.pack(side = RIGHT)


list1 = Listbox(root)
list1.select_set(0)
list1.pack()

list2 = []  #line list
list3 = []  #source list
list4 = []  #recepteur list
list5 = []  #point de rencontre
list6 = []  #resultat

b3 = Button(root, text="new source")
b3.pack()
b4 = Button(root, text="new recever")
b4.pack()
b5 = Button(root, text="new line")
#b5.pack()
b52 = Button(root, text="new line 2")
b52.pack()
b53 = Button(root, text="new line 3")
#b53.pack()
b6 = Button(root, text="parcours")
b6.pack()
b61 = Button(root, text="points de rencontre")
#b61.pack()
b62 = Button(root, text="verification longueur")
b62.pack()
b63 = Button(root, text="simulation")
b63.pack()
b7 = Button(root, text="print 1")
b7.pack()


b3.bind("<Button-1>", new_source_event)
b4.bind("<Button-1>", new_recever_event)
b5.bind("<Button-1>", new_line_event)
b52.bind("<Button-1>", new_line2_event)
b53.bind("<Button-1>", new_line3_event)
b6.bind("<Button-1>", parcours_event)
b61.bind("<Button-1>", rencontre_event)
b62.bind("<Button-1>", verif_len_event)
b63.bind("<Button-1>", simulation_event)
b7.bind("<Button-1>", print_1_event)
can.bind("<Button-1>", cursor_event)

t1 = threading.Thread(target=simulation)


root.mainloop()
