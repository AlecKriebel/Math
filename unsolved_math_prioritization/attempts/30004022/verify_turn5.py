#!/usr/bin/env python3
"""Exact clipping/rank/Cauchy controls; finite matrices are not assumed free."""
import sympy as s
import json
from collections import Counter
from fractions import Fraction as F
C=Counter()
def ck(g,v):
    if not v:raise AssertionError(g)
    C[g]+=1
I=s.I
def clip(x,T):return max(-T,min(x,T))
cases=0;nontrivial=0
families=[
    ([-5,-1,0,1,2,3],[-1,s.Rational(-1,2),0,s.Rational(1,2),1,2]),
    ([-3,-1,1,3],[-4,0,1,5]),
    ([0,1,2,3],[2,2,2,2]),
]
for av,bv in families:
    d=len(av);E=s.eye(d);V=s.ones(d,1);Q=E-2*(V*V.T)/(V.T*V)[0]
    ck('rational_orthogonal_change',Q.T*Q==E)
    A=s.diag(*av);B=Q*s.diag(*bv)*Q.T;Cc=I*(A*B-B*A)
    ck('original_commutator_selfadjoint',Cc.H==Cc)
    for T in [s.Rational(1),s.Rational(2),s.Rational(3),s.Rational(6)]:
        AT=s.diag(*[clip(x,T) for x in av]);BT=Q*s.diag(*[clip(x,T) for x in bv])*Q.T
        CT=I*(AT*BT-BT*AT);D=Cc-CT
        qa=s.Rational(sum(int(bool(abs(x)>T)) for x in av),d);qb=s.Rational(sum(int(bool(abs(x)>T)) for x in bv),d)
        delta=min(1,2*(qa+qb));actual=s.Rational(D.rank(),d)
        ck('strict_tail_a_equals_rank',s.Rational((A-AT).rank(),d)==qa)
        ck('strict_tail_b_equals_rank',s.Rational((B-BT).rank(),d)==qb)
        ck('commutator_difference_identity',D==I*((A-AT)*B-B*(A-AT)+AT*(B-BT)-(B-BT)*AT))
        ck('tail_rank_bound',actual<=delta)
        if 0<delta<1:nontrivial+=1
        for z in [I,s.Rational(1,2)+2*I,-2+s.Rational(1,3)*I]:
            cases+=1;eta=s.im(z);R=(z*E-Cc).inv();RT=(z*E-CT).inv();Diff=s.simplify(R-RT)
            ck('exact_resolvent_identity',s.simplify(Diff-R*D*RT)==s.zeros(d))
            ck('resolvent_rank_bound',s.Rational(Diff.rank(),d)<=actual)
            value=s.simplify(s.trace(Diff)/d);norm2=s.simplify(value*s.conjugate(value))
            ck('exact_cauchy_tail_bound',norm2<=(2*delta/eta)**2)
            ck('sharper_actual_rank_bound',norm2<=(2*actual/eta)**2)
            if delta==0:ck('compact_boundary_exact',value==0)
ck('nontrivial_rank_controls_present',nontrivial>0)
for T in range(1,101):
    epsilon=F(1,T**3)
    for eta in [F(1,5),F(1),F(3)]:
        err=2*T*T*(epsilon*epsilon+epsilon)/((1+epsilon*epsilon)*eta*eta)
        upper=2*(F(1,T**4)+F(1,T))/(eta*eta)
        ck('exact_one_parameter_schedule',0<err<=upper)
    ck('threshold_atoms_unchanged',clip(F(T),F(T))==T and clip(F(-T),F(T))==-T)
z=s.symbols('T',positive=True)
ck('schedule_limit',s.limit(2*(z**-4+z**-1),z,s.oo)==0)
print(json.dumps({'problem_id':30004022,'turn':5,'status':'PASS','counts':dict(sorted(C.items())),
    'exact_assertions':sum(C.values()),'exact_matrix_resolvent_cases':cases,'nontrivial_tail_rank_controls':nontrivial,
    'arithmetic':'exact rational matrices and symbolic identities; no floats',
    'scope':'Deterministic finite controls supplement the affiliated-operator rank proof and credited matrix subordination theorem. No matrix freeness, density convergence or finite fixed-point stopping bound is claimed. Original source target remains unresolved.'},indent=2,sort_keys=True))
