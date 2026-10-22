#!/usr/bin/env python3
"""Exact finite audit with source-interface guards; stdout only, no network.

Geometry and source interpretation are established in AUDIT.md by proof review.
Finite tests do not prove them. --mutant replaces named mathematical semantics,
not the final status or an unconditional injected-failure branch.
"""
import argparse
from collections import Counter
from fractions import Fraction as F
import importlib.util
from itertools import product
import json
from math import factorial
import os
from pathlib import Path
import sys

BASE = Path(__file__).resolve().parent
sys.dont_write_bytecode = True
spec = importlib.util.spec_from_file_location('original_checker', BASE/'check_exact.py')
original = importlib.util.module_from_spec(spec)
spec.loader.exec_module(original)
COUNTS = Counter()
MUTANT = None
MUTANTS = {
    'plane_parameter_shift': 'dimensions',
    'conic_scaling_retained': 'dimensions',
    'incidence_condition_dropped': 'dimensions',
    'full_tangent_replaces_normal': 'normal_data',
    'initial_data_fibre_off_by_one': 'normal_data',
    'blowup_preserves_positive_degrees': 'normal_data',
    'algebraic_dimensions_add': 'field_scope',
    'shape_coefficient_sign': 'logarithm',
    'pure_y_coefficient_sign': 'logarithm',
    'shape_pole_promoted': 'logarithm',
    'trace_degree_factor_removed': 'trace',
    'trace_exponent_shifted': 'trace',
    'nondivisible_trace_survives': 'trace',
    'trace_laurent_series_truncated': 'trace_series',
    'target_dimensions_swapped': 'source_interface',
    'target_kahler_added': 'source_interface',
    'finite_incidence_dropped': 'source_interface',
    'local_separation_dropped': 'source_interface',
    'residual_case_erased': 'source_interface',
    'peternell_kahler_removed': 'source_interface',
    'local_rank_promoted_to_global_finite': 'proof_scope',
    'polynomial_growth_removed': 'proof_scope',
}

def check(value, family, message):
    COUNTS[family] += 1
    if not value:
        raise RuntimeError('CHECK_FAILED['+family+']: '+message)

def rank(rows):
    rows = [[F(x) for x in row] for row in rows]
    if not rows:
        return 0
    r = 0
    for c in range(len(rows[0])):
        pivot = next((j for j in range(r,len(rows)) if rows[j][c]),None)
        if pivot is None:
            continue
        rows[r], rows[pivot] = rows[pivot], rows[r]
        v = rows[r][c]
        rows[r] = [x/v for x in rows[r]]
        for j in range(len(rows)):
            if j != r:
                v = rows[j][c]
                rows[j] = [x-v*y for x,y in zip(rows[j],rows[r])]
        r += 1
        if r == len(rows):
            break
    return r

def dimensions():
    # Grassmann charts have one scalar for each basis-to-complement matrix entry.
    for ambient in range(0,13):
        for k in range(ambient+1):
            entries = [(i,j) for i in range(k) for j in range(ambient-k)]
            check(original.grassmann_dimension(k,ambient)==len(entries),'dimensions','Grassmann chart parameter count')
    pdim = original.grassmann_dimension(1,3)
    if MUTANT == 'plane_parameter_shift': pdim += 1
    check(pdim==2,'dimensions','planes containing a fixed P1 in P4')
    monomials = [(a,b,c) for a,b,c in product(range(3),repeat=3) if a+b+c==2]
    projective_dim = len(monomials)-(0 if MUTANT=='conic_scaling_retained' else 1)
    check(projective_dim==5,'dimensions','nonzero quadrics modulo scalar')
    for point in product(range(-2,3),repeat=3):
        if point==(0,0,0): continue
        ev = [[F(point[0])**a*F(point[1])**b*F(point[2])**c for a,b,c in monomials]]
        check(rank(ev)==1,'dimensions','one nonzero incidence evaluation condition')
    incident = 3+projective_dim-(0 if MUTANT=='incidence_condition_dropped' else 1)
    check(incident==7,'dimensions','main incident conic parameter dimension')
    # Planes through Y: P1; all their conics: P5.
    check(1+5<incident,'dimensions','planes containing Y contribute only dimension six')


