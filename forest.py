import csv
import graphviz
import random
import json
import progress.bar

import sys
sys.path.append('D:\\Workbench\\.repos')
from Workspace import workspacelib

verbose = 0


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
        self.root = None
        self.size = None
        


    def __str__(self):
    
        string = 'Tree Root: {} | Size: {}'.format(
            self.root.data,
            self.size,
        )

        return string

   
    def fromTextFile(self, filepath):
        with open(filepath, 'r') as fil:
            data = fil.read()
            data = data.splitlines()
        
        for e in data:
            self.insert(e)


    @classmethod
    def fromCSV(cls, filename, headings=False):         # WIP
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


    def toCSV(self, filename):          # WIP
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
        '''
        Constructs visual representation of tree.
        '''

        dot = graphviz.Digraph(format='png')
        
        def traverse(node, idx=0):
            if node.parent == None:
                dot.node(str(id(node)), node.data)
            else:
                dot.node(str(id(node)), node.data)
                dot.edge(str(id(node.parent)), str(id(node)))
            
            if node.branches != None:
                for branch in node.branches:
                    traverse(branch, idx)

        traverse(self.root)

        path = Workspace.getOpen(file_name='tree', file_ext='.png', output_path='drawings')
        dot.render(path, view=False)


    def pathsToCSV(self):           # WIP
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
    

    def traversalCheck(self):           # WIP
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


    def randomWalk(self):           # WIP
        print('--- Random Walk ---')
        node = self.root
        while node != None:
            print(node)
            try:
                node = random.choice(node.branches)
            except:
                node = None
        
        print('Random walk complete.')


    def calcDist(self):         # WIP
        '''
        Finds the nodal distribution of the tree across levels.
        Returns dict.
        '''
        dist = {}
        for level in range(self.dims[0]):
            count = len([node for node in self.map if node[0] == level])
            dist[level] = count
        

        return dist
        

    def calcDistP(self):            # WIP
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



class NodeB:
    '''
    A binary node class.
    '''

    def __init__(self, data=None, left=None, right=None, parent=None, h=1, bf=0):
        self.data = data
        self.left = left
        self.right = right
        self.parent = parent
        self.h = h
        self.bf = bf


    def __str__(self):
        string = 'NodeB {} | Data ({}): {} | Parent: {} | Left: {} | Right: {} | Height: {} | BF: {}'.format(
            hex(id(self)),
            type(self.data),
            self.data,
            self.parent.data if self.parent else None,
            self.left.data if self.left else None,
            self.right.data if self.right else None,
            self.h,
            self.bf)

        return string

    def getSide(self):
        '''
        Checks wether node is left subtree or right subtree of parent.
        Returns 0 if left, 1 if right. None if parent does not exist.
        '''

        if self.parent:
            if self == self.parent.left:
                return 0
            elif self == self.parent.right:
                return 1


