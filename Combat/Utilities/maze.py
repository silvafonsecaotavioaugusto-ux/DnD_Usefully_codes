from mazelib.generate.DungeonRooms import DungeonRooms
import matplotlib.pyplot as plt
import os
from Error_t import get_integer

h0 = 25
w0 = 25

def room_vert(center_cord: tuple, radius: int):
    return [(center_cord[0] - radius, center_cord[1] - radius), (center_cord[0] + radius, center_cord[1] + radius)]


rooms = [room_vert((h0//2-2,w0//2+2), 3),
            room_vert((h0//2+2,3*w0//2+2), 3),
            room_vert((3*h0//2+2,w0//2-2), 3),
            room_vert((3*h0//2+3,3*w0//2+4), 3),
            room_vert((h0,w0), 5),]

class Maze:

    def __init__(self,
                 h0: float,
                 w0: float,
                 rooms: list,
                 hunt_order: str = 'random',
                 x0: float = 0,
                 y0: float = 0):
        self.h0 = h0
        self.w0 = w0
        self.rooms = rooms
        self.hunt_order = hunt_order.lower().strip()
        self.x = [x0 if x0 != 0 else h0]
        self.y = [y0 if y0 != 0 else w0]
        self.curent_maze = None
        self.update_maze()
    
    
    def update_maze(self):
        maze = DungeonRooms(h0 = self.h0,
                            w0 = self.w0,
                            rooms = self.rooms,
                            hunt_order = self.hunt_order).generate()
        self.curent_maze = maze
    
    def display(self):
        plt.figure()
        plt.imshow(self.curent_maze, colorizer= 'kw')
        plt.plot(self.x, self.y, '.r', markersize = 10)
        plt.show()
    
    def validate_position(self, x_: int, y_: int):
        if self.curent_maze[x_, y_] == 1:
            print('invalid position!')
            return False
        return True
    
    def update_position(self):
        '''each square equals to a 3m x 3m square'''
        for i in range(len(self.x)):
            movement = False
            while not movement:
                delta_x = get_integer(f'horizontal displacement for {i+1}° group: ')
                delta_y = -get_integer(f'vertical displacement for {i+1}° group: ')
                new_x = self.x[i] + delta_x
                new_y = self.y[i] + delta_y
                movement = self.validate_position(new_x, new_y)
            
            self.x[i] = new_x
            self.y[i] = new_y
    
    def split(self):
        for i in range(len(self.x)):
            curent_x = self.x[i]
            curent_y = self.y[i]
            op = input(f'split point at ({curent_x},{curent_y}): ')
            if op.strip().lower() == "s":
                neighbors = [(curent_x+1,curent_y),
                             (curent_x,curent_y+1),
                             (curent_x-1,curent_y),
                             (curent_x,curent_y-1)]
                
                for position in neighbors:
                    if self.validate_position(*position):
                        self.x.append(position[0])
                        self.y.append(position[1])
                        break
                        
            





Maze = Maze(h0, w0, rooms)
