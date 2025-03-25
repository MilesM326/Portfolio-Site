import random

class Boards():
    def __init__(self,team):
        self.guesses=dict()
        self.locations=dict()
        for x in range(10):
            for y in range(10):
                self.guesses[x,y]= "~"
                self.locations[x,y]= "~"
                
class Ship():
    def __init__(self, size, team):
        """orientation: 0 = horizontal; 1 = vertical"""
        self.size=size
        self.points=[]
        self.onBoard=False
        self.team=team
        self.rot=0
    
    def place(self, x, y, orientation, automatic):
        self.rot=orientation
        
        if self.onBoard==True:
            self.remove()
            
        if self.team == 'p1':
            board= p1_board.locations
        elif self.team == 'p2':
            board= p2_board.locations
           
        for n in range (self.size):
            if self.rot==0:
                board[x+n, y]#check if ship fits left
                self.points.append((x+n, y))
            elif self.rot==1:
                board[x, y+n]#check if ship fits up
                self.points.append((x, y+n))
            elif self.rot==2:
                board[x-n, y]#check if ship fits right
                self.points.append((x-n, y))
            elif self.rot==3:
                board[x, y-n]#check if ship fits down
                self.points.append((x, y-n))
        self.onBoard=True
        
        for s in self.points:#check if the points are open
            if board[s]!="~":
                if automatic == False:
                    print('A ship is blocking.')
                self.remove()

    def remove(self):
        #removes piece off the board
        if self.team == 'p1':
            board= p1_board.locations
        elif self.team == 'p2':
            board= p2_board.locations
        for pt in self.points:
            board[pt]='~'
        self.points.clear()
        self.onBoard=False

#Translate text entry
translate=dict()
yco=dict()
letters="ABCDEFGHIJ"
for value in range(0,10):
    yco[value]=letters[value]
    translate[letters[value]]=value
    translate[value]=letters[value]

#board instances
p1_board=Boards(1)
p2_board=Boards(2)

#P1
p1_carrier=    Ship(5,"p1")
p1_battleship= Ship(4,"p1")
p1_cruiser=    Ship(3,"p1")
p1_submarine=  Ship(3,"p1")
p1_destroyer=  Ship(2,"p1")
#P2
p2_carrier=    Ship(5,"p2")
p2_battleship= Ship(4,"p2")
p2_cruiser=    Ship(3,"p2")
p2_submarine=  Ship(3,"p2")
p2_destroyer=  Ship(2,"p2")

#misc
turn=1
running=False
singleplayer=True

p1Score=0
p2Score=0

#shortcuts
p1_ships={1:p1_carrier, 2:p1_battleship, 3:p1_cruiser, 4:p1_submarine, 5:p1_destroyer}
p2_ships={1:p2_carrier, 2:p2_battleship, 3:p2_cruiser, 4:p2_submarine, 5:p2_destroyer}
allships=list()
allships.extend(p1_ships.values())
allships.extend(p2_ships.values())
direction={'west':0, 'north':1, 'east':2, 'south':3}

def match():
    for s in allships:
            if s.team== 'p1':
                b= p1_board.locations
            elif s.team== 'p2':
                b= p2_board.locations
            for p in s.points:
                if s.rot==0:  
                    if s.points[0]== p:
                        b[p]="<"
                    elif s.points[s.size-1]== p:
                        b[p]="}"
                    else:
                        b[p]="O"
                elif s.rot==1:
                    if s.points[0]== p:
                        b[p]="^"
                    elif s.points[s.size-1]== p:
                        b[p]="u"
                    else:
                        b[p]="O"
                elif s.rot==2:
                    if s.points[0]== p:
                        b[p]=">"
                    elif s.points[s.size-1]== p:
                        b[p]="{"
                    else:
                        b[p]="O"
                elif s.rot==3:
                    if s.points[0]== p:
                        b[p]="V"
                    elif s.points[s.size-1]== p:
                        b[p]="n"
                    else:
                        b[p]="O"
def update():
    global p1Score, p2Score, running
    
    for s in allships:
        if len(s.points)==0:
            print("Sunken ship")
            allships.remove(s)    
            if turn==1:
                p1Score+=1
            else:
                p2Score+=1
    if p1Score==5:
        print("Player 1 wins!")
        running=False
    elif p2Score==5:
        print("Player 2 wins!")
        running=False    
    
