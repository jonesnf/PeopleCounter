import time

# Class to hold person id, and centroid info (x, y)
class Person:
    def __init__(self, new_id, x, y):
        self.id = new_id 
        self.x  = x
        self.y  = y

    def update_loc(self, new_centr_x, new_centr_y):
        self.x = new_centr_x
        self.y = new_centr_y

    def ret_loc(self):
        return (self.x, self.y)

