import arcade
import random
import math

SIZE= 800
SPRITE_SCALING_CAR = 0.03
SPRITE_SCALING_WALL = 0.1

C = SIZE/2
GREY = (128,128,128)
WHITE = (255,255,255)
ROAD_HEIGHT = 200
MOVEMENT_SPEED = 15
AREA = []
QUEUE = []
#NUMBER_OF_CARS_IN_INTERSECTION=0

class Car(arcade.Sprite):

    def __init__(self, image, scale, path, goal):
        self.path = path
        self.array_pos = 0
        self.goal = goal
        self.other_cars_list = None
        self.message = None
        self.collision_point = {}
        self.entrei = False
        self.number_of_paused =0
        self.number_of_blocks=0
        self.car_who_blocked_me=None
        
        super().__init__(image, scale)

    def update(self):
        #global NUMBER_OF_CARS_IN_INTERSECTION

        distance_to_all_cars = [arcade.get_distance_between_sprites(self,x) for x in self.other_cars_list]
        #Quando passaste o ponto de colisão
        #if(self.entrei==True and (self.center_x,self.center_y) in self.collision_point.keys()):
        if(self.entrei==True and (self.center_x,self.center_y) not in AREA):
            #NUMBER_OF_CARS_IN_INTERSECTION -=1
            for pos in self.collision_point:
                for carrinho in self.collision_point[pos]:    
                    carrinho.message=None

            self.entrei = False
          #  print("iff 1")


        #kill
        if(int(self.center_x) == int(self.goal[0]) and int(self.center_y) == int(self.goal[1])):
            #print("iff 2")
            self.kill()
     
        #Slow down
        elif((self.array_pos + MOVEMENT_SPEED) > len(self.path)-1):
            self.center_x = self.path[self.array_pos][0]
            self.center_y = self.path[self.array_pos][1]
            self.array_pos +=1 
           # print("ifff 3")


        #MOVE AFTER STOP
        elif(len(list(filter(lambda y : y == True,[(x.center_x, x.center_y) in self.path[self.array_pos:self.array_pos+100] for x in self.other_cars_list])))==0):
            #print("ifff 4")
            #if(NUMBER_OF_CARS_IN_INTERSECTION<3):
            self.center_x = self.path[self.array_pos][0]
            self.center_y = self.path[self.array_pos][1]
            self.array_pos += MOVEMENT_SPEED

        #caso da distancia de travagem
        elif(len(list(filter(lambda x: x < 20 and x>0, distance_to_all_cars)))>0):
            #print("ifff 5")
            self.center_x = self.path[self.array_pos][0]
            self.center_y = self.path[self.array_pos][1]
            self.array_pos += 0


        #SE ALGUÉM JÁ deu set na mensagem
        elif(self.message != None):
            #print("ifff 6")
            #print("car who blocked me : ", (self.car_who_blocked_me.center_x, self.car_who_blocked_me.center_y))
            #print("car who blocked me (MESSAGE): ", self.car_who_blocked_me.message)
            #print("# blocks: ",self.number_of_blocks)
            self.center_x = self.path[self.array_pos][0]
            self.center_y = self.path[self.array_pos][1]
            self.array_pos += 0
            self.number_of_blocks +=1
            
            # desbloqueia-se a ele proprio quando o carro que o bloqueou ja nao esta dentro da area de intersecao
            if((self.car_who_blocked_me.center_x, self.car_who_blocked_me.center_y) not in AREA and self.number_of_blocks>5): 
                self.message=None

            # o carro que o bloqueou tambem esta bloqueado
            elif(self.car_who_blocked_me.message != None): 
                self.message=None

            # o carro que o bloqueou nao esta bloqueado, mas por alguma razao tambem nao anda, por isso obrigar o outro gajo a andar
            elif(self.car_who_blocked_me.message == None): # obrigar o gajo que o bloqueou a andar
                self.car_who_blocked_me.center_x = self.car_who_blocked_me.path[self.car_who_blocked_me.array_pos][0]
                self.car_who_blocked_me.center_y = self.car_who_blocked_me.path[self.car_who_blocked_me.array_pos][1]
                self.car_who_blocked_me.array_pos+=MOVEMENT_SPEED

       

        #IN AREA
        elif((self.center_x,self.center_y) in AREA and self.entrei==False):
            #print("# cars: ",NUMBER_OF_CARS_IN_INTERSECTION)

            '''
            if(NUMBER_OF_CARS_IN_INTERSECTION>3):
                self.center_x = self.path[self.array_pos][0]
                self.center_y = self.path[self.array_pos][1]
                self.array_pos += 0
            else:
            '''
            #NUMBER_OF_CARS_IN_INTERSECTION +=1
            cars_inside = [x for x in self.other_cars_list if (x.center_x,x.center_y) in AREA]
            counter=0
            for car in cars_inside:
                #if (car.message == None): # so bloqueia carros que ainda nao estao bloqueados

                common = [value for value in self.path[self.array_pos:self.array_pos+300] if value in car.path[car.array_pos:car.array_pos+300]]

                if(len(common)>0):
                    mine_n_iterations = abs(common[0][0] - self.center_x) + abs(common[0][1] - self.center_y)
                    other_n_iterations = abs(common[0][0] - car.center_x) + abs(common[0][1] - car.center_y)

                    if(mine_n_iterations < other_n_iterations): # a mesma distancia do ponto de colisao
                    #if( len(self.path[self.array_pos:]) < len(car.path[car.array_pos:])): # so bloqueia aqueles que estao mais longe do destino do que ele proprio
                        #print("mine: ",mine_n_iterations)
                        #print("other: ",other_n_iterations)

                        counter+=1
                        if (common[0] in self.collision_point.keys()):
                            cars_list=self.collision_point[common[0]]
                            cars_list.append(car)
                            self.collision_point[common[0]] = cars_list
                        else:
                            self.collision_point[common[0]] = [car]
                        car.message = 0
                        car.car_who_blocked_me = self
    
           # if(counter!=0):
                #print("bloacked : ",counter)            
            self.entrei = True
            self.center_x = self.path[self.array_pos][0]
            self.center_y = self.path[self.array_pos][1]
            self.array_pos += MOVEMENT_SPEED

        #caso de circulacao normal
        else:
            #print("iff 7")
            self.center_x = self.path[self.array_pos][0]
            self.center_y = self.path[self.array_pos][1]
            self.array_pos += MOVEMENT_SPEED

