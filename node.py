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

