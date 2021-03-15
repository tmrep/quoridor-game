#!/usr/bin/python

import sys
# https://stackoverflow.com/questions/37435369/matplotlib-how-to-draw-a-rectangle-on-image
import matplotlib.pyplot as plt
import matplotlib.patches as patches
# https://pythonspot.com/reading-csv-files-in-python/
import csv
import math

file = sys.argv[1]

moves_player_a = []
moves_player_b = []
comment_player_a = []
comment_player_b = []

edge_size = 1;
gap = 0.2;
wall_lenght = 2*edge_size-gap
stock_vert_gap = edge_size/2;

def plotGameBoard(ax):
    for x in range(1,10):
        for y in range(1,10):
            rect = patches.Rectangle((x*edge_size-(edge_size-gap)/2,y*edge_size-(edge_size-gap)/2),edge_size-gap,edge_size-gap,linewidth=1,edgecolor='#dcdcdc',facecolor='none')
            ax.add_patch(rect)

def getPos(code):
    x = ord(code[0])-ord('a')+1
    y = ord(code[1])-ord('1')+1
    return x,y

def plotWall(ax,code):
    if len(code)!=3:
        error("Invalid lenght of wall code.")
    x, y = getPos(code[0:2])
    if code[2]=='h':
        llx = x-((edge_size-gap)/2)
        lly = y+((edge_size-gap)/2)
        width = wall_lenght
        height = gap
    else:
        llx = x+((edge_size-gap)/2)
        lly = y-((edge_size-gap)/2)
        width = gap
        height = wall_lenght
    rect = patches.Rectangle((llx,lly),width,height,linewidth=1,edgecolor='none',facecolor='#ffa926')
    ax.add_patch(rect)

def plotPlayer(ax,code,player_num):
    if len(code)!=2:
        error("Invalid lenght of player code.")
    x, y = getPos(code[0:2])
    if player_num==1:
        color = "#fff9c0"
    else:
        color = "#71362d"
    circ = patches.Circle((x,y), radius=(edge_size-gap)/2*0.7,linewidth=1,edgecolor='#939393',facecolor=color)
    ax.add_patch(circ)

def plotWallStock(ax,count,player_num):
    llx = edge_size-(edge_size-gap)/2
    separation = (9*edge_size-2*gap)/9
    if player_num==1:
        lly = edge_size-(edge_size-gap)/2-stock_vert_gap-wall_lenght
    else:
        lly = 9*edge_size+(edge_size-gap)/2+stock_vert_gap
    for i in range(1,count+1):
        rect = patches.Rectangle((llx,lly),gap,wall_lenght,linewidth=1,edgecolor='none',facecolor='#ffa926')
        ax.add_patch(rect)
        llx = llx+separation

played_moves = 0;
with open(f"{file}.txt") as csvDataFile:
    csvReader = csv.reader(csvDataFile,delimiter=';')
    for row in csvReader:
        moves_player_a.append(row[0])
        played_moves = played_moves+1;
        if len(row)>1:
            moves_player_b.append(row[1])
            played_moves = played_moves+1;
        else:
            moves_player_b.append("")
        if len(row)>2:
            comment_player_a.append(row[2])
        else:
            comment_player_a.append("")
        if len(row)>3:
            comment_player_b.append(row[3])
        else:
            comment_player_b.append("")

fig,ax = plt.subplots(1)
plotGameBoard(ax)
plotPlayer(ax,"e1",1)
plotPlayer(ax,"e9",2)
plotWallStock(ax,10,1)
plotWallStock(ax,10,2)
# graph settings
ax.set_xlim([0,edge_size*10])
ax.set_ylim([edge_size-(edge_size-gap)/2-stock_vert_gap-wall_lenght,9*edge_size+(edge_size-gap)/2+stock_vert_gap+wall_lenght])
ax.set_aspect('equal')
plt.axis('off')
# plt.show()
plt.savefig(f"{file}_0.png", bbox_inches='tight') # https://chartio.com/resources/tutorials/how-to-save-a-plot-to-a-file-using-matplotlib/
plt.close()
for move_num in range(1,played_moves+1):
    fig,ax = plt.subplots(1)
    plotGameBoard(ax)
    # player a
    remaining_walls = 10;
    for i in range(0,math.ceil(move_num/2)):
        move = moves_player_a[i]
        if len(move)==3:
            remaining_walls = remaining_walls-1;
            plotWall(ax,move)
        else:
            last_player_position = move
    plotPlayer(ax,last_player_position,1)
    plotWallStock(ax,remaining_walls,1)
    # player b
    remaining_walls = 10;
    last_player_position = "e9"
    for i in range(0,math.floor(move_num/2)):
        move = moves_player_b[i]
        if len(move)==3:
            remaining_walls = remaining_walls-1;
            plotWall(ax,move)
        else:
            last_player_position = move
    plotPlayer(ax,last_player_position,2)
    plotWallStock(ax,remaining_walls,2)
    # graph settings
    ax.set_xlim([0,edge_size*10])
    ax.set_ylim([edge_size-(edge_size-gap)/2-stock_vert_gap-wall_lenght,9*edge_size+(edge_size-gap)/2+stock_vert_gap+wall_lenght])
    ax.set_aspect('equal')
    plt.axis('off')
    # plt.show()
    plt.savefig(f"{file}_{move_num:03}.png", bbox_inches='tight') # https://chartio.com/resources/tutorials/how-to-save-a-plot-to-a-file-using-matplotlib/
    # https://stackoverflow.com/questions/339007/how-to-pad-zeroes-to-a-string
    plt.close()
