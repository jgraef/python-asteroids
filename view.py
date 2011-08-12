import pygame
from model import Asteroid, Spaceship, Ufo, Shot
from singleton import singleton
from math import sin, cos


@singleton
class View:
    # custom SDL events
    EVENT_RENDER = pygame.USEREVENT
    EVENT_SIMULATE = pygame.USEREVENT+1
    # human input keys
    key_up = False
    key_left = False
    key_right = False
    key_space = False
    # object type colors
    object_colors = {Asteroid: (255, 255, 255),
                     Spaceship: (0, 0, 255),
                     Ufo: (255, 0, 0),
                     Shot: (0, 255, 0)}
    
    def __init__(self, **params):
        pygame.init()
        self.resolution = params.get("resolution", 640)
        self.fps = params.get("fps", 25)
        self.sim_rate = params.get("sim_rate", 25)
        self.sound = params.get("sound", False)
        self.screen = pygame.display.set_mode((self.resolution, self.resolution),
                                              pygame.FULLSCREEN if params.get("fullscreen", False) else 0)
        self.font = pygame.font.SysFont("helvetica", 12)
        pygame.time.set_timer(self.EVENT_RENDER, int(1000.0/self.fps))
        pygame.time.set_timer(self.EVENT_SIMULATE, int(1000.0/self.sim_rate))

    def render(self, world):
        # black background
        self.screen.fill((0, 0, 0))

        # render objects
        for o in world.objects:
            p = (int(o.x[0]/world.size*self.resolution), int(o.x[1]/world.size*self.resolution))
            r = int(o.size/world.size*self.resolution)
            if (r==0 and o.size>0.0):
                r = 1
            c = self.object_colors[type(o)]
            if (type(o)==Spaceship and o.unmortal_time>world.t and (world.t%0.5)<0.1):
                c = (0, 0, 0)
            if (r>0):
                pygame.draw.circle(self.screen, c, p, r, 1)
                if (o.angle!=None):
                    pygame.draw.line(self.screen, c, p, (p[0]-r*sin(o.angle), p[1]-r*cos(o.angle)))
                else:
                    self.screen.set_at(p, c)

        # render information
        self.draw_text("Time:  "+str(world.t)+" s", (5, 5))
        self.draw_text("Score:  "+str(world.score), (5, 20))
        self.draw_text("Level: "+str(world.level), (5, 35))
        self.draw_text("Lifes: "+str(world.get_spaceship().lifes), (5, 50))

        pygame.display.update()

    def draw_text(self, text, pos):
        surface = self.font.render(text, True, (255, 255, 255))
        self.screen.blit(surface, pos)

    def handle_events(self, controller, world):
        events = pygame.event.get()
        for e in events:
            if (e.type==pygame.QUIT):
                controller.quit()
            elif (e.type==self.EVENT_RENDER):
                self.render(world)
            elif (e.type==self.EVENT_SIMULATE):
                if (self.key_up):
                    controller.input("human", "accelerate")
                if (self.key_left):
                    controller.input("human", "turn_left")
                if (self.key_right):
                    controller.input("human", "turn_right")
                if (self.key_space):
                    controller.input("human", "shoot")
                controller.callback_model_step()
            elif (e.type==pygame.KEYUP):
                self.event_keyboard(controller, e.key, e.mod, False)
            elif (e.type==pygame.KEYDOWN):
                self.event_keyboard(controller, e.key, e.mod, True)
        
    def event_keyboard(self, controller, key, mod, pressed):
        if (key==pygame.K_UP):
            self.key_up = pressed
        elif (key==pygame.K_DOWN):
            self.key_down = pressed
        elif (key==pygame.K_LEFT):
            self.key_left = pressed
        elif (key==pygame.K_RIGHT):
            self.key_right = pressed
        elif (key==pygame.K_SPACE):
            self.key_space = pressed
        elif ((key==pygame.K_LCTRL or key==pygame.K_RCTRL) and not pressed):
            controller.input("human", "hyperspace")
