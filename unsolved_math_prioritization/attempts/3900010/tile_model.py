"""Exact target cell model and all congruent lattice orientations."""
P=frozenset((x,y) for x in range(6) for y in range(3) if not(x>=4 and y<2))
def normalize(cells):
 cells=list(cells);a=min(x for x,y in cells);b=min(y for x,y in cells)
 return tuple(sorted((x-a,y-b) for x,y in cells))
def orientations():
 out=[]
 for reflect in (False,True):
  for rot in range(4):
   q=[]
   for x,y in P:
    if reflect:x=-x
    for _ in range(rot):x,y=-y,x
    q.append((x,y))
   q=normalize(q)
   if q not in out:out.append(q)
 return tuple(out)
D4=orientations()
