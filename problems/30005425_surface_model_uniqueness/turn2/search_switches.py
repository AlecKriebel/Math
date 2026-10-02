import itertools,json,random

def local_options(n,arrows):
 out=[]
 for v in range(n):
  inc=[i for i,(_,t) in enumerate(arrows) if t==v];succ=[i for i,(s,_) in enumerate(arrows) if s==v]
  if len(inc)>2 or len(succ)>2:return
  pairs=list(itertools.product(inc,succ));opts=[]
  for bits in itertools.product((0,1),repeat=len(pairs)):
   r={p for p,b in zip(pairs,bits) if b}
   if all(sum((a,b) in r for b in succ)<=1 and sum((a,b) not in r for b in succ)<=1 for a in inc) and all(sum((a,b) in r for a in inc)<=1 and sum((a,b) not in r for a in inc)<=1 for b in succ):opts.append(r)
  opts=[r for r in opts if not any(r<s for s in opts)]
  out.append([set(pairs)-r for r in opts])
 return out

def finite(trans):
 nxt=dict(trans)
 for a in nxt:
  seen=set();b=a
  while b in nxt:
   if b in seen:return False
   seen.add(b);b=nxt[b]
 return True

def analyze(n,arrows):
 opts=local_options(n,arrows)
 if opts is None:return
 states=[]
 for st in itertools.product(*[range(len(o)) for o in opts]):
  tr=set().union(*(opts[v][i] for v,i in enumerate(st)))
  if finite(tr):states.append(st)
 remaining=set(states);components=[]
 while remaining:
  st=remaining.pop();todo=[st];comp=[st]
  while todo:
   x=todo.pop()
   for v in range(n):
    if len(opts[v])!=2:continue
    y=x[:v]+(1-x[v],)+x[v+1:]
    if y in remaining:remaining.remove(y);todo.append(y);comp.append(y)
  components.append(sorted(comp))
 return {'vertices':n,'arrows':arrows,'options':[[sorted(r) for r in o] for o in opts],'finite_count':len(states),'components':components}
if __name__=='__main__':
 rng=random.Random(33602);checked=0
 for n in range(2,11):
  for k in range(20000):
   outgoing=[v for v in range(n) for _ in range(2)];incoming=outgoing.copy();rng.shuffle(outgoing);rng.shuffle(incoming)
   m=rng.randrange(n,2*n+1);arrows=list(zip(outgoing[:m],incoming[:m]));r=analyze(n,arrows);checked+=1
   if len(r['components'])>1:
    print(json.dumps({'checked':checked,'witness':r},indent=2));raise SystemExit
 print(json.dumps({'checked':checked,'no_disconnected_found':True}))
