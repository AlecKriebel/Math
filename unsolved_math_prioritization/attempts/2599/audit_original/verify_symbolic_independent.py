#!/usr/bin/env python3
"""Independent generic identities for KOU-21.90 using spectral interpolation.

This supplementary check uses SymPy. The finite sieve and nonexistence
certificates in verify_independent.py require only the standard library.
"""
import json
from pathlib import Path
import sympy as s

checks=[]
def equal(x,y,label):
    if s.factor(x-y)!=0: raise AssertionError(label)
    checks.append(label)

# Generic distance algebra; the claimed fusion equalities follow without
# assuming the final three-parameter form.
k,b,c,d,e,x=s.symbols('k b c d e x')
L=s.zeros(4)
beta=[k,b,d,0];gamma=[0,1,c,e]
for j in range(4):
    L[j,j]=k-beta[j]-gamma[j]
    if j>0: L[j-1,j]=beta[j-1]
    if j<3: L[j+1,j]=gamma[j+1]
M=[s.eye(4),L]
for j in (1,2):
    M.append(((L-(k-beta[j]-gamma[j])*s.eye(4))*M[j]-beta[j-1]*M[j-1])/gamma[j+1])
# p_ii^h is column i of the multiplication matrix M_i.
equal(M[3][1,3]-M[3][2,3],-d*(d+e-k-1)/c,'first_fusion_identity')
equal((M[2][1,2]-M[2][3,2]).subs(d,k+1-e),-(b*(c+1)-c*e)/c,'second_fusion_identity')
t,c,a=s.symbols('t c a',positive=True)
k=t*(c+1)+a
L=L.subs({s.Symbol('k'):k,s.Symbol('b'):t*c,s.Symbol('c'):c,s.Symbol('d'):a+1,s.Symbol('e'):t*(c+1)})
theta=[k,a+t,-1,-c-1]
equal(L.charpoly(x).as_expr(),s.prod(x-u for u in theta),'characteristic_polynomial')
valencies=[s.Integer(1),k,t*k,k*(a+1)/(c+1)]
v=s.factor(sum(valencies))
equal(v,(k+1)*(k+c+1)/(c+1),'order_formula')
P=s.zeros(4);Q=s.zeros(4)
for j,th in enumerate(theta):
    values=[s.Integer(1),th]
    values.append(s.factor((th*th-(a+t-1)*th-k)/c))
    values.append(s.factor(((th-(t-1)*(c+1))*values[2]-t*c*th)/(t*(c+1))))
    for r in range(4): P[j,r]=values[r]
    vec=s.Matrix([1,0,0,0])
    for other in theta:
        if other!=th: vec=((L-other*s.eye(4))*vec/(th-other)).applyfunc(s.factor)
    for r in range(4): Q[r,j]=s.factor(v*vec[r])
expected=s.Matrix([[1,k,t*k,k*(a+1)/(c+1)],[1,a+t,-t,-a-1],[1,-1,-t,t],[1,-c-1,a+c+1,-a-1]])
for j in range(4):
    for r in range(4): equal(P[j,r],expected[j,r],f'eigenmatrix_{j}_{r}')
for j in range(4):
    for r in range(4): equal((P*Q)[j,r],v*int(j==r),f'projector_orthogonality_{j}_{r}')
D=(c+1)*(t*t-a-1)-a*(a+1)
H=(c+1)*(a+t+1)**2*(a+c+t+1)**2
expectations=[(1,2,c*t*(k+1)*(k+c+1)*(2*a+c*t+c+2*t+2)/H),
(1,3,c*(k+1)*(k+c+1)*D/H),
(2,1,a*(a+1)*(k+1)*(k+c+1)/((c+1)*(a+t+1)**2)),
(2,3,a*(a+1)*(k+1)*(k+c+1)/((c+1)*(a+t+1)**2)),
(3,1,t*(t-1)*(k+1)*(k+c+1)/((c+1)*(a+c+t+1)**2)),
(3,2,t*(t-1)*(k+1)*(k+c+1)/((c+1)*(a+c+t+1)**2))]
for i,h,formula in expectations:
    equal(sum(Q[r,i]**2*P[h,r] for r in range(4))/v,formula,f'Krein_{i}_{i}_{h}')
for h in (1,2):
    equal(sum(P[j,3]**2*Q[h,j] for j in range(4))/v,a*(a+1)/(c+1),f'distance_three_mu_h{h}')
equal(sum(P[j,3]**2*Q[3,j] for j in range(4))/v,a*(a+1)/(c+1)+t-a-1,'distance_three_lambda')
# Additional connectedness check for the nondegenerate parameter regime.
mu2=s.factor(sum(P[j,2]**2*Q[1,j] for j in range(4))/v)
equal(mu2,t*(c+1)*(t-1),'distance_two_mu')
result={'status':'PASS','sympy_version':s.__version__,'symbolic_identities':checks,'identity_count':len(checks),'distance_two_mu':str(mu2),'method':'Intersection recurrence, characteristic polynomial, and Lagrange spectral projectors; no eigenmatrix inverse and no imported author code.'}
Path(__file__).with_name('SYMBOLIC_AUDIT_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps(result,indent=2))
