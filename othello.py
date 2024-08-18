import tkinter

root = tkinter.Tk()
root.title("Othello")
root.geometry("480x480")

canvas = tkinter.Canvas(root, bg = "green")
canvas.pack(fill = tkinter.BOTH, expand = True)

NUM_SQUARE = 8
w = 480 // NUM_SQUARE
board = [[0] * NUM_SQUARE for i in range(NUM_SQUARE)]
board[3][3] = board[4][4] = 1; board[3][4] = board[4][3] = 2

def draw():
    for y in range(NUM_SQUARE):
        for x in range(NUM_SQUARE):
            match board[y][x]: # match使ってみたかっただけ
                case 0:
                    canvas.create_oval(w*x, w*y, w*(x+1), w*(y+1), fill = "Green", activefill="Yellow", width = 3) # activefillかっこいい
                case 1:
                    canvas.create_oval(w*x, w*y, w*(x+1), w*(y+1), fill = "Black", width = 3)  
                case 2:
                    canvas.create_oval(w*x, w*y, w*(x+1), w*(y+1), fill = "White", width = 3)  

def raytocoords(x,y,a,b):
    """x,yからa,b方向への座標列
    """
    areaContains = lambda x,y : (x>=0 and x<8 and y>=0 and y<8) # 盤上かどうか
    coords=[]
    while(areaContains(x,y)):
        coords.append([x,y])
        x+=a;y+=b
    return coords

coordstodisks = lambda coords,board: [board[c[1]][c[0]] for c in coords]
"""座標列とボードを与えて駒の並びを返す
"""

def nflippable(player, disks):
    """手番player側から見て駒がdisks並びのときに何枚ひっくり返せるか返す
    """
    if len(disks)<=2 or disks[0]!=0: return 0
    for i,v in enumerate(disks[1:]):
        if v==0:
            return 0
        elif v==player:
            return i
    return 0

def coordsflippable(player,x,y,board):
    """手番player側から見てx,yに置いたときにひっくり返せる座標列を返す
    """
    vecs=[[1,0],[1,1],[0,1],[-1,1],[-1,0],[-1,-1],[0,-1],[1,-1]] # 8方向ベクトル
    return sum([c[1:1+nflippable(player,coordstodisks(c, board))] for v in vecs if (c:=raytocoords(x,y,v[0],v[1]))],[])

def clicked(e):
    x = e.x//w; y = e.y//w
    if not (coords := coordsflippable(1,x,y,board)):return # 返せない場合は終わり
    print("Black Turn:",x,y)
    for c in coords:
        board[c[1]][c[0]] = 1
    board[y][x] = 1
    draw()
    canvas.update()
    root.after(1000)

    com=[[x,y,c] for y in range(NUM_SQUARE) for x in range(NUM_SQUARE) if (c:=coordsflippable(2,x,y,board))] # 全着手の生成
    if not com:return # 手が無い場合は終わり
    com = sorted(com, reverse=True,key=lambda z: len(z[2]))[0] # 沢山返せる手を選ぶ
    print("White Turn:",com[0],com[1])
    for c in com[2]:
        board[c[1]][c[0]] = 2
    board[com[1]][com[0]] = 2
    draw()

draw()
# ボタンの作成と配置
root.bind("<Button-1>", clicked)

# イベントループ（TK上のイベントを捕捉し、適切な処理を呼び出すイベントディスパッチャ）
root.mainloop()
