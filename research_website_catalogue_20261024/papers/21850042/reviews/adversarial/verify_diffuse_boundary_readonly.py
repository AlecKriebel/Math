#!/usr/bin/env python3
"""Exact adversarial boundary witness, no source imports, no writes.
This refutes the stated uniform fast-blade error estimate under the detailed
source note's growing-type assumptions; it does not refute the no-overlap conclusion.
"""
import json
import sympy as S
K,r=S.symbols('K r',positive=True)
s=K**2; Q=K
lam_hi=K; lam_lo=K/(K-1); pi_hi=1/K; pi_lo=(K-1)/K
B=S.factor(2*(pi_hi*lam_hi+pi_lo*lam_lo)); H=S.Integer(1)
assert B==4
# Each high-blade endpoint has total portal edge weight exactly one.
outer_hi=S.factor(Q*lam_hi/s); outer_lo=S.factor(Q*lam_lo/s)
assert outer_hi==1
# All residents except one mutant endpoint of a high blade.
# dB: rates in common n-time units, with labelled outer parent event retained.
db_outer_erase=S.Rational(1,2)
db_internal_neighbor_up=r/(r+1)
db_mutant_portal_birth=r/(B+H+(r-1)/K)
db_first_outer=S.factor(db_outer_erase/(1+db_internal_neighbor_up+db_mutant_portal_birth))
db_limit=S.factor(S.limit(db_first_outer,K,S.oo))
assert S.factor(db_limit.subs(r,S.Rational(3,2))-S.Rational(5,19))==0
# Bd: rates after deleting common F denominator. Source endpoint degree is2,
# and every resident portal has degree B+H=5.
bd_outer_erase=S.Rational(1,5)
bd_internal_erase=S.Rational(1,2)
bd_mutant_birth=r
bd_first_outer=S.factor(bd_outer_erase/(bd_outer_erase+bd_internal_erase+bd_mutant_birth))
assert S.factor(bd_first_outer.subs(r,S.Rational(3,2))-S.Rational(1,11))==0
# A single mutant portal, every blade resident: dB raw introduction rates,
# before any isolated-success mark, on the same n-time scale as source Eq(9).
raw_hi=2*r/(2+(r-1)/K)
raw_lo=2*r/(1+1/(K-1)+(r-1)/(K*(K-1)))
assert S.factor(S.limit(raw_hi+raw_lo,K,S.oo)-3*r)==0
assert S.factor(S.limit(raw_hi/(raw_hi+raw_lo),K,S.oo)-S.Rational(1,3))==0
# Expected source child-type weights are f_hi=2*pi_hi*lambda_hi/B=1/2.
f_hi=S.factor(2*pi_hi*lam_hi/B); assert f_hi==S.Rational(1,2)
# Independent finite literal-graph controls of the closed event formulas.
# These controls test formula transcription; the all-K contradiction above is symbolic.
from fractions import Fraction as F
finite_controls=[]
for kval in (2,3,5):
    count=2*kval*kval+kval
    graph=[{} for _ in range(count)]
    def edge(u,v,w):graph[u][v]=w;graph[v][u]=w
    for u in range(kval):
        for v in range(u+1,kval):edge(u,v,F(1,kval-1))
    for jval in range(kval*kval):
        u=kval+2*jval;v=u+1;edge(u,v,F(1))
        weight=F(1,kval) if jval<kval else F(1,kval*(kval-1))
        for portal in range(kval):edge(portal,u,weight);edge(portal,v,weight)
    assert all(sum(graph[p].values())==5 for p in range(kval))
    rval=F(3,2);initial=kval
    for rule in ('Bd','dB'):
        fit=[rval if u==initial else F(1) for u in range(count)]
        total=F(0);outer_erasure=F(0)
        for parent in range(count):
            for target,weight in graph[parent].items():
                if (parent==initial)==(target==initial):continue
                denominator=sum(graph[parent].values()) if rule=='Bd' else sum(fit[x]*w for x,w in graph[target].items())
                rate=fit[parent]*weight/denominator
                total+=rate
                if target==initial and parent<kval:outer_erasure+=rate
        expr=bd_first_outer if rule=='Bd' else db_first_outer
        value=S.factor(expr.subs({K:kval,r:S.Rational(3,2)}))
        assert outer_erasure/total==F(int(value.p),int(value.q))
        finite_controls.append({'K':kval,'rule':rule,'first_outer_erasure_probability':str(outer_erasure/total)})
    fit=[rval if u==0 else F(1) for u in range(count)]
    rates=[F(0),F(0)]
    for target in range(kval,count):
        den=sum(fit[x]*w for x,w in graph[target].items())
        value=rval*graph[target][0]/den
        rates[0 if (target-kval)//2<kval else 1]+=value
    for actual,expr in zip(rates,(raw_hi,raw_lo)):
        value=S.factor(expr.subs({K:kval,r:S.Rational(3,2)}));assert actual==F(int(value.p),int(value.q))
print(json.dumps({'status':'EXACT_BOUNDARY_WITNESS','integer_domain':'K>=2; r>1 fixed','construction':{'s':'K^2','Q':'K','high_blades':'K','high_lambda':'K','low_blades':'K(K-1)','low_lambda':'K/(K-1)','optional_growing_type_labels':'split low blades into K types of K-1 blades each, all with the same lambda','B':str(B),'H':str(H),'portal_edge':'1/(K-1)','high_endpoint_outer_degree':str(outer_hi),'low_endpoint_outer_degree':str(outer_lo)},'assumption_limits':{'Q/s':'1/K -> 0','max_lambda/s':'1/K -> 0','max_portal_edge':'1/(K-1) -> 0','Q_lambda_high/s':'1'},'dB_probability_first_typechange_is_outer_erasure':str(db_first_outer),'dB_probability_limit_at_r_3halves':'5/19','Bd_probability_first_typechange_is_outer_erasure':str(bd_first_outer),'Bd_probability_at_r_3halves':'1/11','single_mutant_portal_dB_raw_introduction_limit':'3*r, versus claimed dilute-blade 4*r','actual_high_blade_raw_target_fraction_limit':'1/3','source_size_biased_high_blade_fraction':str(f_hi),'finite_literal_graph_controls':finite_controls,'scope':'contradiction of vanishing fast-blade intervention and uniform stopped-trace derivation; not a counterexample to final no-overlap conclusion'},indent=2))
