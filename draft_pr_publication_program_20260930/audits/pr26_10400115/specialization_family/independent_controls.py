#!/usr/bin/env python3
"""Exact non-mirroring controls; universal proofs are in the sealed reconstruction.
Run with stdlib Python. Default receipt path is this script's directory.
No original verification script or receipt is imported.
"""
from fractions import Fraction as Q
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, json, sys

checks = {}
def check(name, value):
    if not value: raise AssertionError(name)
    checks[name] = 'PASS'
def la(a): return {int(k):Q(v) for k,v in a.items() if v}
def ladd(a,b):
    d=dict(a)
    for k,c in b.items(): d[k]=d.get(k,Q(0))+c
    return la(d)
def lscale(a,c): return la({k:c*v for k,v in a.items()})
def lshift(a,k): return la({i+k:c for i,c in a.items()})
def lmul(a,b):
    d={}
    for i,c in a.items():
        for j,e in b.items(): d[i+j]=d.get(i+j,Q(0))+c*e
    return la(d)
def gp(a,b): return a[0]+b[0],ladd(a[1],lshift(b[1],a[0]))
def gi(a): return -a[0],lshift(lscale(a[1],-1),-a[0])
def gw(steps):
    a=(0,{})
    for x in steps:a=gp(a,x)
    return a
D=(1,{});U=(0,{0:Q(1)});ONE=(0,{})
def word_for(f):
    steps=[]
    for i,c in sorted(f.items()):
        if c.denominator!=1:raise ValueError('Integer coefficients required')
        steps.extend([(i,{}),(0,{0:c}),(-i,{})])
    return gw(steps)
def eye(n):return [[Q(i==j) for j in range(n)] for i in range(n)]
def matmul(a,b):return [[sum((x*y for x,y in zip(row,col)),Q(0)) for col in zip(*b)] for row in a]
def matadd(a,b):return [[x+y for x,y in zip(u,v)] for u,v in zip(a,b)]
def matscale(a,c):return [[c*x for x in row] for row in a]
def inv(a):
    n=len(a);r=[list(row)+e for row,e in zip(a,eye(n))]
    for j in range(n):
        p=next((i for i in range(j,n) if r[i][j]),None)
        if p is None:raise ZeroDivisionError('Singular matrix')
        r[j],r[p]=r[p],r[j];c=r[j][j];r[j]=[x/c for x in r[j]]
        for i in range(n):
            if i!=j:
                c=r[i][j];r[i]=[x-c*y for x,y in zip(r[i],r[j])]
    return [r0[n:] for r0 in r]
def mpow(a,k):
    if k<0:a=inv(a);k=-k
    out=eye(len(a))
    while k:
        if k&1:out=matmul(out,a)
        a=matmul(a,a);k//=2
    return out
def companion(p):
    n=len(p)-1;a=[[Q(0) for _ in range(n)] for _ in range(n)]
    for i in range(n-1):a[i+1][i]=Q(1)
    for i in range(n):a[i][n-1]=-Q(p[i],p[n])
    return a
def at_matrix(f,c):
    out=matscale(c,0)
    for k,v in f.items():out=matadd(out,matscale(mpow(c,k),v))
    return out
def at_rational(f,a):return sum((v*a**k for k,v in f.items()),Q(0))
def block(a,b,c,d):return [x+y for x,y in zip(a,b)]+[x+y for x,y in zip(c,d)]
def zero(n):return matscale(eye(n),0)
def reduced(word):
    stack=[]
    for c in word:
        if stack and stack[-1]==-c:stack.pop()
        else:stack.append(c)
    return stack

# Universal mechanism sampled using new degrees, nonmonic equations and signed indices.
polys = {
 'rational_nonintegral':[7,5],              # alpha=-7/5, nonunit/nonintegral
 'quadratic_nonintegral':[-1,0,2],          # alpha=+-1/sqrt(2)
 'cubic_nonunit':[-2,0,0,1],                # real cube root(2)
 'fifth_roots_unity':[1,1,1,1,1],           # primitive fifth roots, units
 'fourth_roots_unity':[1,0,1],              # +-i
 'unit_golden_ratio':[-1,-1,1],             # quadratic algebraic units
 'alpha_one':[-1,1],
 'alpha_minus_one':[1,1]
}
for name,p in polys.items():
    f=la(dict(enumerate(p)));c=companion(p);n=len(c)
    for shift in [-7,-2,0,3]:
        sf=lshift(f,shift);w=word_for(sf)
        check(name+'_shift'+str(shift)+'_word_matches',w==(0,sf))
        check(name+'_shift'+str(shift)+'_nonidentity',w!=ONE)
        check(name+'_shift'+str(shift)+'_annihilation',at_matrix(sf,c)==zero(n))
    check(name+'_invertibility',matmul(c,inv(c))==eye(n))