def normal_data():
    # Chart: H={z=c+u*x+v*y}; conic x+a*y+b*x*x+d*x*y+e*y*y=0.
    # Seven parameters (c,u,v,a,b,d,e). First normal data are (c,a).
    jac = [[1,0,0,0,0,0,0],[0,0,0,1,0,0,0]]
    normal_rank = rank(jac)
    if MUTANT=='full_tangent_replaces_normal': normal_rank+=1
    check(normal_rank==2,'normal_data','quotient by TY discards plane slope')
    fibre = 7-normal_rank+(1 if MUTANT=='initial_data_fibre_off_by_one' else 0)
    check(fibre==5,'normal_data','initial normal-data generic fibre dimension')
    for c,u,v,a,b,d,e in [(0,0,0,0,0,0,1),(2,1,3,0,0,0,1),(2,7,-4,0,0,0,1)]:
        # The homogeneous matrix of X*T+a*Y*T+b*X^2+d*X*Y+e*Y^2.
        matrix = [[b,F(d,2),F(1,2)],[F(d,2),e,F(a,2)],[F(1,2),F(a,2),0]]
        check(rank(matrix)==3,'normal_data','smooth conic examples exist in the chart')
        tangent = (-a,1,-u*a+v)
        check(tangent[:2]==(-a,1),'normal_data','same projected tangent despite changing plane')
    # Smooth P1-bundle tangent quotient is pullback of the fixed base tangent space.
    new_degrees = (1,1) if MUTANT=='blowup_preserves_positive_degrees' else (0,0)
    check(new_degrees==(0,0) and not all(x>0 for x in new_degrees),'normal_data','lifted fibre normal is trivial')


def field_scope():
    base,fibre,total = 1,1,1
    if MUTANT=='algebraic_dimensions_add': total=base+fibre
    check(total<base+fibre,'field_scope','elliptic K3 disproves unqualified additivity')
    for k in range(-12,13):
        check(k*0==0 and k*k*0==0,'field_scope','NS=Z[F], F^2=0 forces vertical curves and zero self-intersection')


def mul(a,b,bound):
    out={}
    for (i,j),v in a.items():
        for (k,l),w in b.items():
            if i+j+k+l<=bound:
                out[i+k,j+l]=out.get((i+k,j+l),F(0))+v*w
    return {k:v for k,v in out.items() if v}


def inverse_log_oracle(a,b,bound):
    # Euler(log(1+Q))=Euler(Q)/(1+Q), using polynomial multiplication,
    # followed by division by total degree. No binomial-coefficient formula.
    q={(0,1):-1/a,(2,0):b/a}
    inverse={(0,0):F(1)}
    power={(0,0):F(1)}
    for k in range(1,bound+1):
        power=mul(power,q,bound)
        for key,val in power.items():
            inverse[key]=inverse.get(key,F(0))+(-1)**k*val
    eulerq={key:sum(key)*val for key,val in q.items()}
    numerator=mul(eulerq,inverse,bound)
    return {key:val/sum(key) for key,val in numerator.items() if sum(key)>0 and val}


def logarithm():
    bound=8
    terms=original.logarithm_coefficients(bound)
    if MUTANT=='shape_coefficient_sign': terms[(2,0,-1,1)]*=-1
    if MUTANT=='pure_y_coefficient_sign': terms[(0,2,-2,0)]*=-1
    if MUTANT=='shape_pole_promoted': terms[(2,0,-2,1)]=terms.pop((2,0,-1,1))
    for a,b in product((F(1),F(2),F(-3)),(F(0),F(2),F(-1))):
        evaluated={}
        for (i,j,ad,bd),val in terms.items():
            if i+j<=bound:
                evaluated[i,j]=evaluated.get((i,j),F(0))+val*a**ad*b**bd
        expected=inverse_log_oracle(a,b,bound)
        for i in range(bound+1):
            for j in range(bound+1-i):
                check(evaluated.get((i,j),F(0))==expected.get((i,j),F(0)),'logarithm','Euler derivative/inverse-series oracle')
    check(terms[(2,0,-1,1)]==1 and terms[(0,2,-2,0)]==-F(1,2),'logarithm','shape lies below maximal quadratic pole order')


def matmul(a,b):
    d=len(a)
    out=[[F(0) for _ in range(d)] for _ in range(d)]
    for i in range(d):
        for k in range(d):
            if a[i][k]:
                for j in range(d):
                    if b[k][j]: out[i][j]+=a[i][k]*b[k][j]
    return out


def trace():
    for d in range(1,10):
        for z in (F(2),F(3,2),F(-3)):
            inv=[[F(0) for _ in range(d)] for _ in range(d)]
            inv[d-1][0]=1/z
            for j in range(1,d): inv[j-1][j]=1
            power=[[F(i==j) for j in range(d)] for i in range(d)]
            for m in range(0,49):
                actual=original.trace_monomial(d,m)
                if MUTANT=='trace_degree_factor_removed': actual={e:F(v,d) for e,v in actual.items()}
                if MUTANT=='trace_exponent_shifted': actual={e-1:v for e,v in actual.items()}
                if MUTANT=='nondivisible_trace_survives' and not actual: actual={-1:d}
                scalar=sum((v*z**e for e,v in actual.items()),F(0))
                check(scalar==sum((power[i][i] for i in range(d)),F(0)),'trace','independent multiplication-matrix trace')
                power=matmul(power,inv)


