import math

class Vector(tuple):
    def __add__(self, y):
        if (len(self)==len(y)):
            return Vector((self[i]+y[i] for i in range(len(self))))
        else:
            raise RuntimeError("Can't add vectors of different sizes.")

    def __sub__(self, y):
        if (len(self)==len(y)):
            return Vector((self[i]-y[i] for i in range(len(self))))
        else:
            raise RuntimeError("Can't subtract vectors of different sizes.")

    def __mul__(self, y):
        if (isinstance(y, Vector)):
            if (len(self)==len(y)):
                return sum((self[i]+y[i] for i in range(len(self))))
        else:
            return Vector((x*y for x in self))

    def __rmul__(self, y):
        return self.__mul__(y)

    def __neg__(self):
        return Vector((-x for x in self))

    def __str__(self):
        return "("+(", ".join(map(str, self)))+")"

    def normalize(self):
        n = self.norm()
        print("Vector: "+str(self))
        print("Square: "+str(self.square()))
        print("Norm:   "+str(self.norm()))
        return Vector((x/n for x in self))

    def norm(self):
        return math.sqrt(self.square())

    def square(self):
        return sum((x**2 for x in self))
