#!/usr/bin/env python3
"""Independent finite controls and frozen-author binding; no author code imported.
No numerical calculation here certifies arbitrary-arrangement cohomology vanishing.
"""
import argparse
from fractions import Fraction
from hashlib import sha256
from itertools import combinations, product
from math import comb
from pathlib import Path
import json
import zipfile

ARCHIVE_HASH = 'e70fb6353ef5a98363dfd3cbe9aa66531a1b45ef92e90bde2c19b4e70cf99bf9'
MANIFEST_HASH = 'e999f3f7d15d19152e106ad898c8f6ec2f36b9f5ca7cedbdb067477accbfa867'
NAMES = {'PROOFS.md','README.md','REPORT.md','REPRODUCIBILITY.md','approaches.json',
         'expected_results.json','manifest.json','source_verification.json','verify.py','verify_manifest.py'}
CENSUS_EXPECTED = [32,198,544,1024,1674,2239,2464,2564,2639]
CENSUS_HASH = 'bef16e1d5bca3f1caf2cb1739bdeb160853dbd1228eb8404bb1cf613c435074e'

def need(ok, message):
    if not ok:
        raise ValueError(message)

def determinant(a):
    if not a: return 1
    return sum((-1)**j*a[0][j]*determinant([row[:j]+row[j+1:] for row in a[1:]]) for j in range(len(a)))

def rejected(f):
    try: f()
    except ValueError: return True
    return False

def frozen_binding(root, archive):
    need(root.is_dir() and not root.is_symlink(), 'author root is not regular')
    need({p.name for p in root.iterdir()} == NAMES, 'author path set changed')
    for name in NAMES:
        need((root/name).is_file() and not (root/name).is_symlink(), 'nonregular author member')
    need(sha256((root/'manifest.json').read_bytes()).hexdigest()==MANIFEST_HASH, 'author manifest changed')
    m=json.loads((root/'manifest.json').read_text())
    need(len(m['files'])==9 and {x['path'] for x in m['files']}==NAMES-{'manifest.json'}, 'manifest membership')
    for x in m['files']:
        b=(root/x['path']).read_bytes()
        need(len(b)==x['bytes'] and sha256(b).hexdigest()==x['sha256'], 'bound author bytes changed')
    blob=archive.read_bytes()
    need(len(blob)==25533 and sha256(blob).hexdigest()==ARCHIVE_HASH, 'archive receipt mismatch')
    with zipfile.ZipFile(archive) as z:
        need(len(z.infolist())==10 and set(z.namelist())==NAMES, 'unsafe archive member set')
        need(z.testzip() is None, 'archive CRC failure')
        for entry in z.infolist():
            need(not entry.is_dir() and not (entry.flag_bits & 1), 'directory/encrypted archive member')
            need(z.read(entry)==(root/entry.filename).read_bytes(), 'archive/directory mismatch')
    return {'archive_sha256':ARCHIVE_HASH,'author_files':10,'manifest_sha256':MANIFEST_HASH,'all_members_byte_identical':True}

def frame_and_fermat():
    frame=[[1,0,0],[0,1,0],[0,0,1],[1,1,1]]
    need(all(determinant(list(t)) != 0 for t in combinations(frame,3)), 'frame degeneracy')
    bad=frame[:3]+[[1,1,0]]
    need(any(determinant(list(t))==0 for t in combinations(bad,3)), 'concurrency negative control')
    def valid(n,e):
        need(n>=4 and len(e)==4 and min(e)>=0 and sum(e)==n, 'range/degree')
        need(max(e)<n-1, 'Jacobian ideal')
    for n in range(4,101):
        valid(n,(n-2,2,0,0))
        need(n**n>4*(n-2)**(n-2), 'singularity threshold fails')
        ambient=set()
        for i,j in product(range(4),repeat=2):
            e=[0]*4; e[i]+=n-1; e[j]+=1; ambient.add(tuple(e))
        need(len(ambient)==16, 'ambient Jacobian generators collide')
        # Count quotient monomials using inclusion/exclusion, independent of author's enumeration.
        nontrivial=sum((-1)**k*comb(4,k)*comb(n-k*(n-1)+3,3)
                       for k in range(5) if n-k*(n-1)>=0)
        need(nontrivial==comb(n+3,3)-16, 'Jacobian quotient dimension')
    need(comb(7,3)-16==19, 'quartic embedded dimension')
    controls=[(4,(3,1,0,0)),(4,(2,1,0,0)),(3,(1,2,0,0)),(4,(2,2,0,-1))]
    need(all(rejected(lambda n=n,e=e:valid(n,e)) for n,e in controls),'invalid witness accepted')
    return {'fermat_exponents_checked':[4,100],'quartic_embedded_image_dimension':19,'invalid_witnesses_rejected':len(controls),'concurrent_frame_rejected':True}

def local_tangent():
    checks=0
    for n in range(2,41):
        for a in range(n):
            # Eigenweight of u^k d/du is k-1. Pushforward multiplies by n*u^(n-1).
            k=(a+1)%n
            pushed_exponent=n-1+k
            need((k-1-a)%n==0, 'vector-field character mismatch')
            need((pushed_exponent-a)%n==0, 'pushforward not eigenfunction multiple')
            logarithmic=(pushed_exponent-a)//n
            need(logarithmic==int(a != n-1), 'branch boundary wrong')
            checks+=1
    return {'root_map_orders_checked':[2,40],'eigenweight_cases':checks,'special_boundary':'a = n-1, with no logarithmic factor'}

