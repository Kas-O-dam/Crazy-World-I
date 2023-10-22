import tkinter as tk
import json

from players import Bot

win = tk.Tk()
win.geometry('750x600')
    
class Map():
    def random_move(self, indexes, way="s", enemy="latvia"):
        self.occuped = []
        if way == "w": #west
           pass
        elif way == "s": #south
           if self.map[indexes[0]][indexes[1] - 1][0] == enemy:
               coef = 1
               if self.map[indexes[0]][indexes[1] - 1][3] < self.map[indexes[0]][indexes[1]][3]:
                   self.map[indexes[0]][indexes[1] - 1][0] = self.country
                   self.map[indexes[0]][indexes[1] - 1][3] = self.map[indexes[0]][indexes[1]][3] - self.map[indexes[0]][indexes[1] - 1][3]
                   self.map[indexes[0]][indexes[1]][3] = 0
                #for
        elif way == "n": #north
           pass
        elif way == "e": #east
           pass
        self.mapping()
    def add_building(self):
        pass

    #  ___    ___
    # |   \  /   |
    # | |\ \/ /| |
    # | | \__/ | |
    # |_|      |_|oving and other

    def check_click(self, coordinates):
        self.pixel = self.map[int( ( coordinates.x ) / 15 )][int( ( coordinates.y ) / 15 )] #use prop a, go to describing matrix props |
        try:                                                                                #                                         \_/
            if(self.pixel[0] != "sea"):
                self.text = f"{self.country}\n\n\n\narmy: {self.army}\n\nbuildings: {self.buildings}\n\nmoney: {self.money}\n\n########################\n\ncountry: {self.pixel[0]}\n\npeople: {self.pixel[1]}\n\nbuildings: {self.pixel[2]}\n\narmy: {self.pixel[3]}\n"
                self.replace_info()
                self.replace_adders()
        except:
            pass

    def lookfor(self, event):
        self.real_coords = (event.x, event.y)
    
    def mapping(self):
        for ix,x in enumerate(self.map):
            self.last = (0, 0)
            for iy, y in enumerate(x):
                if(y[0] == "england"):
                    self.fill = "#ccb7b6"
                elif(y[0] == "spain"):
                    self.fill = "#d9d17e"
                elif(y[0] == "portugal"):
                    self.fill = "#679450"
                elif(y[0] == "undefined-land"):
                    self.fill = "#757575"
                elif(y[0] == "france"):
                    self.fill = "#4e5787"
                elif(y[0] == "norway"):
                    self.fill = "#1a1421"
                elif(y[0] == "farer\'s islands"):
                    self.fill = "#ba5b63"
                elif(y[0] == "neutherlands"):
                    self.fill = "#8c3414"
                elif(y[0] == "switzland"):
                    self.fill = "#8c1436"
                elif(y[0] == "italy"):
                    self.fill = "#3c8c14"
                elif(y[0] == "belgium"):
                    self.fill = "#a69949"  
                elif(y[0] == "irland"):
                    self.fill = "#49a657" 
                elif(y[0] == "germany"):
                    self.fill = "#2b2121" 
                elif(y[0] == "austria"):
                    self.fill = "#3d2111" 
                elif(y[0] == "sweden"):
                    self.fill = "#8c8c23" 
                elif(y[0] == "denmark"):
                    self.fill = "#963627" 
                elif(y[0] == "sea"):
                    self.fill = "white"
                    #print("coors: ", (ix, iy))
                    #print("result: ", (ix*3+self.last[0]*3, iy*3+self.last[1]*3))
                	#print("last: ", self.last)
                self.ctx.create_rectangle(ix*7.5+self.last[0]*7.5+1, 
                                          iy*7.5+self.last[1]*7.5+1, 
                                          ix*7.5+self.last[0]*7.5+16, #prop a = 16-1 = 15
                                          iy*7.5+self.last[1]*7.5+16, #prop b = 15/2 = 7.5
                                          # everything is simple
                                          fill=self.fill,
                                          width = 0)
                self.last = (ix, iy)
    
    def remapping(self, event=None):
        self.for_destroy.append(self.ctx)
        #print(event.x, event.y, self.real_coords[1], self.real_coords[0]) #
        self.ctx = tk.Canvas(self.win, width=self.win_width, height=self.win_height, bg="black")
        self.ctx.bind("<ButtonPress-1>", lambda event: self.set_motion_tracker(event))
        self.ctx.bind("<ButtonRelease-1>", lambda event: self.unset_motion_tracker())
        self.mapping()
        try:
            self.ctx_x = int(self.ctx_x - ( self.motion_begin_coordinates_tracker[0] - event.x ) / 10)
            self.ctx_y = int(self.ctx_y - ( self.motion_begin_coordinates_tracker[1] - event.y ) / 10)
        except:
            pass
        if(self.ctx_x < 0):
            self.ctx_x = 0
        if(self.ctx_y < 0):
            self.ctx_y = 0
        
        self.ctx.place(x = self.ctx_x, 
                       y = self.ctx_y)
    
    def set_motion_tracker(self, event):
        self.info.destroy()
        self.motion_tracker = self.win.bind("<Motion>", self.remapping)
        self.motion_begin_coordinates_tracker = (event.x, event.y)
        print("Set") #

    def unset_motion_tracker(self):
        for ctx in self.for_destroy:
            ctx.destroy()
        self.for_destroy = []
        self.win.unbind("<Motion>", self.motion_tracker)
        self.replace_info()
        self.replace_adders()
        print("Unset") #
    
    def replace_info(self):
        self.info.destroy()
        self.info = tk.Text(self.win, fg = "gray", bd = 3, bg = "black", padx=5, pady=5)
        self.info.insert(tk.INSERT, self.text)
        self.info.config(state="disabled")
        self.info.place(
            x=self.win_width / 100 * 70,
            y=0,
            width = self.win_width / 100 * 30
        )
        with open(path, "r") as file:
            pass
    def replace_adders(self):
        self.adders[0].destroy()
        self.adders[1].destroy()
        self.adders = (
            tk.Button(self.win, text = "+", fg = "gray", bg = "black"),
            tk.Button(self.win, text = "+", fg = "gray", bg = "black"),
        )
        counter = 0
        for button in self.adders:
            counter += 6
            button.place(
                width = 25,
                height = 25,
                x = self.win_width / 100 * 90,
                y = self.win_height / 100 * (40 + counter)
            )
        tk.Button(self.win, fg = "gray", text = "Next turn", bg = "black").place(
            width = 150,
            height = 50,
            x = self.win_width / 100 * 75,
            y = self.win_height / 100 * 60
        )
    def __init__(self, win):
        self.win = win
        self.win_width = 750
        self.win_height = 600
        self.text = "Hello my dear player!\n\nIt\'s political strategy \"Crazy World One\", where you can build your superpower, fight in legendary battles and more this, create borders regardless provinces.\n\nI'm believing in you, ruler!"
        self.win.bind("<Motion>", self.lookfor)
        self.win.bind("<Button-3>", lambda x: self.check_click(x))
        self.ctx = tk.Canvas(self.win, width=self.win_width, height=self.win_height, bg="black")
        self.ctx.bind("<ButtonPress-1>", lambda event: self.set_motion_tracker(event))
        self.ctx.bind("<ButtonRelease-1>", lambda event: self.unset_motion_tracker())
        self.ctx_x = 0
        self.ctx_y = 0
        self.country = "estonia"
        self.army = "0"
        self.buildings = "0"
        self.people = "0"
        self.money = "0"
        self.for_destroy = []
        self.real_coords = ()
        self.actions = []
        self.bots = []
        self.map = [
                [
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['undefined-land', 0, 0, 0],
                ],[
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['irland', 0, 0, 0],
                    ['irland', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['spain', 0, 0, 0],
                    ['portugal', 0, 0, 0],
                    ['portugal', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['undefined-land', 0, 0, 0],
                    ['undefined-land', 0, 0, 0],
                ],[
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['england', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['england', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['england', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['england', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['spain', 0, 0, 0],
                    ['spain', 0, 0, 0],
                    ['spain', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['undefined-land', 0, 0, 0],
                    ['undefined-land', 0, 0, 0],
                ],[
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['england', 0, 0, 0],
                    ['england', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['england', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['france', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['spain', 0, 0, 0],
                    ['spain', 0, 0, 0],
                    ['spain', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['undefined-land', 0, 0, 0],
                    ['undefined-land', 0, 0, 0],
                ],[
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['england', 0, 0, 0],
                    ['england', 0, 0, 0],
                    ['england', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['france', 0, 0, 0],
                    ['france', 0, 0, 0],
                    ['france', 0, 0, 0],
                    ['spain', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['undefined-land', 0, 0, 0],
                    ['undefined-land', 0, 0, 0],
                ],[
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['norway', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['england', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['france', 0, 0, 0],
                    ['france', 0, 0, 0],
                    ['france', 0, 0, 0],
                    ['france', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['undefined-land', 0, 0, 0],
                    ['undefined-land', 0, 0, 0],
                ],[
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['norway', 0, 0, 0],
                    ['norway', 0, 0, 0],
                    ['norway', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['neutherlands', 0, 0, 0],
                    ['belgium', 0, 0, 0],
                    ['france', 0, 0, 0],
                    ['france', 0, 0, 0],
                    ['switzland', 0, 0, 0],
                    ['italy', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['italy', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['undefined-land', 0, 0, 0],
                    ['undefined-land', 0, 0, 0],
                ],[
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['norway', 0, 0, 0],
                    ['norway', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['germany', 0, 0, 0],
                    ['germany', 0, 0, 0],
                    ['germany', 0, 0, 0],
                    ['austria', 0, 0, 0],
                    ['italy', 0, 0, 0],
                    ['italy', 0, 0, 0],
                    ['italy', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['italy', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['undefined-land', 0, 0, 0],
                ],[
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['norway', 0, 0, 0],
                    ['sweden', 0, 0, 0],
                    ['sweden', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['denmark', 0, 0, 0],
                    ['germany', 0, 0, 0],
                    ['germany', 0, 0, 0],
                    ['germany', 0, 0, 0],
                    ['austria', 0, 0, 0],
                    ['italy', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['italy', 0, 0, 0],
                    ['italy', 0, 0, 0],
                    ['italy', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                ],[
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['sweden', 0, 0, 0],
                    ['sweden', 0, 0, 0],
                    ['sweden', 0, 0, 0],
                    ['sweden', 0, 0, 0],
                    ['sweden', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['germany', 0, 0, 0],
                    ['germany', 0, 0, 0],
                    ['undefined-land', 0, 0, 0],
                    ['austria', 0, 0, 0],
                    ['undefined-land', 0, 0, 0],
                    ['undefined-land', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['italy', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                    ['sea', 0, 0, 0],
                ]
            ]
        with open('firstNet.json', 'w') as file:
            thirdNet = json.dumps(self.map)
            file.write(thirdNet)
        #self.ctx.create_rectangle(int(self.win_width / 100 * 70), int(0), int(self.win_width), int(self.win_height), fill="black", width=3, outline="gray")
        #print(int(self.win_width / 100 * 80), int(1), int(self.win_width), int(self.win_height)) #
        self.info = tk.Text(self.win, fg = "gray", bd = 3, bg = "black", padx=5, pady=5)
        self.info.insert(tk.INSERT, self.text)
        self.info.config(state="disabled")
        self.adders = (
            tk.Button(self.win, text = "+", fg = "gray", bg = "black"),
            tk.Button(self.win, text = "+", fg = "gray", bg = "black")
        )
        self.mapping()
        self.info.place(
            x=self.win_width / 100 * 70,
            y=0,
            width = self.win_width / 100 * 30
        )

map = Map(win)
bot = Bot(1234, 'france')
map.ctx.place(x=0, y=0)
bot.getJSON()
print(bot.declareWar("spain"))
# map.map = bot.turn(map.map, {'enemies':['spain']}, 4)
# map.remapping()
win.mainloop()