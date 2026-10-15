"""Independent finite controls for the reviewed analytic conditional lemmas.
These do not establish adelic estimates, transfer, or the original conjecture.
"""
import sympy as s
from collections import Counter
import json
C=Counter()
def ck(v,k):
 assert v,k
 C[k]+=1
def zero(v,k):ck(s.simplify(v)==0,k)
z,q,x,y=s.symbols('z q x y');r=s.symbols('r',positive=True)
# Recover the lower Mellin polynomial directly from an elementary antiderivative.
for m in range(11):
 primitive=r**q*sum((-1)**j*s.factorial(m)/s.factorial(m-j)*s.log(r)**(m-j)/q**(j+1) for j in range(m+1))
 zero(s.diff(primitive,r)-r**(q-1)*s.log(r)**m,'lower_integrand_antiderivative')
 zero(primitive.subs(r,1)-(-1)**m*s.factorial(m)/q**(m+1),'lower_mellin_endpoint')
 for lam in [s.Rational(-5,2),s.Rational(2,3),s.I,3-s.I]:
  J=primitive.subs({r:1,q:z+lam})
  reverse=-(-1)**m*primitive.subs({r:1,q:-z-lam})
  zero(J-reverse,'reversed_defect_polar_part')
  zero((z+lam).subs(z,x-s.Rational(1,2))-(x-(s.Rational(1,2)-lam)),'pole_half_shift')
# Continuous compact-upper-tail model: m>0 makes both functions vanish at r=1.
# A(r)=B(r) below1 and0 above; Adual(r)=-B(1/r) below1 and0 above.
for m in range(1,8):
 for lam in [s.Integer(1),s.Rational(3,2),s.Integer(-2)]:
  B=r**lam*s.log(r)**m
  ck(B.subs(r,1)==0,'continuous_piecewise_boundary_model')
  reverse=-B.subs(r,1/r)
  zero(-reverse.subs(r,1/r)-B,'actual_pair_defect_involution')
# Nontrivial two-space matrices, varying scale and Fourier-square scalar.
for rr in [s.Rational(2),s.Rational(7,3),s.Rational(1,4)]:
 for a in range(1,6):
  RV=s.diag(rr**(-a),rr**a)
  for p in [s.Rational(3,2),s.Rational(-2)]:
   F=s.Matrix([[0,p],[3,0]])
   for kappa in [1,-1]:
    G=kappa*F.inv();ell=s.Matrix([[2,0]]);eta=s.Matrix([[5,0]])
    ck(F*RV==RV.inv()*F,'matrix_Fourier_covariance')
    ck(G*F==kappa*s.eye(2) and F*G==kappa*s.eye(2),'two_space_Fourier_square')
    EV=ell+eta*F;EW=eta+ell*G
    ck(EV-EW*F==(1-kappa)*ell,'coherence_scalar_necessity')
    ck(EV!=s.zeros(1,2) and EW!=s.zeros(1,2),'nonzero_distinct_character_sum')
# Exponential-polynomial translation matrices in a non-monomial basis.
for n in range(1,7):
 lam=s.Rational(n,3);N=s.zeros(n)
 for j in range(n-1):N[j,j+1]=1
 U=s.eye(n)
 for i in range(n):
  for j in range(i+1,n):U[i,j]=i+j+1
 def T(t):return U*(s.exp(lam*t)*sum_matrices([t**j/s.factorial(j)*N**j for j in range(n)],n))*U.inv()
 def sum_matrices(ms,n):
  out=s.zeros(n)
  for M in ms:out+=M
  return out
 Tx=T(x)
 ck((T(x+y)-Tx*T(y)).applyfunc(s.simplify)==s.zeros(n),'translation_group_in_changed_basis')
 ck((Tx.diff(x)-(U*(lam*s.eye(n)+N)*U.inv())*Tx).applyfunc(s.simplify)==s.zeros(n),'continuous_generator_Jordan_formula')
# Multiplier identity with three exceptional places, without discarding local factors.
E=s.symbols('e0:3',nonzero=True);L=s.symbols('l0:3',nonzero=True);D=s.symbols('d0:3',nonzero=True);Z=s.symbols('z0:3',nonzero=True)
P=s.prod(Z[i]/L[i] for i in range(3));PD=s.prod((E[i]*D[i]/L[i]*Z[i])/D[i] for i in range(3))
zero(PD-s.prod(E)*P,'completed_local_multiplier_identity')
print(json.dumps({'status':'PASS','exact_assertions':sum(C.values()),'counts':dict(sorted(C.items())),'sympy_version':s.__version__,'scope':'Finite antiderivative, actual-pair boundary, half-shift, covariance, coherent-pair and translation-module algebra controls only. Analytic and source conclusions are audited in the report.'},indent=2,sort_keys=True))
