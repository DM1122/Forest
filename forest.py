import csv
import random
import csvlib
import graphviz


class Node:

    def __init__(self, data=None, parent=None, branches=None, index=None):
        self.data = data
        self.parent = parent
        self.branches = branches
        self.index = index
    

    def __str__(self):
        parent = self.parent.index if self.parent != None else None
        branches = len(self.branches) if self.branches != None else None

        string = 'Node {} | Data ({}): {} | Parent: {} | Branches: {}'.format(
            self.index,
            type(self.data),
            self.data,
            parent,
            branches)

        return string


class Tree:

    def __init__(self, mapp, dims, root, leafs, size, headings=None):
        self.map = mapp
        self.dims = dims
        self.root = root
        self.leafs = leafs
        self.size = size
        self.headings = headings


    def __str__(self):
    
        string = 'Tree Root: {} | Size: {} | Dims: {}'.format(
            self.root.data,
            self.size,
            self.dims
        )

        return string


    @classmethod
    def fromCSV(cls, filename, headings=False):
        with open(filename, 'r') as f:
            reader = csv.reader(f, delimiter=',')
            data = [row for row in reader]

            if headings:
                headings = [row[:1] for row in data]
                headings = [heading[0] for heading in headings]     # transpose
                data = [row[1:] for row in data]

        nodes = []

        root = Node(data=data[0][0].strip(), index=(0,0))       # look into stripping at data ingestion stage
        nodes.append(root)

        def buildBranches(parent):
            #region span
            span = 0
            while not parent.index[1]+1+span > len(data[0])-1:
                neighbour = data[parent.index[0]][parent.index[1]+1+span].strip()
                if neighbour == '':
                    span += 1
                else:
                    break
            #endregion

            #region branches
            branches = []
            if not parent.index[0]+1 > len(data)-1:
                for i, val in enumerate(data[parent.index[0]+1][parent.index[1]:parent.index[1]+span+1]):
                    val = val.strip()
                    if val != '':
                        branch = Node(data=val, parent=parent, index=(parent.index[0]+1, parent.index[1]+i))
                        branches.append(branch)
                        nodes.append(branch)
                parent.branches = branches

                # recurse over all sub branches
                for branch in parent.branches:
                    buildBranches(branch)
            #endregion

        buildBranches(root)
        
        # map
        mapp = dict()
        for node in nodes:
            mapp[node.index] = node
    
        # dims
        dims_h = max([index[0] for index in mapp.keys()]) + 1
        dims_w = max([index[1] for index in mapp.keys()]) + 1
        dims = [dims_h, dims_w]
        
        # leafs
        leafs = []
        for index, node in mapp.items():
            if index[0] == dims[0]-1:        # assumes all leaves exist at same level
                leafs.append(node)

        # size
        size = len(mapp)

        # headings
        if headings:
            return cls(mapp, dims, root, leafs, size, headings)
        else:
            return cls(mapp, dims, root, leafs, size)


    def toCSV(self, filename):
        '''
        Uses a pre-order traversal algorithm to print tree object to csv.
        '''

        stylus = csvlib.Stylus(filename)

    
        def preorder(node, index=[0,0]):

            stylus.writeCell(node.data, index)
            original_index = index.copy()
            index[0] += 1

            try:
                node.branches[0]
            except:
                return original_index[1]
            else:
                marker = preorder(node.branches[0], index)

            original_index[1] += marker+1
            original_index[0] += 1

            try:
                node.branches[1]
            except:
                return original_index[1]
            else:
                marker = preorder(node.branches[1], original_index)
                
                

        preorder(self.root)


    def draw(self):
        dot = graphviz.Digraph(format='png')
                
        def traverse(node, idx=0):
            if node.parent == None:                 # root
                dot.node(str(id(node)), node.data)
            else:
                dot.node(str(id(node)), node.data)
                dot.edge(str(id(node.parent)), str(id(node)))
            
            if node.branches != None:
                for branch in node.branches:
                    traverse(branch, idx)

        traverse(self.root)

        with open('dot.txt', 'w') as f:
            f.write(dot.source)
        dot.render('tree', view=True)

    def pathsToCSV(self):
        '''
        Returns a csv containing all possible tree paths.
        '''

        paths = []
        for leaf in self.leafs:
            path = []
            node = leaf
            while node != None:
                try:
                    path.append(node.data)
                    node = node.parent
                except:
                    node = None
            
            path.reverse()
            paths.append(path)

        with open('paths.csv', mode='w', newline='') as f:
            writer = csv.writer(f, delimiter=',')
            if self.headings:
                writer.writerow(self.headings)
            writer.writerows(paths)
        print('Successfully saved paths to disk.')
    

    def traversalCheck(self):
        print("--- Traversal Check ---")
        print("Leftmost traversal: ")
        node = self.root
        while node != None:
            print(node)
            try:
                node = node.branches[0]
            except:
                node = None

        print("Rightmost traversal: ")
        node = self.root
        while node != None:
            print(node)
            try:
                node = node.branches[-1]
            except:
                node = None

        print("Traversal check complete.")


    def randomWalk(self):
        print('--- Random Walk ---')
        node = self.root
        while node != None:
            print(node)
            try:
                node = random.choice(node.branches)
            except:
                node = None
        
        print('Random walk complete.')


    def calcDist(self):
        '''
        Finds the nodal distribution of the tree across levels.
        Returns dict.
        '''
        dist = {}
        for level in range(self.dims[0]):
            count = len([node for node in self.map if node[0] == level])
            dist[level] = count
        

        return dist
        

    def calcDistP(self):
        '''
        Finds the nodal percentage distribution of the tree across levels.
        Returns dict.
        '''
        distp = {}
        for level in range(self.dims[0]):
            countp = len([node for node in self.map if node[0] == level]) / self.size
            countp *= 100
            countp = round(countp,2)
            distp[level] = countp
        

        return distp
            

if __name__ == '__main__':
    tree = Tree.fromCSV('Laptop2_tree.csv', headings=True)
    print(tree)
    tree.draw()
