"""Independent symbolic sanity checks, not substitutes for the geometric proofs."""
import json
import sympy as s

x,y,r=s.symbols('x y r', real=True)
f=s.Function('f')(x)
a=s.Function('a')(x)
coords=(x,y,r)
g=s.Matrix([[1,0,0],[0,1+f**2*a**2,f**2*a],[0,f**2*a,f**2]])
gi=s.simplify(g.inv())
n=3
Gamma=[[[s.simplify(sum(gi[k,l]*(s.diff(g[l,j],coords[i])+s.diff(g[l,i],coords[j])-s.diff(g[i,j],coords[l])) for l in range(n))/2) for j in range(n)] for i in range(n)] for k in range(n)]
Ric=s.zeros(n)
for i in range(n):
 for j in range(n):
  Ric[i,j]=s.simplify(sum(s.diff(Gamma[k][i][j],coords[k])-s.diff(Gamma[k][i][k],coords[j])+sum(Gamma[k][k][l]*Gamma[l][i][j]-Gamma[k][j][l]*Gamma[l][i][k] for l in range(n)) for k in range(n)))
scalar=s.simplify(sum(gi[i,j]*Ric[i,j] for i in range(n) for j in range(n)))
expected=-2*s.diff(f,x,2)/f-f**2*s.diff(a,x)**2/2
if s.simplify(scalar-expected)!=0: raise RuntimeError('Kaluza-Klein identity failed')
# m=2: quotient metric f^2 (dx^2+dy^2), so normalized scalar is -2(log f)''.
quotient_scaled=-2*s.diff(s.log(f),x,2)
positive_rhs=scalar+f**2*s.diff(a,x)**2/2+2*(s.diff(f,x)/f)**2
if s.simplify(quotient_scaled-positive_rhs)!=0: raise RuntimeError('quotient conformal identity failed')
m=s.symbols('m', positive=True)
c=s.simplify(2-(m-2)/(m-1))
if s.simplify(c-m/(m-1))!=0: raise RuntimeError('dimension coefficient failed')
# Cylinder formula tested on a general warped product with n-dimensional slices.
t=s.symbols('t', real=True)
w=s.Function('w')(t)
d=s.symbols('d', positive=True)
A2=4*d*(s.diff(w,t)/w)**2
trA2=4*d**2*(s.diff(w,t)/w)**2
tr_dd=2*d*(s.diff(w,t,2)/w+(s.diff(w,t)/w)**2)
cylinder_correction=s.simplify(s.Rational(3,4)*A2-s.Rational(1,4)*trA2-tr_dd)
warped_correction=-2*d*s.diff(w,t,2)/w-d*(d-1)*(s.diff(w,t)/w)**2
if s.simplify(cylinder_correction-warped_correction)!=0: raise RuntimeError('long-cylinder identity failed')
result={
 'status':'PASS',
 'checks':[
  'Full coordinate Ricci contraction for f(x)^2(dr+a(x)dy)^2+dx^2+dy^2',
  'Conformal quotient identity in quotient dimension 2',
  'Positive gradient coefficient m/(m-1)',
  'Long-cylinder scalar formula agrees with general warped-product formula'
 ],
 'limitations':'Symbolic consistency checks only. General geometric identities and boundary arguments are proved in the authored report.'
}
print(json.dumps(result,indent=2))
