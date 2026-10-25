"""Independent literal-formula checks; no published verifier is imported.

Requires SymPy 1.14.0. Tensor order is leftmost-most-significant. Sparse real
Pauli multiplication is generated from independent 2x2 matrix multiplication.
"""
import itertools,json,sys
from pathlib import Path
from datetime import datetime,timezone
import sympy as s
checks=[]
pa={'I':s.eye(2),'X':s.Matrix([[0,1],[1,0]]),'Z':s.diag(1,-1),'J':s.Matrix([[0,-1],[1,0]])}
table={}
for a,b in itertools.product(pa,repeat=2):
 for c,sign in itertools.product(pa,[1,-1]):
  if pa[a]*pa[b]==sign*pa[c]:table[a,b]=(sign,c)
if len(table)!=16:raise RuntimeError('basis multiplication incomplete')
def clean(d):return {w:s.expand(c) for w,c in d.items() if s.expand(c)!=0}
def add(*ds):
 d={}
 for x in ds:
  for w,c in x.items():d[w]=d.get(w,0)+c
 return clean(d)
def scale(a,d):return clean({w:a*c for w,c in d.items()})
def mul(a,b):
 out={}
 for w,c in a.items():
  for v,d in b.items():
   signs,word=zip(*(table[x,y] for x,y in zip(w,v)))
   key=''.join(word);out[key]=out.get(key,0)+s.prod(signs)*c*d
 return clean(out)
def adj(a):return {w:s.conjugate(c)*(-1)**w.count('J') for w,c in a.items()}
def shift(a,left,right):return {'I'*left+w+'I'*right:c for w,c in a.items()}
def zero(name,obj):
 vals=list(obj.values()) if isinstance(obj,dict) else list(obj) if isinstance(obj,s.MatrixBase) else [obj]
 bad=[s.simplify(v) for v in vals if s.simplify(v)!=0]
 if bad:raise RuntimeError(name+': '+str(bad[:5]))
 checks.append({'name':name,'pass':True})
def equal(name,a,b):zero(name,add(a,scale(-1,b)))
def dense(a):
 out=s.zeros(2**len(next(iter(a))))
 for w,c in a.items():out+=c*s.kronecker_product(*(pa[z] for z in w))
 return out
def trace(a,n):return s.simplify(2**n*a.get('I'*n,0))

Id={'IIII':s.Integer(1)}
A,B,C,D,E=[{w:s.Integer(1)} for w in ['ZIZZ','ZIJJ','JIZJ','JIJZ','XIXX']]
M=scale(s.Rational(1,2),add(scale(-1,A),scale(-1,B),scale(-1,C),D))
for i,W in enumerate([A,B,C,D,E]):
 equal(f'word {i} involution',mul(W,W),Id);equal(f'word {i} Hermitian',adj(W),W)
for i,j in itertools.combinations(range(4),2):
 words=[A,B,C,D];equal(f'first-four commute {i},{j}',mul(words[i],words[j]),mul(words[j],words[i]))
equal('ABC=D',mul(mul(A,B),C),D)
equal('M squared',mul(M,M),Id);zero('M E anticommute',add(mul(M,E),mul(E,M)))

a,b=s.symbols('a b',real=True)
Hcirc=add(scale(a,M),scale(b,E));h1=shift(Hcirc,0,2);h2=shift(Hcirc,2,0)
res=add(mul(mul(h1,h2),h1),scale(-1,mul(mul(h2,h1),h2)),scale(-s.Rational(1,3),add(h1,scale(-1,h2))))
expected={}
for coeff,words in [(-a*(3*b*b-1)/6,'IIJIJZ JIZJII ZIJJII ZIZZII'),(a*(3*b*b-1)/6,'IIJIZJ IIZIJJ IIZIZZ JIJZII'),(-b*(3*a*a-3*b*b-1)/3,'IIXIXX'),(b*(3*a*a-3*b*b-1)/3,'XIXXII'),(a*(a*a-2*b*b)/2,'JIJZXX JIZJXX XIJXZJ ZIZZXX'),(-a*(a*a-2*b*b)/2,'XIJXJZ XIZXJJ XIZXZZ ZIJJXX')]:
 for w in words.split():expected[w]=coeff
if set(res)!=set(expected):raise RuntimeError('18-word support mismatch')
G=s.groebner([a*a+b*b-1],a,b,domain=s.QQ)
for w in expected:zero('certificate coefficient '+w,G.reduce(s.expand(res[w]-expected[w]))[1])
for sa,sb in itertools.product([1,-1],repeat=2):
 zero(f'four signed circle points {sa},{sb}',{w:c.subs({a:sa*s.sqrt(s.Rational(2,3)),b:sb/s.sqrt(3)}) for w,c in res.items()})
for aa,bb in [(1,0),(-1,0),(0,1),(0,-1),(s.Rational(3,5),s.Rational(4,5))]:
 if all(s.simplify(c.subs({a:aa,b:bb}))==0 for c in res.values()):raise RuntimeError('wrong circle point accepted')
 checks.append({'name':f'negative circle control {aa},{bb}','pass':True})

