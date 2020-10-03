# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 18:14:50 2020

@author: Stéphan
"""
import numpy as np
import turtle as tr
Point = [(-200,200),(0,200),(200,200),(-200,0),(0,0),(200,0),(-200,-200),(0,-200),(200,-200)]
List = [7,8,9,4,5,6,1,2,3]

def grille():
    tr.reset()    
    tr.speed(15)
    tr.up()
    tr.goto(-300,300)
    tr.down()
    tr.width(5)
    tr.goto(-100,300)
    tr.goto(-100,-300)
    tr.goto(100,-300)
    tr.goto(100,300)
    tr.goto(300,300)
    tr.goto(300,100)
    tr.goto(-300,100)
    tr.goto(-300,-100)
    tr.goto(300,-100)
    tr.goto(300,-300)
    tr.goto(-300,-300)
    tr.goto(-300,300)
    tr.goto(300,300)
    tr.goto(300,-100)
    i=0
    while i<9:
        tr.up()
        tr.goto(Point[i])
        tr.down()
        tr.write(List[i])
        i=i+1
    tr.up()
    tr.goto(-350,0)

def croix(numero):
    Point = [(-200,-200),(0,-200),(200,-200),(-200,0),(0,0),(200,0),(-200,200),(0,200),(200,200)]
    tr.speed(5)
    tr.up()
    tr.goto(Point[numero-1])
    tr.down()
    tr.width(5)
    tr.color('red')
    tr.rt(45)
    tr.fd(70)
    tr.fd(-140)
    tr.fd(70)
    tr.rt(90)
    tr.fd(70)
    tr.fd(-140)
    tr.fd(70)
    tr.rt(225)
    tr.up()
    tr.goto(-350,0)
    tr.color('black')
    tr.width(1)
def rond(numero):
    Points = [(-200,-250),(0,-250),(200,-250),(-200,- 50),(0,-50),(200,-50),(-200,150),(0,150),(200,150)]
    tr.width(5)
    tr.color('green')
    tr.goto(Points[numero-1])
    tr.down()
    tr.speed(5)
    tr.circle(50)
    tr.up()
    tr.goto(-350,0)
    tr.color('black')
    tr.width(1)

def Affichage(grid):
    for i in range(len(grid)):
        print("|", end='')
        for j in range(len(grid[0])):
            if grid[i][j]==0: 
                print(" _ ", end='')
            elif grid[i][j]==1: 
                print(" X ", end='')
            elif grid[i][j]==2: 
                print(" O ", end='')
        print("|")
    print("\n")  
   
def ActionPossible(grid):
    case_vide=[]
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j]==0:
                case_vide.append((i,j))
    return case_vide   

def Result(grid,a,maximizingPlayer):
    new_grid=[]
    for i in range(len(grid)):
        new_grid.append([])
        for j in range(len(grid[0])):
            new_grid[i].append(grid[i][j])
    if maximizingPlayer:
        new_grid[a[0]][a[1]]=2
    else:
        new_grid[a[0]][a[1]]=1
    return new_grid
    
def Terminal_Test(grid):
    #chexk la diago descendante
    tempdiago=grid[0][0]
    k_diago=0
    for i in range(len(grid)):
        #check les lignes
        k_ligne=0
        temp=grid[i][0]
        for j in range(len(grid[0])):
            if grid[i][j]!=0 and grid[i][j]==temp:
                k_ligne+=1
            if grid[i][j]!=0 and i==j and grid[i][j]==tempdiago:
                k_diago+=1
        if k_ligne==3:
            if temp==1:
                return True,1
            elif temp==2:
                return True,2  
        if k_diago==3:
            if tempdiago==1:
                return True,1
            elif tempdiago==2:
                return True,2             
    #chexk la diago montante
    tempdiago=grid[0][2]
    k_diago=0
    for j in range(len(grid[0])):
        #check les colonnes
        k_colonne=0
        temp=grid[0][j]
        for i in range(len(grid)):
            if grid[i][j]!=0 and grid[i][j]==temp:
                k_colonne+=1
            if grid[i][j]!=0 and i==2-j and grid[i][j]==tempdiago:
                k_diago+=1
        if k_colonne==3:
            if temp==1:
                return True,1
            elif temp==2:
                return True,2  
        if k_diago==3:
            if tempdiago==1:
                return True,1
            elif tempdiago==2:
                return True,2   
    #Si aucun joueur n'a gagné la partie s'arrête
    if len(ActionPossible(grid))==0:
        return True,0  
    return False,0

def Utility(grid):
    #Si l'un des joueurs a gagné
    if Terminal_Test(grid)[0]:
        if Terminal_Test(grid)[1]==1:
            #on lui retourne -1 si c'est les croix
            return -1
        if Terminal_Test(grid)[1]==2:
            #on lui retourne 1 si c'est les ronds
            return 1
    #sinon on lui retourne 0 car état nul
    return 0    

#L'algo minimax avec l'élagage alpha/béta.    
def minimax(grid, depth, maximizingPlayer, alpha=-np.inf, beta=np.inf):
    best_child_joueur0=[(0,0),-1]  
    best_child_joueurX=[(0,0), 1] 
    if depth == 0 or Terminal_Test(grid)[0]:
        return Utility(grid), best_child_joueur0, best_child_joueurX
    if maximizingPlayer:
        value=-np.inf
        for child in ActionPossible(grid):
            #Affichage(Result(grid,child,maximizingPlayer))                    
            value = max(value, minimax(Result(grid,child,maximizingPlayer), depth-1, False, alpha, beta)[0])     
            if value>=beta:            
                return value, best_child_joueur0, best_child_joueurX
            alpha=max(alpha, value)
            #C'est ici qu'on stock le premier meilleur chemin pour le joueur O
            if best_child_joueur0[1]<value and depth==8:
                best_child_joueur0=[child,value]            
    else:
        value=np.inf
        for child in ActionPossible(grid):
            #Affichage(Result(grid,child,maximizingPlayer))          
            value = min(value, minimax(Result(grid,child,maximizingPlayer), depth-1, True, alpha, beta)[0])           
            if value<=alpha:            
                return value, best_child_joueur0, best_child_joueurX
            beta=min(beta, value)            
            #C'est ici qu'on stock le premier meilleur chemin pour le joueur X
            if best_child_joueurX[1]>value and depth==8:
                best_child_joueurX=[child,value]
    #print("depth =", depth, " O : ", best_child_joueur0, " X : ", best_child_joueurX) #liste[:0]=10 ou trees
    return value, best_child_joueur0, best_child_joueurX

#Pour que le joueur puisse jouer avec la GUI
def Map(a):
    if a==7:
        return (0,0)
    if a==8:
        return (0,1)
    if a==9:
        return (0,2)
    if a==4:
        return (1,0)
    if a==5:
        return (1,1)
    if a==6:
        return (1,2)
    if a==1:
        return (2,0)
    if a==2:
        return (2,1)
    if a==3:
        return (2,2)

#Pour que l'IA puisse jouer avec la GUI
def Map2(a):  
    if a==(0,0):
        return 7
    if a==(0,1):
        return 8
    if a==(0,2):
        return 9
    if a==(1,0):
        return 4
    if a==(1,1):
        return 5
    if a==(1,2):
        return 6
    if a==(2,0):
        return 1
    if a==(2,1):
        return 2
    if a==(2,2):
        return 3 
    

def Game():
    grid_init = np.zeros((3,3))
    """choisissez votre grille de départ : un 0 pour rien, un 1 pour une croix, un 2 pour un rond"""
    grid = np.array([[0, 0, 0,],
                     [0, 0, 0,],
                     [0, 0, 0,]])
    """Select the first player : 1 for Xs, 2 for Os"""
    Player=1
    #Disp the GUI
    grille()
    #Test if the grid is empty, if not disp the grid on the GUI
    test=False
    for i in range(len(grid)):
        for j in range(len(grid[0])):
            if grid[i][j]!=grid_init[i][j]:
                test=True
                break;
        if test:
            break;
    if test:
        for i in range(len(grid)):
            for j in range(len(grid[0])):
                if grid[i][j]==1:
                    croix(Map2((i,j)))
                if grid[i][j]==2:
                    rond(Map2((i,j)))                    
    #Init the game
    while True:
        #Choose the smartness of the IA (1 : weak to 8 : strong)
        depth=8
        Affichage(grid)
        if Terminal_Test(grid)[0]==True:
            break;
        elif Player==1:
            print("C'est au tour du joueur 1:")
            #Pour que les IA s'affrontent ==>
            """IA against IA
            x=minimax(grid, depth, False)[2][0]
            while grid[x[0]][x[1]]!=0:
                #on relance avec une profondeur plus petite car il perd dans tous les cas si l'autre joue parfaitement
                print(depth)
                x = minimax(grid, depth, False)[2][0]  
                depth+=-1                  
            #GUI
            croix(Map2(x))"""
            #or uncomment the part above to see IA against IA, and comment the code below until croix(temp).
            temp=int(input())           
            x=Map(temp)
            while grid[x[0]][x[1]]!=0:
                print("Case déjà jouée, veuillez en saisir une autre :")
                Affichage(grid)
                temp=int(input())
                x=Map(temp)  
            croix(temp)
            #affect the choosen state
            grid[x[0]][x[1]]=1
            Player=2
        elif Player==2:
            print("C'est au tour de l'IA:")
            #minimax(minimax(grid, 5, True))
            x=minimax(grid, depth, True)[1][0]
            while grid[x[0]][x[1]]!=0:
                #on relance avec une profondeur plus petite car il perd dans tous les cas si l'autre joue parfaitement
                #False joueur X
                #True joueur O
                x = minimax(grid, depth, True)[1][0]  
                depth+=-1
            grid[x[0]][x[1]]=2
            rond(Map2(x))            
            Player=1   
    if Terminal_Test(grid)[0]:
        if Terminal_Test(grid)[1]==1:
            print("Joueur 1 a gagné !")
        if Terminal_Test(grid)[1]==2:
            print("L'IA a gagné !")
        if Terminal_Test(grid)[1]==0:
            print("Tie !")   
Game()        


        