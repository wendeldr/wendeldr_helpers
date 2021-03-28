import numpy as np
from openpyxl.styles import Font,NamedStyle
from treelib import Tree
from copy import deepcopy

def coxrow(sheet, rnd, startrow, column, node=None, pthresh=0.05):
    if node is not None:
        sheet.cell(row=startrow, column=column).value = node._identifier
        startrow+=1

    if rnd.b != '':
        sheet.cell(row=startrow, column=column).value = rnd.a
        sheet.cell(row=startrow, column=column+1).value = rnd.b
        sheet.cell(row=startrow, column=column+2).value = rnd.a_hr
        sheet.cell(row=startrow, column=column+3).value = rnd.b_hr
        sheet.cell(row=startrow, column=column+4).value = rnd.a_p
        sheet.cell(row=startrow, column=column+5).value = rnd.b_p

        if type(rnd.a_p) != str:
            if float(rnd.a_p) < pthresh:
                sheet.cell(row=startrow, column=column + 4).style = 'Good'
        if type(rnd.b_p) != str:
            if rnd.b_p < pthresh:
                sheet.cell(row=startrow, column=column + 5).style = 'Good'

        if rnd.istie:
            sheet.cell(row=startrow, column=column).style = 'Neutral'
            sheet.cell(row=startrow, column=column + 1).style = 'Neutral'
        elif rnd.a == rnd.winner:
            sheet.cell(row=startrow, column=column).style = 'Good'
        else:
            sheet.cell(row=startrow, column=column + 1).style = 'Good'
    else:
        sheet.cell(row=startrow, column=column).value = rnd.a
        sheet.cell(row=startrow, column=column + 1).value = rnd.a_hr
        sheet.cell(row=startrow, column=column + 2).value = rnd.a_p

        if type(rnd.a_p) != str:
            if float(rnd.a_p) < pthresh:
                sheet.cell(row=startrow, column=column + 2).style = 'Good'

    return startrow+1, column+5


def sortnodes(filter, x, nodes):
    nodes = [x] + [q for q in nodes_expanded if filter in q]
    return sorted(nodes, key=len, reverse=True)

def sleepstate(str):
    parts = str.split('_')
    if len(parts) > 2:
        return parts[2]
    else:
        return ''

# def print_tournament_5(sheet, tree, covariate):
#     stree = tree.subtree(tree.nodes[covariate].identifier)
#
#     row = 0
#     col = 0
#     nodes_expanded = list(stree.expand_tree())
#
#     while len(nodes_expanded) > 0:
#         col = 0
#         x = nodes_expanded.pop(0)
#         if x == covariate:
#             continue
#
#
#         if 'chf' in x:
#             # nodes = sortnodes('chf',x,nodes_expanded)
#             # prevlen = max([len(z) for z in nodes])
#             # sheet.cell(row, col).value = 'chf'
#             # row+=1
#             # col+=1
#             # done = {}
#             # for rnd in nodes:
#             #     ss = sleepstate(rnd)
#             #     if ss == '':
#             #         pass
#             #     elif ss not in done:
#             #         done[ss] = [row, col]
#             #     else:
#             #         row, col = done[ss]
#             #
#             #     sheet.cell(row, col).value = ss
#             #
#             #     if prevlen != len(rnd):
#             #
#             #     else:
#             #         coxrow(sheet,tree.nodes[rnd],)
#             pass
#
#         elif 'dfa' in x:
#             pass
#         elif 'kurt' in x:
#             pass
#         elif 'lds' in x:
#             pass
#         elif 'mean' in x:
#             pass
#         elif 'sa' in x:
#             pass
#         elif 'sb' in x:
#             pass
#         elif 'sen' in x:
#             pass
#         elif 'sse' in x:
#             pass
#         elif 'skew' in x:
#             pass
#         elif 'std' in x:
#             pass
#         elif 'xa' in x:
#             pass
#         elif 'xb' in x:
#             pass
#         elif 'xen' in x:
#             a=1
#         elif 'xpw' in x:
#             pass
#         elif 'xr' in x:
#             pass
#
#     a=1

def print_tournament(sheet, tree, covariate):
    mask = np.where(np.array([tree.level(tree.nodes[i].identifier) for i in tree.nodes]) == 2)[0]
    nodes = np.array([i for i in tree.nodes])
    analysis = nodes[mask]
    analysis = [x for x in analysis if covariate in x]

    totwiners = []
    row = 1
    for a in analysis:
        name = a.split('_')[-1]
        sheet.cell(row, 1).value = name
        for x in range(1,50):
            sheet.cell(row, x).style = 'Headline 1'
        row+=1
        orig_row=row
        row = print_tournament_recurse(sheet, tree, tree.nodes[a], row=row, column=2)

        sheet.cell(orig_row, 2).value = tree.nodes[a].data.winner
        totwiners.append(tree.nodes[a].data.winner)

    return totwiners


def print_tournament_recurse(sheet, tree, node, lvl=0, row=1, column=1, columns_per_fight=7, do_highlight=False):
    c = ((column-1)*columns_per_fight)+1
    if len(tree.nodes[node._identifier]._successors) > 0:
        for x in node._successors:
            if len(node._successors[x]) > 0:
                for i, s in enumerate(node._successors[x]):
                    if i==0:
                        row = print_tournament_recurse(sheet, tree, tree.nodes[node._successors[x][i]], row=row,
                                                       column=column+1, do_highlight=True)
                    else:
                        row = print_tournament_recurse(sheet, tree, tree.nodes[node._successors[x][i]], row=row,
                                                       column=column + 1)
    else:
        if do_highlight:
            for x in range(1, 50):
                sheet.cell(row, x).style = '20 % - Accent1'

    if node.data is not None:
        for k, rnd in node.data.log.items():
            row, _ = coxrow(sheet, rnd, row, c)
    return row+1
#





    # if nid==None:
    #     nid = "root"
    # node = tree.nodes[nid]
    #
    # # if level == 0:
    # #     return node
    # # else:
    # #     leading = ''.join(map(lambda x: dt_vline + ' ' * 3
    # #     if not x else ' ' * 4, is_last[0:-1]))
    # #     lasting = dt_line_cor if is_last[-1] else dt_line_box
    # #     yield leading + lasting, node
    # children = []
    # for x in node._successors:
    #     for i in node._successors[x]:
    #         children.append(i)
    # # children = [node._successors[i] for i in node._successors]
    # idxlast = len(children) - 1
    #
    # level += 1
    # for idx, child in enumerate(children):
    #     is_last.append(idx == idxlast)
    #     print(child)
    #     print_tournament(sheet, tree, level, is_last, row+1, column+1, nid=child)
    #     is_last.pop()
    #     sheet.cell(row, column).value = child

    # paths = tree.paths_to_leaves()
    # rowidxs = {}
    # for p in paths:
    #     rows = [key.startswith('_'.join(p)) for key in rowidxs]
    #     rowidxs['_'.join(p)] = row + sum(rows) * 2
    # maxpath = max([len(x)-2 for x in paths])
    # maxcol = maxpath * columns_per_fight
    # for p in paths:
    #     l = len(p)-2
    #     col = maxcol-(l * columns_per_fight)
    #     rowidxs[tuple(p)] = row


                    # print(s)