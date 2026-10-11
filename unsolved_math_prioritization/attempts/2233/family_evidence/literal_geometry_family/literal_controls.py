"""Finite diagnostic controls, exact squared distances; not an asymptotic proof."""
import hashlib, itertools, json, pathlib, random
ROOT=pathlib.Path(__file__).resolve().parent
PINNED=ROOT.parent/'pinned_problem.json'
data=json.loads(PINNED.read_text())
statement=data['statement']
print(json.dumps({'pinned_sha256':hashlib.sha256(PINNED.read_bytes()).hexdigest(),
 'id':data['id'],'problem_number':data['problem_number'],
 'statement_repr':repr(statement),'actual_newline_indices':[i for i,c in enumerate(statement) if c=='\n']},indent=2))

def counts(points, vertical_square=1):
 assert len(set(points))==len(points)
 return [len({(p[0]-q[0])**2+vertical_square*(p[1]-q[1])**2
              for q in points if p!=q}) for p in points]

def check_pair_obstruction(points):
 r=counts(points)
 a=sorted(set(r)); n=len(points); h=n-len(a)
 assert 2*h*(h+1)>=n-2
 if len(a)>=2:
  assert a[0]<=h and a[1]<=h+1
  assert n-2<=2*a[0]*a[1]

for n in range(2,201):
 r=counts([(i,0) for i in range(n)])
 assert r==[max(i,n-1-i) for i in range(n)]
 assert len(set(r))==(n+1)//2
print('Exact equally spaced line controls passed for every 2<=n<=200.')

p4=[(0,0),(2,0),(1,1),(-2,0)]
r4=counts(p4,3)
assert r4==[1,2,2,3]
print('Q(sqrt(3)) four-point construction:',r4,'spectrum',sorted(set(r4)))
print('Its coordinates are (0,0),(2,0),(1,sqrt(3)),(-2,0).')

grid=list(itertools.product(range(4),repeat=2))
checked=0
for n in range(2,6):
 for p in itertools.combinations(grid,n):
  check_pair_obstruction(p); checked+=1
print('Pair-circle obstruction finite diagnostic:',checked,'subsets of the 4x4 integer grid, sizes 2 through 5.')

rng=random.Random(2233653)
grid=list(itertools.product(range(-25,26),repeat=2))
for n in range(2,81):
 for trial in range(20):
  check_pair_obstruction(rng.sample(grid,n))
print('Pair-circle obstruction finite diagnostic: 1580 deterministic integer samples, sizes 2 through 80.')
print('No universal or asymptotic claim is inferred from these finite controls.')
