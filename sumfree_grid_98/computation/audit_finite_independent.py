from pathlib import Path
"""Independent replay using target-first sum decomposition and frozenset edges."""
import gzip,json,itertools,glob,copy,sys
from certify_finite import check

def need(c,m):
 if not c: raise ValueError(m)
def replay(c):
 d,n,K=c['d'],c['n'],c['K']; points=list(itertools.product(range(1,n+1),repeat=d)); ix={p:i for i,p in enumerate(points)}
 edges=set()
 for z in points:
  for x in itertools.product(*(range(1,t) for t in z)):
   y=tuple(t-a for t,a in zip(z,x));edges.add(frozenset((ix[x],ix[y],ix[z])))
 def decode(mask):
  need(type(mask) is int and 0<=mask<1<<len(points),'invalid mask')
  return frozenset(i for i in range(len(points)) if mask>>i&1)
 done=set(); pending=['0']; leaves=branches=0
 while pending:
  key=pending.pop()
  if key in done:continue
  done.add(key);D=decode(int(key));node=c['nodes'][key]
  if 'packing' in node:
   leaves+=1;used=set(D)
   for mask in node['packing']:
    e=decode(mask);need(e in edges,'invalid forbidden edge');need(not e&used,'packing overlap');used.update(e)
   need(len(D)+len(node['packing'])>=len(points)-K,'insufficient packing')
  else:
   branches+=1;e=decode(node['edge']);need(e in edges and not e&D,'invalid branch')
   expected={str(int(key)|(1<<v)) for v in e};need(set(node['children'])==expected,'incomplete branch');pending.extend(expected)
 # Do not assume the initial code's point-sum family is feasible: test actual witness constraints.
 best=max(({i for i,p in enumerate(points) if t<=sum(p)<=2*t-1} for t in range(1,d*n+1)),key=len)
 need(len(best)==K and not any(e<=best for e in edges),'invalid lower witness')
 return dict(d=d,n=n,K=K,constraints=len(edges),repeated_summand_constraints=sum(len(e)==2 for e in edges),nodes=len(done),leaves=leaves,branches=branches)

def main():
 output=[]
 paths=sorted(Path(__file__).parent.glob('finite_certificate*.json.gz'))
 expected={(2,n) for n in range(2,9)}|{(3,n) for n in range(2,6)}|{(4,3)}
 need(len(paths)==12,'exactly 12 certificates required')
 seen_specs=set()
 for path in paths:
  with gzip.open(path,'rt') as f:c=json.load(f)
  spec=(c['d'],c['n']);need(spec in expected and spec not in seen_specs,'unexpected or duplicate certificate');seen_specs.add(spec)
  r=replay(c);check(c);mutants=[]
  x=copy.deepcopy(c);x['K']-=1;mutants.append(('smaller_K',x))
  x=copy.deepcopy(c);x['K']+=1;mutants.append(('larger_K',x))
  leaf=next(k for k,v in c['nodes'].items() if 'packing' in v and v['packing'])
  x=copy.deepcopy(c);x['nodes'][leaf]['packing'][0]=0;mutants.append(('invalid_edge',x))
  x=copy.deepcopy(c);x['nodes'][leaf]['packing'].append(x['nodes'][leaf]['packing'][0]);mutants.append(('overlapping_packing',x))
  branch=next((k for k,v in c['nodes'].items() if 'children' in v),None)
  if branch is not None:
   x=copy.deepcopy(c);x['nodes'][branch]['children'].pop();mutants.append(('missing_branch',x))
  for name,x in mutants:
   for validator in (check,replay):
    try:validator(x)
    except (ValueError,KeyError):pass
    else:raise ValueError('Mutation accepted: '+name+' '+str(path)+' '+validator.__name__)
  r['rejected_mutations']=[name for name,_ in mutants];output.append(r)
 need(seen_specs==expected,'missing certificate')
 # Explicitly check construction against all ordered pairs, including equal pairs.
 p=list(itertools.product((1,2,3),repeat=6));S={x for x in p if 9<=sum(x)<=17};extra={tuple(3 if i==j else 1 for i in range(6)) for j in range(6)};A=S|extra
 need(len(S)==700 and len(A)==706,'wrong construction size')
 need(all(tuple(a+b for a,b in zip(x,y)) not in A for x in A for y in A),'not sum-free')
 need(max(sum(t<=sum(x)<2*t for x in p) for t in range(1,19))==700,'wrong slice maximum')
 print(json.dumps(dict(python_optimization=sys.flags.optimize,certificates=output,d6n3=dict(size=706,best_slice=700,ordered_pairs=len(A)**2)),indent=2))
if __name__=='__main__':main()
