from collections import defaultdict


##################################################################################
# undirected graph
class Graph:
    def __init__(self, numberOfNodes):
        self.numberOfNodes = numberOfNodes
        self.graph = defaultdict(list)

    def addEdge(self, v, w):
        self.graph[v].append(w)
        self.graph[w].append(v)

    def DFSUtil(self, v, visited):
        if visited[v]:
            return
        print(v, end=' ')
        visited[v] = True
        for w in self.graph[v]:
            self.DFSUtil(w, visited)

    def BFSUtil(self, v, visited):
        q = list()
        q.append(v)
        while len(q) > 0:
            first_elem = q.pop(0)
            visited[first_elem] = True
            print(first_elem, end=' ')
            for w in self.graph[first_elem]:
                if not visited[w]:
                    q.append(w)
                    visited[w] = True

    def DFS(self):
        visited = [False] * self.numberOfNodes
        v = 2
        self.DFSUtil(v, visited)
        print("")

    def BFS(self):
        visited = [False] * self.numberOfNodes
        v = 2
        self.BFSUtil(v, visited)
        print("")


def create_graph():
    graph = Graph(12)
    graph.addEdge(0, 1)
    graph.addEdge(0, 2)
    graph.addEdge(0, 3)
    graph.addEdge(1, 4)
    graph.addEdge(1, 5)
    graph.addEdge(3, 6)
    graph.addEdge(3, 7)
    graph.addEdge(4, 8)
    graph.addEdge(4, 9)
    graph.addEdge(6, 10)
    graph.addEdge(6, 11)
    return graph


def test_DFS():
    print("DFS")
    graph = create_graph()
    graph.DFS()


def test_BFS():
    print("BFS")
    graph = create_graph()
    graph.BFS()


# DFS
test_DFS()

# BFS
test_BFS()

##################################################################################
# binary search tree


class TreeNode:
    def __init__(self, value):
        self.value = value
        self.leftNode = None
        self.rightNode = None
        self.parent = None


# AVL tree
class BalancedBinarySearchTree:
    def __init__(self):
        self.root = None

    def rebalance(self, new_node):
        if new_node.parent != self.root:
            grand_parent = new_node.parent.parent
            parent = new_node.parent
            if grand_parent.rightNode is None and grand_parent.leftNode == parent and parent.leftNode == new_node:
                #RR
                parent.leftNode = None
                grand_parent.rightNode = new_node
                new_node.parent = grand_parent
                tmp = grand_parent.value
                grand_parent.value = parent.value
                parent.value = new_node.value
                new_node.value = tmp
            elif grand_parent.rightNode is None and grand_parent.leftNode == parent and parent.rightNode == new_node:
                #LR
                parent.rightNode = None
                grand_parent.rightNode = new_node
                new_node.parent = grand_parent
                tmp = grand_parent.value
                grand_parent.value = new_node.value
                new_node.value = tmp
            elif grand_parent.leftNode is None and grand_parent.rightNode == parent and parent.rightNode == new_node:
                #LL
                parent.parent = grand_parent.parent
                parent.leftNode = grand_parent
                grand_parent.parent = parent
                grand_parent.rightNode = None
            elif grand_parent.leftNode is None and grand_parent.rightNode == parent and parent.leftNode == new_node:
                #RL
                new_node.parent = grand_parent.parent
                new_node.leftNode = grand_parent
                new_node.rightNode = parent
                parent.parent = new_node
                grand_parent.parent = new_node
                grand_parent.rightNode = None
                parent.leftNode = None

    def insertNode(self, value):
        if self.root is not None:
            cur = self.root
            new_node = TreeNode(value)
            while cur is not None:
                if cur.value > value:
                    if cur.leftNode is None:
                        cur.leftNode = new_node
                        cur.leftNode.parent = cur
                        break
                    else:
                        cur = cur.leftNode
                else:
                    if cur.rightNode is None:
                        cur.rightNode = new_node
                        cur.rightNode.parent = cur
                        break
                    else:
                        cur = cur.rightNode
            self.rebalance(new_node)
        else:
            self.root = TreeNode(value)
            self.parent = self.root

    def BFS(self):
        q = []
        q.append(self.root)
        id_2_layer_map = {}
        id_2_layer_map[id(q[0])] = 0
        last_layer = 0
        while len(q) > 0:
            first_element = q.pop(0)
            if id_2_layer_map[id(first_element)] != last_layer:
                last_layer += 1
                print("")
            print(first_element.value, end=' ')
            if first_element.leftNode is not None:
                q.append(first_element.leftNode)
                id_2_layer_map[id(first_element.leftNode
                                  )] = id_2_layer_map[id(first_element)] + 1
            if first_element.rightNode is not None:
                q.append(first_element.rightNode)
                id_2_layer_map[id(first_element.rightNode
                                  )] = id_2_layer_map[id(first_element)] + 1

        print("")


# test BFS for AVL tree


def create_avl_tree():
    t = BalancedBinarySearchTree()
    t.insertNode(4)
    t.insertNode(3)
    t.insertNode(9)
    t.insertNode(1)
    t.insertNode(7)
    t.insertNode(16)
    t.insertNode(15)
    t.insertNode(13)
    return t


def test_BFS_for_avl_tree():
    print("BFS for AVL tree")
    t = create_avl_tree()
    t.BFS()


test_BFS_for_avl_tree()

##################################################################################
# dynamoDB implemented by hash table and b-tree


class BTreeNode:
    def __init__(self):
        pass


class BTree:
    def __init__(self, value):
        pass

    def delete_node(self):
        pass

    def add_node(self):
        pass


class DynamoDB:
    def __init__(self):
        self.nodes = dict()

    def put_item(self, key, value):
        self.nodes[key] = BTree(value)

    def get_item(self, key):
        pass


##################################################################################
# quick sort & heap sort

import math


def partition(data, low, high):
    pe = data[low]
    pi = low
    left = low + 1
    right = high
    while pi < right:
        if pe >= data[left]:
            data[pi] = data[left]
            pi = left
            left = left + 1
        else:
            data[left], data[right] = data[right], data[left]
            right = right - 1

    data[pi] = pe
    return pi


def quick_sort(data, low, high):
    if (high - low) < 1:
        return

    mid = partition(data, low, high)

    quick_sort(data, low, mid - 1)
    quick_sort(data, mid + 1, high)


data = [5, 5, 5, 5, 1, 5]
quick_sort(data, 0, len(data) - 1)
print(data)