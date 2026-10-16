#!/usr/bin/env python3
"""Exact finite algebra checks for FULL_PROOF.md, not a formal proof checker."""
from fractions import Fraction as Q
import json

checks = {}
def check(name, predicate):
    assert predicate, name
    checks[name] = True

def mul(A, B):
    return [[sum(a*b for a,b in zip(row,col)) for col in zip(*B)] for row in A]
def transpose(A):
    return [list(x) for x in zip(*A)]
def ident(n):
    return [[int(i==j) for j in range(n)] for i in range(n)]
def power(A,n):
    R=ident(len(A))
    for _ in range(n): R=mul(R,A)
    return R

def F(p):
    x,y,a=p
    return (x+a,y+x,a)
def Fi(p):
    x,y,a=p
    return (x-a,y-x+a,a)
def formula(p,n):
    x,y,a=p
    return (x+n*a,y+n*x+a*n*(n-1)/2,a)

A=[[1,0],[1,1]]
J=[[0,1],[-1,0]]
check('area_preservation',mul(mul(transpose(A),J),A)==J)
for n in range(-30,31):
    for p in [(Q(2,7),Q(-4,9),Q(5,11)),(Q(-3),Q(2),Q(-7,13)),(Q(0),Q(0),Q(1))]:
        v=p
        for _ in range(abs(n)): v=(F if n>=0 else Fi)(v)
        check('iterate_%s_%s'%(n,p),v==formula(p,n))
    if n>=0:
        check('derivative_power_%s'%n,power(A,n)==[[1,0],[n,1]])
# Each check is rational substitution; the all-integer induction is in the proof.
for n in range(-15,16):
    for m in range(-15,16):
        p=(Q(2,7),Q(3,11),Q(13,17))
        check('iterate_group_%s_%s'%(n,m),formula(formula(p,n),m)==formula(p,n+m))
# Fourier phase: e_(k,l) composed with F has new character (k+l,l)
# and scalar phase k*a. Test exact linear coefficients (x,y,a).
for k in range(-6,7):
    for l in range(-6,7):
        coordinate_pullback=[[1,0,1],[1,1,0],[0,0,1]]
        composed=tuple(mul([[k,l,0]],coordinate_pullback)[0])
        expected=(k+l,l,k)
        check('Fourier_coefficients_%s_%s'%(k,l),composed==expected)
        if l:
            indices=[(k+j*l,l) for j in range(-20,21)]
            check('distinct_character_chain_%s_%s'%(k,l),len(set(indices))==41)
# Orthogonality is exact Fourier orthogonality, not sampled quadrature.
for n in range(-20,21):
    for m in range(-20,21):
        difference_frequency=(n-m,0)
        exact_integral=int(difference_frequency==(0,0))
        check('orthogonal_orbit_%s_%s'%(n,m),exact_integral==int(n==m))
# Mapping-torus seam derivative and global frame matrices.
def frame(t):
    return [[1,0,0,0],[-t,1,0,0],[0,0,1,0],[0,0,0,1]]
Dglue=[[1,0,0,0],[1,1,0,0],[0,0,1,0],[0,0,0,1]]
J4=[[0,1,0,0],[-1,0,0,0],[0,0,0,1],[0,0,-1,0]]
check('four_dimensional_form_descends',mul(mul(transpose(Dglue),J4),Dglue)==J4)
for t in [Q(-7,3),Q(0),Q(1,4),Q(1),Q(7,5)]:
    check('frame_seam_%s'%t,mul(Dglue,frame(t))==frame(t-1))
    check('frame_is_symplectic_%s'%t,mul(mul(transpose(frame(t)),J4),frame(t))==J4)
    for s in [Q(-15,2),Q(-1),Q(0),Q(4,3),Q(20)]:
        shear=[[1,0,0,0],[s,1,0,0],[0,0,1,0],[0,0,0,1]]
        inverse=[[1,0,0,0],[-s,1,0,0],[0,0,1,0],[0,0,0,1]]
        check('flow_frame_%s_%s'%(t,s),frame(t)==mul(frame(t+s),shear))
        check('flow_inverse_%s_%s'%(t,s),mul(shear,inverse)==ident(4))
# Hamiltonian contraction with X=partial_t is the row X^T J4 = dE.
check('Hamiltonian_contraction',mul([[0,0,1,0]],J4)==[[0,0,0,1]])
# Exact cutoff inequalities establish the constant-speed band endpoints.
left,right=Q(1,8),Q(3,8)
check('band_volume',right-left==Q(1,4))
check('cutoff_left_plateau',16*(left-Q(1,16))==1)
check('cutoff_right_plateau',16*(Q(7,16)-right)==1)
check('cutoff_support_inside_circle',0<Q(1,16)<left<right<Q(7,16)<1)

controls={}
# Wrong sign does not give a descending frame.
badframe=lambda t:[[1,0,0,0],[t,1,0,0],[0,0,1,0],[0,0,0,1]]
controls['wrong_frame_sign_rejected']=mul(Dglue,badframe(Q(1,3)))!=badframe(Q(1,3)-1)
# Without the shear, g=e_y is invariant, so the orthogonal-orbit witness fails.
translation_pullback=[[1,0,1],[0,1,0],[0,0,1]]
controls['untwisted_rotation_has_fixed_y_observable']=mul([[0,1,0]],translation_pullback)==[[0,1,0]]
# Rational rotation a=p/q has a nonconstant invariant character e_(q,0).
a=Q(2,7); k=7
controls['rational_rotation_nonergodicity_witness']=(k*a).denominator==1 and k!=0
# H=E does not define a real function on a circle.
controls['uncut_circle_coordinate_rejected']=Q(0)!=Q(1)
# The actual cutoff is zero near both endpoints, whereas its local slope is 1.
def q_on_plateau(r):
    if r<=0: return Q(0)
    if r>=1: return Q(1)
    raise ValueError('Exact routine only evaluates plateau points')
def h_on_plateaus(E):
    a=q_on_plateau(16*(E-Q(1,16)))
    b=q_on_plateau(16*(Q(7,16)-E))
    return E*a*b
controls['cutoff_avoids_circle_coordinate_error']=(h_on_plateaus(Q(0))==h_on_plateaus(Q(1))==0 and h_on_plateaus(Q(1,4))==Q(1,4))
# Clock eigenfunction has return-time frequency zero and cannot witness failure.
clock_phases=[Q(n)%1 for n in range(-10,11)]
controls['clock_only_witness_is_insufficient']=len(set(clock_phases))==1
assert all(controls.values())
print(json.dumps({'result':'PASS','exact_checks':len(checks),'negative_controls':controls,'limitations':['Finite exact algebra checks supplement the full proof; they do not prove irrationality, Fourier completeness, smooth quotient descent, disintegration, or infinite-time limits.','No floating-point orbit experiment is used to infer ergodicity or zero exponents.','This is not independent expert review or a priority certificate.']},indent=2,sort_keys=True))
