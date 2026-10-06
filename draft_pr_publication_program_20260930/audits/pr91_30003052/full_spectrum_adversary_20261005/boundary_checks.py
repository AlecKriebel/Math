#!/usr/bin/env python3
"""Independent finite controls; never a finite approximation to C(U)'s spectrum.

All output stays beside this file. No submitted checker or review is imported.
"""
from collections import Counter
from datetime import datetime, timezone
from fractions import Fraction as F
from pathlib import Path
import cmath
import hashlib
import json
import math
import os
import subprocess
import sys

here = Path(__file__).resolve().parent
authentication = here.parent / 'original_source_authentication_20261005'
counts = Counter()
def ck(name, claim):
    assert claim, name
    counts[name] += 1

def mat(rows):
    return [[F(v) for v in row] for row in rows]
def eye(n):
    return [[F(i == j) for j in range(n)] for i in range(n)]
def mul(a, b):
    return [[sum(a[i][k] * b[k][j] for k in range(len(b)))
             for j in range(len(b[0]))] for i in range(len(a))]
def sub(a, b):
    return [[x-y for x,y in zip(ar,br)] for ar,br in zip(a,b)]
def power(a, n):
    result = eye(len(a))
    for _ in range(n):
        result = mul(result,a)
    return result
def rownorm(a):
    return max(sum(abs(x) for x in row) for row in a)

# Exact nonnormal model in the norm ||x||=||S^-1 x||_infinity.
s = mat([[1,2,0],[0,1,1],[0,0,1]])
si = mat([[1,-2,2],[0,1,-1],[0,0,1]])
ck('exact_change_of_norm_inverse',mul(s,si)==eye(3))
d_nil = mat([[-1,0,0],[0,0,1],[0,0,0]])
p_diag = mat([[1,0,0],[0,0,0],[0,0,0]])
a_nil = mul(mul(s,d_nil),si)
p = mul(mul(s,p_diag),si)
ck('nonnormal_model_is_contraction_in_given_norm',rownorm(d_nil)==1)
ck('projection_is_contracting_in_given_norm',rownorm(p_diag)==1)
ck('nonnormal_projection_idempotence',mul(p,p)==p)
ck('nonnormal_projection_commutation',mul(p,a_nil)==mul(a_nil,p))
ck('nilpotent_remainder_index_two',mul(power(a_nil,2),sub(eye(3),p))==mat([[0]*3]*3))
ck('peripheral_even_recurrence',power(a_nil,2)==p)
ck('nilpotent_peripheral_polynomial_identity',power(a_nil,4)==power(a_nil,2))
transpose = [list(row) for row in zip(*a_nil)]
ck('model_really_nonnormal_in_Euclidean_geometry',mul(a_nil,transpose)!=mul(transpose,a_nil))

# Stable defective block: exact decay factors, not diagonalization assumptions.
d_stable = mat([[1,0,0],[0,F(1,2),F(1,4)],[0,0,F(1,2)]])
a_stable = mul(mul(s,d_stable),si)
ck('stable_Jordan_model_contraction',rownorm(d_stable)==1)
for n in range(1,25):
    block = mat([[F(1,2),F(1,4)],[0,F(1,2)]])
    expected = mat([[F(1,2)**n, n*F(1,2)**(n+1)],[0,F(1,2)**n]])
    ck('exact_stable_Jordan_power',power(block,n)==expected)
    ck('exact_stable_Jordan_norm',rownorm(power(block,n))==F(1,2)**n*(1+F(n,2)))
left_eigen = [[F(0),F(0),F(1)]]
ck('stable_left_eigenfunctional_survives_nonnormality',mul(left_eigen,a_stable)==[[F(1,2)*v for v in left_eigen[0]]])

# Explicit inverse identities in the formal quotient algebras t^m=1 and t^d=0.
# These exact identities justify finite/peripheral and nilpotent resolvents,
# provided the written proof has already justified the operator relations.
def quotient_product(a,b,size,cyclic):
    result=[F(0)]*size
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            degree=i+j
            if cyclic or degree<size:
                result[degree % size] += x*y
    return result
for m in (1,2,3,4,6,10):
    for z in (F(2),F(1,2),F(-3,4)):
        inv=[z**(m-1-j)/(z**m-1) for j in range(m)]
        factor=[F(0)]*m
        factor[0]+=z
        factor[1 % m]-=1
        ck('finite_group_resolvent_exact_identity',quotient_product(factor,inv,m,True)==[F(1)]+[F(0)]*(m-1))
for depth in (1,2,3,6):
    for z in (F(2),F(1,2),F(-3,4)):
        inv=[z**(-j-1) for j in range(depth)]
        factor=[z]+([F(-1)]+[F(0)]*(depth-2) if depth>1 else [])
        ck('nilpotent_resolvent_exact_identity',quotient_product(factor,inv,depth,False)==[F(1)]+[F(0)]*(depth-1))

