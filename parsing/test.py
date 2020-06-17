class s:
    def __init__(self, x):
        self.x = x
        self.getX()
    def getX(self):
        print(self.x)
        return self.x
x = s(3)
print(x)