def printboard(player):
    if player==1:
        board=p1_board
    elif player==2:
        board=p2_board
    print("Your Pieces:"+" "*16+"Guesses:")
    print("   0 1 2 3 4 5 6 7 8 9" + " "*5 + "|" + " "*4 + "0 1 2 3 4 5 6 7 8 9")
    for y in range(10):
        position=""
        guesses=""
        for x in range(10):
            position= position + " " + board.locations[x,y]
            guesses= guesses + " " + board.guesses[x,y]
        print(" " +letters[y] + position + " "*5 + "|" + " "*2 +letters[y] + guesses)
    print()

def randomPlacement(player):
    if player==1:
        t= p1_ships
    elif player==2:
        t= p2_ships
        
    for s in t.values():
        while s.onBoard==False:
            rot=random.randrange(0,4)
            x=random.randrange(0,10)
            y=random.randrange(0,10)
            try:
                s.place(x, y, rot, True)
            except:
                s.remove()
        match()

def manual(sel, player):
    startPos=input("Enter starting position:\n")
    while True:
        try:
            facing=direction[input("Heading: north, south, east, west\n")]
            break
        except:
            pass

    if player==1:
        s=p1_ships
    elif player==2:
        s=p2_ships
        
    for char in startPos:
        if char.isdigit()==True:
            
            xpos=int(char)
        elif char.isalpha()==True:
            
            ypos=translate[char.upper()]
    try:
        s[sel].place(xpos, ypos, facing, False)
    except:
        print("Ship doesn't fit\n")
        s[sel].remove()
    else:
        match()

def guess(x, y, player):
    if player==1:
        attack= p1_board
        defend= p2_board
        defending_ships= p2_ships.values()
    elif player==2:
        attack= p2_board
        defend= p1_board
        defending_ships= p1_ships.values()
    if defend.locations[x,y] == 'M' or defend.locations[x,y] == '~':
        attack.guesses[x,y]= 'M'
        defend.locations[x,y]= 'M'
        print('Miss at '+str(x)+' '+translate[y])
    else:
        attack.guesses[x,y]= 'X'
        defend.locations[x,y]= 'X'
        print('Hit at '+str(x)+' '+translate[y])
        for s in defending_ships:
            for pt in s.points:
                if pt ==(x,y):
                    s.points.remove(pt)

def setup():
    global singleplayer
    print("*"*30)
    print("\t  BATTLESHIP")
    print("*"*30)
    pieces=p1_ships.values()
    while True:
        try:
            num=input("1 or 2 players?\n")
            if int(num)==1:
                singleplayer=True
                break
            elif int(num)==2:
                singleplayer=False
                break
        except:
            pass
    if singleplayer==False:
        for p in range(1,3):
            print("Player " + str(p)+ " place your ships:\n")
            for s in pieces:
                while s.onBoard==False:
                    sel=input("Pick a piece to place or ENTER for random placement:\n 1.carrier\n 2.battleship\n 3.cruiser\n 4.submarine\n 5.destroyer\n")
                    try:
                        if int(sel)>0 and int(sel)<6:
                            manual(int(sel),p)
                            printboard(p)
                    except:
                        randomPlacement(p)
                        printboard(p)
            pieces=p2_ships.values()
            print("_"*52+"\n")
    else:
        print("Player 1 place your ships:\n")
        for s in pieces:
            while s.onBoard==False:
                sel=input("Pick a piece to place or replace. Hit ENTER for random placement:\n 1.carrier\n 2.battleship\n 3.cruiser\n 4.submarine\n 5.destroyer\n")
                try:
                    if int(sel)>0 and int(sel)<6:
                        manual(int(sel),1)
                        printboard(1)
                except:
                    randomPlacement(1)
                    printboard(1)
        print("_"*52+"\n")
        randomPlacement(2)
                    
    

def main():
    global turn
    if turn==1:
        p=1
        
    else:
        p=2
    if singleplayer==False:
        printboard(p)    
        g=input('Make a guess (char,int) or (int,char):')
        try:
            for char in g:
                if char.isdigit()==True:
                    xpos=int(char)
                elif char.isalpha()==True:
                    ypos=translate[char.upper()]
            guess(xpos,ypos,p)
        except:
            print("Invalid input, try again.")
            turn*=-1
    if singleplayer==True:
        if turn==1:
            printboard(1)    
            g=input('Make a guess:')
            try:
                for char in g:
                    if char.isdigit()==True:
                        xpos=int(char)
                    elif char.isalpha()==True:
                        ypos=translate[char.upper()]
                guess(xpos,ypos,1)
            except:
                print("Invalid input, try again.")
                turn*=-1
        else:
            x=random.randrange(0,10)
            y=random.randrange(0,10)
            guess(x,y,2)
        
#Start   
setup()
running=True
while running==True:
    print("_"*52+"\n")
    if turn==1:
        print("Player 1")
    else:
        print("Player 2")
    main()
    update()
    turn*=-1
