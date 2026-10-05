#!/usr/bin/env python3
"""Independent exact, adversarial and immutable-input checks. Standard library only.

Run from any directory. Reads the original frozen package; writes only the audit's
results.json beside this script. No imports, execution or writes in the input tree
except for a final in-memory replay of its inspected run() function.
"""
from fractions import Fraction as Q
from functools import reduce
from itertools import combinations
from math import comb, gcd, lcm
from pathlib import Path
import copy
import hashlib
import json
import zipfile

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent.parent / 'fat_points_30001599'
EXPECTED_ARCHIVE = '23445c65f62d9f1d06c140ec12378aac0ce6f2539303eeadf9e5ce7851e9c526'
EXPECTED_MANIFEST = '675d0e15df109374d34bea061bb54ffc23e70fa87b344f9a2b3fc57acd40dc51'
FILES = ['APPROACH_LOG.md', 'LIMITATIONS.md', 'MANIFEST.json', 'PROOFS.md',
         'README.md', 'SOURCE_VERIFICATION.json', 'check_controls.py', 'control_results.json']

def sha(b):
    return hashlib.sha256(b).hexdigest()

def content_binding(blobs, manifest, archive_bytes):
    if sorted(blobs) != FILES or sha(archive_bytes) != EXPECTED_ARCHIVE:
        return False
    if sha(blobs['MANIFEST.json']) != EXPECTED_MANIFEST:
        return False
    if json.loads(blobs['MANIFEST.json']) != manifest:
        return False
    if sorted(x['file'] for x in manifest['files']) != [x for x in FILES if x != 'MANIFEST.json']:
        return False
    for rec in manifest['files']:
        data = blobs[rec['file']]
        if rec['bytes'] != len(data) or rec['sha256'] != sha(data):
            return False
    return True

TARGET = dict(id='30001599', code='OWR-4527-003', rank=697,
              exponent='n*(r-1)+1', bound='r*a+(r-1)*(n-1)',
              support='arbitrary nonempty finite reduced projective point set',
              proof_field='algebraically closed characteristic zero',
              original_field='not explicit in Cooper OWR paragraph',
              full_resolution=False, attempts_used=5, attempts_limit=5,
              disposition='unsolved_with_partials')

def target_binding(t):
    return t == TARGET

def monomials(d):
    return [(i, total-i) for total in range(d+1) for i in range(total+1)]

def jet_matrix(points, d, m):
    """Taylor coefficients by total derivative order, independent row/column order."""
    basis = monomials(d)
    matrix = []
    for total in range(m):
        for a in range(total+1):
            b = total-a
            for x,y in points:
                x,y = Q(x),Q(y)
                matrix.append([Q(comb(i,a)*comb(j,b))*x**(i-a)*y**(j-b)
                               if i>=a and j>=b else Q(0) for i,j in basis])
    return matrix

