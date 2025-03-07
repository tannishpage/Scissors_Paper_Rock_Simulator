#import pygame
        
import pygame
import random
import matplotlib.pyplot as plt
import time
# initialize pygame

random.seed(42)

class Ball(pygame.sprite.Sprite):

    def __init__(self, center, surface, size, color, speed, ball_type='Ball', id=0, life_span=5):
        pygame.sprite.Sprite.__init__(self)
        self.speed_x = abs(speed[0])
        self.speed_y = abs(speed[1])

        self.move_dir_x = speed[0]
        self.move_dir_y = speed[1]
        
        self.center_x = center[0]
        self.center_y = center[1]

        self.color = color
        
        self.surface = surface
        self.size = size
        
        self.circle = pygame.draw.circle(self.surface, self.color, (self.center_x, self.center_y), self.size)

        self.ball_type = ball_type
        self.id = id
        self.life_span = life_span
        self.start_time = time.time()
        
    def update(self, collision_list):
        self.move()
        self.if_on_edge_bounce()
        self.circle = pygame.draw.circle(self.surface, self.color, (self.center_x, self.center_y), self.size)
        return self.collide(collision_list)

    def collide(self, collision_list):
        for col_key in collision_list:
            if (((collision_list[col_key].circle.left >= self.circle.left) and (collision_list[col_key].circle.left <= self.circle.right)) or\
                ((collision_list[col_key].circle.right >= self.circle.left) and (collision_list[col_key].circle.right <= self.circle.right))) and\
               (((collision_list[col_key].circle.top >= self.circle.top) and (collision_list[col_key].circle.top <= self.circle.bottom)) or\
                ((collision_list[col_key].circle.bottom >= self.circle.top) and (collision_list[col_key].circle.bottom <= self.circle.bottom))):
                # print(f"COLLISION BETWEEN {col_obj.ball_type}.{col_obj.id} and {self.ball_type}.{self.id}")
                # Remove col_obj and create a new self object
                return col_key

        
    def if_on_edge_bounce(self):
        if self.circle.left <= 0:
            self.move_dir_x = self.speed_x
        elif self.circle.right >= self.surface.get_width():
            self.move_dir_x = -self.speed_x
    
        if self.circle.top <= 0:
            self.move_dir_y = self.speed_y
        elif self.circle.bottom >= self.surface.get_height():
            self.move_dir_y = -self.speed_y
        
        
    def move(self):
        self.center_x = self.center_x + self.move_dir_x
        self.center_y = self.center_y + self.move_dir_y
        

pygame.init()
 
# define width of screen
width = 1920
# define height of screen
height = 1080
screen_res = (width, height)
 
pygame.display.set_caption("Scissor Paper Rock")
screen = pygame.display.set_mode(screen_res)
 
# define colors
red = (255, 0, 150)
blue = (0, 255, 255)
green = (0, 255, 0)
black = (0, 0, 0)


# define ball
scissor_id = 399
paper_id = 399
rock_id = 399

scissor_pop_history = []
paper_pop_history = []
rock_pop_history = []
total_pop_histor = []

total = scissor_id + paper_id + rock_id + 3

speed = 5
size = 10
min_life_span = 1
max_life_span = 3

scissors = {f"Scissors.{x}":Ball((random.randint(30, width-30), random.randint(30, height-30)), screen, size, red, (random.uniform(-speed, speed), random.uniform(-speed, speed)), "Scissors", x, life_span=random.randint(min_life_span, max_life_span)) for x in range(0, scissor_id + 1)}
paper = {f"Paper.{x}":Ball((random.randint(30, width-30), random.randint(30, height-30)), screen, size, green, (random.uniform(-speed, speed), random.uniform(-speed, speed)), "Paper", x, life_span=random.randint(min_life_span, max_life_span)) for x in range(0, paper_id + 1)}
rock = {f"Rock.{x}":Ball((random.randint(30, width-30), random.randint(30, height-30)), screen, size, blue, (random.uniform(-speed, speed), random.uniform(-speed, speed)), "Rock", x, life_span=random.randint(min_life_span, max_life_span)) for x in range(0, rock_id + 1)}

# ball_obj_2 = Ball((150, 150), screen, 20, (1, 1))
# pygame.draw.circle(surface=screen, color=red, center=[100, 100], radius=40)
# define speed of ball
# speed = [X direction speed, Y direction speed]
 
# game loop

clock = pygame.time.Clock()
start_time = time.time()
frame_count = 0

threshold_paper = 0.3333
threshold_scissors = 0.3333
threshold_rock = 0.3333

