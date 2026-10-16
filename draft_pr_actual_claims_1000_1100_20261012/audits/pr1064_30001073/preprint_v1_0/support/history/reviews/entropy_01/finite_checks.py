#!/usr/bin/env python3
"""Fresh finite corroboration, not a universal proof or historical replay.
Exact rational probabilities/support, Decimal logs at stated precision.
"""
from collections import defaultdict
from decimal import Decimal, getcontext
from fractions import Fraction as F
from itertools import permutations, product
from pathlib import Path
import datetime, hashlib, json, platform, sys

getcontext().prec = 120
TOL = Decimal('1e-95')
ZERO = Decimal(0)
ONE = Decimal(1)
E4 = Decimal(4).exp()

def dec(q):
    if isinstance(q, Decimal):
        return q
    if isinstance(q, F):
        return Decimal(q.numerator) / Decimal(q.denominator)
    return Decimal(q)

def xlogx(q):
    return ZERO if q == 0 else dec(q) * dec(q).ln()

def g(q):
    if q == 0: return ZERO
    if q == 1: return ONE
    z = dec(q)
    return -z*z*z.ln()/(ONE-z)

def h(q):
    if q == 0: return ZERO
    z=dec(q)
    return z*z*(ONE-z.ln())

def d(b,a):
    if a == 0:
        assert b == 0
        return ZERO
    if b == 0: return dec(a)
    return dec(b)*(dec(b)/dec(a)).ln()-dec(b)+dec(a)

def nonnegative(q):
    assert q >= -TOL, str(q)

def nearzero(q):
    assert abs(q) <= TOL, str(q)

def js(q):
    if isinstance(q,(Decimal,F)): return str(q)
    return q

def law_check(name, law):
    n=len(next(iter(law)))
    assert sum(law.values(),F(0))==1
    assert all(w>0 for w in law.values())
    assert all(sorted(x)==list(range(n)) for x in law)
    b=[[sum((w for x,w in law.items() if x[i]==j),F(0)) for j in range(n)] for i in range(n)]
    assert all(sum(row,F(0))==1 for row in b)
    assert all(sum((b[i][j] for i in range(n)),F(0))==1 for j in range(n))
    H=-sum((xlogx(w) for w in law.values()),ZERO)
    marginal_cross=sum((xlogx(v) for row in b for v in row),ZERO)
    orders=list(permutations(range(n)))
    ElogZ=ZERO
    minlocal=None
    history_count=0
    for order in orders:
        chain=ZERO
        for depth,i in enumerate(order):
            histories=defaultdict(dict)
            prior=order[:depth]
            for x,w in law.items():
                key=tuple(x[r] for r in prior)
                histories[key][x]=w
            for key, sublaw in histories.items():
                history_count+=1
                mass=sum(sublaw.values(),F(0))
                assert mass>0
                available=set(range(n))-set(key)
                Z=sum((b[i][j] for j in available),F(0))
                assert Z>0
                q=[sum((w for x,w in sublaw.items() if x[i]==j),F(0))/mass for j in range(n)]
                assert sum(q,F(0))==1
                assert all(q[j]==0 or (j in available and b[i][j]>0) for j in range(n))
                condH=-sum((xlogx(v) for v in q),ZERO)
                cross=sum((dec(q[j])*dec(b[i][j]).ln() for j in range(n) if q[j]>0),ZERO)
                kl=dec(Z).ln()-condH-cross
                nonnegative(kl)
                minlocal=kl if minlocal is None else min(minlocal,kl)
                chain+=dec(mass)*condH
                ElogZ+=dec(mass)*dec(Z).ln()/Decimal(len(orders))
        nearzero(chain-H)
    correction=-Decimal(n)+sum((g(v) for row in b for v in row),ZERO)
    nonnegative(ElogZ-H-marginal_cross)
    nonnegative(correction-ElogZ)
    nonnegative(correction-H-marginal_cross)
    record={'name':name,'n':n,'positive_permutations':len(law),'reveal_orders':len(orders),'positive_histories':history_count,'exact_marginals':[[str(v) for v in row] for row in b],'minimum_local_KL':str(minlocal),'local_to_chain_slack':str(ElogZ-H-marginal_cross),'Jensen_integral_slack':str(correction-ElogZ),'entropy_lemma_slack':str(correction-H-marginal_cross)}
    return record,b,H,correction

def matrix_check(name,A):
    A=[[F(v) for v in row] for row in A]
    n=len(A)
    assert all(len(row)==n and sum(row,F(0))==1 and min(row)>=0 for row in A)
    weights={}
    for x in permutations(range(n)):
        w=F(1)
        for i,j in enumerate(x): w*=A[i][j]
        if w: weights[x]=w
    P=sum(weights.values(),F(0))
    S=sum((v*v for row in A for v in row),F(0))
    assert F(1)<=S<=n
    if not P:
        return {'name':name,'n':n,'permanent':'0','zero_permanent_case':True,'S':str(S)}
    law={x:w/P for x,w in weights.items()}
    record,b,H,correction=law_check(name,law)
    D=sum((dec(b[i][j])*(dec(b[i][j])/dec(A[i][j])).ln() for i in range(n) for j in range(n) if b[i][j]>0),ZERO)
    scalarD=sum((d(b[i][j],A[i][j]) for i in range(n) for j in range(n)),ZERO)
    nearzero(D-scalarD)
    assert all(b[i][j]==0 or A[i][j]>0 for i in range(n) for j in range(n))
    crossA=sum((dec(b[i][j])*dec(A[i][j]).ln() for i in range(n) for j in range(n) if b[i][j]>0),ZERO)
    nearzero(dec(P).ln()-H-crossA)
    raw=sum((h(v) for row in A for v in row),ZERO)
    logP=dec(P).ln()
    rhs1=-Decimal(n)+E4*raw
    rhs2=-Decimal(n)+E4*dec(S)*(ONE+Decimal(n).ln())
    nonnegative(correction-D-logP)
    nonnegative(rhs1-correction+D)
    nonnegative(rhs2-rhs1)
    for i in range(n):
        for j in range(n): nonnegative(E4*h(A[i][j])-g(b[i][j])+d(b[i][j],A[i][j]))
    record.update({'permanent':str(P),'S':str(S),'column_sums':[str(sum((A[i][j] for i in range(n)),F(0))) for j in range(n)],'input_positive_marginal_zero':[[i,j] for i in range(n) for j in range(n) if A[i][j]>0 and b[i][j]==0],'gibbs_bound_slack':str(correction-D-logP),'entrywise_bound_slack':str(rhs1-logP),'frobenius_bound_slack':str(rhs2-logP),'D':str(D),'sum_scalar_d':str(scalarD)})
    if n>=2:
        nonnegative(Decimal(3)*E4*dec(S)*Decimal(n).ln()-Decimal(n)-logP)
    return record