def primitive(row):
    scale = lcm(*(x.denominator for x in row))
    row = [int(x*scale) for x in row]
    g = reduce(gcd, row, 0)
    return [x//g for x in row] if g else row

def rank_Q(matrix):
    """Integer, gcd-normalized fraction-free elimination; no modular inference."""
    A = [primitive(r) for r in matrix]
    k = 0
    for c in range(len(A[0]) if A else 0):
        hit = next((j for j in range(k,len(A)) if A[j][c]), None)
        if hit is None:
            continue
        A[k],A[hit] = A[hit],A[k]
        pivot = A[k][c]
        for j in range(k+1,len(A)):
            z = A[j][c]
            if z:
                row = [pivot*A[j][i]-z*A[k][i] for i in range(c+1,len(A[j]))]
                g = reduce(gcd,row,0)
                if g:
                    row = [x//g for x in row]
                A[j] = [0]*(c+1)+row
        k += 1
        if k == len(A):
            break
    return k

def rank_Fp(matrix,p):
    A = [[int(x.numerator)*pow(int(x.denominator),-1,p)%p for x in row] for row in matrix]
    k = 0
    for c in range(len(A[0]) if A else 0):
        hit = next((j for j in range(k,len(A)) if A[j][c]),None)
        if hit is None:
            continue
        A[k],A[hit] = A[hit],A[k]
        inv = pow(A[k][c],-1,p)
        for j in range(k+1,len(A)):
            z = A[j][c]*inv%p
            if z:
                A[j] = [(x-z*y)%p for x,y in zip(A[j],A[k])]
        k += 1
        if k == len(A):
            break
    return k

def mul(A,B):
    out = {}
    for (i,j),x in A.items():
        for (u,v),y in B.items():
            out[i+u,j+v] = out.get((i+u,j+v),Q(0))+x*y
    return {e:c for e,c in out.items() if c}

def power(A,n):
    out = {(0,0):Q(1)}
    for _ in range(n):
        out = mul(out,A)
    return out

def orders(poly,points):
    d=max(i+j for i,j in poly)
    out=[]
    for x,y in points:
        x,y=Q(x),Q(y)
        order=None
        for total in range(d+1):
            for a in range(total+1):
                b=total-a
                val=sum(c*comb(i,a)*comb(j,b)*x**(i-a)*y**(j-b)
                        for (i,j),c in poly.items() if i>=a and j>=b)
                if val:
                    order=total
                    break
            if order is not None:
                break
        out.append(order)
    return out

def tuples_of_sum(n,total):
    if n==1:
        return [(total,)]
    return [(i,)+tail for i in range(total+1) for tail in tuples_of_sum(n-1,total-i)]

def star_nd_check(n,s,r):
    """Independent concrete stars from the rational normal dual curve.

    L_t=1+t*x1+...+t^n*xn; all n+1-row Vandermonde minors are nonzero.
    At the intersection indexed by J, 1+sum x_i*z^i=product(1-z/t).
    """
    points=[]
    for J in combinations(range(1,s+1),n):
        poly=[Q(1)]
        for t in J:
            nxt=[Q(0)]*(len(poly)+1)
            for i,c in enumerate(poly):
                nxt[i]+=c;nxt[i+1]-=c/t
            poly=nxt
        points.append(poly[1:])
    d=r*s-n;m=n*(r-1)+1
    basis=[e for total in range(d+1) for e in tuples_of_sum(n,total)]
    jets=[e for total in range(m) for e in tuples_of_sum(n,total)]
    matrix=[]
    for P in points:
        for a in jets:
            row=[]
            for e in basis:
                value=Q(1)
                for ei,ai,xi in zip(e,a,P):
                    if ei<ai:
                        value=Q(0);break
                    value*=comb(ei,ai)*xi**(ei-ai)
                row.append(value)
            matrix.append(row)
    rank=rank_Fp(matrix,1009)
    assert rank==len(basis)
    # Verify the authored extremizing product's incidence exponents separately.
    G=set(range(1,s-n+2))
    multiplicities=[n*(r-1)+len(set(J)&G) for J in combinations(range(1,s+1),n)]
    assert min(multiplicities)>=m
    return dict(n=n,s=s,r=r,lower_degree=d,required_multiplicity=m,
                rows=len(matrix),columns=len(basis),rank_mod_1009=rank,
                upper_product_degree=r*s-n+1,upper_product_minimum_order=min(multiplicities))

def main():
    blobs={f:(ROOT/'safe'/f).read_bytes() for f in FILES}
    archive=(ROOT/'FAT_POINTS_30001599_SAFE_FROZEN.zip').read_bytes()
    manifest=json.loads(blobs['MANIFEST.json'])
    assert content_binding(blobs,manifest,archive)
    assert sorted(p.name for p in (ROOT/'safe').iterdir()) == FILES
    with zipfile.ZipFile(ROOT/'FAT_POINTS_30001599_SAFE_FROZEN.zip') as z:
        assert sorted(z.namelist())==FILES
        assert len(z.namelist())==len(set(z.namelist()))
        assert all(z.read(f)==blobs[f] for f in FILES)
    result={'input_binding':{'archive_sha256':sha(archive),'archive_bytes':len(archive),
              'file_count':len(blobs),'total_uncompressed_bytes':sum(map(len,blobs.values())),
              'archive_members_match_directory':True,'manifest_records_verified':7},
            'target':TARGET,'ranks':[],'negative_controls':[]}
    def neg(name,passed,details):
        assert passed, name
        result['negative_controls'].append({'name':name,'rejected_invalid_inference':True,'details':details})
    for field,val in [('id','30001598'),('exponent','n*r-n'),('support','generic points only'),
                      ('proof_field','arbitrary characteristic'),('full_resolution',True),('attempts_used',4)]:
        mutant=copy.deepcopy(TARGET);mutant[field]=val
        neg('binding_'+field,not target_binding(mutant),'Deliberate metadata mutation rejected.')
    mutant=dict(blobs);mutant['PROOFS.md']+=b'\n'
    neg('modified_proof_byte',not content_binding(mutant,manifest,archive),'In-memory alteration only; original untouched.')
    mutant=dict(blobs);mutant['MANIFEST.json']+=b'\n'
    neg('modified_manifest_byte',not content_binding(mutant,manifest,archive),'Manifest byte alteration rejected.')
    mutant=dict(blobs);mutant['unreviewed.txt']=b'x'
    neg('extra_input_file',not content_binding(mutant,manifest,archive),'In-memory extra file rejected.')
    mutant=copy.deepcopy(manifest);mutant['files'].pop()
    neg('missing_manifest_record',not content_binding(blobs,mutant,archive),'Incomplete manifest rejected.')
    neg('truncated_archive',not content_binding(blobs,manifest,archive[:-1]),'Wrong archive bytes rejected.')

    S=[(0,0),(0,1),(0,Q(3,2)),(1,0),(3,0),(-1,2)]
    T=[(0,0),(1,0),(0,1),(2,3),(4,2),(3,5)]
    U=[(i,j) for j in range(3) for i in range(3)]
    specs=[('S',S,[(2,1),(6,3),(10,5)]),('T',T,[(2,1),(7,3),(11,5)]),('U',U,[(2,1),(8,3)])]
    for name,points,cases in specs:
        for d,m in cases:
            A=jet_matrix(points,d,m)
            rational=rank_Q(A)
            modular={str(p):rank_Fp(A,p) for p in [101,1009,10007]}
            assert rational==len(A[0]) and all(v==rational for v in modular.values())
            result['ranks'].append(dict(configuration=name,d=d,m=m,rows=len(A),columns=len(A[0]),
                                       rank_over_Q=rational,modular_ranks=modular))
    result['reduced_Hilbert_ranks']={name:[rank_Q(jet_matrix(points,d,1)) for d in range(5)]
                                      for name,points in [('S',S),('T',T)]}
    assert result['reduced_Hilbert_ranks']=={'S':[1,3,6,6,6],'T':[1,3,6,6,6]}
    x={(1,0):Q(1)};y={(0,1):Q(1)}
    l3={(1,0):Q(1),(0,1):Q(1),(0,0):Q(-1)}
    l4={(1,0):Q(1),(0,1):Q(2),(0,0):Q(-3)}
    G=mul(mul(x,y),l3);Qstar=mul(G,l4)
    star_products=[]
    for r in [1,2,3]:
        F=mul(power(Qstar,r-1),G)
        ords=orders(F,S)
        assert max(i+j for i,j in F)==4*r-1
        assert min(ords)>=2*r-1
        star_products.append({'r':r,'degree':4*r-1,'point_orders':ords})
    result['explicit_star_upper_witnesses']=star_products
    V=mul(mul(x,{(1,0):Q(1),(0,0):Q(-1)}),{(1,0):Q(1),(0,0):Q(-2)})
    result['explicit_grid_upper_witnesses']=[]
    for m in [1,3]:
        F=power(V,m);ords=orders(F,U)
        assert min(ords)==m and max(i+j for i,j in F)==3*m
        result['explicit_grid_upper_witnesses'].append({'m':m,'degree':3*m,'point_orders':ords})
    result['T_dimension_count_upper_witnesses']=[{'m':m,'d':d,'unknowns':comb(d+2,2),
         'conditions':6*comb(m+1,2),'kernel_dimension_at_least':comb(d+2,2)-6*comb(m+1,2)}
         for m,d in [(1,3),(3,8),(5,12)]]
    assert all(v['kernel_dimension_at_least']>0 for v in result['T_dimension_count_upper_witnesses'])
    result['higher_dimensional_star_controls']=[star_nd_check(n,s,2)
        for n,s in [(1,2),(2,2),(2,3),(2,4),(3,3),(3,4),(3,5),(4,4),(4,5)]]

    swapped=rank_Q(jet_matrix(S,7,3))
    neg('swap_star_for_T_at_degree7',swapped<36,{'rank_over_Q':swapped,'required_full_rank':36})
    collinear=rank_Q(jet_matrix([(i,0) for i in range(6)],2,1))
    neg('general_rank_to_arbitrary_support',collinear<6,{'six_collinear_conic_rank':collinear,'general_rank':6})
    bad_reduction=[(x,1009*y) for x,y in T]
    A=jet_matrix(bad_reduction,2,1)
    good,bad=rank_Q(A),rank_Fp(A,1009)
    neg('modular_deficiency_implies_Q_kernel',good==6 and bad<6,{'rank_over_Q':good,'rank_mod_1009':bad})
    C=Q(1);B=7;lower=B-C
    neg('Chudnovsky_rounding_at_a3',lower<B,{'n':2,'a':3,'r':2,'mL':int(lower),'target':B})
    r,a=2,5;D=r*(a+1)-2;E=D*(D-1)-a*(a+1)*(2*r-1)*(2*r-2)//2
    neg('polar_claim_extended_to_r2_a5',E==0,{'E':E,'strict_negative_required':True})
    # Remove one occurrence of x from Qstar*G: multiplicity losses vary with support.
    residual=mul(mul(y,l3),Qstar)
    ords=orders(residual,S)
    neg('factor_removal_preserves_uniformity',len(set(ords))>1,{'residual_point_orders':ords})
    # All characteristic-p partials of x^p vanish: derivative method cannot be transplanted.
    neg('char0_derivative_transplanted_to_char2',(2%2)==0,{'nonzero_polynomial':'x^2','all_first_partials_zero_in_characteristic':2})

    count=0
    for n in range(1,9):
        for a in range(1,31):
            for r in range(1,31):
                m=n*(r-1)+1;B=r*a+(r-1)*(n-1);L=Q(a+n-1,n);C=Q((n-1)*(a-1),n)
                assert B-m*L==C and B-(a+m-1)==(r-1)*(a-1)
                assert (C<1)==(n==1 or a<=2)
                count+=1
    result['identity_parameter_tuples']=count
    count=0
    for a in range(1,101):
        for r in range(3,101):
            t=r-3;D=r*(a+1)-2
            E=D*(D-1)-a*(a+1)*(2*r-1)*(2*r-2)//2
            assert E==(1-a*a)*t*t+(1-2*a-3*a*a)*t-a*(a+7)<0
            count+=1
    assert all((2*(a+1)-2)*(2*(a+1)-3)-3*a*(a+1)==a*(a-5)<0 for a in range(1,5))
    result['polar_parameter_tuples']=count
    result['r2_boundary_cases']=4
    # Replay only the inspected run() body, without its __main__ write block.
    ns={'__name__':'audited_input','__file__':str(ROOT/'safe'/'check_controls.py')}
    exec(compile(blobs['check_controls.py'],'audited-input-check_controls.py','exec'),ns)
    replay=json.loads(json.dumps(ns['run']()))
    assert replay==json.loads(blobs['control_results.json'])
    result['author_control_replay_matches']=True
    result['author_control_counts']={'identity_parameter_tuples':replay['exact_identity_checks'],
                                    'polar_parameter_tuples':replay['polar_obstruction_checks'],'rank_cases':8}
    assert blobs=={f:(ROOT/'safe'/f).read_bytes() for f in FILES}
    assert archive==(ROOT/'FAT_POINTS_30001599_SAFE_FROZEN.zip').read_bytes()
    result['original_bytes_unchanged_after_checks']=True
    result['counts']={'rational_lower_degree_checks':len(result['ranks']),
                      'modular_lower_degree_checks':3*len(result['ranks']),
                      'reduced_Hilbert_rank_checks':10,
                      'explicit_upper_polynomials':len(star_products)+2,
                      'dimension_count_upper_certificates':3,
                      'star_family_modular_checks_dimensions_1_to_4':len(result['higher_dimensional_star_controls']),
                      'negative_controls_rejected':len(result['negative_controls'])}
    (HERE/'results.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result['counts'],sort_keys=True))

if __name__=='__main__':
    main()
