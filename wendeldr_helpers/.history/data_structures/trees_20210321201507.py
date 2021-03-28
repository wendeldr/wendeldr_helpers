
import numpy as np
from treelib import Node, Tree

def postorder(tree, node, depthlimit=999999999999, currentdepth=0):
    ret = []
    if len(tree.nodes[node._identifier]._successors) > 0 and currentdepth < depthlimit:
        for x in node._successors:
            if len(node._successors[x]) > 0:
                for i, s in enumerate(node._successors[x]):
                    d = postorder(tree, tree.nodes[node._successors[x][i]],depthlimit=depthlimit,currentdepth=currentdepth+1)
                    ret = ret + d
                    ret.append(tree.nodes[node._successors[x][i]].data)
                    # print(s)

    return ret




def postorder_contestents(tree, node, depthlimit=1):
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
                participents.append(log.a)
                participents.append(log.b)
                # raise NotImplementedError
            else:
                participents.append(log.winner)
    return participents


def printall(tree):
    for x in tree.nodes:
        a=1