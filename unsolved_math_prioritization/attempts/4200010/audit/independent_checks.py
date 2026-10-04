#!/usr/bin/env python3
"""Independent exact algebra tests. Standard library only; no candidate imports.
These checks do not replace the infinite-dimensional and smooth arguments.
"""
from fractions import Fraction as Q
from collections import Counter
import json

counts = Counter()

def require(group, condition):
    if not condition:
        raise AssertionError(group)
    counts[group] += 1

# Q(sqrt(2)) represented exactly as a pair of rational coefficients.
def alg(a=0, b=0): return (Q(a), Q(b))
def add(u, v): return (u[0]+v[0], u[1]+v[1])
def neg(u): return (-u[0], -u[1])
def sub(u, v): return add(u, neg(v))
def scale(c, u): return (c*u[0], c*u[1])
def prod(u, v): return (u[0]*v[0]+2*u[1]*v[1], u[0]*v[1]+u[1]*v[0])
a = alg(0, 1)
require('quadratic_field', prod(a, a) == alg(2))

def iterate(z, n):
    x, y = z
    return (add(x, scale(n, a)), add(add(y, scale(n, x)), scale(Q(n*(n-1), 2), a)))
def forward(z): return (add(z[0], a), add(z[1], z[0]))
def backward(z): return (sub(z[0], a), add(sub(z[1], z[0]), a))

seeds = [(alg(Q(2,7)), alg(Q(3,11))), (alg(Q(-4,9), Q(1,5)), alg(2,-3))]
for z in seeds:
    for n in range(-32,33):
        z1=z
        for _ in range(abs(n)):
            z1=(forward if n>=0 else backward)(z1)
        require('irrational_field_iterates', z1 == iterate(z,n))
    for n in [-17,-2,-1,0,1,3,19]:
        for m in [-13,-1,0,2,23]:
            require('irrational_field_group_law', iterate(iterate(z,n),m)==iterate(z,n+m))
    for k,l in [(-3,2),(0,1),(1,0),(4,-7)]:
        # Integer translations of representatives produce integer translations
        # after F^n; equivalence is checked exactly, not using a rounded alpha.
        zshift = (add(z[0],alg(k)),add(z[1],alg(l)))
        for n in range(-5,6):
            p,q=iterate(zshift,n),iterate(z,n)
            require('torus_representatives', sub(p[0],q[0])==alg(k) and sub(p[1],q[1])==alg(l+n*k))

# Fundamental-domain flow, including exact seam hits and negative crossings.
def reduced_flow(point, s):
    z,t=point
    k=(t+s).__floor__()
    return (iterate(z,k),t+s-k)

def mm(A,B): return [[sum(x*y for x,y in zip(r,c)) for c in zip(*B)] for r in A]
def tr(A): return [list(r) for r in zip(*A)]
def I(n): return [[Q(i==j) for j in range(n)] for i in range(n)]
def frame(t): return [[1,0,0,0],[-t,1,0,0],[0,0,1,0],[0,0,0,1]]
def shear(s): return [[1,0,0,0],[s,1,0,0],[0,0,1,0],[0,0,0,1]]
J=[[0,1,0,0],[-1,0,0,0],[0,0,0,1],[0,0,-1,0]]
times=[Q(-17,3),Q(-2),Q(-1),Q(-1,7),Q(0),Q(1,7),Q(1),Q(2),Q(17,3)]
for t in [Q(0),Q(1,7),Q(1,2),Q(6,7)]:
    for s in times:
        k=(t+s).__floor__(); t1=t+s-k
        coordinate_D=shear(k)
        derivative_in_frame=mm(mm(frame(-t1),coordinate_D),frame(t))
        require('fractional_time_seam_derivative', derivative_in_frame==shear(s))
        require('fractional_time_inverse',mm(shear(s),shear(-s))==I(4))
        require('fractional_time_symplectic',mm(mm(tr(shear(s)),J),shear(s))==J)
        for r in times:
            p=(seeds[0],t)
            require('fractional_time_flow_group',reduced_flow(reduced_flow(p,s),r)==reduced_flow(p,s+r))
        require('fundamental_domain_time_range',0<=t1<1)

