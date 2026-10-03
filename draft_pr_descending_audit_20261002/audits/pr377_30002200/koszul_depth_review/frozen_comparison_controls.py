#!/usr/bin/env python3
"""Post-seal independent controls. Reads frozen candidate only for bindings/receipts.
The actual inclusion matrix is independently generated from the primary formula.
"""
from pathlib import Path
from itertools import combinations
from hashlib import sha256
import json
from independent_koszul_controls import Matrix,boundary,compositions,quotient_dimension

HERE=Path(__file__).resolve().parent
SNAP=HERE.parent/'snapshot'
CAND=SNAP/'unsolved_math_prioritization/attempts/30002200'


def poly_dim(r,degree): return len(compositions(degree,r))
def syzygy_dim(r,b,k,degree):
    if degree%2: return 0
    return boundary(r,b,k,(degree+2*b*k)//2).rank()

def iota_component(r,m,degree):
    source=[];target=[]
    for j in range(r+1):
        for J in combinations(range(r),j):
            if (degree+3*j)%2==0:
                for alpha in compositions((degree+3*j)//2,r):
                    target.append(('V',J,alpha))
                    if j<=m: source.append(('V',J,alpha))
            if j<=m and (degree+3*j+1)%2==0:
                for alpha in compositions((degree+3*j+1)//2,r): source.append(('W',J,alpha))
    ti={v:i for i,v in enumerate(target)}
    M=Matrix(len(target),len(source))
    for col,(kind,J,alpha) in enumerate(source):
        if kind=='V': M[ti[(kind,J,alpha)],col]=1
        else:
            for i in range(r):
                if i in J:continue
                beta=list(alpha);beta[i]+=1
                Jp=tuple(sorted(J+(i,)))
                M[ti[('V',Jp,tuple(beta))],col]=(-1)**sum(j>i for j in J)
    rank=M.rank()
    return dict(degree=degree,source_dim=len(source),target_dim=len(target),rank=rank,
                kernel=len(source)-rank,cokernel=len(target)-rank)

def main():
    snapshot=json.loads((HERE.parent/'snapshot_manifest.json').read_text())
    assert snapshot['head']=='75bea4d3be9904e90c3843892671a440ba4d2c42'
    for entry in snapshot['files']:
        b=(SNAP/entry['path']).read_bytes()
        assert len(b)==entry['bytes'] and sha256(b).hexdigest()==entry['sha256']
    manifests=[]
    for mf,root in [('FINAL_SOURCE_MANIFEST.json',CAND),('PUBLICATION_MANIFEST.json',CAND),('REVIEW_MANIFEST.json',CAND/'review')]:
        data=json.loads((root/mf).read_text())
        for e in data['files']:
            b=(root/e['path']).read_bytes()
            assert len(b)==e['bytes'] and sha256(b).hexdigest()==e['sha256']
        manifests.append(dict(manifest=mf,explicit_hash_bound_entries=len(data['files'])))
    for ours,theirs in [('author_358064.stdout.txt','SOURCE_CASE_CHECKS.json'),('old_983.stdout.txt','review/INDEPENDENT_CHECKS.json')]:
        assert (HERE/ours).read_bytes()==(CAND/theirs).read_bytes()
    sources=json.loads((CAND/'SOURCE_MANIFEST.json').read_text())['sources']
    ownraw={'OWR_2012_49.pdf':'OWR49_2012.pdf','Franz_2015_corrected_2023.pdf':'Franz1403.4485v4.pdf',
            'Franz_Huang_2020.pdf':'FranzHuangAGT2020.pdf','Allday_Franz_Puppe.pdf':'AFP1111.0957v2.pdf'}
    for entry in sources:
        b=(HERE/'raw_sources'/ownraw[entry['file']]).read_bytes()
        assert len(b)==entry['bytes'] and sha256(b).hexdigest()==entry['sha256']
    ranks=[]
    for h in range(16):
        c=iota_component(5,2,h-15);q=iota_component(5,2,h-14)
        expected_c=(poly_dim(5,h//2) if h%2==0 else 0)+(5*poly_dim(5,(h-3)//2) if (h-3)%2==0 else 0)+syzygy_dim(5,1,2,h-6)
        expected_q=(5*poly_dim(5,(h-10)//2) if (h-10)%2==0 else 0)+(poly_dim(5,(h-13)//2) if (h-13)%2==0 else 0)+syzygy_dim(5,1,4,h-9)
        assert c['cokernel']==expected_c and q['kernel']==expected_q,(h,c,q,expected_c,expected_q)
        ranks.append(dict(cohomology_degree=h,C=c,Q=q,C_predicted=expected_c,Q_predicted=expected_q))
    print(json.dumps(dict(head=snapshot['head'],snapshot_hash_bound_files=len(snapshot['files']),
                         nested_manifests=manifests,primary_pdf_retrievals_hash_exact=len(sources),
                         author_receipt_byte_exact=True,old_review_receipt_byte_exact=True,
                         rank5_independent_inclusion_component_controls=ranks,
                         rank5_extension=dict(left_free_target_shifts=[0,3],right_koszul_shift=9,
                                              right_free_quotient_shifts=[10,13],correct_target_minus_quotient=[-9,-6],
                                              old_frozen_assertions_arithmetic_only=True)),indent=2))
    print('PASS: frozen bindings and full receipts; independent actual inclusion matrices reproduce corrected left/right grading.')
    print('REPAIR REQUIRED: guide line 54, author checker line 59, old reviewer checker line 33, old review extension paragraph use quotient free shifts as targets.')

if __name__=='__main__':main()
