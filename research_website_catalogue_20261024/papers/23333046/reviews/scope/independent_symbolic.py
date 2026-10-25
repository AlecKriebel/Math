"""Own independent polynomial controls; not a finite-series proof substitute."""
import sympy as s,json
t,y,u,e,H=s.symbols('t y u e H')
def red2(expr,variables):
 n=s.fraction(s.cancel(expr))[0];return s.Poly(n,*variables,modulus=2).as_expr()
def red_e(expr):return s.rem(s.Poly(s.expand(expr),e,modulus=2),s.Poly(e**3,e,modulus=2)).as_expr()
def require(x,label):
 if not x:raise RuntimeError(label)
q=t**2/(1+t);rho_u=t/(1+u*t)
actual=s.together(q.subs(t,rho_u)-q/(1+q));n=s.fraction(actual)[0]
remainder=s.groebner([u**2+u+1],u,t,modulus=2).reduce(n)[1]
require(remainder==0,'F4 induced quotient')
sigma=y/(1+y)
def T(f):return (1+y)**2*f.subs(y,sigma)
require(red2(T(y*H)-y*H-y**2*H,(y,H))==0,'arbitrary invariant coefficient coboundary')
require(red2(T(y**2*H)-y**2*H,(y,H))==0,'arbitrary invariant coefficient fixedness')
require(red2(T(1+y)-(1+y),(y,))==0,'enlarged module nonzero constant invariant')
M=s.Matrix([[1,e],[1,1]]);C=s.Matrix([[1+e,e],[0,1]]);Mp=M.subs(e,e+e**2)
conj=Mp*C-(1+e)*C*M
require(all(red_e(v)==0 for v in conj),'exact projective conjugacy')
require(all(red_e(v)==0 for v in M*M-(1+e)*s.eye(2)),'exact involution')
no_scalar=[str(red_e(v)) for v in Mp*C-C*M]
require(any(v!='0' for v in no_scalar),'omitted scalar negative control')
wrong_weight=red2((1+y)*(y/(1+y))-y-y**2,(y,));require(wrong_weight!=0,'wrong derivation weight negative')
wrong_module=red2((1+y).subs(y,0),(y,));require(wrong_module==1,'full module invariant has forbidden constant')
odd=[str(s.Poly(v,e,modulus=3).as_expr()) for v in M*M-(1+e)*s.eye(2)]
require(any(v!='0' for v in odd),'odd characteristic is outside this involution mechanism')
print(json.dumps({'status':'PASS','independent_of_supplied_arithmetic':True,'quotient_numerator_mod_u2_u_1_GF2':str(remainder),'coboundary_with_arbitrary_fixed_H':0,'invariant_with_arbitrary_fixed_H':0,'enlarged_module_invariant':'1+y has constant1, fixed by T, hence cannot be a coboundary since all (T-1)h have constant0','conjugacy_and_involution_remainders':[str(red_e(v)) for v in conj],'negative_omitted_scalar_remainders':no_scalar,'negative_wrong_weight_remainder':str(wrong_weight),'negative_odd_characteristic_involution_remainders':odd,'limitation':'Full-series fixed-field/valuation and all-natural-map argument are separate written proofs in INITIAL_CLAIMS.md; this programme verifies exact algebraic identities and controls.'},indent=2))
