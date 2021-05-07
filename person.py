import time

class Person:
    def __init__(self, new_id, x, y):
        self.id = new_id 
        self.x  = x
        self.y  = y

    def update_loc(self, new_x, new_y):
        self.x = x
        self.y = y

    def ret_loc(self):
        return (self.x, self.y)
