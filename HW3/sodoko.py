import time

class Sodoko:

  def __init__(self, dim, fileDir):
    self.dim = dim
    self.expandedNodes = 0
    with open(fileDir) as f:
      content = f.readlines()
      self.board = [list(x.strip()) for x in content]
    self.rv = self.getRemainingValues()

  def update_domains_on_change(self, x, y):
    changed = []
    for i in range(self.dim):
      if self.board[x][i] == '0':
        pos = x * self.dim + i
        if str(self.board[x][y]) in self.rv[pos]:
          self.rv[pos].remove(str(self.board[x][y]))
          changed.append(pos)
      if self.board[i][y] == '0':
        pos = i * self.dim + y
        if str(self.board[x][y]) in self.rv[pos]:
          self.rv[pos].remove(str(self.board[x][y]))
          changed.append(pos)
    boxRow = x - x % 3
    boxCol = y - y % 3
    for i in range(3):
      for j in range(3):
        if self.board[boxRow+i][boxCol+j] == '0':
          pos = (boxRow + i) * self.dim + (boxCol + j)
          if str(self.board[x][y]) in self.rv[pos]:
            self.rv[pos].remove(str(self.board[x][y]))
            changed.append(pos)
    return changed

      

  def update_domains_on_removal(self, x, y, changed):
    for i in changed:
      self.rv[i].append(str(self.board[x][y]))

  def getRemainingValues(self):
    RV = []
    for row in range(self.dim):
      for col in range(self.dim):
        if self.board[row][col] != '0':
          RV.append(['x'])
        else:
          RV.append(self.getDomain(row, col))
    return RV
  
  def getDomain(self, row, col):
    RVCell = [str(i) for i in range(1, self.dim + 1)]
    for i in range(self.dim):
        if self.board[row][i] != '0':
            if self.board[row][i] in RVCell:
                RVCell.remove(self.board[row][i])
    for i in range(self.dim):
        if self.board[i][col] != '0':
            if self.board[i][col] in RVCell:
                RVCell.remove(self.board[i][col])
    boxRow = row - row % 3
    boxCol = col - col % 3
    for i in range(3):
        for j in range(3):
            if self.board[boxRow+i][boxCol+j] != '0':
                if self.board[boxRow+i][boxCol+j] in RVCell:
                    RVCell.remove(self.board[boxRow+i][boxCol+j])
    return RVCell

  def getNextLocation_with_ordering(self): # with ordering
    x = -1
    y = -1
    l = self.dim + 1
    for i in range(self.dim):
      for j in range(self.dim):
        if self.board[i][j] == '0':
          pos = i * self.dim + j
          if len(self.rv[pos]) < l:
            x = i
            y = j
            l = len(self.rv[pos])
    return x, y


  def getNextLocation_without_ordering(self): # without ordering
    x = -1
    y = -1
    for i in range(self.dim):
      for j in range(self.dim):
        if self.board[i][j] == '0':
          x = i
          y = j
          break;
    return x, y


  def solveCspBackTracking(self):
    location = self.getNextLocation_with_ordering()
    if location[0] == -1:
      return True
    else:
      pos = location[0] * self.dim + location[1]
      self.expandedNodes += 1
      for choice in self.rv[pos]:
        self.board[location[0]][location[1]] = str(choice)
        changed = self.update_domains_on_change(location[0], location[1])
        # self.rv = self.getRemainingValues()
        if self.solveCspBackTracking():
          return True
        self.update_domains_on_removal(location[0], location[1], changed)
        self.board[location[0]][location[1]] = '0'
    return False

  def solveSimpleBackTracking(self):
    location = self.getNextLocation_without_ordering()
    if location[0] == -1:
      return True
    else:
      self.expandedNodes += 1
      for choice in range(1, self.dim+1):
        if self.isSafe(location[0], location[1], choice):
          self.board[location[0]][location[1]] = str(choice)
          if self.solveSimpleBackTracking():
            return True
          self.board[location[0]][location[1]] = '0'
    return False


  def isSafe(self, location_x, location_y, choice):
    if self.check_row(location_x, choice) and self.check_column(location_y, choice) and self.check_box(location_x, location_y, choice):
      return True

  def check_row(self, location_x, choice):
    for i in range(self.dim):
      if self.board[location_x][i] == str(choice):
        return False
    return True

  def check_column(self, location_y, choice):
    for i in range(self.dim):
      if self.board[i][location_y] == str(choice):
        return False
    return True

  def check_box(self, location_x, location_y, choice):
    x = location_x - location_x % 3
    y = location_y - location_y % 3
    for i in range(3):
      for j in range(3):
        if self.board[x+i][y+j] == str(choice):
          return False
    return True



s = Sodoko(9, "b.txt")
start = time.time()
result = s.solveSimpleBackTracking()
print("expanded nodes: ", s.expandedNodes)
print(f"time taken: {time.time()-start}")
for i in range(9):
  for j in range(9):
    print(s.board[i][j], end=" ")
  print()