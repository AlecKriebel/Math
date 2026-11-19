import sympy as s, itertools, json

def test(name,rays,cones):
 d=len(rays[0]); n=len(rays); P=[]
 for cone in cones:
  V=s.Matrix([rays[i] for i in cone]); S=s.zeros(d,n)
  for j,i in enumerate(cone): S[j,i]=1
  P.append(V.inv()*S)
 out=[]
 for w in rays:
  A=s.Matrix.vstack(*[s.Matrix([w])*(p-P[0]) for p in P[1:]])
  out.append(n-A.rank()-d)
 return dict(name=name,dimension=d,rays=rays,maximal_cones=[tuple(c) for c in cones],nonlinear_kernel_dimensions=out)
rows=[]
for d in (2,3):
 rays=[tuple(int(i==j) for i in range(d)) for j in range(d)]+[(-1,)*d]
 rows.append(test('P'+str(d),rays,list(itertools.combinations(range(d+1),d))))
for n in (0,1,2,5):
 rows.append(test('F'+str(n),[(1,0),(0,1),(-1,n),(0,-1)],[(0,1),(1,2),(2,3),(3,0)]))
rays=[(1,0,0),(-1,0,0),(0,1,0),(0,-1,0),(0,0,1),(0,0,-1)]
cones=list(itertools.product((0,1),(2,3),(4,5)))
rows.append(test('P1xP1xP1',rays,cones))
cones.remove((0,2,4)); cones += [(6,2,4),(0,6,4),(0,2,6)]
rows.append(test('Bl_point_P1xP1xP1',rays+[(1,1,1)],cones))
for row in rows:
 for cone in row["maximal_cones"]:
  if any(i<0 or i>=len(row["rays"]) for i in cone): raise ValueError("invalid ray index")
print(json.dumps(rows,indent=2))