matrices=[
 ('n1',[[1]]),
 ('identity3',[[1,0,0],[0,1,0],[0,0,1]]),
 ('uniform2',[[F(1,2)]*2 for _ in range(2)]),
 ('uniform4',[[F(1,4)]*4 for _ in range(4)]),
 ('noncolumn2',[[F(9,10),F(1,10)],[F(4,5),F(1,5)]]),
 ('positive_unused_edge2',[[F(1,2),F(1,2)],[0,1]]),
 ('sparse_cycle3',[[F(1,2),F(1,2),0],[F(1,2),0,F(1,2)],[0,F(1,2),F(1,2)]]),
 ('uniform_blocks4',[[F(1,2),F(1,2),0,0],[F(1,2),F(1,2),0,0],[0,0,F(1,2),F(1,2)],[0,0,F(1,2),F(1,2)]]),
 ('zero_permanent2',[[1,0],[1,0]]),
 ('dense_asymmetric3',[[F(1,2),F(1,3),F(1,6)],[F(1,7),F(2,7),F(4,7)],[F(5,11),F(3,11),F(3,11)]]),
 ('near_deterministic2',[[1-F(1,10**50),F(1,10**50)],[F(1,10**40),1-F(1,10**40)]]),
]
records=[matrix_check(name,A) for name,A in matrices]
arbitrary=[
 ('nonuniform_two_atom4',{(0,1,2,3):F(1,7),(1,0,3,2):F(6,7)}),
 ('nonuniform_three_atom3',{(0,1,2):F(1,11),(1,2,0):F(3,11),(2,0,1):F(7,11)}),
]
for name,law in arbitrary: records.append(law_check(name,law)[0])

# Endpoint and switch-line probes; no interpolation or universal extrapolation.
vals={ZERO,ONE,Decimal('0.5'),Decimal('0.1'),Decimal('0.9')}
for k in [1,3,10,30,70,100]:
    vals.add(Decimal(10)**(-k))
    if k<=70: vals.add(ONE-Decimal(10)**(-k))
pairs=set(product(vals,vals))
E2=Decimal(2).exp()
for a in vals:
    if a>0 and E2*a<=1:
        for r in [ONE-Decimal('1e-40'),ONE,ONE+Decimal('1e-40')]:
            pairs.add((a,E2*a*r))
valid=[(a,b) for a,b in pairs if 0<=a<=1 and 0<=b<=1 and (a>0 or b==0)]
min_abs=None
for a,b in valid:
    slack=E4*h(a)-g(b)+d(b,a)
    nonnegative(slack)
    if min_abs is None or slack<min_abs[0]: min_abs=(slack,a,b)

# A greedy marginal procedure can reach a dead end on a history outside mu support.
# The submitted positive-history proof never needs that conditional law.
cycle=[[F(1,2),F(1,2),0],[F(1,2),0,F(1,2)],[0,F(1,2),F(1,2)]]
partial=[(0,1),(1,2)]
assert cycle[0][1]>0 and cycle[1][2]>0 and cycle[2][0]==0
assert all(not (x[0]==1 and x[1]==2) for x in permutations(range(3)) if all(cycle[i][x[i]]>0 for i in range(3)))

report={'completed_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'method':'Fresh exact Fraction enumeration of finite laws/histories and 120-digit Decimal evaluation of logarithmic inequalities. Not a replay of historical scripts. Not a universal proof, formal verification, interval certificate, or extrapolation.','python':sys.version,'platform':platform.platform(),'decimal_precision':getcontext().prec,'numerical_tolerance':str(TOL),'matrix_cases':len(matrices),'arbitrary_permutation_laws':len(arbitrary),'scalar_boundary_pairs':len(valid),'minimum_scalar_slack':{'slack':str(min_abs[0]),'a':str(min_abs[1]),'b':str(min_abs[2])},'positive_histories_total':sum(r.get('positive_histories',0) for r in records),'finite_checks_pass':True,'records':records,'greedy_deadend_example':{'matrix':[[str(x) for x in row] for row in cycle],'partial_assignment':partial,'remaining_edge':[2,0],'positive_gibbs_history':False,'relevance':'Confirms need to exclude impossible conditional histories; candidate does so. No defect in candidate theorem.'}}
report['script_sha256']=hashlib.sha256(Path(__file__).read_bytes()).hexdigest()
Path('FINITE_CHECKS.json').write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps({k:report[k] for k in ['completed_utc','matrix_cases','arbitrary_permutation_laws','scalar_boundary_pairs','positive_histories_total','decimal_precision','finite_checks_pass','script_sha256']},indent=2))
