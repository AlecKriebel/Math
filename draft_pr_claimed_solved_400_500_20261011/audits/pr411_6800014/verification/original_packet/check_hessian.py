"""Exact symbolic second variation for an almost-abelian Ricci pinching candidate.
No numerical approximation is used in the assertions.
"""
import sympy as sp
u=sp.symbols('u', positive=True)
b=sp.symbols('b11 b12 b13 b14 b22 b23 b24 b33 b34 b44',real=True)
b11,b12,b13,b14,b22,b23,b24,b33,b34,b44=b
A=sp.Matrix([[0,-1,0,0],[1,0,0,0],[0,0,0,u],[0,0,0,0]])
B=sp.Matrix([[b11,b12,b13,b14],[b12,b22,b23,b24],[b13,b23,b33,b34],[b14,b24,b34,b44]])
def comm(X,Y): return X*Y-Y*X
def inner(X,Y):return sp.trace(X*Y.T)
def sym(X):return (X+X.T)/2
V=comm(B,A); W=comm(B,V)
S=sym(A); U=sym(V); T=sym(W)
s=inner(S,S); sd=2*inner(S,U); sdd=2*inner(U,U)+2*inner(S,T)
K=comm(A,A.T); Kd=comm(V,A.T)+comm(A,V.T)
Kdd=comm(W,A.T)+2*comm(V,V.T)+comm(A,W.T)
q=inner(K,K); qd=2*inner(K,Kd); qdd=2*inner(Kd,Kd)+2*inner(K,Kdd)
Rd=sp.factor(qd/s**2-2*q*sd/s**3)
Rdd=sp.factor(qdd/s**2-4*qd*sd/s**3-2*q*sdd/s**3+6*q*sd**2/s**4)
print('R=q/s^2 =',sp.factor(q/s**2)); print('R prime =',Rd)
print('R second =',Rdd)
print('Hessian coefficients =',sp.factor(Rdd*u**4/128))
assert Rd == 0
expected=64/u**4*((4-2*u*u)*((b11-b22)**2+4*b12**2)+(b13*b13+b14*b14+b23*b23+b24*b24)+4*u*(b13*b24-b14*b23))
assert sp.factor(Rdd-expected)==0
print('Expected identity verified exactly.')
H=sp.hessian(Rdd,b)/2
print('Hessian eigenvalues =',H.eigenvals())
