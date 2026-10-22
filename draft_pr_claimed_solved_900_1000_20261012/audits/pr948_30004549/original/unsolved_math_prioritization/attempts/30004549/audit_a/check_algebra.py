from itertools import permutations
import sympy as s

# Coordinates u,v,x,y; sparse alternating forms use ascending tuple keys.
def wedge(a,b):
    c={}
    for I,av in a.items():
        for J,bv in b.items():
            seq=I+J
            if len(set(seq)) != len(seq): continue
            inv=sum(seq[i]>seq[j] for i in range(len(seq)) for j in range(i+1,len(seq)))
            key=tuple(sorted(seq))
            c[key]=c.get(key,0)+(-1)**inv*av*bv
    return {I:s.simplify(v) for I,v in c.items() if s.simplify(v)!=0}
def add(a,b):
    return {I:s.simplify(a.get(I,0)+b.get(I,0)) for I in set(a)|set(b) if s.simplify(a.get(I,0)+b.get(I,0))!=0}
def scale(c,a): return {I:s.simplify(c*v) for I,v in a.items()}
V=(0,1,2,3)
p,q,r=s.symbols('p q r', real=True)
D=1-q-r*r/4
alpha={(0,2):1,(1,3):-1}
beta={(0,3):1,(1,2):1-q,(0,1):p,(1,3):-r}
assert wedge(alpha,alpha)=={V:2}
assert wedge(beta,beta)=={V:2*(1-q)}
assert wedge(alpha,beta)=={V:r}
eta=add(beta,scale(-r/2,alpha))
assert wedge(alpha,eta)=={}
assert s.simplify(wedge(eta,eta)[V]-2*D)==0
# Complex canonical form uses D>0; its conjugate is supplied explicitly.
O=add(alpha,scale(s.I/s.sqrt(D),eta))
Ob=add(alpha,scale(-s.I/s.sqrt(D),eta))
assert wedge(O,O)=={}
assert wedge(O,Ob)=={V:4}
print('PASS general cutoff: alpha^2=2vol; beta^2=2(1-R_x)vol; alpha beta=R_y vol')
print('PASS normalized canonical form: O^2=0; O conjugate(O)=4vol')

u,v,x,y,eps=s.symbols('u v x y eps', real=True)
k=1-eps*x
c=s.sqrt(k)
coords=(u,v,x,y)
J=s.Matrix([[0,-c,0,0],[1/c,0,0,0],[0,0,0,-1/c],[0,0,c,0]])
assert s.simplify(J*J)==-s.eye(4)
A=s.zeros(4); B=s.zeros(4)
for (i,j),value in alpha.items(): A[i,j]=value; A[j,i]=-value
bcore={(0,3):1,(1,2):k}
for (i,j),value in bcore.items(): B[i,j]=value; B[j,i]=-value
assert s.simplify(J.T*A*J+A)==s.zeros(4)
assert s.simplify(J.T*B*J+B)==s.zeros(4)
def bracket(X,Y):
    return s.Matrix([s.simplify(sum(X[j]*s.diff(Y[i],coords[j])-Y[j]*s.diff(X[i],coords[j]) for j in range(4))) for i in range(4)])
e=[s.eye(4)[:,i] for i in range(4)]
N=bracket(J*e[0],J*e[2])-J*bracket(J*e[0],e[2])-J*bracket(e[0],J*e[2])-bracket(e[0],e[2])
assert s.simplify(N-s.Matrix([-eps/(2*k),0,0,0]))==s.zeros(4,1)
print('PASS core J^2=-I and J-anti-invariance of alpha,beta')
print('PASS core N_J(partial_u,partial_x)=-eps/(2(1-eps*x)) partial_u')
