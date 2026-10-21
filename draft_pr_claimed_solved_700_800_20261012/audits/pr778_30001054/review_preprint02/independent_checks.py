
import itertools, collections, json, random, math
states=[p for p in itertools.permutations(range(4)) if p.index(0)<p.index(1) and p.index(2)<p.index(3)]
def R(p): return tuple(x^1 for x in p[::-1])
def transition(p,q):
 d=[i for i in range(len(p)) if p[i]!=q[i]]
 if len(d)!=2 or d[1]!=d[0]+1: return None
 a,b=d
 return (q[a],q[b]) if p[a]==q[b] and p[b]==q[a] and p[a]//2!=p[b]//2 else None
words=[]
for h in itertools.product(states,repeat=4):
 w=h+tuple(map(R,h)); swaps=[transition(w[i],w[(i+1)%8]) for i in range(8)]
 if None in swaps:continue
 if any(all(w[i]==w[(i+k)%8] for i in range(8)) for k in (1,2,4)):continue
 words.append((w,swaps))
counts=collections.Counter((all(c==1 for c in collections.Counter(s).values()),sum((a%2)!=(b%2) for a,b in s)) for w,s in words)
A=(0,2,1,3);B=(0,2,3,1);C=(2,0,3,1);w=(A,B,A,B,C,B,C,B)
sw=[transition(w[i],w[(i+1)%8]) for i in range(8)]
rng=random.Random(77830001054); controls=[]
for n in range(2,13):
 for trial in range(20):
  p=tuple(range(2*n));target=tuple(x^1 for x in p[::-1]);rank={x:i for i,x in enumerate(target)};half=[]
  while p!=target:
   half.append(p)
   j=rng.choice([i for i in range(2*n-1) if rank[p[i]]>rank[p[i+1]]])
   q=list(p);q[j],q[j+1]=q[j+1],q[j];p=tuple(q)
  z=half+[tuple(x^1 for x in p[::-1]) for p in half]
  ev=[transition(z[i],z[(i+1)%len(z)]) for i in range(len(z))]
  if None in ev or len(ev)!=8*math.comb(n,2) or len(collections.Counter(ev))!=len(ev):raise ValueError('separated counterexample')
 controls.append({'n':n,'random_geodesics':20,'full_length':8*math.comb(n,2)})
print(json.dumps({'states':states,'half_tuples':6**4,'primitive_words':len(words),'class_counts':[{ 'switch_once':k[0],'mixed':k[1],'count':v} for k,v in counts.items()],'witness_member':any(x==w for x,s in words),'witness_switches':sw,'separated_controls':controls,'status':'PASS'},indent=2))
