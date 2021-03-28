from openpyxl.styles import PatternFill, Border, Side, Alignment, Protection, Font

def FullBorder(size='thin'):
  return Border(left=Side(border_style=size,
                          color='FF000000'),
                right=Side(border_style=size,
                           color='FF000000'),
                top=Side(border_style=size,
                         color='FF000000'),
                bottom=Side(border_style=size,
                            color='FF000000'),
                diagonal=Side(border_style=None,
                              color='FF000000'),
                diagonal_direction=0,
                outline=Side(border_style=None,
                             color='FF000000'),
                vertical=Side(border_style=None,
                              color='FF000000'),
                horizontal=Side(border_style=None,
                               color='FF000000')
               )