while True:
    # event loop
    for event in pygame.event.get():
        # check if a user wants to exit the game or not
        if event.type == pygame.QUIT:
            plt.plot(range(0, len(scissor_pop_history)), scissor_pop_history, color='red')
            # plt.plot(range(0, len(scissor_exp_moving_avg)), scissor_exp_moving_avg)
            plt.plot(range(0, len(paper_pop_history)), paper_pop_history, color='green')
            # plt.plot(range(0, len(paper_exp_moving_avg)), paper_exp_moving_avg)
            plt.plot(range(0, len(rock_pop_history)), rock_pop_history, color='blue')
            # plt.plot(range(0, len(rock_exp_moving_avg)), rock_exp_moving_avg)
            plt.plot(range(0, len(total_pop_histor)), total_pop_histor, color='black')
            plt.legend(["Scissors", "Scissors EMA", "Paper", "Paper EMA", "Rock", "Rock EMA", "Total Population"])
            plt.xlabel("Time (Frames)")
            plt.ylabel("Number of Objects")
            plt.show()
            exit()

    screen.fill(black)
    scissor_keys = list(scissors.keys())
 
    # fill black color on screen
    for key in scissor_keys:
        if time.time() - scissors[key].start_time >= scissors[key].life_span:
            scissors[key].kill()
            scissors.pop(key)
        else:
            collision_key = scissors[key].update(paper)
            if collision_key is not None:
                paper[collision_key].kill()
                paper.pop(collision_key)
                scissor_id += 1
                scissors[f"Scissors.{scissor_id}"] = Ball((random.randint(30, width-30), random.randint(30, height-30)), screen, size, red, (random.uniform(-speed, speed), random.uniform(-speed, speed)), "Scissors", scissor_id, life_span=random.randint(min_life_span, max_life_span))
                
            
            
    paper_keys = list(paper.keys())

    for key in paper_keys:
        if time.time() - paper[key].start_time >= paper[key].life_span:
            paper[key].kill()
            paper.pop(key)
        else:
            collision_key = paper[key].update(rock)
            if collision_key is not None:
                rock[collision_key].kill()
                rock.pop(collision_key)
                paper_id += 1
                paper[f"Paper.{paper_id}"] = Ball((random.randint(30, width-30), random.randint(30, height-30)), screen, size, green, (random.uniform(-speed, speed), random.uniform(-speed, speed)), "Paper", paper_id, life_span=random.randint(min_life_span, max_life_span))


    rock_keys = list(rock.keys())

    for key in rock_keys:
        if time.time() - rock[key].start_time >= rock[key].life_span:
            rock[key].kill()
            rock.pop(key)
        else:
            collision_key = rock[key].update(scissors)
            if collision_key is not None:
                scissors[collision_key].kill()
                scissors.pop(collision_key)
                rock_id += 1
                rock[f"Rock.{rock_id}"] = Ball((random.randint(30, width-30), random.randint(30, height-30)), screen, size, blue, (random.uniform(-speed, speed), random.uniform(-speed, speed)), "Rock", rock_id, life_span=random.randint(min_life_span, max_life_span))

    # Reproduction:
    if random.uniform(0, 1) >= 1 - threshold_rock:
        rock_id += 1
        rock[f"Rock.{rock_id}"] = Ball((random.randint(30, width-30), random.randint(30, height-30)), screen, size, blue, (random.uniform(-speed, speed), random.uniform(-speed, speed)), "Rock", rock_id, life_span=random.randint(min_life_span, max_life_span))
    
    if random.uniform(0, 1) >= 1 - threshold_paper:
        paper_id += 1
        paper[f"Paper.{paper_id}"] = Ball((random.randint(30, width-30), random.randint(30, height-30)), screen, size, green, (random.uniform(-speed, speed), random.uniform(-speed, speed)), "Paper", paper_id, life_span=random.randint(min_life_span, max_life_span))

    if random.uniform(0, 1) >= 1 - threshold_scissors:
        scissor_id += 1
        scissors[f"Scissors.{scissor_id}"] = Ball((random.randint(30, width-30), random.randint(30, height-30)), screen, size, red, (random.uniform(-speed, speed), random.uniform(-speed, speed)), "Scissors", scissor_id, life_span=random.randint(min_life_span, max_life_span))

    
    print(f"Total: {len(scissors) + len(paper) + len(rock)} Scissors: {len(scissors)} Paper: {len(paper)} Rock: {len(rock)} Time: {time.time() - start_time:.2f} s Frame Count: {frame_count}") #"Scissors:", len(scissors), "Paper:", len(paper), "Rock:", len(rock))

    scissor_pop_history.append(len(scissors))
    paper_pop_history.append(len(paper))
    rock_pop_history.append(len(rock))
    total_pop_histor.append(len(scissors) + len(paper) + len(rock))

    threshold_scissors = len(scissors) / (len(scissors) + len(paper) + len(rock))
    threshold_paper = len(paper) / (len(scissors) + len(paper) + len(rock))
    threshold_rock = len(rock) / (len(scissors) + len(paper) + len(rock))

    if len(scissors) + len(paper) + len(rock) == 0:
        print("Simulation Over!")
        break

    dt = clock.tick(60)
    pygame.display.flip()
    frame_count += 1

def exponential_moving_average(values, alpha):
    # First value of moving avg is the first value in the series
    moving_averages = [values[0]]
    for value in values[1:]:
        # Calculating simple moving average
        moving_averages.append(moving_averages[-1] +\
                                (alpha*(value - moving_averages[-1])))
    return moving_averages

# scissor_exp_moving_avg = exponential_moving_average(scissor_pop_history, 0.005)
# paper_exp_moving_avg = exponential_moving_average(paper_pop_history, 0.005)
# rock_exp_moving_avg = exponential_moving_average(rock_pop_history, 0.005)

plt.plot(range(0, len(scissor_pop_history)), scissor_pop_history, color='red')
# plt.plot(range(0, len(scissor_exp_moving_avg)), scissor_exp_moving_avg)
plt.plot(range(0, len(paper_pop_history)), paper_pop_history, color='green')
# plt.plot(range(0, len(paper_exp_moving_avg)), paper_exp_moving_avg)
plt.plot(range(0, len(rock_pop_history)), rock_pop_history, color='blue')
# plt.plot(range(0, len(rock_exp_moving_avg)), rock_exp_moving_avg)
plt.plot(range(0, len(total_pop_histor)), total_pop_histor, color='black')
plt.legend(["Scissors", "Scissors EMA", "Paper", "Paper EMA", "Rock", "Rock EMA", "Total Population"])
plt.xlabel("Time (Frames)")
plt.ylabel("Number of Objects")
plt.show()