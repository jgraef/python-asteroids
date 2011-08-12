from vector import Vector
from math import sin, cos, pi
from random import uniform


class Object:
    collision_mask = []
    
    # TODO add vector graphic for collision detection
    def __init__(self, world, x = (0.0, 0.0), angle = None):
        self.world = world
        self.x = Vector(x)
        self.v = Vector((0.0, 0.0))
        self.a = Vector((0.0, 0.0))
        self.angle = angle
        self.size = 0.0

    def integrate(self, dt):
        self.x += self.v*dt + 0.5*self.a*dt**2
        self.v += self.a*dt
        self.a = Vector((0.0, 0.0))

    def accelerate(self, a = (0.0, 0.0)):
        self.a += a

    def accelerate_polar(self, a = 0.0, angle = None):
        if (angle==None):
            angle = self.angle
        self.a += Vector((-a*sin(angle), -a*cos(angle)))

    def collision_detection(self, objB):
        return (self.x-objB.x).norm()<=self.size+objB.size

    def on_collision(self, objB):
        pass


class Shot(Object):
    def __init__(self, world, shooter, v):
        Object.__init__(self, world, shooter.x, shooter.angle)
        self.collision_mask = [Asteroid, Ufo]
        self.shooter = shooter
        self.v = shooter.v+Vector((-v*sin(shooter.angle), -v*cos(shooter.angle)))
        self.size = 0.001
        self.death_time = world.t+2.5

    def on_collision(self, objB):
        self.world.remove_object(self)
        if (type(objB)==Ufo):
            self.world.score += 1000
        elif (type(objB)==Asteroid):
            self.world.score += 100

    def integrate(self, dt):
        if (self.world.t<self.death_time):
            Object.integrate(self, dt)
        else:
            self.world.remove_object(self)


class Asteroid(Object):
    def __init__(self, world, x = (0.0, 0.0), v = (0.0, 0.0)):
        Object.__init__(self, world, x)
        self.collision_mask = [Shot, Spaceship, Ufo]
        self.v = Vector(v)
        self.size = 0.05
        self.smallest_size = self.size/4.0
        self.num_fragments = 2

    def on_collision(self, objB):
        # TODO play explosion animation
        if (self.size>self.smallest_size):
            for i in range(self.num_fragments):
                f = Asteroid(self.world, self.x+Vector((uniform(-0.5*self.size, 0.5*self.size), uniform(-0.5*self.size, 0.5*self.size))), self.world.floating_speed())
                f.size = self.size/2.0
                self.world.add_object(f)
        self.world.remove_object(self)
            

class Spaceship(Object):
    def __init__(self, world, **params):
        Object.__init__(self, world, (0.5*world.size, 0.5*world.size), 0.0)
        self.collision_mask = [Asteroid, Ufo]
        self.lifes = params.get("lifes", 3)
        self.max_shots = params.get("max_shots")
        self.unmortal_time = params.get("unmortal_time", 3.0)
        self.reloading_time = params.get("reloading_time", 0.1)
        self.unmortal = world.t+self.unmortal_time
        self.reloading = 0.0
        self.acceleration = params.get("acceleration", 0.2)
        self.turn_rate = params.get("turn_rate", 0.1)
        self.shot_speed = params.get("shot_speed", 0.2)
        self.max_shots = params.get("max_shots", 10)
        self.size = 0.02

    def on_collision(self, objB):
        if (self.unmortal<self.world.t):
            # TODO play explosion animation
            self.unmortal = self.world.t+self.unmortal_time
            self.x = Vector((0.5*self.world.size, 0.5*self.world.size))
            self.v = Vector((0.0, 0.0))
            self.angle = 0.0
            if (self.lifes==0):
                self.world.controller.gameover(self.world.score)
            else:
                self.lifes -= 1

    def shoot(self):
        if (self.reloading<self.world.t and len(self.world.get_shots())<self.max_shots):
            self.world.add_object(Shot(self.world, self, self.shot_speed))
            self.reloading = self.world.t+self.reloading_time

    def hyperspace(self):
        self.x = Vector((uniform(0.0, self.world.size), uniform(0.0, self.world.size)))
        self.v = Vector((0, 0))

    def accelerate(self):
        self.accelerate_polar(self.acceleration)

    def turn(self, direction):
        self.angle = (self.angle+direction*self.turn_rate)%(2.0*pi)
    

class Ufo(Object):
    def __init__(self, world, x = (0.0, 0.0), v = (0.0, 0.0)):
        Object.__init__(self, world, x, 0.0)
        self.collision_mask = [Asteroid, Ufo]
        self.size = 0.01

    def on_collision(self, objB):
        self.world.remove_object(self)


class World:
    def __init__(self, controller, dt = 0.1):
        self.controller = controller
        self.size = 1.0
        self.dt = dt
        self.t = 0.0
        self.max_floating_speed = 0.1
        self.level = 1
        self.objects = []
        self.add_object(Spaceship(self))
        self.spawn_asteroids()
        self.score = 0

    def integrate(self):
        for o in self.objects:
            o.integrate(self.dt)
            o.x = Vector((x%self.size for x in o.x))
        self.t += self.dt

        if (self.get_asteroids()==[]):
            self.level += 1
            self.score += 100
            self.remove_object(*self.get_shots())
            self.spawn_asteroids()

    def collision_detection(self):
        # TODO need only to do 0.5*(n**2 - n) checks
        checked = []
        
        for oA in self.objects:
            for oB in filter(lambda o: (o, oA) not in checked and (oA, o) not in checked and o!=oA and (type(o) in oA.collision_mask or type(oA) in o.collision_mask), self.objects):
                checked.append((oA, oB))
                if (oA.collision_detection(oB)):
                    if (type(oA) in oB.collision_mask):
                        oB.on_collision(oA)
                    if (type(oB) in oA.collision_mask):
                        oA.on_collision(oB)

    def add_object(self, *objects):
        for o in objects:
            if (o not in self.objects):
                self.objects.append(o)

    def remove_object(self, *objects):
        for o in objects:
            if (o in self.objects):
                self.objects.remove(o)

    def get_spaceship(self):
        return self.get_objects(Spaceship, True)

    def get_spaceships(self):
        return self.get_objects(Spaceship)

    def get_ufo(self):
        return self.get_objects(Ufo, True)

    def get_asteroids(self):
        return self.get_objects(Asteroid)

    def get_shots(self):
        return self.get_objects(Shot)

    def get_objects(self, t, only_one = False):
        l = list(filter(lambda o: type(o)==t, self.objects))
        if (only_one):
            if (l==[]):
                return None
            else:
                return l[0]
        else:
            return l

    def random_position(self):
        return Vector((uniform(0.0, self.size), uniform(0.0, self.size)))

    def floating_speed(self):
        return Vector((uniform(0.0, self.max_floating_speed), uniform(0.0, self.max_floating_speed)))

    def spawn_asteroids(self):
        for i in range(self.level+2):
            self.add_object(Asteroid(self, self.random_position(), self.floating_speed()))
