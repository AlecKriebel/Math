"""New exact matrix/scalar checks. Does not import deposited programs or results.
These finite checks diagnose algebra/boundaries; the universal theorem uses the written proof.
"""
import sympy as s,json,time

def zero(a):return all(s.simplify(x)==0 for x in a)
def main():
 start=time.monotonic();I=s.eye(2);ii=s.I
 z=s.diag(1,-1);x=s.Matrix([[0,1],[1,0]])
 U=ii*z;V=ii*x;E=s.Matrix([[1,ii],[2-ii,-1]])
 assert not zero(U*V-V*U)
 cases=0;rejected_order=False
 for t in [s.Rational(0),s.Rational(1,7),s.Rational(1,2),s.Rational(999,1000),s.Rational(1)]:
  q=(1-t*t)/(1+t*t);RU=(I+t*U).inv();RV=(I+t*V).inv();FU=(U+t*I)*RU;FV=(V+t*I)*RV
  assert zero(U.conjugate().T*U-I) and zero(V.conjugate().T*V-I)
  assert zero((I+t*U).conjugate().T*(I+t*U)-(1+t*t)*I)
  assert zero(FU.conjugate().T*FU-I)
  assert zero(FU-FV-(1-t*t)*RU*(U-V)*RV)
  derivative=E*RU-(U+t*I)*RU*t*E*RU;expected=(1-t*t)*RU*E*RU
  assert zero(derivative-expected)
  # On Re U=0 the resolvents are a scalar multiple of unitaries, so both
  # ideal norms attain q times the input norm; HS squared is rational.
  hs_in=s.trace(E.conjugate().T*E);hs_out=s.trace(derivative.conjugate().T*derivative)
  assert s.simplify(hs_out-q*q*hs_in)==0
  if t==0:assert zero(FU-U)
  if t==1:assert zero(FU-I) and zero(derivative)
  if t not in [0,1]:rejected_order|=not zero(FU-FV-(1-t*t)*RU*RV*(U-V))
  assert zero((I+t*I)*(I+t*I).inv()-I)
  cases+=1
 assert rejected_order
 # Independent scalar derivation, with c=cos(theta) in [0,1].
 t,c=s.symbols('t c',nonnegative=True);q=(1-t*t)/(1+t*t);ang=(1-t*t)/(1+t*t+2*t*c)
 assert s.cancel(q-ang-2*t*c*(1-t*t)/((1+t*t)*(1+t*t+2*t*c)))==0
 assert s.cancel(ang.subs(c,0)-q)==0
 assert ang.subs({c:-1,t:s.Rational(1,2)})==3
 assert q.subs(t,s.Rational(1,2))==s.Rational(3,5)
 # The chart relation is an identity in a single matrix; actual nontrivial
 # matrices above have invertible I+W and avoid the omitted eigenvalue -1.
 for W in [U,V]:
  t=s.Rational(1,3);F=(W+t*I)*(I+t*W).inv();C=lambda M:(I-M)*(I+M).inv()
  assert zero(C(F)-(1-t)/(1+t)*C(W))
 # Exact one-matrix composition law supporting time monotonicity.
 for W in [U,V]:
  s0,u=s.Rational(1,4),s.Rational(2,3);v=(s0+u)/(1+s0*u);f=lambda M,a:(M+a*I)*(I+a*M).inv()
  assert zero(f(f(W,s0),u)-f(W,v))
 # Explicit frame equivariance with independently chosen noncommuting frames.
 A=s.Matrix([[0,1],[-1,0]]);Q=s.diag(ii,1);R=s.Matrix([[s.Rational(3,5),s.Rational(4,5)],[-s.Rational(4,5),s.Rational(3,5)]])
 def h(A,W,t):return A*(W+t*I)*(I+t*W).inv()
 for t in [s.Rational(0),s.Rational(2,3),s.Rational(1)]:
  assert zero(h(Q*A*R,R.conjugate().T*U*R,t)-Q*h(A,U,t)*R)
 print(json.dumps({'exact_noncommuting_matrix_time_cases':cases,'actual_inverses_unitarity_difference_and_derivative':True,'HS_squared_boundary_factor_exact':True,'wrong_resolvent_order_rejected':bool(rejected_order),'scalar_angle_factor_identity':True,'scalar_semicircle_boundary_equality':True,'outside_semicircle_factor_three_vs_three_fifths':True,'classical_Cayley_scaling':True,'frame_equivariance':True,'time_composition_law':True,'finite_diagnostics_not_universal_proof':True,'seconds':time.monotonic()-start},indent=2))
if __name__=='__main__':main()
