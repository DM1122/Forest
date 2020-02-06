import graphviz

# import sys
# sys.path.append('C:\\Users\\DMara\\Documents\\_Workbench\\Workspace')
# from workspacelib import Workspace


class Graph:
    '''
    A general-purpose graph class.
    '''

    def __init__(self, matrix, headers=None):
        self.matrix = matrix
        self.headers = headers
    
    
    def draw(self):
        dot = graphviz.Graph(format='png', engine='neato')

        dimm = len(self.matrix)
        
        for i in range(dimm):
            for j in range(i,dimm):
                if self.headers:
                    x, y = self.headers[i], self.headers[j]
                else:
                    x, y = str(i), str(j)

                if self.matrix[i][j] != 0:
                    dot.edge(x, y, label=str(self.matrix[i][j]), len=str(self.matrix[i][j]))
                else:
                    dot.node(x)
                    dot.node(y)

        dot.render('graph', view=True)  



if __name__ == '__main__':
    matrix = [
        [0, 1, 0, 2, 0],
        [1, 1, 3, 0, 0],
        [0, 3, 0, 0, 0],
        [2, 0, 0, 0, 0],
        [0, 0, 0, 0, 0]
    ]

    headers = ['A', 'B', 'C', 'D', 'E']

    graph = Graph(matrix=matrix, headers=headers)
    graph.draw()