import sympy as s
from itertools import permutations
ru, rx, ry = s.symbols('R_u R_x R_y', real=True)

def wedge(a,b):
    out = {}
    for p,c in a.items():
      for q,d in b.items():
        pq=p+q
        if len(set(pq)) < len(pq): continue
        sign=(-1)**sum(pq[i]>pq[j] for i in range(len(pq)) for j in range(i+1,len(pq)))
        key=tuple(sorted(pq)); out[key]=s.simplify(out.get(key,0)+sign*c*d)
    return {p:s.simplify(c) for p,c in out.items() if s.simplify(c)!=0}

def plus(a,b):
    return {p:s.simplify(a.get(p,0)+b.get(p,0)) for p in set(a)|set(b) if s.simplify(a.get(p,0)+b.get(p,0))!=0}
def scale(c,a): return {p:s.simplify(c*v) for p,v in a.items() if s.simplify(c*v)!=0}
e=[{(i,):s.S.One} for i in range(4)]
u,v,x,y=e
alpha=plus(wedge(u,x),scale(-1,wedge(v,y)))
beta=plus(wedge(u,y),wedge(v,x))
dr={(0,):ru,(1,):s.Symbol('R_v'),(2,):rx,(3,):ry}
delta=wedge(dr,v)
bp=plus(beta,delta)
V={(0,1,2,3):s.S.One}
assert wedge(alpha,alpha)==scale(2,V)
assert wedge(alpha,bp)==scale(ry,V)
assert wedge(bp,bp)==scale(2*(1-rx),V)
assert plus(wedge(u,alpha),scale(-1,wedge(v,bp)))=={}
D=1-rx-ry**2/4
b0=scale(1/s.sqrt(D),plus(bp,scale(-ry/2,alpha)))
Theta=plus(alpha,scale(s.I,b0))
assert wedge(Theta,Theta)=={}
theta1=plus(u,scale(-ry/2+s.I*s.sqrt(D),v))
theta2=plus(scale(1-s.I*ry/(2*s.sqrt(D)),x),plus(scale(s.I/s.sqrt(D),y),scale(s.I*ru/s.sqrt(D),v)))
assert plus(wedge(theta1,theta2),scale(-1,Theta))=={}
eps,X=s.symbols('epsilon x', real=True)
a=s.sqrt(1-eps*X)
J=s.Matrix([[0,-a,0,0],[1/a,0,0,0],[0,0,0,-1/a],[0,0,a,0]])
assert s.simplify(J*J)==-s.eye(4)
coords=s.symbols('u v x y',real=True)
# x symbol above has same assumptions and identity as coords[2].
def bracket(U,W):
    return s.simplify(s.Matrix([sum(U[j]*s.diff(W[i],coords[j])-W[j]*s.diff(U[i],coords[j]) for j in range(4)) for i in range(4)]))
U=s.eye(4)[:,0]; W=s.eye(4)[:,2]
N=s.simplify(bracket(J*U,J*W)-J*bracket(J*U,W)-J*bracket(U,J*W)-bracket(U,W))
assert s.simplify(N-s.Matrix([-eps/(2*(1-eps*X)),0,0,0]))==s.zeros(4,1)
print('PASS: wedge Gram matrix; closed third form identity; normalized decomposable Theta; explicit general coframe; J^2=-Id; N(partial_u,partial_x)=-epsilon/[2(1-epsilon*x)] partial_u')
