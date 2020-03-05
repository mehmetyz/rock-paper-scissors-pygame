import socket,sys,os,engine,socket,time
import tkinter as form
class Connection:
    def __init__(self):
        self.Socket = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        self.Connected = False
        self.RemoteIPAddress = ''
        self.Port = 0
    @staticmethod
    def create_exists_connection(socket):
        c = Connection()
        c.Socket = socket
        (c.RemoteIPAddress,c.Port) = socket.getpeername()
        return c

    def connect(self,address = str, port = int):
            if not self.Connected:
                self.Socket.connect((address,port))
                self.Connected = True
            else:
                raise socket.error("connection already exists.")

    def disconnect(self):
        try:
            if self.Connected:
                self.Socket.disconnect()
                self.Connected = False
        except:
            raise socket.error("connection can not be disconnected.")

    def listen(self,port = int):
        if port <= 0 :
            raise Exception("the port is invalid.")
        skt = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        try:
            skt.bind(('',port))
            skt.settimeout(10)
            skt.listen(1)
            
            self.Socket,host = skt.accept()
            self.Connected = True
        except socket.timeout:
            self.Connected = False
            form.messagebox.showinfo("NO CONNECTION","TIMEOUT : There is no connection request.\nPlease Try Again.")
        except Exception as e:
            raise Exception(e.args[0])

    def send(self,text):
        if not self.Connected:
            raise socket.error("there is no connection.")
        try:
            buffer = bytes(text,"UTF-8")
            self.Socket.send(buffer)
        except:
            raise Exception("there was an error while sending")
        return True

    def receive(self):
        if not self.Connected:
            raise socket.error("there is no connection.")
        try:
            buffer = str(self.Socket.recv(16),encoding = "UTF-8")
        except:
             raise socket.error("there was an error while receiving.")
        return buffer

    def close(self):
        if not self.Socket._closed:
            self.Socket.close()
            time.sleep(1)
            self.Connected = False
            self.Socket = None
            return True
        else:
            return False

class ConnectionForm:
    def __init__(self,master,title):
        self.Title = title
        self.Master = master
        self.Connection = False
    def render(self):
        self.root = form.Toplevel(master = self.Master)
        self.root.geometry("{0}x{1}+{2}+{3}".format(250,250,int(self.root.winfo_screenwidth()/2)-125,int(self.root.winfo_screenheight()/2-125)))
        self.root.resizable(0,0)
        
        def onclosing():
            self.Master.deiconify()
            sys.exit(1)
            self.root.destroy()
        self.root.protocol("WM_DELETE_WINDOW",onclosing)
        self.root.title(self.Title)
        self.__design__()
        self.root.mainloop()

    def __design__(self):

        self.IPAddress = "localhost"
        self.Port = "1234"
        self.Username = "Player2"
        self.root.tk_setPalette(background = "cyan",foreground = "red")

        hostLBL = form.Label(master = self.root,text = "Connection Host ",font="assets/font.ttf",compound = "left")
        portLBL = form.Label(master = self.root,text = "IP Port ",font="assets/font.ttf",compound = "right")
        usernameLBL = form.Label(master = self.root,text = "User Name ",font="assets/font.ttf",compound = "right")

        hostTXT = form.Entry(master = self.root,width = 20,background = "white")
        portTXT = form.Entry(master = self.root,width = 20,background = "white")
        usernameTXT = form.Entry(master = self.root,width = 20,background = "white")

        img = form.PhotoImage(file = "assets/enter.png").subsample(2,2)
        join = form.Button(master = self.root,text = "Join",activebackground = "red",image = img,activeforeground = "white" ,width = 100,height = 30,justify = "right",compound = "left",bg = "red",fg = "white",cursor = "hand2")

        join.image = img
        connectF = form.Radiobutton(master = self.root,text = "Client",value = 1,activebackground = "blue",indicatoron = 0)
        listenF = form.Radiobutton(master= self.root,text = "Server",value = 2,activebackground = "blue",indicatoron = 0)


        connectF.pack(anchor = "w",side = "bottom")
        listenF.pack(anchor = "w",side = "bottom")
        connectF.select()


        def _set_listen(event):
            hostTXT.config(state = "disabled")
            join.config(text = "Create")
            self.conn_type  ="TO_LISTEN"
            self.Username = "Player1"
            usernameTXT.delete(0,form.END)
            usernameTXT.insert(0,self.Username)
            join.bind("<Button>",self.create_connection)

        def _set_connect(event):
            hostTXT.config(state = "normal")
            join.config(text="Join")
            self.conn_type = "TO_CONNECT"
            self.Username = "Player2"
            usernameTXT.delete(0,form.END)
            usernameTXT.insert(0,self.Username)
            join.bind("<Button>",self.connect)
        _set_connect(None)
        def _text_change(event):
            self.root.update()
            self.Username = usernameTXT.get()
        def _port_change(event):
            self.root.update()
            self.Port = portTXT.get()

        listenF.bind("<Button>",_set_listen)
        connectF.bind("<Button>",_set_connect)
        usernameTXT.bind("<KeyRelease>",_text_change)
        portTXT.bind("<KeyRelease>",_port_change)

        hostLBL.pack()
        hostTXT.pack()
        hostTXT.insert(0,self.IPAddress)

        portLBL.pack()
        portTXT.pack()
        portTXT.insert(0,self.Port)

        usernameLBL.pack()
        usernameTXT.pack()

        join.pack(side = "bottom")
        self.root.update()

    def connect(self,event):
        c = Connection()
        c.connect(self.IPAddress,int(self.Port))
        if c.Connected:
            self.Connection = c
            game = engine.Engine("play_with_friend",600,300,self.Master.winfo_screenwidth()/2-300,self.Master.winfo_screenheight()/2-150)
            game.Player1 = engine.Player(self.Username)
            c.send('PLAYER:%s'%self.Username)
            recv = c.receive().split(':')
            if recv[0] == 'PLAYER':
                game.Player2 = engine.Player(recv[1])
            else:
                raise Exception('there is a problem during the connection\nCONNECTION IP ADDRESS: %s\nCONNECTION PORT: %d'%(c.RemoteIPAddress,c.Port))
            self.root.withdraw()
            game.render(self.Master,c)
    def create_connection(self,event):
        c = Connection()
        c.listen(int(self.Port))
        if c.Connected:
            game = engine.Engine("play_with_friend",600,300,self.root.winfo_screenwidth()/2-300,self.root.winfo_screenheight()/2-150)
            self.Connection = c
            c.send("PLAYER:%s"%self.Username)
            game.Player1 = engine.Player(self.Username)
            recv = c.receive().split(':')
            if recv[0] == 'PLAYER':
                game.Player2 = engine.Player(recv[1])
            else:
                raise Exception('there is a problem during the connection\nCONNECTION IP ADDRESS: %s\nCONNECTION PORT: %d'%(c.RemoteIPAddress,c.Port))

            self.root.withdraw()
            game.render(self.Master,c)
