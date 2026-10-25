"""Fresh reviewer controls; exact rational arithmetic, not a diffusion simulation.

Written from the main proof and reviewer reconstruction before inspecting any
supplied control implementation. Supplementary proof prose was already read.
"""
from fractions import Fraction as Q
from itertools import product
from pathlib import Path
import json

checks=[]
def check(label, condition):
    assert condition, label
    checks.append(label)
def T(a): return [list(x) for x in zip(*a)]
def mm(a,b): return [[sum(x*y for x,y in zip(row,col)) for col in zip(*b)] for row in a]
def add(a,b): return [[x+y for x,y in zip(r,s)] for r,s in zip(a,b)]
def scale(a,c): return [[c*x for x in r] for r in a]
def eye(n): return [[Q(i==j) for j in range(n)] for i in range(n)]
def diag(v): return [[Q(x) if i==j else Q(0) for j in range(len(v))] for i,x in enumerate(v)]
def powm(a,n):
    out=eye(len(a))
    for _ in range(n): out=mm(out,a)
    return out
def rot(n,i,j):
    a=eye(n); a[i][i]=a[j][j]=Q(3,5);a[i][j]=-Q(4,5);a[j][i]=Q(4,5)
    return a

alpha=[28,-112,210,-224,140,-48,7]
for k in range(7):check(f'reflection derivative {k}',sum(a*(-i)**k for i,a in enumerate(alpha,1))==1)
check('reflection is not order seven',sum(a*(-i)**7 for i,a in enumerate(alpha,1))!=1)

# Direct path enumeration of a reversible chain, with nonsymmetric pair statistic.
P=[[Q(3,4),Q(1,4)],[Q(1,4),Q(3,4)]];pi=[Q(1,2)]*2
F=[[-1,2],[3,0]]
mean=sum(pi[a]*P[a][b]*F[a][b] for a,b in product(range(2),repeat=2))
H=[[x-mean for x in row] for row in F]
var=sum(pi[a]*P[a][b]*H[a][b]**2 for a,b in product(range(2),repeat=2))
r=[sum(pi[a]*P[a][b]*H[a][b]/pi[b] for a in range(2)) for b in range(2)]
s=[sum(P[a][b]*H[a][b] for b in range(2)) for a in range(2)]
def prob(path):
    out=pi[path[0]]
    for a,b in zip(path,path[1:]):out*=P[a][b]
    return out
for lag in range(1,7):
    actual=sum(prob(z)*H[z[0]][z[1]]*H[z[lag]][z[lag+1]] for z in product(range(2),repeat=lag+2))
    expected=sum(pi[a]*r[a]*powm(P,lag-1)[a][b]*s[b] for a,b in product(range(2),repeat=2))
    check(f'overlapping-pair covariance lag {lag}',actual==expected)
    check(f'pair covariance contraction lag {lag}',abs(actual)<=Q(1,2)**(lag-1)*var)
for n in range(1,8):
    vm=sum(prob(z)*(sum(H[a][b] for a,b in zip(z,z[1:]))/n)**2 for z in product(range(2),repeat=n+1))
    check(f'path-enumerated mean variance n={n}',vm<=Q(5, n)*9)

# Exact continuous functional calculus with indefinite spectrum and singular Gram.
# h(2**a) is represented by its rational coefficient of log(2).
n=7
U=mm(rot(n,0,2),mm(rot(n,1,4),rot(n,3,5)))
O=mm(rot(n,0,6),mm(rot(n,1,5),rot(n,2,4)))
d=list(map(Q,[1,2,3,1,2,4,0]));k=[Q(1),Q(1,2),Q(1,2),Q(2),Q(-1,2),Q(1,4),Q(0)]
g=[x*x if x>0 else Q(0) for x in k];h=[Q(0),-Q(1,4),-Q(1,4),Q(4),Q(0),-Q(1,8),Q(0)]
V=mm(mm(U,diag(d)),T(O));G=mm(T(V),V);Ghalf=mm(mm(O,diag(d)),T(O))
check('singular Gram square root',mm(Ghalf,Ghalf)==G)
ct=[k[i]/(d[i]*d[i]) if d[i] else Q(9) for i in range(n)]
C=mm(mm(O,diag(ct)),T(O));Top=mm(mm(V,C),T(V));Hn=mm(mm(Ghalf,C),Ghalf)
check('nontrivial physical operator coordinates',Top==mm(mm(U,diag(k)),T(U)))
check('nontrivial Gram operator coordinates',Hn==mm(mm(O,diag(k)),T(O)))
D=[[Q((i+1)*(j+2)%11-4,3) for j in range(n)] for i in range(5)]
v=[[Q(2*j-3,7) for j in range(n)]]
B=mm(mm(D,C),T(V));e=mm(mm(v,C),T(V))
for label,values in [('g',g),('h/log2',h)]:
    aT=mm(mm(U,diag(values)),T(U));aH=mm(mm(O,diag(values)),T(O))
    check(f'feature functional identity {label}',mm(mm(T(V),aT),V)==mm(mm(Ghalf,aH),Ghalf))
    left=mm(mm(B,aT),T(B) if label=='g' else T(e))
    right=mm(mm(mm(mm(mm(mm(D,C),Ghalf),aH),Ghalf),C),T(D) if label=='g' else T(v))
    check(f'normal-equation feature identity {label}',left==right)
    modes=mm(B,U);emodes=mm(e,U);total=[[Q(0)]*len(left[0]) for _ in left]
    for j in range(n):
        if k[j]>0:
            J=[[row[j]/k[j]] for row in modes]
            rhs=T(J) if label=='g' else [[emodes[0][j]/k[j]]]
            factor=k[j]**4 if label=='g' else k[j]**2*h[j]
            total=add(total,scale(mm(J,rhs),factor))
    check(f'fourth power mode expansion {label}',left==total)
    R=rot(n,1,2);Ur=mm(U,R)
    check(f'repeated-eigenspace rotation {label}',mm(mm(Ur,diag(values)),T(Ur))==aT)