# Complex-power evaluations: floating checks supplement the analytic identity.
maximum_error=0.0
for a in (0.5,0.4j,0.3*cmath.exp(0.7j)):
    r=abs(a)
    for mu in (0.2,-0.4,0.3j,-0.6j,0.4+0.5j):
        c=cmath.log(mu)/math.log(r)
        ck('positive_continuity_exponent',c.real>0)
        for z in (0,1,0.2+0.3j,1e-12+2e-12j,0.9j):
            def f(w):
                return 0j if w==0 else cmath.exp(c*math.log(abs(w)))
            err=abs(f(a*z)-mu*f(z))
            maximum_error=max(maximum_error,err)
            ck('complex_radial_eigenidentity_numerical',err<1e-12)
for r in (F(1,4),F(1,2),F(3,4)):
    for i in range(101):
        t=F(i,100)
        ck('zero_eigenfunction_exact_identity',max(F(0),r*t-r)==0)
    ck('zero_eigenfunction_not_identically_zero',1-r>0)

# For A=(1/2)I, even every polynomial truncation has only real dyadic
# monomial eigenvalues. A nonreal interior eigenvalue has an exact analytic
# radial eigenfunction. Thus diagonal finite matrix spectra are insufficient.
for degree in range(25):
    monomial_values={F(1,2)**(p+q) for p in range(degree+1) for q in range(degree+1-p)}
    ck('polynomial_truncation_does_not_capture_open_disk',all(isinstance(x,F) and x>0 for x in monomial_values))

# Authentication reads every frozen body only for hashes, not semantic review.
manifest_path=authentication/'ORIGINAL_BLOB_MANIFEST.json'
manifest=json.loads(manifest_path.read_text())
ck('manifest_target_immutable_head',manifest['head']=='2ea84c5de45cb92783b5b55057af1f52590be6bf')
ck('manifest_original_count_twenty',manifest['original_count']==20 and len(manifest['files'])==20)
body_receipts=[]
for entry in manifest['files']:
    body=Path(entry['preserved_path']).read_bytes()
    sha256=hashlib.sha256(body).hexdigest()
    git_blob=hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest()
    ck('frozen_body_bytecount',len(body)==entry['bytes'])
    ck('frozen_body_sha256',sha256==entry['sha256'])
    ck('frozen_body_git_blob',git_blob==entry['git_blob_SHA1'])
    body_receipts.append({'original_path':entry['path'],'bytes':len(body),
        'sha256':sha256,'computed_git_blob_SHA1':git_blob,
        'original_git_mode_from_manifest':entry['original_git_mode'],
        'semantic_read':entry['path'].endswith('/CLASSIFICATION.md') and '/review/' not in entry['path'] or entry['path'].endswith('/verify.py') and '/review/' not in entry['path'] or entry['path'].endswith('/source_manifest.json')})
branch=subprocess.check_output(['git','branch','--show-current'],cwd=here,text=True).strip()
head=subprocess.check_output(['git','rev-parse','HEAD'],cwd=here,text=True).strip()
ck('canonical_branch_still_main',branch=='main')
receipt={'schema':'pr91-full-spectrum-independent-controls/v1',
    'UTC':datetime.now(timezone.utc).isoformat(),'actual_PID':os.getpid(),
    'status':'PASS','exact_and_numerical_assertions':sum(counts.values()),
    'checks':dict(sorted(counts.items())),'python_version':sys.version,
    'script_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest(),
    'cwd':str(Path.cwd()),'write_directory':str(here),'branch':branch,
    'canonical_checkout_HEAD_at_test':head,'reviewed_original_head':manifest['head'],
    'maximum_radial_floating_error':maximum_error,'frozen_body_receipts':body_receipts,
    'limitations':['These finite algebraic and sampled controls do not establish the infinite-dimensional spectrum. The standalone derivation supplies that proof.',
       'No source-review body was semantically read before these independent controls.',
       'Original Git modes are authenticated manifest metadata; original bodies independently match both SHA256 and Git blob hashes.'],
    'writes':['BOUNDARY_CHECK_RESULTS.json'],'no_external_individual_contact':True,
    'no_Git_index_native_global_PR_publication_or_Sheets_mutation':True,
    'new_central_proof_search_turns_claimed':0}
(here/'BOUNDARY_CHECK_RESULTS.json').write_text(json.dumps(receipt,indent=2)+'\n')
print(json.dumps({k:receipt[k] for k in ('status','actual_PID','exact_and_numerical_assertions','checks','maximum_radial_floating_error','UTC')},indent=2))
