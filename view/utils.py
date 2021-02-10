class Formater:
  def print_table(self, table, field_widthes):
    self.print_border(field_widthes)
    self.print_row(table[0], field_widthes)
    self.print_border(field_widthes)
    for row in table[1:]:
      self.print_row(row, field_widthes)
      self.print_border(field_widthes)
    print(f'{len(table) - 1} row(s) found')

  def parse_table(self, table):
    field_width = []
    cell_width = []
    for j in range(len(table[0])):  # from col 0 to last col
      for i in range(len(table)):  # from row 0 to last row
        cell_width.append(len(table[i][j]))  # get len of string in this offset
      field_width.append(max(cell_width))
      cell_width = []
    return field_width

  def print_border(self, field_widthes):
    for i in range(len(field_widthes) - 1):
      print('+', '-' * field_widthes[i], sep='-', end='-')
    print('+', '-' * field_widthes[i + 1], '+', sep='-')

  def print_row(self, row, field_widthes):
    for i in range(len(row) - 1):
      print('|', row[i].ljust(field_widthes[i]), end=' ')
    print('|', row[i + 1].ljust(field_widthes[i + 1]), '|')