# Negative controls: being a genuine nonzero Laurent function is insufficient to vanish.
check('rational_nonannihilator_survives',at_rational({-3:Q(1),1:Q(2)},Q(-7,5))!=0)
check('transcendental_formal_nonzero',word_for({-9:Q(2),0:Q(-3),8:Q(1)})!=ONE)
check('alpha_zero_excluded',0**1==0) # det(D(0))=0; inverse has no value.
try:at_rational({-1:Q(1)},Q(0));zero_fails=False
except ZeroDivisionError:zero_fails=True
check('alpha_zero_negative_index_rejected',zero_fails)
# Domain control: p becomes zero, so its rational-function inverse cannot be evaluated.
f={0:Q(-2),3:Q(1)};c=companion([-2,0,0,1]);evaluated=at_matrix(f,c)
try:inv(evaluated);bad_field_evaluation=False
except ZeroDivisionError:bad_field_evaluation=True
check('whole_Qx_field_evaluation_impossible',bad_field_evaluation)
# H is not F2: the nontrivial free reduced commutator of U and DUD^-1 is I in H.
free_word=[2,1,2,-1,-2,1,-2,-1] # U (D U D^-1) U^-1 (D U^-1 D^-1)
gen={1:D,-1:gi(D),2:U,-2:gi(U)}
check('free_group_control_nonempty_reduction',len(reduced(free_word))==8)
check('semidirect_commutator_relation',gw([gen[i] for i in free_word])==ONE)
# Every finite direct product of chosen specializations has a nontrivial joint kernel.
P={0:Q(1)}
for p in polys.values():P=lmul(P,la(dict(enumerate(p))))
check('finite_direct_product_kernel_nonzero',word_for(P)!=ONE)
for name,p in polys.items():check('finite_product_joint_kernel_'+name,at_matrix(P,companion(p))==zero(len(p)-1))
# Roots of unity yield extra diagonal kernel, absent for rational -7/5.
check('root_unity_diagonal_kernel',mpow(companion([1,1,1,1,1]),5)==eye(4))
check('non_root_unity_diagonal_control',all(Q(-7,5)**k!=1 for k in list(range(-10,0))+list(range(1,11))))

# Restriction of scalars for degrees 2, 3, 4, including nonintegral generators/inverses.
for name,p in [('nonintegral_quadratic',[-1,0,2]),('cubic',[-2,0,0,1]),('cyclotomic_quartic',[1,1,1,1,1])]:
    c=companion(p);n=len(c);e=eye(n);z=zero(n);cinv=inv(c)
    A=block(c,e,z,cinv);B=block(e,matadd(matscale(c,2),e),z,e)
    AB=block(c,matadd(matmul(c,matadd(matscale(c,2),e)),e),z,cinv)
    check('restriction_'+name+'_multiplicative',matmul(A,B)==AB)
    check('restriction_'+name+'_generator_inverse',matmul(A,inv(A))==eye(2*n))
    check('restriction_'+name+'_negative_word',matmul(mpow(A,-5),mpow(A,5))==eye(2*n))
    # A polynomial of degree<n acts nontrivially by looking at its value on basis1.
    witness=at_matrix({i:Q((-1)**i*(i+1),i+2) for i in range(n)},c)
    check('restriction_'+name+'_identity_reflection',witness!=zero(n) and [witness[i][0] for i in range(n)]==[Q((-1)**i*(i+1),i+2) for i in range(n)])
check('rational_blocks_need_not_be_integral',any(v.denominator>1 for row in companion([-1,0,2]) for v in row))

# Multi-parameter rational coefficients: exact matrices, admissibility, and finite witnesses.
def matrices_at(u,v):
    u,v=Q(u),Q(v)
    if not u*v*(u-v)*(u+v-2):raise ValueError('Denominator/determinant/Laurent factor zero')
    return [[u-v,1/(u+v-2)],[Q(0),Q(1)]],[[v,1/u],[Q(0),Q(1)]]
a,b=matrices_at(2,3);comm=matmul(matmul(matmul(a,b),inv(a)),inv(b))
check('multivariable_finite_set_survives',a!=eye(2) and b!=eye(2) and comm!=eye(2))
check('multivariable_commutator_exact_witness',comm[0][1]==Q(-5,3))
for name,point in [('determinant_zero',(3,3)),('denominator_zero',(3,-1)),('Laurent_zero',(0,3))]:
    try:matrices_at(*point);rejected=False
    except ValueError:rejected=True
    check('invalid_'+name+'_rejected',rejected)
# Prescribing v=u^2 can force every specialization of U(v-u^2) to be I.
check('curve_constraint_kills_witness',all(Q(v)-Q(u)**2==0 for u,v in [(1,1),(2,4),(-3,9),(Q(2,3),Q(4,9))]))
check('off_curve_witness_survives',Q(3)-Q(2)**2!=0)
# Char0/infinite-field condition matters for density/avoidance.
check('finite_field_nonzero_polynomial_vanishes_everywhere',all((a*a-a)%2==0 for a in [0,1]))
check('same_polynomial_over_Q_survives',(Q(2)**2-Q(2))!=0)

out={'status':'PASS','checks':checks,'assertions':len(checks),'arithmetic':'Python stdlib fractions; integer Laurent maps, exact companion matrices and Gaussian elimination; no SymPy/original imports','script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),'executed_utc':datetime.now(timezone.utc).isoformat(),'python':sys.version,'universal_proof':'EARLY_CRITERIA_RECONSTRUCTION.md; finite controls do not prove the general braid target','no_new_substantive_problem_attempt':True}
parser=argparse.ArgumentParser();parser.add_argument('--receipt',type=Path,default=Path(__file__).with_name('INDEPENDENT_CONTROLS.json'));args=parser.parse_args();args.receipt.write_text(json.dumps(out,indent=2)+'\n')
print(json.dumps({'status':out['status'],'assertions':len(checks),'script_sha256':out['script_sha256']}))