H=add(scale(s.sqrt(s.Rational(2,3)),M),scale(-1/s.sqrt(3),E))
q=(1+s.I*s.sqrt(3))/2;kappa=q-1
R=add(scale((q-1)/2,Id),scale((q+1)/2,H));P=scale(s.Rational(1,2),add(Id,scale(-1,H)))
equal('R unitarity',mul(adj(R),R),Id)
zero('R Hecke relation',mul(add(R,Id),add(R,scale(-q,Id))))
R1,R2=shift(R,0,2),shift(R,2,0)
equal('exact 64-dimensional Yang Baxter relation',mul(mul(R1,R2),R1),mul(mul(R2,R1),R2))
equal('projection idempotence',mul(P,P),P);equal('projection Hermitian',adj(P),P)
zero('rank from projection trace',trace(P,4)-8)
for side in [0,1]:
 def ptr(F):
  out={}
  for w,c in F.items():
   traced,retained=(w[:2],w[2:]) if side==0 else (w[2:],w[:2])
   if traced=='II':out[retained]=out.get(retained,0)+4*c
  return out
 equal(f'projection partial trace side {side}',ptr(P),{'II':2})
 equal(f'positive enhancement side {side}',ptr(R),{'II':2*kappa})
 equal(f'negative enhancement side {side}',ptr(adj(R)),{'II':2/kappa})
equal('local order cube',mul(mul(R,R),R),scale(-1,Id))
zero('matrix skein identity',add(R,scale(-q,adj(R)),scale(-kappa,Id)))
P1,P2=shift(P,0,2),shift(P,2,0);I6={'IIIIII':s.Integer(1)}
T=add(mul(mul(P1,P2),P1),scale(-s.Rational(1,3),P1))
zero('non-Temperley-Lieb norm witness',trace(mul(adj(T),T),6)/64-s.Rational(1,18))
F1,F2=add(I6,scale(-1,P1)),add(I6,scale(-1,P2))
TC=add(mul(mul(F1,F2),F1),scale(-s.Rational(1,3),F1))
zero('complemented norm witness',trace(mul(adj(TC),TC),6)/64-s.Rational(1,18))

# Within-site qubit permutation and generalized shifts.
swap=lambda w:w[1]+w[0]+w[3]+w[2]
Hp={swap(w):c for w,c in H.items()}
KH={w[1:]:c for w,c in Hp.items()}
equal('literal three-qubit reflection formula',KH,{'ZZZ':-1/s.sqrt(6),'ZJJ':-1/s.sqrt(6),'JJZ':-1/s.sqrt(6),'JZJ':1/s.sqrt(6),'XXX':-1/s.sqrt(3)})
K=add({'III':(q-1)/2},scale((q+1)/2,KH))
for shiftby,expectednorm in [(1,24),(2,0)]:
 k1,k2=shift(K,0,shiftby),shift(K,shiftby,0)
 rr=add(mul(mul(k1,k2),k1),scale(-1,mul(mul(k2,k1),k2)))
 zero(f'generalized shift {shiftby} Frobenius norm',trace(mul(adj(rr),rr),3+shiftby)-expectednorm)

AA=scale(-s.I*s.sqrt(2),M);BB=scale(s.I,E)
UK=scale(s.Rational(1,2),add(AA,mul(AA,BB)));VK=scale(s.Rational(1,2),add(AA,scale(-1,mul(AA,BB))))
equal('quaternion U square',mul(UK,UK),scale(-1,Id));equal('quaternion V square',mul(VK,VK),scale(-1,Id))
equal('quaternion UV',mul(UK,VK),BB);zero('quaternion anti-commutator',add(mul(UK,VK),mul(VK,UK)))
sqrt2=s.sqrt(2);ii=s.I
S=s.Matrix([[2+sqrt2,-ii*sqrt2,ii*sqrt2,2-sqrt2],[sqrt2,ii*(2+sqrt2),ii*(2-sqrt2),-sqrt2],[-(2-sqrt2),-ii*sqrt2,ii*sqrt2,-(2+sqrt2)],[-sqrt2,ii*(2-sqrt2),ii*(2+sqrt2),sqrt2]])/4
zero('literal S is unitary',S.H*S-s.eye(4));SS=s.kronecker_product(S,S)
U={'IZZI':ii};V={'XIXX':ii};op=lambda f:{w[2:]+w[:2]:c for w,c in f.items()}
zero('literal swapped U comparison',SS.H*dense(op(U))*SS-dense(UK))
zero('literal swapped V comparison',SS.H*dense(op(V))*SS-dense(VK))
RGR=scale(kappa/2,add(Id,U,V,mul(U,V)))
zero('literal full local equivalence',SS.H*dense(op(RGR))*SS-dense(R))
if all(s.simplify(c)==0 for c in SS.H*dense(RGR)*SS-dense(R)):raise RuntimeError('site-swap negative control failed')
checks.append({'name':'negative control: deleting site swap breaks displayed S equivalence','pass':True})

def braidtrace(n,word):
 out={'I'*(2*n):s.Integer(1)}
 for gen in word:out=mul(out,shift(R if gen>0 else adj(R),2*(abs(gen)-1),2*(n-abs(gen)-1)))
 return s.simplify(kappa**(-sum(1 if z>0 else -1 for z in word))*trace(out,2*n)/2**n)
for n,word,value in [(1,[],2),(2,[],4),(2,[1,1],-2),(2,[-1,-1],-2),(2,[1,1,1],-4),(2,[-1,-1,-1],-4),(3,[1,-2]*2,-4),(3,[1,-2]*3,2),(2,[1],2),(2,[-1],2)]:
 zero(f'link and stabilization control n={n},word={word}',braidtrace(n,word)-value)

result={'utc':datetime.now(timezone.utc).isoformat(),'python':sys.version,'sympy':s.__version__,'count':len(checks),'checks':checks,'certificate_words':len(res),'limitations':'Exact finite algebra from literal published formulas. Not proof of arbitrary-n trace uniqueness, classification, algorithm complexity or topological identification; those require written/primary-source review.'}
Path(__file__).with_name('fresh-exact-results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
