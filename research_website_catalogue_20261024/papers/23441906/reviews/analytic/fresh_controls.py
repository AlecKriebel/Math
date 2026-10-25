"""Independent exact controls. No submitted verification imports.
Ring arithmetic uses explicit coefficient convolution and a four-bit chart of V.
The ideal search closes prime-field spans from projective directions, not all
19,999 element seeds, and records only valid ideal consequences.
"""
from itertools import product
from pathlib import Path
import json,time,hashlib,datetime
OUT=Path(__file__).resolve().parent
start=time.time()
R=list(product(range(5),repeat=4));zeroR=(0,)*4
addR=lambda a,b:tuple((x+y)%5 for x,y in zip(a,b))
scaleR=lambda a,k:tuple(k*x%5 for x in a)
def mulR(a,b):
 return (0,a[0]*b[0]%5,(a[0]*b[1]+a[1]*b[0])%5,(a[0]*b[2]+a[1]*b[1]+a[2]*b[0])%5)
def logR(r):
 a,b,c,d=r
 return (a,(b+2*a*a)%5,(c+4*a*b+2*a**3)%5,(d+4*a*c+2*b*b+a*a*b+a**4)%5)
def expR(t):
 a,b,c,d=t
 return (a,(b+3*a*a)%5,(c+a*b+a**3)%5,(d+a*c+3*b*b+3*a*a*b+4*a**4)%5)
