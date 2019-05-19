import arcade
import random
import math

SIZE= 800
SPRITE_SCALING_CAR = 0.02
SPRITE_SCALING_WALL = 0.1

C = SIZE/2
GREY = (128,128,128)
WHITE = (255,255,255)
ROAD_HEIGHT = 200
MOVEMENT_SPEED = 10

class Car(arcade.Sprite):

    def __init__(self, image, scale, path, goal):
        self.path = path
        self.array_pos = 0
        self.goal = goal
        super().__init__(image, scale)
        self.speed = 0

    def update(self):
        if(int(self.center_x) == int(self.goal[0]) and int(self.center_y) == int(self.goal[1])):
             self.kill()

        elif((self.array_pos + MOVEMENT_SPEED) > len(self.path)):
            #slow down
            self.center_x = self.path[self.array_pos][0]
            self.center_y = self.path[self.array_pos][1]
            self.array_pos +=1

        else:
            self.center_x = self.path[self.array_pos][0]
            self.center_y = self.path[self.array_pos][1]
            self.array_pos +=MOVEMENT_SPEED

class MyGame(arcade.Window):
    def __init__(self, size,cars):
        super().__init__(size,size)

        arcade.set_background_color(arcade.color.AMAZON)
        
        self.cars_list = None
        self.wall_list = None
        self.paths = None
        self.departCoords = [(0,SIZE/2 -50),(800,SIZE/2 + 50),(450,0),(350,800)]
        self.goalCoords = [(0, SIZE/2+50),(800, SIZE/2 -50),(350,0),(450,800)]


    def setup(self):
        self.cars_list = arcade.SpriteList()
        self.wall_list= arcade.SpriteList()
        self.paths=[]

        self.create_car_sprites()

        self.draw_walls(0,200,200)
        self.draw_walls(0,200,100)
        self.draw_walls(600,800,200)
        self.draw_walls(600,800,100)
        self.draw_walls(600,800,600)
        self.draw_walls(600,800,800)
        self.draw_walls(0,200,600)
        self.draw_walls(0,200,800)       

    
    def draw_walls(self, x_begin, x_max, y_begin):
        for x in range(x_begin, x_max):
            wall = arcade.Sprite("black.png", SPRITE_SCALING_WALL)
            wall.center_x = x
            wall.center_y = y_begin
            self.wall_list.append(wall)

    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()
        self.create_road()
        self.draw_lanes(1)
        self.wall_list.draw()
        self.cars_list.draw()
        # Your drawing code goes here

    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here. """
        #self.physics_engine.update()
        
        #for car in self.cars_list:
        #    car.forward(3)
        #self.create_car_sprites()
        xpto = arcade.check_for_collision_with_list(self.car_sprite, self.cars_list)
        print(xpto)
        self.cars_list.update()
        #hit_list = arcade.check_for_collision_with_list(self.player_sprite, self.coin_list) #list of collisions

    def create_car_sprites(self):
        """Create all cars"""

        for i in range(0,10):

            depart = random.randint(0,3)
            goal = random.randint(0,3)

            while (depart== goal):
                depart = random.randint(0,3)
                goal = random.randint(0,3)


            depart_coords= self.departCoords[depart]
            goal_coords= self.goalCoords[goal]

            path = self.create_paths(depart_coords, goal_coords)

            self.car_sprite = Car("car.png", SPRITE_SCALING_CAR, path, goal_coords)

            self.car_sprite.center_x = self.departCoords[depart][0]    
            self.car_sprite.center_y = self.departCoords[depart][1]
            self.cars_list.append(self.car_sprite)


    def create_paths(self, depart_coords, goal_coords):
        print("depart: ",depart_coords, " goal: ",goal_coords)    
        
        depart=[0,0]
        goal=[0,0]

        depart[0] = int(depart_coords[0])
        depart[1] = int(depart_coords[1])
        
        goal[0] = int(goal_coords[0])
        goal[1] = int(goal_coords[1])
                
        final_path=[]

        if(depart[0]==0):   # when agent departs from (0,150)
            if(depart[1]==goal[1]): # from (0,150) to (800,150)
                final_path=[(x,depart[1]) for x in range(depart[0], goal[0])]           
            else:
                p1=[(x, depart[1]) for x in range(depart[0], goal[0])]
                if(depart[1]>goal[1]): #from (0,150) to (450,0)
                    p2=[(goal[0], y) for y in range(depart[1], goal[1], -1)]
                else:   #from (0,150) to (550,800)
                    p2=[(goal[0], y) for y in range(depart[1], goal[1])]        
                
                final_path=p1+p2

        elif(depart[0]==450): #when agent departs from (550,0)
            if(depart[0]==goal[0]): #from (550,0) to (550,800)
                final_path = [(depart[0],y) for y in range(depart[1],goal[1])]
            else:
                p1 = [(depart[0],y) for y in range(depart[1],goal[1])]
                if(depart[0]>goal[0]): # from (550,0) to (0,250)
                    p2=[(x, goal[1]) for x in range(depart[0], goal[0], -1)]
                else: #from (550,0)  to (800,150)
                    p2 =[(x, goal[1]) for x in range(depart[0], goal[0])]

                final_path =p1+p2                    
        elif(depart[0] == 800): #when agent departs from (800,250):
            if(depart[1] == goal[1]):
                final_path = [(x,depart[1]) for x in range(depart[0], goal[0], -1)]
            else:
                p1= [(x,depart[1]) for x in range(depart[0], goal[0], -1)]
                if(depart[1]>goal[1]): #from (800, 250) to (450,0)
                    p2 =[(goal[0] , y) for y in range(depart[1], goal[1], -1)]
                else:   # from (800, 250) to (550,800)
                    p2 =[(goal[0], y) for y in range(depart[1], goal[1])]
                final_path =p1+p2
        else: # when agent departs from (350, 800)
            if(depart[0]==goal[0]): 
                final_path =[(depart[0], y) for y in range(depart[1], goal[1], -1)]
            else:
                p1=[(depart[0], y) for y in range(depart[1], goal[1], -1)]
                if(depart[0]>goal[0]): # from (450, 800) to (0, 250)
                    p2 =[(x, goal[1]) for x in range(depart[0], goal[0], -1)]
                else:  # from (450, 800) to (800, 150)
                    p2 =[(x, goal[1]) for x in range(depart[0], goal[0])]                    

                final_path =p1+p2

        final_path.append((goal[0],goal[1]))
        return final_path

    def create_road(self):
        arcade.draw_rectangle_filled(C,C,SIZE,ROAD_HEIGHT,GREY)
        arcade.draw_rectangle_filled(C,C,ROAD_HEIGHT,SIZE,GREY)
        arcade.draw_line(0,C,C-ROAD_HEIGHT/2,C,WHITE,2)#horizontal left
        arcade.draw_line(C+ROAD_HEIGHT/2,C,SIZE,C,WHITE,2)#Horizonal right
        arcade.draw_line(C,0,C,C-ROAD_HEIGHT/2,WHITE,2)#vertical bot
        arcade.draw_line(C,C+ROAD_HEIGHT/2,C,SIZE,WHITE,2)#vertical top

    def draw_lanes(self,num_lanes):
        aux_acum = (ROAD_HEIGHT/2) / num_lanes
        for i in range (num_lanes-1):
            #left side H
            arcade.draw_line(0,C-aux_acum,C-ROAD_HEIGHT/2,C-aux_acum,WHITE)
            arcade.draw_line(0,C+aux_acum,C-ROAD_HEIGHT/2,C+aux_acum,WHITE)
            #draw regular stop line
            arcade.draw_line(C-ROAD_HEIGHT/2,C,C-ROAD_HEIGHT/2,C-ROAD_HEIGHT/2,WHITE)
            arcade.draw_line(C+ROAD_HEIGHT/2,C,C+ROAD_HEIGHT/2,C+ROAD_HEIGHT/2,WHITE)
            arcade.draw_line(C+ROAD_HEIGHT/2,C-ROAD_HEIGHT/2,C,C-ROAD_HEIGHT/2,WHITE)
            arcade.draw_line(C-ROAD_HEIGHT/2,C+ROAD_HEIGHT/2,C,C+ROAD_HEIGHT/2,WHITE)
            #right side H
            arcade.draw_line(C+ROAD_HEIGHT/2,C+aux_acum,SIZE,C+aux_acum,WHITE)
            arcade.draw_line(C+ROAD_HEIGHT/2,C-aux_acum,SIZE,C-aux_acum,WHITE)
            #top side V
            arcade.draw_line(C-aux_acum,0,C-aux_acum,C-ROAD_HEIGHT/2,WHITE)
            arcade.draw_line(C+aux_acum,0,C+aux_acum,C-ROAD_HEIGHT/2,WHITE)
            #bot side V
            arcade.draw_line(C-aux_acum,SIZE,C-aux_acum,C+ROAD_HEIGHT/2,WHITE)
            arcade.draw_line(C+aux_acum,SIZE,C+aux_acum,C+ROAD_HEIGHT/2,WHITE)
            aux_acum = aux_acum + (ROAD_HEIGHT/2 )/ num_lanes 

def main():
    game = MyGame(SIZE,30)
    game.setup()
    arcade.run()

if __name__ == "__main__":
    main()