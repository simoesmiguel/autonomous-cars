import arcade
import random
import math

#SCREEN_WIDTH = 1000
SIZE= 800  # Map will be always a square
SPRITE_SCALING_CAR = 0.03
SPRITE_SCALING_WALL = 0.1

C = SIZE/2
GREY = (128,128,128)
WHITE = (255,255,255)
ROAD_HEIGHT = 200
MOVEMENT_SPEED = 5



class Car(arcade.Sprite):
    """ Player class """

    def __init__(self, image, scale, goal):
        """ Set up the player """
        self.goal= goal
        # Call the parent init
        super().__init__(image, scale)

        #hold the speed.
        self.speed = 0

    def update(self):
        '''
        # Convert angle in degrees to radians.
        angle_rad = math.radians(self.angle)

        # Rotate the car
        self.angle += self.change_angle

        # Use math to find our change based on our speed and angle
        self.center_x += -self.speed * math.sin(angle_rad)
        self.center_y += self.speed * math.cos(angle_rad)
        '''
        if(self.goal[0] > self.center_x):
            self.center_x +=1

        elif(self.goal[0] < self.center_x):
            self.center_x-=1

        elif(self.goal[1] < self.center_y):
            self.center_y-=1

        elif(self.goal[1] > self.center_y):
            self.center_y+=1




class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, size,cars):
        super().__init__(size,size)

        arcade.set_background_color(arcade.color.AMAZON)
        
        self.cars_list = None

        self.wall_list = None


        self.coords=[(0,SIZE/4 -50,0),(800,SIZE/4 + 50,180),(550,0,90),(450,800,-90)]


    def setup(self):
        self.cars_list = arcade.SpriteList()
        self.wall_list= arcade.SpriteList()
        
        self.create_car_sprites()
        # Set up your game here


        self.draw_walls(0,200,200)
        self.draw_walls(0,200,100)

        self.draw_walls(600,800,200)
        self.draw_walls(600,800,100)
        self.draw_walls(600,800,600)
        
        self.draw_walls(600,800,800)

        self.draw_walls(0,200,600)

        self.draw_walls(0,200,800)
    


        #self.physics_engine = arcade.PhysicsEngineSimple(self.cars_list,
        #                                                    self.wall_list)        

    
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
        self.cars_list.update()
         

    def create_car_sprites(self):
        """Create all cars"""

        for i in range(0,41):

            depart = random.randint(0,3)
            goal = random.randint(0,3)

            while (depart== goal):
                depart = random.randint(0,3)
                goal = random.randint(0,3)

            self.car_sprite = Car("car.png", SPRITE_SCALING_CAR, [self.coords[goal][0],self.coords[goal][1]])

            self.car_sprite.center_x = self.coords[depart][0]    
            self.car_sprite.center_y = self.coords[depart][1]
            self.car_sprite.radians = self.coords[depart][2]
            self.cars_list.append(self.car_sprite)



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
            
        
    def on_key_press(self, key, modifiers):
        if key == arcade.key.UP:
            self.car_sprite.change_y = MOVEMENT_SPEED
        elif key == arcade.key.DOWN:
            self.car_sprite.change_y = -MOVEMENT_SPEED
        elif key == arcade.key.LEFT:
            self.car_sprite.change_x = -MOVEMENT_SPEED
        elif key == arcade.key.RIGHT:
            self.car_sprite.change_x = MOVEMENT_SPEED

    def on_key_release(self, key, modifiers):
        if key == arcade.key.UP or key == arcade.key.DOWN:
            self.car_sprite.change_y = 0
        elif key == arcade.key.LEFT or key == arcade.key.RIGHT:
            self.car_sprite.change_x = 0

def main():
    game = MyGame(SIZE,30)
    game.setup()
    arcade.run()


if __name__ == "__main__":
    main()