class MyGame(arcade.Window):
    def __init__(self, size,cars):
        super().__init__(size,size)

        arcade.set_background_color(arcade.color.AMAZON)
        
        self.cars_list = None
        self.wall_list = None
        self.paths = None
        self.counter = 0
        self.iterations = 8
        self.departCoords = [(0,SIZE/2 -50),(800,SIZE/2 + 50),(450,0),(350,800)]
        self.goalCoords = [(0, SIZE/2+50),(800, SIZE/2 -50),(350,0),(450,800)]

    def setup(self):
        self.cars_list = arcade.SpriteList()
        self.wall_list= arcade.SpriteList()
        self.paths=[]
        self.create_sensor_area()

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
        arcade.start_render()
        self.create_road()
        self.draw_lanes(1)
        self.wall_list.draw()
        self.cars_list.draw()

    def update(self, delta_time):
        if(self.iterations>0):
            self.counter+=1
            if (self.counter == 20):
                self.create_car_sprites()
                self.counter = 0
                self.iterations-=1
        if len(self.cars_list) == 0:
            arcade.close_window()
        for car in self.cars_list:
            car.other_cars_list = list((filter(lambda x : x != car,self.cars_list)))

        self.cars_list.update()


    def create_car_sprites(self):
        for i in range(0,4):
            depart = i
            goal = random.randint(0,3)

            while (depart == goal):
                depart = i
                goal = random.randint(0,3)

            depart_coords= self.departCoords[depart]
            goal_coords= self.goalCoords[goal]

            path = self.create_paths(depart_coords, goal_coords)

            if (depart == 1):
                self.car_sprite = Car("car.png", SPRITE_SCALING_CAR, path, goal_coords)
            elif(depart ==2):
                self.car_sprite = Car("car1.png", SPRITE_SCALING_CAR, path, goal_coords)
            elif(depart == 3):
                self.car_sprite = Car("car2.png", SPRITE_SCALING_CAR, path, goal_coords)
            else:
                self.car_sprite = Car("car3.png", SPRITE_SCALING_CAR, path, goal_coords)
            self.car_sprite.center_x = self.departCoords[depart][0]    
            self.car_sprite.center_y = self.departCoords[depart][1]

            distance_to_all_cars = [arcade.get_distance_between_sprites(self.car_sprite,x) for x in self.cars_list]

            if not(len(list(filter(lambda x: x < 70, distance_to_all_cars)))>0):
                self.cars_list.append(self.car_sprite)


    def create_paths(self, depart_coords, goal_coords):        
        depart=[0,0]
        goal=[0,0]

        depart[0] = int(depart_coords[0])
        depart[1] = int(depart_coords[1])
        
        goal[0] = int(goal_coords[0])
        goal[1] = int(goal_coords[1])
                
        final_path=[]

        if(depart[0]==0):   # when agent departs from (0,150)
            if(depart[1]==goal[1]): # from (0,350) to (800,350)
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
    def create_sensor_area(self):
        area = []
        global AREA
        for i in range(200,600):
            for j in range(200,600):
                area.append((i,j))
        AREA = area

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