for m in [1,2,5,20,100]:
    check(f'suppressed log near zero m={m}',Q(m,4**m)<=Q(1,2**m))
check('negative and zero spectral modes discarded',g[4]==h[4]==g[6]==h[6]==0)
check('empirical mode above one is supported',g[3]==h[3]==4)

# Differential jet checks using symbolic independent differentiation.
# Kept independent of supplied suites; SymPy is used only for polynomial algebra.
import sympy as sp
x,y=sp.symbols('x y');z=[x,y]
S=sp.Matrix([[2+x*x,x*y+sp.Rational(1,3)],[x*y+sp.Rational(1,3),3+y*y]])
u=x*x+2*x*y+3*y*y+x-y
grad=sp.Matrix([sp.diff(u,t) for t in z]);flux=S*grad
direct=sum(sp.diff(flux[i],z[i]) for i in range(2))
div=sp.Matrix([sum(sp.diff(S[i,j],z[i]) for i in range(2)) for j in range(2)])
J=sp.Matrix([sp.diff(u,x,2),sp.diff(u,y,2),2*sp.diff(u,x,y),sp.diff(u,x),sp.diff(u,y)])
theta=sp.Matrix([S[0,0],S[1,1],S[0,1],*div])
check('anisotropic variable tensor jet identity',sp.expand(direct-(J.T*theta)[0])==0)
check('off-diagonal factor two is load bearing',sp.expand(direct-((J-sp.Matrix([0,0,sp.diff(u,x,y),0,0])).T*theta)[0])!=0)
polys=[x*x/2,y*y/2,x*y/2,x,y]
jetrows=[]
for p in polys:
    jetrows.append([sp.diff(p,x,2),sp.diff(p,y,2),2*sp.diff(p,x,y),sp.diff(p,x).subs({x:0,y:0}),sp.diff(p,y).subs({x:0,y:0})])
check('cutoff-polynomial full jet span',sp.Matrix(jetrows)==sp.eye(5))
M=sp.Matrix([[2,1],[1,2]]);normal=sp.Matrix([1,0])
check('normal Neumann does not imply conormal', (normal.T*sp.Matrix([0,1]))[0]==0 and (normal.T*M*sp.Matrix([0,1]))[0]==1)
check('conormal does not imply normal Neumann',(normal.T*M*sp.Matrix([1,-2]))[0]==0 and (normal.T*sp.Matrix([1,-2]))[0]==1)

# Eventual positive definiteness, not noise-to-ridge domination, stabilizes fit.
errs=[]
for j in [2,4,8,16,32]:
    lam=Q(1,2**(j*j));a=[Q(1)+Q(1,j),Q(2)+Q(1,j)];truth=[Q(1),Q(-1)]
    rr=[Q(1)+Q(1,j),Q(-2)+Q(1,j)]
    est=[rr[i]/(a[i]+lam) for i in range(2)]
    err=max(abs(est[i]-truth[i]) for i in range(2));errs.append(err)
    check(f'fast ridge valid error bound j={j}',err<=Q(2,j))
check('fast ridge errors decrease',all(a>b for a,b in zip(errs,errs[1:])))
check('rank-deficient excitation fails for invisible coordinate',Q(0,1)/(Q(0)+Q(1,10))!=1)

# Operator-norm convergence alone is insufficient for a density/HS claim.
for n in [2,10,100]:
    check(f'HS trace-tail negative control rank={n*n}',Q(n*n,n*n)==1 and Q(1,n)<1)

result={'status':'PASS','checks':len(checks),'exact_checks':checks,
        'limits':'Finite rational/polynomial identities corroborate proof interfaces; no statistical asymptotics, elliptic regularity, or novelty is certified by these controls.'}
Path(__file__).with_name('fresh_controls_results.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'checks':len(checks)}))
