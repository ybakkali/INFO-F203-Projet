from random import random,randint,choice
from Graph import Graph
import matplotlib.pyplot as plt
from matplotlib import patches
import numpy as np

class Hypergraph :
    def __init__(self,V={},E={},incidenceMatrix = []) :
        self.V = V
        self.E = E
        self.incidenceMatrix = incidenceMatrix if incidenceMatrix != [] else self.IncidenceGraphMatrix()
        self.dicoV = self.MakeGraph()
        self.Vertices = self.getVertices()
        self.Edges = self.getEdges()
        self.PrimalGraph = self.PrimalGraphMatrix()
        self.incidenceMatrixTranspose = self.incidenceMatrix_Transpose()

    def getVertices(self) :
        return self.V

    def getEdges(self) :
        lst = []
        for Vertex in self.dicoV :
            for Vertex2 in self.dicoV[Vertex] :
                if {Vertex,Vertex2} not in lst :
                    lst.append({Vertex,Vertex2})
        return lst

    def MakeGraph(self) :
        dicoV = {}
        for elem in self.V :
            dicoV[elem] = []

        for hyperedge in self.E :
            x = len(self.E[hyperedge])
            if x > 1 :
                for i in range(x) :
                    for j in range(i+1,x) :
                        if self.E[hyperedge][i] not in dicoV[self.E[hyperedge][j]] :
                            dicoV[self.E[hyperedge][j]].append(self.E[hyperedge][i])
                        if self.E[hyperedge][j] not in dicoV[self.E[hyperedge][i]] :
                            dicoV[self.E[hyperedge][i]].append(self.E[hyperedge][j])
        return dicoV

    def PrimalGraphMatrix(self) :
        n = len(self.V)
        Matrix = [[ 0 for _ in range(n)] for _ in range(n)]
        for Vertex in self.dicoV :
            for Vertex2 in self.dicoV[Vertex] :
                Matrix[self.stringDigit(Vertex)-1][self.stringDigit(Vertex2)-1] = 1

        return Matrix

    def IncidenceGraphMatrix(self) :
        IncidenceMatrix = [[0 for _ in range(len(self.E))] for _ in range(len(self.V)) ]
        for hyperedge in self.E :
            for Vertex in self.E[hyperedge] :
                IncidenceMatrix[self.stringDigit(Vertex)-1][self.stringDigit(hyperedge)-1] = 1

        return IncidenceMatrix

    def incidenceMatrix_Transpose(self) :
        n = len(self.incidenceMatrix)
        m = len(self.incidenceMatrix[0])
        """
        MatrixTranspose = [[0 for i in range(n)] for j in range(m)]
        for i in range(n) :
            for j in range(m) :
                MatrixTranspose[j][i] = self.incidenceMatrix[i][j]
        """
        MatrixTranspose = []
        for i in range(m):
            MatrixTranspose.append([row[i] for row in self.incidenceMatrix])

        return MatrixTranspose

    def generateDualGraph(self) :
        V = set()
        E = {}
        for i in range(len(self.incidenceMatrixTranspose)) :
            Vertex = "E" + str(i+1)
            V.add(Vertex)
            for j in range(len(self.incidenceMatrixTranspose[0])) :
                hyperedge = "Ev" + str(j+1)
                if hyperedge not in E :
                    E[hyperedge] = []
                if self.incidenceMatrixTranspose[i][j] == 1 :
                    E[hyperedge].append(Vertex)

        return Hypergraph(V,E)

    def find_cliques(self,P,R=set(),X=set(),cliques=[]) :
        """
        R := is the set of nodes of a maximal clique.
        P := is the set of possible nodes in a maximal clique.
        X := is the set of nodes that are excluded.
        """

        if not P and not X  :
            if len(R) >= 2 and R not in cliques :
                cliques.append(R)
        else :
            pivot = choice(list(P.union(X)))
            for vertex in P.difference(self.dicoV[pivot]) :
                newP = P.intersection(self.dicoV[vertex])
                newR = R.union({vertex})
                newX = X.intersection(self.dicoV[vertex])
                self.find_cliques(newP,newR,newX,cliques)
                P.difference({vertex})
                X.union({vertex})
        return cliques

    def checkCliques(self) :
        cliques = self.find_cliques(self.V)
        print("Les cliques maximales du graphe :",cliques)
        check = True
        E_values = [set(liste) for liste in self.E.values()]

        for clique in cliques :
            check = clique in E_values
            if not check :
                break

        return check


    def stringDigit(self,str) :
        res = ""
        for letter in str :
            if letter.isdigit() :
                res += letter
        return int(res)

    def show(self):
        plt.figure(figsize=(20,10))
        ax = plt.axes()
        ax.set_aspect("equal")
        plt.axis("off")

        pos = dict()

        if len(self.V) > 0:
            y = 1
            dy = 1/len(self.V)

            for v in self.V:
                pos[v] = y
                ax.add_artist(plt.Circle((0, y), 0.02, color="red",clip_on=False))
                plt.text(0,y,v,horizontalalignment="center",verticalalignment="center",fontsize=10,color="black")
                y-= dy

        if len(self.E.keys()) > 0:
            y = 1
            dy = 1/len(self.E.keys())

            for e in self.E.keys():
                ax.add_artist(plt.Circle((1, y), 0.02, color="red",clip_on=False))
                plt.text(1,y,e,horizontalalignment="center",verticalalignment="center",fontsize=10,color="black")

                for v in self.E[e]:
                    line = plt.Line2D([0.98,0.02], [y,pos[v]],color=(np.random.random(),np.random.random(),np.random.random()),linewidth=5,alpha=0.5,clip_on=False)
                    ax.add_line(line)

                y -= dy

        plt.show()

