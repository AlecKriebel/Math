"""Fresh review controls: no imports from candidate or earlier reviews."""
import json,itertools,math,hashlib,sys
from collections import deque
from fractions import Fraction

def need(x,s):
 if not x:raise ValueError(s)
def offsets(q,A,wrong=False):
 h=lambda a:int(a%q in A)
 return [a for a in range(q) for _ in range(1+(-1 if wrong else 1)*(h(-a-1)-h(-a)))]
def construct(banks,orient):
 counters=[(q,a) for q,A in banks for a in offsets(q,A)]
 Q=len(counters);P=max(q for q,A in banks);N=Q+P+int(orient)
 es={(0,v) for v in range(1,Q+1)}
 for v,(q,a) in enumerate(counters,1):
  destinations=range(Q+1,Q+q+1) if orient else [0,*range(Q+1,Q+q)]
  es.update((v,t) for t in destinations)
 es.update((t,0) for t in range(Q+1,N))
 adj=[tuple(sorted(t for u,t in es if u==v)) for v in range(N)]
 B=sum(q*(q+1)//2-len(A) for q,A in banks)
 x=[0]+[a for q,a in counters]+[0]*(N-Q-1);x[0]=Q+B-1-sum(x)
 return adj,x,counters,B

def step(adj,x,v,dissipate=False):
 d=len(adj[v]);need(x[v]>=d,'legal')
 y=list(x);y[v]-=d
 if not dissipate:
  for t in adj[v]:y[t]+=1
 need(min(y)>=0,'nonnegative')
 if not dissipate:need(sum(y)==sum(x),'conserved')
 return tuple(y)
def orbit(adj,x,highest=False,dissipate_from=None):
 x=tuple(x);seen=set();f=[0]*len(x)
 while x not in seen:
  seen.add(x);active=[v for v in range(len(x)) if x[v]>=len(adj[v])]
  if not active:return True,x,f,len(seen)
  v=active[-1] if highest else active[0]
  x=step(adj,x,v,dissipate_from is not None and v>=dissipate_from);f[v]+=1
  need(len(seen)<200000,'orbit budget')
 return False,x,f,len(seen)
def determinant(m):
 a=[[Fraction(x) for x in r] for r in m];r=Fraction(1)
 for i in range(len(a)):
  pivot=next((j for j in range(i,len(a)) if a[j][i]),None)
  if pivot is None:return 0
  if pivot!=i:a[i],a[pivot]=a[pivot],a[i];r=-r
  val=a[i][i];r*=val;a[i]=[x/val for x in a[i]]
  for j in range(i+1,len(a)):
   val=a[j][i];a[j]=[x-val*y for x,y in zip(a[j],a[i])]
 need(r.denominator==1,'integral cofactor');return int(r)
def strong(adj):
 for v in range(len(adj)):
  s={v};q=[v]
  for a in q:
   for b in adj[a]:
    if b not in s:s.add(b);q.append(b)
  if len(s)<len(adj):return False
 return True
def main():
 R={'bank_subsets':0,'bank_phases':0,'physical_bank_graphs':0,'physical_checkpoint_firings':0,'arbitrary_orbits':0,'cofactor_graphs':0,'generic_markings':0,'actual_halting_vectors':0,'semantic_faults':[]}
 for q in range(2,8):
  for bits in range(1,1<<q):
   A={i for i in range(q) if bits>>i&1};o=offsets(q,A)
   need(len(o)==q,'q distinct physical counters');R['bank_subsets']+=1
   for k in range(-2*q,3*q):
    K=q*(q-1)//2-len(A);s=sum((a+k)%q for a in o)
    need(s==K+q*int(k%q in A),'storage');R['bank_phases']+=1
   for oriented in (False,True):
    adj,x,cs,B=construct([(q,A)],oriented);Q=len(cs);N=len(adj);mass=sum(x)
    need(N==Q+q+int(oriented),'N')
    need(sum(map(len,adj))==Q+q*q+q-1+int(oriented),'E')
    need(strong(adj),'connected')
    need(all(v not in adj[v] for v in range(N)),'no loops')
    need(all(len(adj[v])==len(set(adj[v])) for v in range(N)),'simple')
    if oriented:need(all(v not in adj[t] for v in range(N) for t in adj[v]),'oriented')
    need(all(not any(t and adj[t]!=(0,) for t in adj[v]) for v in range(1,N)),'root DAG depth')
    # Run exactly until first accepting phase, no phase certificate taken on faith.
    for k in range(q+1):
     need(list(x[1:Q+1])==[(a+k)%m for m,a in cs],'physical residues')
     need(not any(x[Q+1:]),'returns zero')
     need(x[0]==mass-sum(x[1:Q+1]),'checkpoint conservation')
     need((x[0]<Q)==(k%q in A),'halting phase')
     if x[0]<Q:break
     x=step(adj,x,0);R['physical_checkpoint_firings']+=1
     for v in range(1,Q+1):
      if x[v]>=len(adj[v]):x=step(adj,x,v);R['physical_checkpoint_firings']+=1
     for t in range(Q+1,N):
      while x[t]:x=step(adj,x,t);R['physical_checkpoint_firings']+=1
    else:raise ValueError('nonempty A never accepted')
    R['physical_bank_graphs']+=1
 # Bank mixtures deliberately include q=2 full A, incompatible phases, and coprime clocks.
 families=[[(2,{0,1})],[(2,{0,1}),(3,{2})],[(3,{0}),(3,{1})],[(3,{1}),(5,{0})],[(3,{0,1}),(5,{0,1}),(15,{1,6,10})]]
 for banks in families:
  M=math.lcm(*(q for q,A in banks));expected=any(all(k%q in A for q,A in banks) for k in range(M))
  for oriented in (False,True):
   adj,x,cs,B=construct(banks,oriented)
   for highest in (False,True):
    yes,z,f,length=orbit(adj,x,highest);need(yes==expected,'arbitrary mixture outcome');R['arbitrary_orbits']+=1
 # Meaningful faults: raw bank sign reversal moves a specific accepting phase; threshold +1 changes YES to NO; loss changes NO to YES.
 q=3;A={0};wrong=offsets(q,A,True);need(sum(wrong)!=q*(q-1)//2-len(A)+q,'reversed bank phase rejected')
 R['semantic_faults'].append({'fault':'reverse multiplicity sign','q':q,'A':[0],'correct_storage_phase0':5,'damaged_storage_phase0':1,'rejected':True})
 for oriented in (False,True):
  adj,x,cs,B=construct([(3,{0})],oriented);yes,_,_,_=orbit(adj,x);x[0]+=1;bad,_,_,_=orbit(adj,x)
  need(yes and not bad,'root extra changes YES');R['semantic_faults'].append({'fault':'extra root chip','oriented':oriented,'before_halts':yes,'after_halts':bad})
  adj,x,cs,B=construct([(3,{0}),(3,{1})],oriented);yes,_,_,_=orbit(adj,x);bad,z,_,_=orbit(adj,x,dissipate_from=1+len(cs))
  need(not yes and bad and sum(z)<sum(x),'physical loss changes NO');R['semantic_faults'].append({'fault':'return emits no chip','oriented':oriented,'before_halts':yes,'after_halts':bad,'chips_lost':sum(x)-sum(z)})
 # Fresh classical union/complement check: all clause subsets for 2 and 3 variables.
 R['CRT_formulas']=0;R['CRT_phase_tests']=0;R['nonBoolean_local_extras']=0
 for n,primes in [(2,(3,5)),(3,(3,5,7))]:
  signs=list(itertools.product((False,True),repeat=n));M=math.prod(primes)
  for select in range(1<<len(signs)):
   clauses=[signs[j] for j in range(len(signs)) if select>>j&1]
   sat=any(all(any(bit==sign for bit,sign in zip(bits,c)) for c in clauses) for bits in itertools.product((False,True),repeat=n))
   # New allowed clause representation obtained by Boolean CRT residue enumeration.
   allowed=[]
   for c in clauses:
    allowed.append({k for k in range(M) if all(k%q in (0,1) for q in primes) and any(bool(k%q)==sign for q,sign in zip(primes,c))})
   accepted=False
   for k in range(M):
    variable_ok=all(k%q in (0,1) for q in primes)
    ours=variable_ok and all(k in A for A in allowed)
    # Literal earlier bad language is defined separately by unique failed tuple.
    invalid=any(k%q>=2 for q in primes)
    bad_clause=any(all(k%q==int(not sign) for q,sign in zip(primes,c)) for c in clauses)
    need(ours == (not (invalid or bad_clause)),'literal classical union complement')
    if clauses and not variable_ok:
     need(invalid and not bad_clause,'local nonBoolean extras already variable-invalid');R['nonBoolean_local_extras']+=1
    accepted |= ours;R['CRT_phase_tests']+=1
   need(accepted==sat,'CRT SAT polarity');R['CRT_formulas']+=1
 need(not any((b and not b) for b in (False,True)) and any((b and b) for b in (False,True)),'erased negative literal semantic fault')
 R['semantic_faults'].append({'fault':'erase negative literal in (x) and (not x)','before_SAT':False,'after_SAT':True,'rejected':True})
 # Cofactor orientation, kernel and coordinate certificate bounds on all n<=3 and sampled n=4 SC graphs, independently with exact elimination.
 for n in (2,3,4):
  pairs=[(u,v) for u in range(n) for v in range(n) if u!=v]
  masks=range(1<<len(pairs)) if n<4 else range(0,1<<len(pairs),17)
  for mask in masks:
   adj=[tuple(v for i,(u,v) in enumerate(pairs) if u==r and mask>>i&1) for r in range(n)]
   if not strong(adj):continue
   L=[[len(adj[v]) if u==v else -int(u in adj[v]) for v in range(n)] for u in range(n)]
   tree=[determinant([[L[u][v] for v in range(n) if v!=r] for u in range(n) if u!=r]) for r in range(n)]
   g=math.gcd(*tree);pi=[t//g for t in tree]
   need(min(pi)>0 and max(tree)<=(n-1)**(n-1),'tree size')
   need(all(sum(L[u][v]*pi[v] for v in range(n))==0 for u in range(n)),'column kernel')
   R['cofactor_graphs']+=1
   for x in itertools.product(range(4),repeat=n):
    if sum(x)>3:continue
    R['generic_markings']+=1
    yes,z,f,_=orbit(adj,x,True)
    if yes:
     R['actual_halting_vectors']+=1
     need(any(a<b for a,b in zip(f,pi)),'period subtraction')
     need(all(f[v]+1<=(n-1)**(2*n-2) for v in range(n)),'bit bound')
     need(all(f[u]+1<=len(adj[v])*(f[v]+1) for u in range(n) for v in adj[u]),'additive arc bound')
     need(all(x[u]-sum(L[u][v]*f[v] for v in range(n))==z[u] for u in range(n)),'balance')
 adj=[(1,),(0,2),(0,)];yes,z,f,_=orbit(adj,[1,0,0]);need(yes and f==[1,0,0] and f[0]>len(adj[1])*f[1],'actual omitted-slack counterexample')
 R['semantic_faults'].append({'fault':'omit additive certificate slack','edges':[[0,1],[1,0],[1,2],[2,0]],'input':[1,0,0],'actual_f':f,'false_claim':'f0 <= d1*f1','rejected':True})
 R['status']='PASS';R['candidate_code_imported']=False;R['scope']='Fresh finite controls, not a proof or priority certification.'
 return R
if __name__=='__main__':
 if sys.argv[1:]==['--invalid']:raise ValueError('unconditional review guard')
 need(not sys.argv[1:],'unexpected arguments')
 print(json.dumps(main(),sort_keys=True,indent=2))
