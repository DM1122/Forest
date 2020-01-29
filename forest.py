import csv
import graphviz
import os
import random



class Node:

    def __init__(self, data=None, parent=None, branches=None, height=1, bf=0, index=None):
        self.data = data
        self.parent = parent
        self.branches = branches
        self.height = height
        self.bf = bf
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

    def __init__(self):
        self.map = None
        self.dims = None
        self.root = None
        self.leafs = []
        self.size = None


    def __str__(self):
    
        string = 'Tree Root: {} | Size: {} | Dims: {}'.format(
            self.root.data,
            self.size,
            self.dims
        )

        return string

   
    def fromTextFile(self, filepath):
        with open(filepath, 'r') as fil:
            data = fil.read()
            data = data.splitlines()
        
        for e in data:
            self.insert(e)



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
        if not os.path.exists('drawings'):
            os.mkdir('drawings')
        
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

        i = 0
        print(os.listdir('drawings'))
        while os.path.exists('drawings/tree{}.png'.format(i)):
            i += 1
            
        dot.render('drawings/tree{}'.format(i), view=False)


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
            

    def updateHeight(self, node):
        '''
        Recursively updates the height attribute of each node in the tree starting from the node passed.
        '''

        if node != None:
            node.height = max(self.updateHeight(node.left), self.updateHeight(node.right))
            return node.height + 1
        else:
            return 1


    def updateBalanceFactor(self, node):
        '''
        Recursively updates the balance factor attribute of each node in the tree starting from the node passed.
        '''
        if node != None:
            if node.right != None and node.left != None:
                node.bf = node.right.height - node.left.height
            elif node.right != None and node.left == None:
                node.bf = node.right.height
            elif node.right == None and node.left != None:
                node.bf = - node.left.height
            elif node.right == None and node.left == None:
                node.bf = 0

            self.updateBalanceFactor(node.left)
            self.updateBalanceFactor(node.right)
        else:
            return


    def balanced_insert(self, node, curr = None):
        curr = curr if curr else self.root
        self.insert(node, curr)

        # balancing
        self.updateHeight(self.root)
        self.updateBalanceFactor(self.root)

    
        self.balance(self.root)

        # self.draw()


    def balance(self, node):
        '''
        Recursivly balances tree using avl algorithms.
        '''
        if node == None:
            return

        if node.bf <= -2:
                print('{}: {} {} '.format(node.val, node.bf, 'Rotating right'))
                if node.left.bf <= -1:
                    self.rightRotate(node)
                elif node.left.bf >= 1:
                    self.leftRotate(node.left)
                    self.rightRotate(node)

                self.updateHeight(self.root)
                self.updateBalanceFactor(self.root)
            
        elif node.bf >= 2:
                print('{}: {} {} '.format(node.val, node.bf, 'Rotating left'))
                if node.right.bf >= 1:
                    self.leftRotate(node)
                elif node.right.bf <= -1:
                    self.rightRotate(node.right)
                    self.leftRotate(node)

                self.updateHeight(self.root)
                self.updateBalanceFactor(self.root)
            

        self.balance(node.left)
        self.balance(node.right)


    def leftRotate(self, node):
        A = node
        B = node.right
        C = node.right.left

        B.parent = A.parent
        if A.parent == None:
            self.root = B

        if A.parent != None:
            if A == A.parent.right:
                A.parent.right = B
            else:
                A.parent.left = B


        A.right = C

        if C != None:
            C.parent = A

        B.left = A

        A.parent = B


    def rightRotate(self, node):
        A = node
        B = node.left
        C = node.left.right

        B.parent = A.parent
        if A.parent == None:
            self.root = B

        if A.parent != None:
            if A == A.parent.left:
                A.parent.left = B
            else:
                A.parent.right = B

        A.left = C

        if C != None:
            C.parent = A

        B.right = A

        A.parent = B


    def search(self, query, curr = None):
        curr = curr if curr else self.root

        if query < curr.val[0]:
            if curr.left is not None:
                return self.search(query, curr.left)
        elif query > curr.val[0]:
            if curr.right is not None:
                return self.search(query, curr.right)
        else:
            return curr


    def insert(self, node, curr = None):
        curr = curr if curr else self.root
        # insert at correct location in BST
        if node._val < curr._val:
            if curr.left is not None:
                self.insert(node, curr.left)
            else:
                node.parent = curr
                curr.left = node
        else:
            if curr.right is not None:
                self.insert(node, curr.right)
            else:
                node.parent = curr
                curr.right = node
        return


    def draw(self):
        if not os.path.exists('drawings'):
            os.mkdir('drawings')

        dot = graphviz.Digraph(format='png')

        def traverse(node, idx=0):
            if node.parent == None:                 # root
                dot.node(str(id(node)), '{}\nbf:{}\nh:{}'.format(node.val[0],node.bf,node.height))
            else:
                dot.node(str(id(node)), '{}\nbf:{}\nh:{}'.format(node.val[0],node.bf,node.height))
                dot.edge(str(id(node.parent)), str(id(node)))

            if node.left != None:
                traverse(node.left, idx)
            if node.right != None:
                traverse(node.right, idx)


        traverse(self.root)

        i = 0
        while os.path.exists('drawings/tree{}.png'.format(i)):
            i += 1

        dot.render('drawings/tree{}'.format(i), view=False)


    def is_balanced(self):
        '''
        Checks whether tree is balanced. Checks balance factor for every node. Returns true if all bfs are between -1 and 1.
        '''

        def traverse(node):
            if node != None:
                if node.bf <=-2 or node.bf >= 2:
                    return False

                if traverse(node.left) == False or traverse(node.right) == False:
                    return False

        result = traverse(self.root)
        if result == None:
            result = True

        return result

    def delete(self, query):
        pass







if __name__ == '__main__':
    pass