class BSTree:
    '''
    A binary search tree implementation.
    '''

    def __init__(self):
        self.root = None


    def __str__(self):
        string = 'BSTree {} | Size: {} | Root: {}'.format(
            hex(id(self)),
            self.getSize(),
            self.root.data)

        return string

   
    def fromTXT(self, filepath):
        with open(filepath, 'r') as fil:
            data = fil.read()
            data = data.splitlines()
        
        for e in data:
            self.insert(e)

    def fromCSV(self, filepath):
        with open(filepath, 'r') as fil:
            reader = csv.reader(fil, delimiter='\t')
            data = [row for row in reader]

            bar = progress.bar.Bar('Inserting CSV "{}"'.format(filepath), max=len(data))
            for row in data:
                cargo = (data[0], data[1]) ### Look into allowing an arbitrary number of elements here


    def fromJSON(self, filepath):
        with open(filepath, 'r') as fil:
            data = json.load(fil)
        
        
        bar = progress.bar.Bar('Inserting JSON', max=len(data))
        for key, value in data.items():
            cargo = (key, value)
            self.insert(data=cargo)
            bar.next()
        bar.finish()


    def insert(self, data):
        print('[forest]: Inserting {}'.format(data)) if verbose>=1 else False

        node = NodeB(data=data)

        if self.root == None:
            self.root = node
            inserted = True
        else:
            inserted = False
            curr = self.root

        while not inserted:
            if node.data < curr.data:
                if curr.left == None:
                    curr.left = node
                    node.parent = curr
                    
                    inserted = True
                else:
                    print('[forest]: Moving insert left') if verbose>=2 else False
                    curr = curr.left

            elif node.data > curr.data:
                if curr.right == None:
                    curr.right = node
                    node.parent = curr
                    inserted = True
                else:
                    print('[forest]: Moving insert right') if verbose>=2 else False
                    curr = curr.right


    def delete(self, node):     #WIP

        def deleteNoChildren(node):
            node = None
        
        def deleteOneChild(node):
            # child = node.left if node.left else child = node.right
            # self.swap(node, child)
            # child = None
            pass

        # if node.left == None and node.right == None:        # node has no children
        #     node = None
        # elif (node.left == None) != (node.right == None):   # node has only one child
        #     if node.left == None:                           # only child must be right
        #         node.right.parent = node.parent

        #         if node.getSide() == 0:
        #             node.parent.left = node.right
        #         elif node.getSide() == 1:
        #             node.parent.right = node.right

                

        #     elif node.right == None:                        # only child must be left
        #         node.left.parent = node.parent

        #         if node.getSide() == 0:
        #             node.parent.left = node.left
        #         elif node.getSide() == 1:
        #             node.parent.right = node.left

        #         node = None

        # elif node.left != None and node.right != None:      # node has two children
        #     nodeA = node
        #     nodeB = self.succ(node)
        #     self.swap(nodeA, nodeB)
        #     nodeB = None
            


    def swap(self, nodeA, nodeB):
        '''
        Swaps the data of any two nodes in the tree.
        '''

        nodeA.data, nodeB.data = nodeB.data, nodeA.data

        # # swap parent-node refs
        # if nodeA.getSide() == 0:
        #     nodeA.parent.left = nodeB
        # elif nodeA.getSide() == 1:
        #     nodeA.parent.right = nodeB
        
        # if nodeB.getSide() == 0:
        #     nodeB.parent.left = nodeA
        # elif nodeB.getSide() == 1:
        #     nodeB.parent.right = nodeA

        # # swap node-parent refs
        # nodeA.parent, nodeB.parent = nodeB.parent, nodeA.parent

        # # swap child-node refs
        # if nodeA.left:
        #     nodeA.left.parent = nodeB
        # if nodeA.right:
        #     nodeA.right.parent = nodeB

        # if nodeB.left:
        #     nodeB.left.parent = nodeA
        # if nodeB.right:
        #     nodeB.right.parent = nodeA

        # # swap node-child refs
        # nodeA.left, nodeB.left = nodeB.left, nodeA.left
        # nodeA.right, nodeB.right = nodeB.right, nodeA.right


    def traverse(self, node=None, mode=None, foo=None):
        node = self.root if node == None else node

        def preOrder(node, foo=None):
            nodes = []

            if node:
                foo(node) if foo else False
                nodes.append(node)
                nodes.extend(preOrder(node.left, foo))
                nodes.extend(preOrder(node.right, foo))
            
            return nodes

        def inOrder(node, foo=None):
            nodes = []

            if node:
                nodes.extend(inOrder(node.left, foo))
                foo(node) if foo else False
                nodes.append(node)
                nodes.extend(inOrder(node.right, foo))
            
            return nodes

        def postOrder(node, foo=None):
            nodes = []

            if node:
                nodes.extend(postOrder(node.left, foo))
                nodes.extend(postOrder(node.right, foo))
                foo(node) if foo else False
                nodes.append(node)
            
            return nodes

        def shootLeft(node, foo=None):
            nodes = []

            if node:
                foo(node) if foo else False
                nodes.append(node)
                nodes.extend(shootLeft(node.left, foo))
            
            return nodes

        def shootRight(node, foo=None):
            nodes = []

            if node:
                foo(node) if foo else False
                nodes.append(node)
                nodes.extend(shootRight(node.right, foo))
            
            return nodes


        if mode == 'pre' or mode == None:
            return preOrder(node, foo)
        elif mode == 'in':
            return inOrder(node, foo)
        elif mode == 'post':
            return postOrder(node, foo)
        elif mode == 'left':
            return shootLeft(node, foo)
        elif mode == 'right':
            return shootRight(node, foo)
        else:
            raise ValueError('Traversal mode not recognized. Use either "pre", "in", "post", "left", "right"')


    def search(self, query):
        '''
        Searches BST for query and returns node. Otherwise returns false.
        '''

        if query == self.root.data[0]:
            result = self.root
            found = True
        else:
            curr = self.root
            found = False

        while not found:
            if curr:
                if query == curr.data[0]:
                    result = curr
                    found = True
                elif query < curr.data[0]:
                    curr = curr.left
                elif query > curr.data[0]:
                    curr = curr.right
            else:
                result = False
                break
        

        return result


    def prec(self, node):
        '''
        Returns predecessor of node.
        '''

        if node.left:
            return self.traverse(node.left, mode='right')[-1]
        else:
            while node != None:
                if node.parent and node == node.parent.right:
                    return node.parent
                node = node.parent
            
            return False


    def succ(self, node):
        '''
        Returns successor of node.
        '''

        if node.right:
            return self.traverse(node.right, mode='left')[-1]
        else:
            while node != None:
                if node.parent and node == node.parent.left:
                    return node.parent
                node = node.parent
            
            return False


    def draw(self):
        '''
        Constructs visual representation of BSTree.
        '''
        
        graph = graphviz.Digraph(format='png')
        graph.attr('node', shape='box')

        def draw_link(node):
            graph.node(str(id(node)), label=
            '{}\nh: {}\nbf: {}\n'.format(
                str(node.data)[:12],
                str(node.h),
                str(node.bf)))

            if node.left:
                graph.edge(str(id(node)), str(id(node.left)))
            else:
                null = str(random.randint(1000000000000,9999999999999))
                graph.attr('node', shape='point')
                graph.edge(str(id(node)), null)
                graph.attr('node', shape='box')

            if node.right:
                graph.edge(str(id(node)), str(id(node.right)))
            else:
                null = str(random.randint(1000000000000,9999999999999))
                graph.attr('node', shape='point')
                graph.edge(str(id(node)), null)
                graph.attr('node', shape='box')
            

        self.traverse(self.root, mode='pre', foo=draw_link)

        path = workspacelib.Workspace.getOpen(file_name='tree', file_ext='.png', output_path='temp/drawings')
        graph.render(path, view=False)


    def getSize(self):
        return len(self.traverse())


if __name__ == '__main__':
    tree = BSTree()
    tree.fromTXT('data/test.txt')
    nodeA = tree.search('A')
    nodeB = tree.search('B')

    tree.delete(nodeA)



