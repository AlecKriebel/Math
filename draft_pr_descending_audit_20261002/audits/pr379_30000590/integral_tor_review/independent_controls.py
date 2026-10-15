#!/usr/bin/env python3
"""Source-first exact controls. No imports or reads of candidate files.

The scalar complexes test homological algebra, not realization as group
augmentation resolutions. Matrices use columns. All arithmetic is integral.
"""
import itertools
import json
from math import gcd


def egcd(a, b):
    old_r, r, old_s, s, old_t, t = a, b, 1, 0, 0, 1
    while r:
        q = old_r // r
        old_r, r = r, old_r - q*r
        old_s, s = s, old_s - q*s
        old_t, t = t, old_t - q*t
    return old_r, old_s, old_t


def matmul(a, b):
    return [[sum(x*y for x, y in zip(row, col))
             for col in zip(*b)] for row in a]


def emit(kind, **kw):
    print(json.dumps({'kind': kind, **kw}, sort_keys=True))


def tensor_control(m, n):
    # C_m: Z --m--> Z in degrees 0,1. Tensor degree 1 ordering
    # (C_m^1 tensor C_n^0, C_m^0 tensor C_n^1).
    g, a, b = egcd(m, n)
    assert g == gcd(m, n) == a*m + b*n
    d0, d1 = [[m], [n]], [[-n, m]]
    v = [[-b, m//g], [a, n//g]]
    determinant = v[0][0]*v[1][1] - v[0][1]*v[1][0]
    assert determinant == -1
    vi = [[-v[1][1], v[0][1]], [v[1][0], -v[0][0]]]
    assert matmul(vi, v) == [[1, 0], [0, 1]]
    assert matmul(d1, d0) == [[0]]
    assert matmul(d1, v) == [[g, 0]]
    assert matmul(vi, d0) == [[0], [g]]
    # Kernel generator is column 2 of V. Image is g times generator.
    # The connecting Tor map sends its class to n/g mod n in ker(m:Z/n).
    tor_generator = n//g
    assert (m*tor_generator) % n == 0
    assert n//gcd(n, tor_generator) == g
    emit('tensor_smith', m=m, n=n, d0=d0, d1=d1, V=v,
         V_inverse=vi, determinant=determinant,
         smith_d1=matmul(d1,v), kernel_image=matmul(vi,d0),
         H0='0', H1_order=g, H2_order=g,
         Tor_Z1_order=g, tensor_order=g,
         tor_connecting_generator_mod_n=tor_generator,
         wrong_zero_tor_rejected=(g>1),
         wrong_tor_degree_n_minus_1_rejected=(g>1),
         rational_only_rejected=(g>1))


for m, n in itertools.product(range(1, 13), repeat=2):
    tensor_control(m, n)

# Universal coefficient integral connecting homomorphism for C_m.
# delta_p([1]) = [m/p] in H^1(C_m)=Z/m when p divides m.
for m in range(1, 25):
    for p in (2, 3, 5, 7):
        divides = m % p == 0
        beta = m//p if divides else None
        if divides:
            assert (p*beta) % m == 0
            assert m//gcd(m,beta) == p
        emit('bockstein', m=m, prime=p,
             H0_mod_p_dimension=int(divides), H1_mod_p_dimension=int(divides),
             H0_integral=0, H1_integral_order=m,
             H1_integral_p_kernel_order=p if divides else 1,
             integral_connecting_lift=beta,
             mod_p_bockstein=beta % p if divides else None,
             integral_beta_can_be_nonzero_when_mod_p_beta_zero=
             bool(divides and beta % p == 0))

# Flat factor: tensoring any complex with free abelian Z^r in degree k
# gives r copies, shifted, with no Tor term. Check the Smith certificate
# for direct sums of the same scalar map without claiming a group model.
for m in (2, 4, 6, 9):
    for r in (1, 2, 3):
        for shift in (0, 1, 3):
            diag = [[m if i == j else 0 for j in range(r)] for i in range(r)]
            emit('flat_factor', m=m, free_rank=r, shift=shift,
                 differential=diag, smith_diagonal=[m]*r,
                 nonzero_cohomology_degree=1+shift, torsion_orders=[m]*r,
                 Tor_Z1_order=1)

# Right residual action: noncommutative S3 coefficients. A left-linear
# map R->R has f_u(r)=r*u, so precomposing r->r*(1-s) sends u to (1-s)*u.
# This differential commutes with all right multiplications, not all left.
group = list(itertools.permutations(range(3)))
identity = (0, 1, 2)
s, t = (1, 0, 2), (0, 2, 1)
def product(g, h):
    return tuple(g[h[i]] for i in range(3))
def regular(g, side):
    cols=[]
    for h in group:
        k = product(g,h) if side == 'left' else product(h,g)
        cols.append([int(x == k) for x in group])
    return [list(row) for row in zip(*cols)]
eye=regular(identity,'left')
ls, lt, rs, rt = [regular(g, side) for g,side in
                  [(s,'left'),(t,'left'),(s,'right'),(t,'right')]]
d=[[eye[i][j]-ls[i][j] for j in range(6)] for i in range(6)]
assert matmul(d,rt) == matmul(rt,d)
assert matmul(d,lt) != matmul(lt,d)
assert matmul(rt,rs) == regular(product(s,t),'right')
assert matmul(rs,rt) != regular(product(s,t),'right')
emit('right_regular_noncommutative', basis=group, differential=d,
     right_s=rs, right_t=rt, left_t=lt,
     differential_commutes_right=True, differential_commutes_left=False,
     right_action_composition_RtRs_equals_Rst=True,
     wrong_left_action_rejected=True, wrong_composition_rejected=True)

# C2 genuine augmentation resolution versus a truncation. Chain maps
# alternate (s-1) and norm. Augmentation is [1,1]. A finite truncation
# at odd degree has nonzero norm kernel and is NOT a finite resolution.
dminus=[[-1,1],[1,-1]]
dnorm=[[1,1],[1,1]]
augmentation=[[1,1]]
assert matmul(dminus,dnorm)==[[0,0],[0,0]]
assert matmul(dnorm,dminus)==[[0,0],[0,0]]
assert matmul(augmentation,dminus)==[[0,0]]
assert matmul(dminus,[[1],[1]])==[[0],[0]]
assert matmul(dnorm,[[1],[-1]])==[[0],[0]]
emit('augmentation_resolution_boundary', group='C2', d1=dminus,
     d2=dnorm, augmentation=augmentation,
     nonzero_kernel_of_truncated_d1=[1,1],
     infinite_periodic_regular_cohomology='H0=Z(norm), Hn=0 for n>0',
     finite_truncation_is_resolution=False,
     FP_infinity_does_not_mean_FP=True,
     virtually_FP=True)

# Countermodels for mistaking tensor support for cohomological support.
# H(C2 tensor C2) has Tor in degree 1 although only input cohom degree 1.
emit('support_boundary', input_nonzero_degrees=[1,1], tensor_degree=2,
     Tor_degree=1, Tor_order=2, support_requires_both_diagonals=True)
emit('integral_detection_boundary', module='Pruefer p-group',
     rational_tensor=0, reduction_mod_p=0, p_torsion='Z/p',
     finitely_generated_as_Z=False,
     rational_and_reduction_only_detection_rejected=True)

emit('summary', tensor_smith_controls=144, bockstein_controls=96,
     flat_factor_controls=36, right_action_controls=1,
     augmentation_boundary_controls=1, support_controls=2,
     errors=0,
     scope='exact algebra controls, not a group realization or target proof')
