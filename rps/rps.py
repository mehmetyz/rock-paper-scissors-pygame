import tkinter as tki
import engine as game
import connection as con

tk = tki.Tk()
tk.resizable(0,0)
widthofScreen = tk.winfo_screenwidth()
heightofScreen = tk.winfo_screenheight()

tk.geometry(str.format("300x100+{0}+{1}",str(int(widthofScreen/2-150)),str(int(heightofScreen/2-50))))
tk.title("Rock Paper Scissors")


def play_with_computer(event):
    engine = game.Engine("play_with_computer",600,300,widthofScreen/2-300,heightofScreen/2-150)
    tk.withdraw()
    engine.render(tk)


def play_with_friend(event):
    con_form = con.ConnectionForm(tk,"RPS - Multiplayer")
    tk.withdraw()
    con_form.render()

btn1 = tki.Button(tk,text = "Play With Computer",width = "20",height = "10", fg = "white", bg = "darkblue",activebackground = "darkblue",activeforeground = "white",cursor = "hand2")
btn2 = tki.Button(tk,text = "Play With Friend",width = "20",height = "10",fg = "white", bg = "darkred",activebackground = "darkred",activeforeground = "white",cursor = "hand2")


btn1.pack(side = "left")
btn2.pack(side = "right")


btn1.bind("<Button-1>",play_with_computer)
btn1.bind("<KeyPress-Return>",play_with_computer)


btn2.bind("<Button-1>",play_with_friend)
btn2.bind("<KeyPress-Return>",play_with_friend)


tk.mainloop()
