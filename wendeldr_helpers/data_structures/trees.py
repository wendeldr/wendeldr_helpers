
import numpy as np
from treelib import Node, Tree

def postorder(tree, node, depthlimit=999999999999, currentdepth=0):
    ret = []
    if len(tree.nodes[node._identifier]._successors) > 0 and currentdepth < depthlimit:
        for x in node._successors:
            if len(node._successors[x]) > 0:
                for i, s in enumerate(node._successors[x]):
                    d = postorder(tree, tree.nodes[node._successors[x][i]], depthlimit=depthlimit, currentdepth=currentdepth+1)
                    ret = ret + d
                    if tree.nodes[node._successors[x][i]].data is not None:
                        ret.append(tree.nodes[node._successors[x][i]].data)
                    # print(s)

    return ret



def postorder_contestents(tree, node, depthlimit=1, take_ties=True):
    data = postorder(tree,node,depthlimit=depthlimit)
    participents = []
    for x in data:
        # if len(x.log.keys()) > 1:

        #     for lvl, log in x.log.items():
        #         if log.istie:

        #         s=1
        #     raise NotImplementedError

        for lvl, log in x.log.items():
            if log.istie:
                if take_ties:
                    participents.append(log.a)
                    participents.append(log.b)
                else:
                    participents.append(log.winner)
            else:
                participents.append(log.winner)
    return list(set(participents))


def printall(tree):
    tree.show()
    for n in tree.expand_tree():
        if n == 'root':
            continue 
        tree.nodes[n]
        covariate = k

        a=1

def postorder_fight(tree, node, depthlimit=999999999999, currentdepth=0):
    ret = []
    if len(tree.nodes[node._identifier]._successors) > 0 and currentdepth < depthlimit:
        for x in node._successors:
            if len(node._successors[x]) > 0:
                for i, s in enumerate(node._successors[x]):
                    d = postorder_fight(tree, tree.nodes[node._successors[x][i]], depthlimit=depthlimit, currentdepth=currentdepth+1)
                    ret = ret + d
                    if tree.nodes[node._successors[x][i]].data is not None:
                        ret.append(tree.nodes[node._successors[x][i]].data)
                    # print(s)

    return ret