# Independently parameterize the six edges of a four-point frame, rather than using
# the author's five monodromy vectors. E_ij is the joining line of the complementary pair.
LINE_LABELS=['12','13','14','23','24','34']
LABELS=sorted(LINE_LABELS+['15','25','35','45'])

def geometry():
    classes={}
    for lab in LINE_LABELS:
        endpoints=set(range(1,5))-set(map(int,lab))
        classes[lab]=(1,)+tuple(-int(i in endpoints) for i in range(1,5))
    for i in range(1,5): classes[str(i)+'5']=(0,)+tuple(int(j==i) for j in range(1,5))
    return classes

DIV=geometry()

def geometric_type(n, five):
    six=list(five)+[(-sum(five))%n]
    vals=dict(zip(LINE_LABELS,six))
    incident_sums=[]
    for i in range(1,5):
        s=sum(vals[lab] for lab in LINE_LABELS if str(i) not in lab)
        incident_sums.append(s); vals[str(i)+'5']=s%n
    # Coefficient of H is total line weight/n. Coefficient of E_i is a carry.
    ell=(sum(six)//n,)+tuple(-(s//n) for s in incident_sums)
    numerator=tuple(sum(vals[lab]*DIV[lab][q] for lab in LABELS) for q in range(5))
    need(numerator==tuple(n*x for x in ell),'geometric Picard formula mismatch')
    selected=tuple(lab for lab in LABELS if vals[lab]<n-1)
    return ell,selected,vals

def census():
    witness=(1,1,2,1,2) # The source character (2,2,2,1,1) expressed as five line residues.
    ell,j,res=geometric_type(3,witness)
    need(ell==(3,-1,-1,-1,-1) and j==('12','13','23','45'),'exceptional witness mismatch')
    rows=[list(DIV[x]) for x in j]
    minors=[determinant([[row[c] for c in cols] for row in rows]) for cols in combinations(range(5),4)]
    need(any(minors),'residue rank less than four')
    need(geometric_type(3,(1,1,2,1,1))[:2]!=(ell,j),'mutated witness undetected')
    h=sha256(); results=[]; total=0
    for n in range(2,13):
        types=set()
        for five in product(range(n),repeat=5):
            e,s,_=geometric_type(n,five)
            need(0<=e[0]<=5 and all(-2<=x<=0 for x in e[1:]),'explicit geometric class bounds')
            types.add((e,s))
        total+=n**5
        if n<=10:
            need(len(types)==CENSUS_EXPECTED[n-2],'independent type count mismatch')
            h.update(str(n).encode()+b':'+json.dumps(sorted(types),separators=(',',':')).encode()+b'\n')
        results.append({'n':n,'characters':n**5,'different_sheaf_types':len(types)})
    need(h.hexdigest()==CENSUS_HASH,'independent type census digest mismatch')
    return {'characters_independently_enumerated':total,'census':results,'author_range_type_digest':h.hexdigest(),
            'exceptional_character_residues':[res[x] for x in LABELS],'residue_rank':4,'picard_rank':5,
            'logarithmic_h1_dimension_from_residue_sequence':1,'mutated_exceptional_character_rejected':True}

def integer_boundary_controls():
    # Concrete Presburger occurrence sets with nontrivial periods and a finite exception.
    periods={2:0,3:1}; tested=0
    for n in range(2,301):
        for p,r in periods.items():
            exists=any(p*c==n-r for c in range(n))
            need(exists==(n%p==r),'affine congruence occurrence')
            tested+=1
        exists=any((n-1-2*c)>=0 and (n-1-2*c)%3==0 for c in range(n))
        need(exists==(n>=3),'finite preperiod control')
        tested+=1
    # Negative carries and the upper residue facet must not be dropped.
    cases=0
    for n in range(2,16):
        for c in range(n):
            value=-3*c; k,a=divmod(value,n)
            need(0<=a<n and value==n*k+a,'signed carry')
            need((a==n-1) != (a<=n-2),'disjoint exhaustive facets')
            if a==n-1:
                need(not 0<=a<=n-2,'boundary mistakenly placed in interior')
            cases+=1
    return {'affine_integer_occurrence_checks':tested,'signed_carry_boundary_checks':cases,
            'tested_periods':[2,3],'finite_exception_checked':2,
            'limit':'These examples test implementation hazards; the all-exponent theorem requires the written semilinearity proof.'}

def main():
    p=argparse.ArgumentParser(); home=Path(__file__).resolve().parent.parent
    p.add_argument('--author-dir',type=Path,default=home/'hirzebruch_kummer_30003859')
    p.add_argument('--archive',type=Path,default=home/'HIRZEBRUCH_KUMMER_30003859_AUTHOR_SAFE_FREEZE.zip')
    a=p.parse_args()
    result={'status':'PASS_INDEPENDENT_SCOPED_CONTROLS','frozen_binding':frozen_binding(a.author_dir,a.archive),
            'fermat':frame_and_fermat(),'local_tangent_formula':local_tangent(),'quadrangle':census(),
            'integer_occurrence':integer_boundary_controls(),
            'limits':['Not a general cohomology computation','Not a formal proof certification',
                      'No conclusion of intended-conjecture resolution','No local-rigidity periodicity claim']}
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__': main()
