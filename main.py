import arcade

#SCREEN_WIDTH = 1000
SIZE= 1000  # Map will be always a square
SPRITE_SCALING_CAR = 0.4
C = SIZE / 2
GREY = (128,128,128)
WHITE = (255,255,255)
ROAD_HEIGHT = 200

class MyGame(arcade.Window):
    """ Main application class. """

    def __init__(self, size,cars):
        super().__init__(size,size)

        arcade.set_background_color(arcade.color.AMAZON)

    def setup(self):
        self.cars_list = arcade.SpriteList()
        self.car_sprite = arcade.Sprite("car.png",SPRITE_SCALING_CAR)
        self.car_sprite.center_x = 0
        self.car_sprite.center_y = C
        self.cars_list.append(self.car_sprite)
        # Set up your game here
        pass

    def on_draw(self):
        """ Render the screen. """
        arcade.start_render()
        self.create_road()
        self.draw_lanes(2)
        self.cars_list.draw()
        # Your drawing code goes here

    def update(self, delta_time):
        """ All the logic to move, and the game logic goes here. """
        pass

    def create_car_sprites(self):
        """Create all cars"""
        #for i in range()
        pass
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
