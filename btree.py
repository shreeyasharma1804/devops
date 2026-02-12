MAXKEYS = 3

[1,2,3]

class Node:

    def __init__(self):
        self.values = []
        self.children = []
        self.parent = None

class BTree():

    def __init__(self):
        self.root = Node()

    def getRoot(self):
        return self.root

    def insert(self, value, node):
        if(len(node.children) == 0):
            if(len(node.values) == 0):
                node.values.append(value)
            else:
                for i in range(len(node.values)-1):
                    if(node.values[i] > value and node.values[i+1] < value):
                        node.values.insert(i, value)
                        break
                node.values.append(value)
            if(len(node.values) > MAXKEYS):
                self.splitNode(node)

        elif(value < node.values[0]):
            self.insert(value, node.children[0])

        elif(value > node.values[-1]):
            self.insert(value, node.children[-1])

        else:
            for i in range(1, len(node.values)-1):
                if(value > node.values[i-1] and value < node.values[i]):
                    self.insert(value, node.children[i])

    def splitNode(self, node):
        evictedKeyIndex = MAXKEYS%2
        evictedKey = node.values[evictedKeyIndex]
        newNodeLeft = Node()
        newNodeLeft.values = node.values[:evictedKeyIndex]
        newNodeLeft.children = node.children
        newNodeRight = Node()
        newNodeRight.values = node.values[evictedKeyIndex+1:]
        newNodeRight.children = node.children
        # print(newNodeRight.values)

        if(node.parent):
            print("Here")
            return
        else:
            newNodeRoot = Node()
            newNodeRoot.values.append(evictedKey)
            newNodeRoot.children.append(newNodeLeft)
            newNodeRoot.children.append(newNodeRight)
            self.root = newNodeRoot

        newNodeLeft.parent = newNodeRoot
        newNodeRight.parent = newNodeRoot

    def printTree(self, node):
        if(len(node.values) == 0):
            return
        print(node.values)
        print("------------------------------------------------------")
        for node in node.children:
            self.printTree(node)

tree = BTree()
tree.insert(30, tree.getRoot())
tree.insert(35, tree.getRoot())
tree.insert(40, tree.getRoot())
tree.insert(45, tree.getRoot())
tree.insert(31, tree.getRoot())
tree.insert(32, tree.getRoot())
tree.insert(46, tree.getRoot())
tree.insert(33, tree.getRoot())

tree.printTree(tree.getRoot())
