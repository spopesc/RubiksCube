# A class to represent a Rubik's cube.
class RubiksCube:
    
    # Initialize and set all faces equivalent to a solved cube, with yellow facing up.
    def __init__(self):
        self.U = [["Y"] * 3 for i in range(3)]
        self.F = [["B"] * 3 for i in range(3)]
        self.R = [["R"] * 3 for i in range(3)]
        self.B = [["G"] * 3 for i in range(3)]
        self.L = [["O"] * 3 for i in range(3)]
        self.D = [["W"] * 3 for i in range(3)]
    
    # A method to rotate a matrix 90 degree clockwise.
    def rotate(self, face):
        n = len(face)
        rotated = [[0] * n for i in range(n)]
        
        for i in range(n):
            for j in range(n):
                rotated[j][n - 1 - i] = face[i][j]
        
        return rotated
    
    # Print the cube in a human-friendly format.
    def show(self):
        n = len(self.U)
        print()
        for i in range(n):
            for j in range(n):
                print(self.U[i][j], end = " ")
            print()
        print()
        
        for i in range(n):
            for j in range(n):
                print(self.F[i][j], end = " ")
            print("\t", end = "")
            for j in range(n):
                print(self.R[i][j], end = " ")
            print("\t", end = "")
            for j in range(n):
                print(self.B[i][j], end = " ")
            print("\t", end = "")
            for j in range(n):
                print(self.L[i][j], end = " ")
            print()
        print()
        
        for i in range(n):
            for j in range(n):
                print(self.D[i][j], end = " ")
            print()
        print("\n" + "-" * 40)            
    
    # Where all the fun happens!
    def move(self, direction, show = False):
        
        if show: print(f"Selected move: {direction}")
        
        if len(direction) == 2:
            if direction[1] == "2":
                for i in range(2): self.move(direction[0])
            if direction[1] == "'":
                for i in range(3): self.move(direction[0])
        
        if direction == "x":
            temp = self.U
            self.U = self.F
            self.F = self.D
            self.D = self.B
            self.B = temp
            self.R = self.rotate(self.R)
            for i in range(2): self.B = self.rotate(self.B)
            for i in range(2): self.D = self.rotate(self.D)
            for i in range(3): self.L = self.rotate(self.L)
            
        if direction == "y":
            temp = self.F
            self.F = self.R
            self.R = self.B
            self.B = self.L
            self.L = temp
            self.U = self.rotate(self.U)
            for i in range(3): self.D = self.rotate(self.D)
        
        if direction == "z":
            self.move("y")
            self.move("x'")
            self.move("y'")
    
        if direction == "U":
            self.U = self.rotate(self.U)
            temp = self.F[0]
            self.F[0] = self.R[0]
            self.R[0] = self.B[0]
            self.B[0] = self.L[0]
            self.L[0] = temp
            
        if direction == "D":
            self.D = self.rotate(self.D)
            temp = self.F[2]
            self.F[2] = self.L[2]
            self.L[2] = self.B[2]
            self.B[2] = self.R[2]
            self.R[2] = temp
        
        if direction == "R":
            self.move("z'")
            self.move("U")
            self.move("z")
        
        if direction == "L":
            self.move("z")
            self.move("U")
            self.move("z'")
        
        if direction == "F":
            self.move("x")
            self.move("U")
            self.move("x'")
        
        if direction == "B":
            self.move("x'")
            self.move("U")
            self.move("x")
        
        if direction == "M":
            self.move("R")
            self.move("L'")
            self.move("x'")
    
    # Perform multiple `move()` steps.
    def alg(self, algorithm):
        algorithm = algorithm.split()
        for i in algorithm:
            self.move(i)
    
    # Scramble the cube.
    def scramble(self, show = False):
        from random import randint
        alg = ""
        possible_moves = "U D R L F B U' D' R' L' F' B' U2 D2 R2 L2 F2 B2".split()
        for i in range(randint(28, 36)):
            alg += possible_moves[randint(0, 17)] + " "
        if show: print(f"\nScrambling cube: {alg}")
        self.alg(alg)
    
    # Revert the cube to its solved state.
    def reset(self):
        self.U = [["Y"] * 3 for i in range(3)]
        self.F = [["B"] * 3 for i in range(3)]
        self.R = [["R"] * 3 for i in range(3)]
        self.B = [["G"] * 3 for i in range(3)]
        self.L = [["O"] * 3 for i in range(3)]
        self.D = [["W"] * 3 for i in range(3)]

"""cube = RubiksCube()
cube.show()
cube.alg("M' D M'")
cube.show()"""