def sig(r,e):return tuple(x*(-1 if e and i%2==0 else 1)%5 for i,x in enumerate(r))
def fullV(v):return v|((bin(v).count("1")%2)<<4)
def beta(v,w):return bin(fullV(v)&fullV(w)).count("1")%2
def quad(v):return (bin(fullV(v)).count("1")//2)%2
def rot(v,s):
 t=fullV(v);s%=5
 return (((t<<s)|(t>>(5-s)))&31)&15
G=[]
for i in range(4):G.append(tuple(1 if j==i else 0 for j in range(4))+(0,0))
G += [(0,0,0,0,1<<i,0) for i in range(4)]+[(0,0,0,0,0,1)]
Z=(0,0,0,0,0,0)
def add(a,b):return addR(a[:4],b[:4])+(a[4]^b[4],a[5]^b[5])
def neg(a):return scaleR(a[:4],-1)+a[4:]
def sub(a,b):return add(a,neg(b))
def lam(a,b,no_sign=False,no_rotation=False):
 r,v,z=a[:4],a[4],a[5];u,w,Zz=b[:4],b[4],b[5]
 su=sig(u,0 if no_sign else z^quad(v));mw=rot(w,0 if no_rotation else logR(r)[3])
 return addR(su,mulR(r,su))+(mw,Zz^beta(v,mw))
def circ(a,b,**kw):return add(a,lam(a,b,**kw))
def star(a,b,**kw):return sub(lam(a,b,**kw),b)
def psi(a):return logR(a[:4])[:3]+(a[5]^quad(a[4]),a[4],logR(a[:4])[3])
# Universal coefficient-level ring identity: all625^2 ring inputs, both signs.
for r in R:
 assert logR(expR(r))==r and expR(logR(r))==r
 assert logR(sig(r,1))==sig(logR(r),1)
for r in R:
 for u in R:
  assert logR(addR(addR(r,u),mulR(r,u)))==addR(logR(r),logR(u))
# V identities and nondegeneracy checked exhaustively with a four-bit chart.
for v in range(16):
 assert quad(v)^quad(0)==quad(v)
 assert (all(beta(v,w)==0 for w in range(16)))==(v==0)
 for w in range(16):
  assert quad(v^w)==(quad(v)^quad(w)^beta(v,w))
  for s in range(5):
   assert rot(v^w,s)==(rot(v,s)^rot(w,s))
   assert beta(rot(v,s),rot(w,s))==beta(v,w)
   assert quad(rot(v,s))==quad(v)
 assert rot(v,5)==v
 assert (rot(v,1)==v)==(v==0)
assert len({rot(v,1)^v for v in range(16)})==16
# Exact psi bijection for all20,000 elements and both-sided inverse from
# the semidirect group; no enumeration of8e12 associative triples is claimed.
B=[r+(v,z) for r in R for v in range(16) for z in range(2)]
assert len({psi(a) for a in B})==20000
for a in B:
 k0,k1,k2,e,v,s=psi(a)
 invlog=((-k0*(-1 if e else 1))%5,(-k1)%5,(-k2*(-1 if e else 1))%5,(-s)%5)
 iv=rot(v,-s); inv=expR(invlog)+(iv,e^quad(iv))
 assert circ(a,inv)==Z and circ(inv,a)==Z
# Additive automorphism and multiplication transport checked on each a and
# nine additive generators; universal linearity follows from displayed blocks.
for a in B:
 pa=psi(a)
 for b in G:
  pb=psi(b); q=psi(circ(a,b))
  expect=tuple((pa[i]+pb[i]*(-1 if pa[3] and i in (0,2) else 1))%5 for i in range(3))+(pa[3]^pb[3],pa[4]^rot(pb[4],pa[5]),(pa[5]+pb[5])%5)
  assert q==expect
# Prime-field row spaces implement valid consequences of ideal membership.
def chart(a,p):
 if p==5:return a[:4]
 return tuple((a[4]>>j)&1 for j in range(4))+(a[5],)
def elem(v,p):
 if p==5:return tuple(v)+(0,0)
 return zeroR+(sum(x<<j for j,x in enumerate(v[:4])),v[4])
def insert(rows,x,p):
 x=list(x)
 for row in rows:
  pivot=next(i for i,c in enumerate(row) if c)
  if x[pivot]:
   f=x[pivot];x=[(a-f*b)%p for a,b in zip(x,row)]
 if not any(x):return False
 pivot=next(i for i,c in enumerate(x) if c);f=pow(x[pivot],-1,p);x=[v*f%p for v in x]
 rows.append(tuple(x));rows.sort(key=lambda r:next(i for i,c in enumerate(r) if c));return True
def closure(seed,**kw):
 rows={5:[],2:[]};events=[]
 def add_element(x,reason):
  # 6x and5x are primary projections; encoded by separate charts.
  for p in (5,2):
   if insert(rows[p],chart(x,p),p):events.append({'p':p,'vector':chart(x,p),'reason':reason})
 add_element(seed,'seed and primary projection')
 while True:
  old=sum(map(len,rows.values()))
  for p in (5,2):
   for row in tuple(rows[p]):
    i=elem(row,p)
    for j,g in enumerate(G):
     add_element(sub(lam(g,i,**kw),i),'lambda_g(i)-i; g='+str(j))
     add_element(star(i,g,**kw),'i*g; g='+str(j))
  if sum(map(len,rows.values()))==old:break
 return [len(rows[5]),len(rows[2])],events
lines=[]
for r in R:
 if any(r) and next(c for c in r if c)==1:lines.append(r+(0,0))
assert len(lines)==156
lines += [zeroR+(v,z) for v in range(16) for z in range(2) if v or z]
assert len(lines)==187
receipts=[]
for seed in lines:
 ranks,events=closure(seed);assert ranks==[4,5]
 receipts.append({'seed':seed,'ranks':ranks,'steps':len(events),'events':events})
assert star(star(G[0],G[0]),G[0])==G[2]
no_sign_ranks,_=closure(G[-1],no_sign=True)
no_rotation_ranks,_=closure(G[0],no_rotation=True)
assert no_sign_ranks==[0,1] and no_rotation_ranks==[4,0]
(OUT/'fresh-ideal-directions.json').write_text(json.dumps(receipts,indent=2)+'\n')
# Small asymmetric-product boundary controls use generic operations rather
# than the simplified lemma formula, including additive subtraction.
def test_asym(T,S,ta,tn,b,alpha):
 A=list(product(T,S));zero=(T[0],0);n=len(S)
 plus=lambda a,c:(ta(a[0],c[0]),(a[1]+c[1]+b(a[0],c[0]))%n)
 n=len(S)
 circ2=lambda a,c:(ta(a[0],alpha(a[1],c[0])),(a[1]+c[1])%n)
 negatives={a:next(c for c in A if plus(a,c)==zero) for a in A}
 minus=lambda a,c:plus(a,negatives[c])
 la=lambda a,c:minus(circ2(a,c),a)
 st=lambda a,c:minus(la(a,c),c)
 brace_fail=None;triple_nonzero=None
 for a,c,d in product(A,repeat=3):
  assert plus(plus(a,c),d)==plus(a,plus(c,d))
  assert circ2(circ2(a,c),d)==circ2(a,circ2(c,d))
  if la(a,plus(c,d))!=plus(la(a,c),la(a,d)) and brace_fail is None:brace_fail=[a,c,d]
  if st(st(a,c),d)!=zero and triple_nonzero is None:triple_nonzero=[a,c,d,st(st(a,c),d)]
 return {'size':len(A),'brace_fail':brace_fail,'triple_nonzero':triple_nonzero,'multiplicative_abelian':all(circ2(a,c)==circ2(c,a) for a,c in product(A,repeat=2)),'double_10':plus((T[1],0),(T[1],0))}
c4=test_asym([0,1],[0,1],lambda x,y:x^y,lambda x:x,lambda x,y:x*y,lambda s,x:x)
assert c4['brace_fail'] is None and c4['triple_nonzero'] is None and c4['double_10']==(0,1)
d8=test_asym([0,1,2,3],[0,1],lambda x,y:x^y,lambda x:x,lambda x,y:((x&1)*((y>>1)&1)+((x>>1)&1)*(y&1))%2,lambda s,x:x^(((x>>1)&1) if s else 0))
assert d8['brace_fail'] is None and d8['triple_nonzero'] is not None and not d8['multiplicative_abelian']
carry=test_asym([0,1,2],[0,1,2],lambda x,y:(x+y)%3,lambda x:-x%3,lambda x,y:(x+y)//3,lambda s,x:x)
assert carry['brace_fail'] is not None
result={'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS','seconds':time.time()-start,'ring_elements':625,'ring_log_additivity_pairs':625**2,'V_elements':16,'psi_bijection_and_inverse_elements':20000,'psi_transport_generator_pairs':20000*9,'ideal_projective_directions':187,'ideal_direction_split':{'F5_lines':156,'F2_lines':31},'every_direction_reaches_prime_ranks':[4,5],'triple_star_x':list(G[2]),'mutations':{'remove_sign_action_closure_of_binary_z':no_sign_ranks,'remove_rotation_closure_of_x':no_rotation_ranks},'small_asymmetric_boundaries':{'nonsplit_C4_addition':c4,'nonabelian_Sylow_D8_triple_witness':d8,'nonbilinear_carry_cocycle_rejected_as_brace':carry},'ideal_direction_receipt_sha256':hashlib.sha256((OUT/'fresh-ideal-directions.json').read_bytes()).hexdigest(),'limits':'Exact finite/factored controls supplement the universal proof. No full20000^3 association enumeration or finite enumeration of all possible asymmetric presentations is claimed.'}
(OUT/'fresh-controls.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
