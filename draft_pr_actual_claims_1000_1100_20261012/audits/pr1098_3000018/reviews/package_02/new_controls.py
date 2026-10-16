"""Whole02: new inverse-bank, mixed noncoprime and exhaustive phase confluence controls.
No imports from candidate or earlier reviewer programs. All guards are exceptions.
"""
import sys,json,itertools,math,random
from collections import deque

def need(x,s):
 if not x: raise ValueError(s)
def offsets(q,A):
 return tuple(a for a in range(q) for j in range(1+int((-a-1)%q in A)-int((-a)%q in A)))
def graph(bs,o):
 cs=[(q,a) for q,A in bs for a in offsets(q,A)];Q=len(cs);P=max(q for q,A in bs)
 N=1+Q+P-(not o);ad=[[] for _ in range(N)];ad[0]=list(range(1,Q+1))
 for v,(q,a) in enumerate(cs,1):ad[v]=list(range(Q+1,Q+q+1)) if o else [0]+list(range(Q+1,Q+q))
 for t in range(Q+1,N):ad[t]=[0]
 B=sum(q*(q+1)//2-len(A) for q,A in bs);x=[0]+[a for q,a in cs]+[0]*(N-Q-1);x[0]=Q+B-1-sum(x)
 need(x[0]>=0,'root nonnegative');return ad,tuple(x),cs,B

def fire(ad,x,v,drop=None):
 need(x[v]>=len(ad[v]),'legal');y=list(x);y[v]-=len(ad[v])
 for t in ad[v]:
  if (v,t)!=drop:y[t]+=1
 need(min(y)>=0,'nonnegative')
 if drop is None:need(sum(y)==sum(x),'conservation')
 return tuple(y)
def orbit(ad,x,drop=None):
 seen=set();f=[0]*len(ad)
 while x not in seen:
  seen.add(x);vs=[v for v in range(len(ad)) if x[v]>=len(ad[v])]
  if not vs:return True,x,f
  v=vs[(len(seen)*7)%len(vs)];x=fire(ad,x,v,drop);f[v]+=1
  need(len(seen)<100000,'orbit finite budget')
 return False,x,f

def all_phase(ad,initial):
 """Enumerate every legal nonroot firing order, including simultaneous ready returns."""
 seen={initial};queue=deque([initial]);term=set();edges=0
 while queue:
  x=queue.popleft();vs=[v for v in range(1,len(ad)) if x[v]>=len(ad[v])]
  if not vs:term.add(x)
  for v in vs:
   y=fire(ad,x,v);edges+=1
   if y not in seen:seen.add(y);queue.append(y)
 return seen,term,edges

def det(m):
 # Bareiss, independently integer-only (not the former fractional elimination).
 a=[list(r) for r in m];n=len(a);last=1;sgn=1
 for k in range(n-1):
  if a[k][k]==0:
   p=next((i for i in range(k+1,n) if a[i][k]),None)
   if p is None:return 0
   a[k],a[p]=a[p],a[k];sgn=-sgn
  pivot=a[k][k]
  for i in range(k+1,n):
   for j in range(k+1,n):
    z=a[i][j]*pivot-a[i][k]*a[k][j];need(z%last==0,'Bareiss exact division');a[i][j]=z//last
  for i in range(k+1,n):a[i][k]=0
  last=pivot
 return sgn*a[-1][-1]
def main():
 R={'inverse_word_tests':0,'rotation_covariance':0,'mixed_noncoprime_instances':0,'all_phase_states':0,'all_phase_edges':0,'all_phase_terminal_tests':0,'first_period_deletion_words':0,'first_period_deletion_remaining_firings':0,'larger_cofactor_graphs':0,'larger_markings':0,'actual_stabilizing_vectors':0,'faults':[]}
 # Inverse direction: a balanced multiplicity word has two-level height storage
 # iff its integrated wrapping deficit has exactly two heights distance one.
 for q in range(2,7):
  for c in itertools.product(range(3),repeat=q):
   if sum(c)!=q:continue
   storage=[sum(c[a]*((a+k)%q) for a in range(q)) for k in range(q)]
   dif={v-min(storage) for v in storage};two=dif=={0,q}
   if two:
    A={k for k,v in enumerate(storage) if v==max(storage)}
    need(tuple(c)==tuple(offsets(q,A).count(a) for a in range(q)),'inverse recovery of exact bank')
   R['inverse_word_tests']+=1
  for mask in range(1,1<<q):
   A={i for i in range(q) if mask>>i&1};off=offsets(q,A)
   for shift in range(q):
    rotated={(a-shift)%q for a in A};off2=offsets(q,rotated)
    need(sorted((a+shift)%q for a in off)==sorted(off2),'phase-shift physical priming covariance')
    R['rotation_covariance']+=1
 # Distinct from prior banks: all nonempty sets q=2 paired with all q=4 sets,
 # then q=4/q=6 noncoprime cases. Test exact accepted phases and genuine phase confluence.
 mixtures=[]
 for a in range(1,4):
  for b in range(1,16):mixtures.append([(2,{i for i in range(2) if a>>i&1}),(4,{i for i in range(4) if b>>i&1})])
 mixtures += [[(4,{1}),(6,{3})],[(4,{0,2}),(6,{1,3,5})],[(2,{0,1}),(6,{2,4})]]
 for bs in mixtures:
  M=math.lcm(*(q for q,A in bs));expected=any(all(k%q in A for q,A in bs) for k in range(M))
  for o in (False,True):
   ad,x,cs,B=graph(bs,o);Q=len(cs);mass=sum(x)
   for k in range(M+1):
    need(x[1:Q+1]==tuple((a+k)%q for q,a in cs),'mixed offsets');need(not any(x[Q+1:]),'empty returns')
    accepts=all(k%q in A for q,A in bs);need((x[0]<Q)==accepts,'mixed exact stop phase')
    if accepts:break
    if k==M:break
    start=fire(ad,x,0)
    if k==0 and len(ad)<=12:
     states,term,edges=all_phase(ad,start);need(len(term)==1,'all nonroot schedules converge');x=next(iter(term))
     R['all_phase_states']+=len(states);R['all_phase_edges']+=edges;R['all_phase_terminal_tests']+=1
    else:
     y=start
     while True:
      v=next((v for v in range(1,len(ad)) if y[v]>=len(ad[v])),None)
      if v is None:break
      y=fire(ad,y,v)
     x=y
    need(sum(x)==mass,'mixed mass')
   need(accepts==expected,'mixed halting equivalence');R['mixed_noncoprime_instances']+=1
 # Independent Laplacian cofactors on random n=5,6 with a guaranteed Hamiltonian cycle.
 rng=random.Random(109802)
 for n in (5,6):
  for sample in range(25):
   ad=[sorted({(v+1)%n}|{u for u in range(n) if u!=v and rng.randrange(5)==0}) for v in range(n)]
   L=[[len(ad[j]) if i==j else -int(i in ad[j]) for j in range(n)] for i in range(n)]
   cof=[det([[L[i][j] for j in range(n) if j!=r] for i in range(n) if i!=r]) for r in range(n)]
   need(min(cof)>0 and max(cof)<=(n-1)**(n-1),'larger cofactor bound');g=math.gcd(*cof);pi=[x//g for x in cof]
   need(all(sum(L[i][j]*pi[j] for j in range(n))==0 for i in range(n)),'larger kernel orientation');R['larger_cofactor_graphs']+=1
   # Independent first-period deletion, including incomplete period quotas.
   initial=tuple(len(ad[v]) for v in range(n));state=initial;word=[]
   for tick in range(200):
    active=[v for v in range(n) if state[v]>=len(ad[v])]
    need(active,'mass above stable capacity');v=active[rng.randrange(len(active))];word.append(v);state=fire(ad,state,v)
   removed=[0]*n;replay=initial;kept=0
   for v in word:
    if removed[v]<pi[v]:removed[v]+=1
    else:replay=fire(ad,replay,v);kept+=1
   need(all(removed[v]<=pi[v] for v in range(n)),'deleted quotas')
   if removed==pi:need(replay==state,'complete period deletion endpoint')
   R['first_period_deletion_words']+=1;R['first_period_deletion_remaining_firings']+=kept
   for trial in range(10):
    x=tuple(rng.randrange(len(ad[v])+1) for v in range(n));yes,z,f=orbit(ad,x);R['larger_markings']+=1
    if yes:
     need(any(f[v]<pi[v] for v in range(n)),'larger period subtraction');need(all(f[v]+1<=(n-1)**(2*n-2) for v in range(n)),'larger bit bound')
     need(all(f[u]+1<=len(ad[v])*(f[v]+1) for u in range(n) for v in ad[u]),'larger arc direction');R['actual_stabilizing_vectors']+=1
 # Fresh physical faults: collapse equal-offset counters, and omit one counter-return output.
 bs=[(4,{1}),(6,{3})];ad,x,cs,B=graph(bs,True)
 need(len(cs)>len(set(cs)),'equal offsets really repeat')
 R['faults'].append({'fault':'merge repeated (modulus,offset) counters','original_Q':len(cs),'merged_Q':len(set(cs)),'violates_exact_q_counters':True})
 ad,x,cs,B=graph([(4,{2})],True);counter=next(v for v in range(1,5) if x[v]==3)
 y=fire(ad,fire(ad,x,0),counter);bad=fire(ad,fire(ad,x,0),counter,(counter,ad[counter][-1]))
 need(sum(bad)==sum(y)-1,'omitted physical output detected');R['faults'].append({'fault':'omit one distinct counter output','lost_chips':sum(y)-sum(bad)})
 # Wrong path direction fails concretely in a legal halting word found on a fixed graph.
 ad=[[1],[0,2],[0]];yes,z,f=orbit(ad,(1,0,0));need(yes and f[0]==1 and f[1]==0,'actual slack counterexample')
 need(f[0]+1<=len(ad[1])*(f[1]+1) and not(f[0]<=len(ad[1])*f[1]),'additive slack necessary')
 R['faults'].append({'fault':'delete additive certificate slack','actual_f':f,'final':z})
 R['candidate_or_prior_code_imported']=False;R['status']='PASS';R['limitation']='Finite independent falsification controls, not a proof or literature certification.'
 return R
if __name__=='__main__':
 if sys.argv[1:]==['--invalid']:raise ValueError('whole02 unconditional exception control')
 need(not sys.argv[1:],'unexpected arguments')
 print(json.dumps(main(),sort_keys=True,indent=2))
