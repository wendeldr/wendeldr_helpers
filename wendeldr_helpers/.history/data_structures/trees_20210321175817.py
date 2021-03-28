

from treelib import Node, Tree

def postorder(tree, node):
    ret = []
    if len(tree.nodes[node._identifier]._successors) > 0:
        for x in node._successors:
            if len(node._successors[x]) > 0:
                for i, s in enumerate(node._successors[x]):
                    ret.append(tree.nodes[node._successors[x][i]].data)
                    # print(s)
                return postorder(tree, tree.nodes[node._successors[x][i]]) + ret
    return ret




def postorder_contestents(tree, node):
    data = postorder(tree,node)
    participents = []
    for x in lst:
        for lvl in x.log:
            pass