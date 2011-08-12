import math
# vector.py - Simple Asteroids game engine
# Copyright (C) 2011 by Janosch Gräf <janosch.graef@gmx.net>
#
# Permission is hereby granted, free of charge, to any person obtaining a copy
# of this software and associated documentation files (the "Software"), to deal
# in the Software without restriction, including without limitation the rights
# to use, copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the Software is
# furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY,
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL THE
# AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING FROM,
# OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN
# THE SOFTWARE.

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