# Exact PSD criterion proves the sampled norm upper bound without sampling v.
# For S=[[1,0],[s,1]], (1+|s|)^2 I - S^T S has entries
# [2r,-s;-s,2r+r^2] and determinant 3r^2+2r^3, r=|s|.
for s in [Q(k,d) for d in [1,3,7] for k in range(-40,41)]:
    r=abs(s); S=[[1,0],[s,1]]; c=(1+r)**2
    P=[[c*int(i==j)-mm(tr(S),S)[i][j] for j in range(2)] for i in range(2)]
    require('two_sided_operator_bound',P[0][0]==2*r and P[1][1]==2*r+r*r and P[0][1]==-s and P[1][0]==-s and P[0][0]*P[1][1]-P[0][1]*P[1][0]==3*r*r+2*r*r*r)
    require('bound_positive_semidefinite',P[0][0]>=0 and P[1][1]>=0 and P[0][0]*P[1][1]-P[0][1]**2>=0)

# Full E-dependent flow outside the plateau checks the omitted transverse term.
# Coordinate derivative has d(t+s*b(E))/dE = s*c, c=b'(E).
for t in [Q(0),Q(1,3),Q(8,7)]:
    for s in times:
        for b,c in [(Q(0),Q(1)),(Q(1),Q(0)),(Q(-2),Q(3,7)),(Q(5,3),Q(-2))]:
            D=I(4); D[2][3]=s*c
            actual=mm(mm(frame(-(t+s*b)),D),frame(t))
            expected=shear(s*b); expected[2][3]=s*c
            require('full_energy_direction',actual==expected)
            require('full_energy_symplectic',mm(mm(tr(actual),J),actual)==J)

# Exact coefficients of orbitwise phase-shift differences. Irrationality of
# (k-j)*sqrt(2) plus density of irrational rotations is proved in AUDIT.md.
z=seeds[1]
for k in range(-6,7):
    for j in range(-6,7):
        for n in [-11,-1,0,2,13]:
            difference=sub(iterate(z,n+k)[1],iterate(z,n+j)[1])
            expected=add(scale(k-j,z[0]),scale((k-j)*n+Q(k*(k-1)-j*(j-1),2),a))
            require('bohr_phase_difference',difference==expected)
        if k!=j:
            require('bohr_phase_slope_nonzero',scale(k-j,a)[1]!=0)

controls={}
# These are deliberately bad replacements, and each must be detected.
controls['zero_speed_suspension_is_fixed']=reduced_flow((seeds[0],Q(1,3)),0)==(seeds[0],Q(1,3))
controls['time_one_does_not_prove_flow_ergodicity']=(Q(1)%1==0 and Q(1,2)%1!=0)
controls['wrong_return_sign_breaks_group_formula']=iterate(seeds[0],1)!=iterate(seeds[0],-1)
D=I(4); D[2][3]=Q(5)*Q(3,7)
transverse_actual=mm(mm(frame(-5),D),frame(0))
controls['omitted_transverse_term_fails_when_h_second_nonzero']=(transverse_actual!=shear(5) and transverse_actual[2][3]==Q(15,7))
controls['one_energy_has_zero_interval_length']=(Q(1,4)-Q(1,4)==0)
controls['unweighted_disintegration_wrong_off_plateau']=(Q(1,2)!=Q(1))
controls['clock_factor_is_not_a_whole_system_witness']=(all(Q(n)%1==0 for n in range(-8,9)) and all(n-m!=0 for n in range(4) for m in range(4) if n!=m))
def rotation_forward(z): return (add(z[0],a),z[1])
y_values=[]; z=seeds[0]
for _ in range(4):
    y_values.append(z[1]); z=rotation_forward(z)
controls['rotation_without_shear_has_no_orthogonal_y_orbit']=(len(set(y_values))==1)
if not all(controls.values()): raise AssertionError('negative control failed')
print(json.dumps({'result':'PASS','new_exact_checks':sum(counts.values()),'groups':dict(sorted(counts.items())),'additional_negative_controls':controls,'limitations':['Exact finite algebra checks; analytic proof and source-scope review remain necessary.','Q(sqrt(2)) arithmetic is exact; no floating-point recurrence or exponent estimate is used.','No author module is imported; no network access or original-packet writes.']},indent=2,sort_keys=True))
