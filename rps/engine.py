import pygame as pg
import connection
import time,os,random
from tkinter import messagebox


class Engine:

    def __init__(self,game = str,width = int,height = int, Xpad = int, Ypad = int):
        os.environ['SDL_VIDEO_WINDOW_POS'] = "%d,%d" % (Xpad,Ypad)
        pg.init()
        pg.font.init()

        pg.display.set_caption("ROCK PAPER SCISSORS")

        self.ScreenInfo = {"width":width,"height":height,"Xpos":Xpad,"Ypos":Ypad}
        self.middleX, self.middleY = int(self.ScreenInfo["width"]/2),int(self.ScreenInfo["height"]/2)

        self.Screen = pg.display.set_mode((width,height))

        if  game == "play_with_computer":
            self.GameType = 'COMPUTER'
            self.Player1 = Player("Player")
            self.Player2 = Player.create_computer()
        elif game == "play_with_friend":
            self.GameType = 'DUO'
        else:
            raise ValueError("Game type is invalid.")
        self.Running = False

    def play_with_computer(self):
        i = 1
        while i <= 20:
            n = random.choice(["rock","paper","scissors"])
            time.sleep(0.1)
            self.select("p2",n)
            i+=1
        self.select("p2",n)
        time.sleep(1)

    def play_with_friend(self,c = connection.Connection):

        self.set_text("WAITING FOR " + self.Player2.Name,self.middleX-150,self.middleY+70)
        c.send("PLAYED:%s" %self.Player1.Selection)
        recv = c.receive()
        if(recv == 'EXIT'):
            messagebox.showerror("ERROR","there is no connection")
            c.close()
            self.exit()
            self.Playable = False
            return
        recv = recv.split(':')
        self.Player2.Selection = recv[1]
        self.init()
        self.set_text(self.Player2.Name + ' Selected: '+ recv[1],self.middleX-150,self.middleY+70)
        self.select('p2',self.Player2.Selection)
        time.sleep(2)
        self.draw_score()
        self.init()
        self.set_text(self.win_player(),self.middleX-150,self.middleY+70)
    def init(self):

        GAME1COLOR = (0,220,102)
        GAME2COLOR = (0,102,220)
        self.Screen.fill(GAME1COLOR if self.GameType == 'COMPUTER' else GAME2COLOR)
        rock = pg.transform.scale(pg.image.load("assets/rock.png"),(100,100))
        paper = pg.transform.scale(pg.image.load("assets/paper.png"),(100,100))
        scissors = pg.transform.scale(pg.image.load("assets/scissors.png"),(100,100))
        info = pg.transform.scale(pg.image.load("assets/info.png"),(40,40))

        self.Screen.blit(rock,[self.middleX-160,self.middleY-50])
        self.Screen.blit(paper,[self.middleX-50,self.middleY-50])
        self.Screen.blit(scissors,[self.middleX+60,self.middleY-50])
        self.Screen.blit(info,[int(self.ScreenInfo["width"]-40),0])
        pg.display.flip()
        self.draw_score()

    def load_play_button(self):
        play = pg.transform.scale(pg.image.load("assets/go.png"),(100,50))
        self.Screen.blit(play,[self.middleX-50,self.middleY+95])
        pg.display.update()

    def win_player(self):

            if self.Player1.Selection == self.Player2.Selection:
                return "DRAW"
            else:
                if self.Player1.Selection == "rock":
                    if self.Player2.Selection =="paper":
                        self.Player2.add_point(1)
                        return (self.Player2.Name+" won")
                    else:
                        self.Player1.add_point(1)
                        return (self.Player1.Name+" won")
                elif self.Player1.Selection == "paper":
                    if self.Player2.Selection =="scissors":
                        self.Player2.add_point(1)
                        return (self.Player2.Name+" won")
                    else:
                        self.Player1.add_point(1)
                        return (self.Player1.Name+" won")
                else:
                    if self.Player2.Selection == "rock":
                        self.Player2.add_point(1)
                        return (self.Player2.Name+" won")
                    else:
                        self.Player1.add_point(1)
                        return (self.Player1.Name+" won")


    def select(self,player,s_value):

        self.init()
        color = (255,255,255) if player == "p1" else (0,0,0)
        if s_value == "rock":
            value = "Your selection: 'Rock'" if player == "p1" else self.Player2.Name + " Selection: "+self.Player2.Selection
            self.set_text(value, self.middleX-150,self.middleY+70)
            pg.draw.rect(self.Screen, color, [self.middleX-160,self.middleY-50, 100, 100], 2)

        elif s_value == "paper":
            value = "Your selection: 'Paper'" if player == "p1" else self.Player2.Name + " Selection: "+self.Player2.Selection
            self.set_text(value,self.middleX-150,self.middleY+70)
            pg.draw.rect(self.Screen, color , [self.middleX-50,self.middleY-50, 100, 100], 2)

        elif s_value == "scissors":
            value = "Your selection: 'Scissors'" if player == "p1" else self.Player2.Name + " Selection: "+self.Player2.Selection
            self.set_text(value,self.middleX-150,self.middleY+70)
            pg.draw.rect(self.Screen, color , [self.middleX+60,self.middleY-50, 100, 100], 2)
        else:
            raise Exception("Selection is wrong")
        pg.display.update()

        p = self.Player1 if player == "p1" else self.Player2
        p.set_selection(s_value)

        if player== "p1": self.load_play_button()
        self.Playable = True

    def render(self,master,conn = None):
        self.init()
        if self.Running == False:
            self.set_text("Make Your Choice",self.middleX-150,self.middleY+70)
        self.Running = True
        self.Playable = False
        self.Master = master

        while self.Running:
            for event in pg.event.get():

                if event.type == pg.QUIT:
                    if conn != None:
                        conn.send("EXIT")
                    self.Running = False
                    self.exit()
                if event.type == pg.MOUSEBUTTONUP:
                    pos = pg.mouse.get_pos()
                    self.init()
                    if int(self.ScreenInfo["width"]-40)<=pos[0]<=int(self.ScreenInfo["width"]) and 0 <= pos[1] <= 40:
                        self.set_text("Created by developer4-391",self.middleX-150,self.middleY+70)
                    elif self.middleX-160 <= pos[0] <= self.middleX-60 and self.middleY-50 <= pos[1] <= self.middleY+50:
                        self.select("p1","rock")
                    elif self.middleX-50 <= pos[0] <= self.middleX+50 and self.middleY-50 <= pos[1] <= self.middleY+50:
                        self.select("p1","paper")
                    elif self.middleX+60 <= pos[0] <= self.middleX+160 and self.middleY-50 <= pos[1] <= self.middleY+50:
                        self.select("p1","scissors")
                    elif self.Playable and self.middleX-50 <= pos[0] <= self.middleX+50 and self.middleY+95 <= pos[1] <= self.middleY+145:
                        if self.GameType == 'COMPUTER':
                            self.play_with_computer()
                            self.draw_score()
                            self.init()
                            self.set_text(self.win_player(),self.middleX-150,self.middleY+70)
                            time.sleep(0.5)
                            self.init()
                            self.set_text("Make Your Choice",self.middleX-150,self.middleY+70)
                        elif self.GameType == 'DUO':
                            if conn != None:
                                self.play_with_friend(conn)
                            if(self.Playable):
                                self.init()
                                self.set_text("Make Your Choice",self.middleX-150,self.middleY+70)
                                self.Playable = False
                    else:
                        self.set_text("Make Your Choice",self.middleX-150,self.middleY+70)
            if self.Player1.Point >= 5 or self.Player2.Point >= 5:
                messagebox.showinfo("GAME OVER","WINNER: "+ (self.Player1.Name if self.Player1.Point > self.Player2.Point else self.Player2.Name ))
                self.Player1.Point = 0
                self.Player2.Point = 0
                self.init()
                self.set_text("Make Your Choice",self.middleX-150,self.middleY+70)
                self.draw_score()


    def set_text(self,text = str,x = int,y = int):
        font = pg.font.Font("assets/font.ttf",30)
        self.TextRender = font.render(text,True,(255,0,0))
        self.Screen.blit(self.TextRender,(x,y))
        pg.display.update()

    def draw_score(self):
        self.set_text(str(self.Player1),0,0)
        self.set_text(str(self.Player2),0,30)

    def exit(self):
        self.Master.deiconify()
        pg.quit()

class Player:
    def __init__(self,name = str):
        self.Name = name
        self.Point = 0
        self.Selection = ""
    def add_point(self,point = int):
        self.Point += point
    def rename(self,new_name):
        self.Name = new_name
    def __str__(self):
        return str.format(" {0} has {1} point.",self.Name,self.Point)
    def set_selection(self,value):
        self.Selection = value

    @staticmethod
    def create_computer():
        com = Player("Computer")
        return com
