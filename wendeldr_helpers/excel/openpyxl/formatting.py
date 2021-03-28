import numpy as np

from openpyxl.styles import PatternFill, Border, Side, Alignment, Protection, Font, numbers
from openpyxl.worksheet.dimensions import ColumnDimension, DimensionHolder
from openpyxl.utils import get_column_letter
from openpyxl.formatting.rule import CellIsRule

from wendeldr_helpers.excel.openpyxl.formats import FullBorder

def column_conditional_lt(ws,col,val=0.05,start=1):
    red_color = 'ffc7ce'
    red_color_font = '9c0103'

    red_font = Font(color=red_color_font)
    red_fill = PatternFill(start_color=red_color, end_color=red_color, fill_type='solid')
    c = get_column_letter(col)
    ws.conditional_formatting.add(f'{c}{start}:{c}{ws.max_row}', CellIsRule(operator='lessThan', formula=[f'{val}'], fill=red_fill, font=red_font))


def format_univariate(ws):
     
    # % of N event
    for r in range(1,ws.max_row+1):
        ws.cell(r,7).number_format = numbers.FORMAT_PERCENTAGE_00 

    # % of N NOevent
    for r in range(1,ws.max_row+1):
        ws.cell(r,9).number_format = numbers.FORMAT_PERCENTAGE_00 

    # % of N NOevent
    for r in range(1,ws.max_row+1):
        ws.cell(r,10).number_format = numbers.FORMAT_PERCENTAGE_00 

    # rest
    for c in range(11,25):
        for r in range(1,ws.max_row+1):
            ws.cell(r,c).number_format = numbers.FORMAT_NUMBER_00

    # lines
    for r in range(1,ws.max_row+1):
        ws.cell(r,2).border = Border(left=Side(border_style='thick',color='FF000000'))

    for r in range(1,ws.max_row+1):
        ws.cell(r,10).border = Border(left=Side(border_style='thick',color='FF000000'))

    for r in range(1,ws.max_row+1):
        ws.cell(r,15).border = Border(left=Side(border_style='thick',color='FF000000'))
        
    for r in range(1,ws.max_row+1):
        ws.cell(r,20).border = Border(left=Side(border_style='thick',color='FF000000'))

def fit_column_width(ws, columns = []):
    dim_holder = DimensionHolder(worksheet=ws)

    if type(columns) == int:
        todo = np.array([columns])
    else:
        if len(columns) == 0:
            todo = list(range(1,ws.max_column+1))
        else:
            todo = columns
    column_widths = {}
    for c in todo:
        column_widths[c] = 2
        for r in range(1,ws.max_row+1):               
            column_widths[c] = max(column_widths[c],len(str(ws.cell(r,c))) - 5)


    for i in column_widths:
        dim_holder[get_column_letter(i)] = ColumnDimension(ws, min=i, max=i, width=column_widths[i])

    ws.column_dimensions = dim_holder


def bold_header(ws):
    for col_num in range(ws.min_column, ws.max_column):
        ws.cell(1, col_num+1).font = Font(bold=True)
        ws.cell(1, col_num+1).border = FullBorder()
        ws.cell(1, col_num+1).alignment = Alignment(wrap_text=True)