def printMatrix(Matrix) :
    n = len(Matrix)
    m = len(Matrix[0])
    print("\n".join([" ".join([str(Matrix[i][j]) for j in range(m)]) for i in range(n)]))

def random_graph_generator(n,m):
    V = set(["v" + str(i) for i in range(1,n+1)])
    E = {}
    for i in range(1,m+1) :
        E["E" + str(i)] = []

    incidenceMatrix = [[0 for _ in range(m)] for _ in range(n)]
    for i in range(n):
        for j in range(m):
            if random() < 0.5:

                Vertex = "v" + str(i+1)
                hyperedge = "E" + str(j+1)
                E[hyperedge].append(Vertex)

                incidenceMatrix[i][j] = 1
    """
    ### PRINT Matrix
    printMatrix(incidenceMatrix)
    ### PRINT E
    for elem in E :
        print(elem + " :" , E[elem])
    """
    return Hypergraph(V,E,incidenceMatrix)

def test_hypertree(hypergraph) :
    hypergraphDual = hypergraph.generateDualGraph()
    hypergraphDual.show()
    hypergraphDual_Primal = Graph(hypergraphDual.V,hypergraphDual.dicoV)
    return hypergraphDual.checkCliques() and hypergraphDual_Primal.is_chordal()

graphe = random_graph_generator(randint(1,15),randint(1,15))
#graphe = random_graph_generator(15,15)
print("Vertices of graph:")
print(graphe.Vertices)
print("Edges of graph:")
print(graphe.Edges)
print("Adjacency Matrix")
printMatrix(graphe.PrimalGraph)

print("Incidence Matrix ")
printMatrix(graphe.incidenceMatrix)
print("Incidence Matrix Transpose")
printMatrix(graphe.incidenceMatrixTranspose)
print("\n\n\n\n")

grapheDual = graphe.generateDualGraph()
print("Vertices of dual graph:")
print(grapheDual.Vertices)
print("Edges of dual graph:")
print(grapheDual.Edges)
print("Adjacency Matrix")
printMatrix(grapheDual.PrimalGraph)
print("Incidence Matrix ")
printMatrix(grapheDual.incidenceMatrix)
print("Incidence Matrix Transpose")
printMatrix(grapheDual.incidenceMatrixTranspose)

print("\n\n\n\n")
print("Is Hypertree :",test_hypertree(graphe))
