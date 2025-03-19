class TunnelPoint:
    def __init__(self, x : float, y : float, z : float, radius : float):
        self.x = x
        self.y = y
        self.z = z
        self.radius = radius

    def get_coordinates(self):
        return (self.x, self.y, self.z)
    
    def get_radius(self):
        return self.radius

    def __str__(self):
        return "Point: (" + str(self.x) + ", " + str(self.y) + ", " + str(self.z) + ", " + str(self.radius) +")"
    
    def __repr__(self):
        return self.__str__()
    
    def __eq__(self, other):
        return self.x == other.x and self.y == other.y and self.z == other.z and self.radius == other.radius
    
    def __hash__(self):
        return hash((self.x, self.y, self.z, self.radius))