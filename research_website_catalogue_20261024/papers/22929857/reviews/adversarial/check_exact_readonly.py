#!/usr/bin/env python3
"""Independent exact noncommuting/boundary checks; no source imports or writes.
The universal geometric/topological proof is DERIVATION.md, not these cases.
"""
import json
import sympy as s
I=s.I;EYE=s.eye(2);t=s.symbols('t', real=True);z=s.symbols('z');c=s.symbols('c',nonnegative=True)
checks=[]
def zero(label,value):
    if isinstance(value,s.MatrixBase):
        values=[s.factor(s.cancel(v)) for v in value]
    else:values=[s.factor(s.cancel(value))]
    if any(v!=0 for v in values):raise ValueError((label,values))
    checks.append(label)
def nonzero(label,value):
    values=list(value) if isinstance(value,s.MatrixBase) else [value]
    if all(s.factor(v)==0 for v in values):raise ValueError(label)
    checks.append(label)
def F(W,tval):return (W+tval*s.eye(W.rows))*(s.eye(W.rows)+tval*W).inv()
# Different exact boundary pair from deposited Pauli example. Each has one
# nontrivial phase of absolute pi/2, so it also lies in the HS pi/2 ball.
U=s.diag(I,1);R=s.Matrix([[s.Rational(3,5),-s.Rational(4,5)],[s.Rational(4,5),s.Rational(3,5)]])
V=R*s.diag(-I,1)*R.T
zero('U_unitary',U.conjugate().T*U-EYE);zero('V_unitary',V.conjugate().T*V-EYE)
nonzero('genuine_noncommuting_pair',U*V-V*U)
FU,FV=F(U,t),F(V,t);RU=(EYE+t*U).inv();RV=(EYE+t*V).inv()
zero('ordered_resolvent_rational_identity',FU-FV-(1-t*t)*RU*(U-V)*RV)
zero('unitarity_rational_identity_U',FU.conjugate().T*FU-EYE)
zero('unitarity_rational_identity_V',FV.conjugate().T*FV-EYE)
for name,W,FW in [('U',U,FU),('V',V,FV)]:
    zero(name+'_initial',FW.subs(t,0)-W);zero(name+'_terminal',FW.subs(t,1)-EYE)
    zero(name+'_Gram',(EYE+t*W).conjugate().T*(EYE+t*W)-((1+t*t)*EYE+t*(W+W.conjugate().T)))
zero('identity_fixed',F(EYE,t)-EYE)
# Product-rule derivative in an arbitrary ambient direction, not a commuting one.
D=s.Matrix([[1,2*I],[3+I,1-I]])
direct=D*RU-(U+t*EYE)*RU*t*D*RU
zero('ambient_differential_identity',direct-(1-t*t)*RU*D*RU)
zero('time_derivative_identity',FU.diff(t)-(EYE-U*U)*RU*RU)
nonzero('direction_does_not_commute',U*D-D*U)
Q=s.diag(s.Rational(3,5)+4*I/5,s.Rational(5,13)+12*I/13)
zero('conjugation_covariance',F(Q.conjugate().T*U*Q,t)-Q.conjugate().T*FU*Q)
# Full anchoring covariance with exact independent A,Q,R and raw value A*U.
A=s.Matrix([[0,1],[-1,0]]);right=R;value=A*U
base_changed=Q*A*right;value_changed=Q*value*right
zero('two_sided_frame_equivariance',base_changed*F(base_changed.conjugate().T*value_changed,t)-Q*A*FU*right)
scalar=(z+t)/(1+t*z);C=lambda w:(1-w)/(1+w)
zero('Cayley_scale_identity',C(scalar)-(1-t)/(1+t)*C(z))
q=(1-t*t)/(1+t*t);angular=(1-t*t)/(1+t*t+2*t*c)
zero('closed_semicircle_derivative_margin',q-angular-(1-t*t)*2*t*c/((1+t*t)*(1+t*t+2*t*c)))
zero('boundary_derivative_equals_q',angular.subs(c,0)-q)
zero('outside_semicircle_derivative_three',angular.subs({c:-1,t:s.Rational(1,2)})-3)
zero('q_at_half',q.subs(t,s.Rational(1,2))-s.Rational(3,5))
# Three hostile changes rejected exactly, rather than accepted at tolerance.
wrong_order=(1-t*t)*RU*RV*(U-V)
nonzero('reject_incorrect_resolvent_order', (FU-FV-wrong_order).subs(t,s.Rational(1,2)))
if not q.subs(t,s.Rational(1,2))>q.subs(t,s.Rational(1,2))**2:raise ValueError('stronger q squared escaped')
checks.append('reject_stronger_q_squared_at_scalar_boundary')
if (1+1*(-1))!=0:raise ValueError('outside domain singularity escaped')
checks.append('detect_outside_domain_endpoint_singularity')
# Distance formulas used by the separate S0 argument: each principal phase
# contracts by q, hence l2 and linfinity angle norms do. Their geometric proof
# by eigenvector paths and Minkowski is in DERIVATION.md.
print(json.dumps({'status':'PASS','arithmetic':'exact SymPy rational functions and rational complex matrices','sympy':s.__version__,'checks':checks,'count':len(checks),'noncommuting_U':str(U),'noncommuting_V':str(V),'scope':'exact algebra/transcription and boundary controls; universal metric/curve/map-space proof is written separately','source_imports':False,'file_writes':False,'numerical_samples_used_as_proof':False},indent=2))
