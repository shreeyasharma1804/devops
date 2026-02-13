MAXKEYS = 3

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

    def insert(self, value, node, index=0):
        inserted = False
        if(len(node.children) == 0):
            if(len(node.values) == 0):
                node.values.append(value)
            else:
                for i in range(len(node.values)):
                    if(value < node.values[i]):
                        node.values.insert(i, value)
                        inserted = True
                        break
                if(not inserted):
                    node.values.append(value)
            # print(value, node.values)
            # print("-----------------------------")
            self.splitNode(node, index)

        elif(value < node.values[0]):
            self.insert(value, node.children[0], 0)

        elif(value > node.values[-1]):
            self.insert(value, node.children[-1], len(node.children)-1)

        else:
            for i in range(1, len(node.values)):
                if(value > node.values[i-1] and value < node.values[i]):
                    self.insert(value, node.children[i], i)

    def splitNode(self, node, index):

        if(len(node.values) <= MAXKEYS):
            return

        evictedKeyIndex = MAXKEYS%2
        evictedKey = node.values[evictedKeyIndex]
        newNodeLeft = Node()
        newNodeRight = Node()
        newNodeLeft.values = node.values[:evictedKeyIndex]
        newNodeRight.values = node.values[evictedKeyIndex+1:]
    
        if(len(node.children) > 0):
            newNodeLeft.children = node.children[:evictedKeyIndex+1]
            newNodeRight.children = node.children[evictedKeyIndex+1:]

        if(node.parent):

            newNodeRight.parent = node.parent
            newNodeLeft.parent = node.parent

            # print(node.values, node.parent.values)
            # print("New nodes", newNodeLeft.values, newNodeRight.values)


            inserted = False
            insertedIndex = 0
            for i in range(len(node.parent.values)):
                if(evictedKey < node.parent.values[i]):
                    inserted = True
                    insertedIndex = i
                    node.parent.values.insert(i, evictedKey)
                    break
            if(not inserted):
                insertedIndex = len(node.parent.values)
                node.parent.values.append(evictedKey)

            del node.parent.children[index]
            node.parent.children.insert(index, newNodeRight)
            node.parent.children.insert(index, newNodeLeft)

            self.splitNode(node.parent, 0)

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
tree.insert(36, tree.getRoot())
tree.insert(34, tree.getRoot())
tree.insert(20, tree.getRoot())
tree.insert(21, tree.getRoot())
tree.insert(47, tree.getRoot())
tree.insert(37, tree.getRoot())
tree.insert(38, tree.getRoot())
tree.insert(39, tree.getRoot())
tree.printTree(tree.getRoot())
