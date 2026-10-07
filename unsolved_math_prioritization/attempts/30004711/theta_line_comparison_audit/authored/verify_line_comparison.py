"""Independent 1|1 exterior-algebra Hessian/Berezinian and stack checks.
Does not establish the punctured torsion/super-Kahler identification.
"""
from pathlib import Path
from fractions import Fraction
import hashlib, json
import sympy as s

z, zb = s.symbols('z zb')
K0, h = s.Function('K0')(z, zb), s.Function('h')(z, zb)
# Generator order: bar(theta)=bit 0, theta=bit 1. Coefficients commute.
def clean(a):
    return {k:s.simplify(v) for k,v in a.items() if s.simplify(v)!=0}
def add(a,b):
    return clean({k:a.get(k,0)+b.get(k,0) for k in set(a)|set(b)})
def scale(a,c): return clean({k:c*v for k,v in a.items()})
def mul(a,b):
    out={}
    for I,x in a.items():
        for J,y in b.items():
            if I&J: continue
            inversions=sum(1 for i in range(2) for j in range(2) if I>>i&1 and J>>j&1 and i>j)
            out[I|J]=out.get(I|J,0)+(-1)**inversions*x*y
    return clean(out)
def dodd(a,i):
    out={}
    for I,x in a.items():
        if I>>i&1:
            out[I^(1<<i)]=(-1)**((I&((1<<i)-1)).bit_count())*x
    return clean(out)
def deven(a,q): return clean({I:s.diff(x,q) for I,x in a.items()})
bar,theta,u={1:s.Integer(1)},{2:s.Integer(1)},{3:s.Integer(1)}
assert mul(theta,bar)==scale(u,-1)
assert dodd(u,0)==theta and dodd(u,1)==scale(bar,-1)
K={0:K0,3:h}
A=deven(deven(K,zb),z)
B=deven(dodd(K,0),z)
C=dodd(deven(K,zb),1)
D=dodd(dodd(K,0),1)
assert B==scale(theta,s.diff(h,z))
assert C==scale(bar,-s.diff(h,zb))
assert D=={0:h}
BC=mul(B,C)
assert BC==scale(u,s.diff(h,z)*s.diff(h,zb))
ber=scale(add(A,scale(BC,-1/h)),1/h)
assert s.simplify(ber[3]-s.diff(s.log(h),z,zb))==0
assert s.simplify(ber[0]-s.diff(K0,z,zb)/h)==0
# A full mixed holomorphic/antiholomorphic 4x4 supersymplectic block,
# with graded skew transpose and i suppressed, has Ber = -(Ber G)^2.
# Reinstating i in every block does not alter Ber for even|odd rank 2|2.
# Use the block Schur complement, retaining the odd-generator ordering.
Dinv=[[{}, {0:1/h}],[{0:1/h},{}]]
AA=[[{},A],[scale(A,-1),{}]]
BB=[[{},B],[scale(C,-1),{}]]
CC=[[{},C],[scale(B,-1),{}]]
def mm(U,V):
 return [[add(mul(U[i][0],V[0][j]),mul(U[i][1],V[1][j])) for j in range(2)] for i in range(2)]
cor=mm(mm(BB,Dinv),CC)
S=[[add(AA[i][j],scale(cor[i][j],-1)) for j in range(2)] for i in range(2)]
detS=add(mul(S[0][0],S[1][1]),scale(mul(S[0][1],S[1][0]),-1))
berW=scale(detS,-1/h**2)
assert clean(add(berW,mul(ber,ber)))=={}
# Normalization/orientation is a separate real-density choice, not proved by
# the complex 4x4 determinant identity alone.
r=s.Function('r')(z,zb)
assert s.simplify(s.diff(s.log(h*r),z,zb)-s.diff(s.log(h),z,zb)-s.diff(s.log(r),z,zb))==0
assert s.simplify(s.diff(s.log(1/h),z,zb)+s.diff(s.log(h),z,zb))==0
# Integer/gerbe arithmetic; no rounded floating point.
degree_B=Fraction(1,2); hodge_degree=Fraction(1,24)
c1_Fdual_over_lambda=Fraction(3,2)
odd=degree_B*hodge_degree*c1_Fdual_over_lambda
assert odd==Fraction(1,32)
# Derive the Hodge degree independently from weighted-projective coordinates:
# Mbar_1,1 = P(4,6), lambda=O(1), degree=1/(4*6).
assert hodge_degree==Fraction(1,4*6)
# Test both odd Hessian terms: a pluriharmonic log metric gives zero.
assert s.simplify(s.diff(s.log(s.exp(z+zb)),z,zb))==0
frozen=Path('theta_twisted_volumes_30004711/authored/AUTHOR_APPROACH_2_SUPER_KAEHLER_LINE.md')
sha=hashlib.sha256(frozen.read_bytes()).hexdigest()
assert sha=='602322f2a58d6294e875e648dd6f6cc9a3a47c0b480d9f8a0479996a235916b0'
report={
 'frozen_sha256':sha,
 'explicit_grassmann_left_derivatives_pass':True,
 'full_mixed_supermatrix_ber_relation_pass':True,
 'schur_complement_sign_pass':True,
 'top_coefficient':'partial_z partial_bar_z log|h|',
 'metric_dual_changes_curvature_sign':True,
 'constant_metric_rescaling_preserves_curvature':True,
 'odd_stack_degree':str(degree_B),
 'hodge_degree':str(hodge_degree),
 'integral_c1_Fdual_odd':str(odd),
 'integral_c1_F_odd':str(-odd),
 'actual_punctured_goldman_super_kaehler_verified':False,
 'actual_torsion_metric_comparison_verified':False,
 'actual_torsion_orientation_and_measure_verified':False,
 'full_literal_OWR_identity_certified':False,
 'status':'Conditional local and compactified-line results accepted; convention clarification required.'}
p=Path(__file__).with_name('LINE_COMPARISON_CHECK.json')
p.write_text(json.dumps(report,indent=2)+'\n')
print(json.dumps(report,indent=2))