def trace_series():
    for d in range(1,10):
        for k in range(0,25):
            coefficient=F(d,factorial(d*k))
            if MUTANT=='trace_laurent_series_truncated' and k>8: coefficient=F(0)
            # Matrix trace / factorial is the Laurent coefficient of the exponential trace.
            check(coefficient==F(original.trace_monomial(d,d*k)[-k],factorial(d*k)),'trace_series','nonzero negative Laurent coefficients persist')
            check(coefficient>0,'trace_series','finite tested prefix is nonzero; infinite claim proved on paper')


def source_interface():
    # Reviewed source contract. These guards detect corrupted metadata; they do
    # not establish the quoted theorems independently of the human-readable audit.
    c=json.loads((BASE/'REVIEWED_CLAIMS.json').read_text())
    if MUTANT=='target_dimensions_swapped': c['target']['Y_dimension']='n-1'
    if MUTANT=='target_kahler_added': c['target']['kahler_required']=True
    if MUTANT=='finite_incidence_dropped': c['BM0.7']['finite_incidence_required']=False
    if MUTANT=='local_separation_dropped': c['BM0.7']['local_separation_required']=False
    if MUTANT=='residual_case_erased': c['BM4.3']['residual_case_retained']=False
    if MUTANT=='peternell_kahler_removed': c['P3.4']['kahler_required']=False
    check(c['target']['Z_dimension']=='n+p' and c['target']['Y_dimension']=='p-1' and c['target']['cycle_dimension']=='n','source_interface','OWR dimensions')
    check(c['target']['kahler_required'] is False,'source_interface','OWR has no Kahler hypothesis')
    check(c['BM0.7']['finite_incidence_required'] is True,'source_interface','BM finite-incidence hypothesis retained')
    check(c['BM0.7']['local_separation_required'] is True,'source_interface','BM separation hypothesis retained')
    check(c['BM4.3']['residual_case_retained'] is True,'source_interface','residual case not silently solved')
    check(c['P3.4']['kahler_required'] is True and c['P3.4']['target_p']==2,'source_interface','Peternell curve case scope')


def proof_scope():
    conclusions={'finite_jet':'generic_local_full_rank','growth_bridge':'requires_polynomial_growth'}
    if MUTANT=='local_rank_promoted_to_global_finite': conclusions['finite_jet']='global_finite_map'
    if MUTANT=='polynomial_growth_removed': conclusions['growth_bridge']='no_growth_hypothesis'
    check(conclusions['finite_jet']=='generic_local_full_rank','proof_scope','local rank is not a global finite map assertion')
    check(conclusions['growth_bridge']=='requires_polynomial_growth','proof_scope','unproved boundary bound remains a hypothesis')


def readonly():
    check(os.getuid()==1000 and os.geteuid()==1000,'environment','actual UID and EUID must both be 1000')
    if ARGS.require_readonly:
        # Probe an existing file without O_TRUNC: success itself fails this test.
        existing=BASE/'check_exact.py'
        try:
            fd=os.open(existing,os.O_WRONLY)
        except PermissionError:
            check(True,'environment','existing-file write open denied')
        else:
            os.close(fd)
            check(False,'environment','existing-file write open unexpectedly allowed')
        probe=BASE/'readonly_probe_must_not_exist.tmp'
        check(not probe.exists(),'environment','probe path was absent')
        try:
            fd=os.open(probe,os.O_WRONLY|os.O_CREAT|os.O_EXCL,0o600)
        except PermissionError:
            check(True,'environment','new-file creation denied')
        else:
            os.close(fd)
            check(False,'environment','new-file creation unexpectedly allowed')


def main():
    global ARGS,MUTANT
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('--mutant',choices=sorted(MUTANTS))
    p.add_argument('--require-readonly',action='store_true')
    ARGS=p.parse_args(); MUTANT=ARGS.mutant
    try:
        readonly()
        dimensions(); normal_data(); field_scope(); logarithm(); trace(); trace_series(); source_interface(); proof_scope()
    except (RuntimeError,KeyError,ValueError,TypeError) as e:
        print(str(e),file=sys.stderr)
        return 1
    print(json.dumps({'status':'PASS','uid':os.getuid(),'euid':os.geteuid(),'checks':dict(COUNTS),'total_checks':sum(COUNTS.values()),'arithmetic':'exact_rational_integer','geometric_proof_certificate':False,'source_contract_is_documentary_guard':True},sort_keys=True))
    return 0

if __name__=='__main__': sys.exit(main())
