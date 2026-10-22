#!/usr/bin/env python3
"""Independent exact audit controls. No author-code imports or network required.
Finite controls corroborate, but do not certify, the infinite proofs.
"""
from fractions import Fraction as Q
from itertools import product
from math import isqrt, ceil
from pathlib import Path
from hashlib import sha256
import json
import zipfile

ROOT = Path(__file__).resolve().parents[1]
MANIFEST_SHA = '00cc2ffbfcf74549e852fc4bf2af6f7de4596f398339ec726d46c8b563b5ef11'
ARCHIVE_SHA = '53368885eec40f19b35d99a029ffadcc8174d7ebdb32bc36f90699d8acc87a39'

def block_endpoint(b0, c0, m, length):
    """Diagonalize independently using both eigenvalues, rather than replay."""
    plus = (c0 + m*b0)*Q(m,m-1)**length
    minus = (c0 - m*b0)*Q(m,m+1)**length
    return (plus-minus)/(2*m), (plus+minus)/2

def integrity():
    a=ROOT/'author'
    data=(a/'AUTHOR_MANIFEST.json').read_bytes()
    assert sha256(data).hexdigest()==MANIFEST_SHA
    manifest=json.loads(data)
    expected={'AUTHOR_MANIFEST.json'}|{x['path'] for x in manifest['files']}
    assert {p.name for p in a.iterdir() if p.is_file()}==expected
    for row in manifest['files']:
        data=(a/row['path']).read_bytes()
        assert len(data)==row['bytes']
        assert sha256(data).hexdigest()==row['sha256']
    zpath=ROOT/'AUTHORED_REVIEW_PACKET.zip'
    assert sha256(zpath.read_bytes()).hexdigest()==ARCHIVE_SHA
    with zipfile.ZipFile(zpath) as z:
        assert set(z.namelist())=={'author/'+n for n in expected}
        for n in expected:
            assert z.read('author/'+n)==(a/n).read_bytes()
    return {'authored_files_including_manifest':len(expected), 'archive_exact':True}

def direct_sums(seq):
    """Recompute each sum from its definition, independent of state updates."""
    return [(sum(seq[:n],Q(0)),
             sum((Q(n-k)*a for k,a in enumerate(seq[:n])),Q(0)))
            for n in range(1,len(seq)+1)]

def potential_checks():
    trials=steps=good=0
    ms=(Q(2), Q(13,6), Q(5,2), Q(29,10), Q(3), Q(31,7), Q(8))
    for seed in (Q(1),Q(1,2),Q(1,17)):
        for xs in product(range(4), repeat=5):
            seq=[seed]+[Q(n*x,3) for n,x in zip(range(2,7),xs)]
            sums=direct_sums(seq)
            for m in ms:
                trials+=1
                previous=seed
                count=0
                for n,((b,c),a) in enumerate(zip(sums,seq),1):
                    p=(c+m*b)/(n+m)
                    assert p>=previous
                    if n>1:
                        old_b,old_c=sums[n-2]
                        identity=((n-1)*old_b-old_c+(n-1+m)*(m+1)*a)
                        assert p-previous==identity/((n+m)*(n-1+m))
                    if a>0 and c<=m*m*a and n>=ceil(m):
                        good+=1
                        count+=1
                        assert p>=m/(m-1)*Q(n-1+m,n+m)*previous
                        assert p>=(1+1/(2*m))*previous
                        assert p<=m*m*(1+m)
                        assert seed*(1+1/(2*m))**count<=m*m*(1+m)
                    steps+=1
                    previous=p
    return {'sequence_threshold_cases':trials,'index_checks':steps,'good_large_indices':good,
            'noninteger_threshold_parameters':True}

def blocks():
    results=[]
    # Closed-form endpoint plus independent direct-sum comparison for short blocks.
    for m in (2,3,7,8,9,16,31,32,64):
        b0,c0=Q(1),Q(m-1)
        aa=[]
        for r in range(1,13):
            _,c=block_endpoint(b0,c0,m,r)
            aa.append(c/(m*m))
            b_direct=b0+sum(aa,Q(0))
            c_direct=c0+r*b0+sum((Q(r-k)*a for k,a in enumerate(aa)),Q(0))
            b_closed,c_closed=block_endpoint(b0,c0,m,r)
            assert (b_direct,c_direct)==(b_closed,c_closed)
            assert aa[-1]==(c_direct)/(m*m)
    # Full recursive first two stages, checking endpoints by diagonalization.
    b,c,end=Q(1),Q(1),1
    for j in (1,2):
        budget=16*b*4**(2**j)
        m=max(end+1,2,isqrt(budget.numerator//budget.denominator))
        while m*m<budget:
            m+=1
        assert m> end and m*m>=budget
        c+=(m-1-end)*b
        assert c<m*b
        length=2**j*m
        b1,c1=block_endpoint(b,c,m,length)
        a_last=c1/(m*m)
        # c_r increases since b_r and a_r are positive; endpoint bounds all terms.
        assert 0<a_last<=Q(m,6)
        assert Q(length,2**j*m)==1
        results.append({'stage':j,'m':m,'length':length,'endpoint_cap_exact':True})
        b,c,end=b1,c1,m+length-1
    sharp=[]
    for m in (8,9,15,16,17,31,32,33,63,64,65,127):
        h=0
        while 16*4**(h+1)<=m*m:
            h+=1
        assert 16*4**h<=m*m<16*4**(h+1)
        b1,c1=block_endpoint(Q(1),Q(m-1),m,m*h)
        assert c1/(m*m)<=Q(m,6)
        sharp.append({'m':m,'count_lower_bound':m*h})
    return {'recursive_stages':results,'sharp_nonpowers_included':sharp,
            'two_eigenvalue_crosschecks':108}

def negative_controls():
    m=16
    b,c=Q(1),Q(m-1)
    wrong=(c+b)/(m*m)
    assert (c+b+wrong)/wrong==m*m+1
    m,b,c=2,Q(100),Q(100)
    assert (c+b)/(m*m-1)>m
    # A denominator n alone, instead of n+m, does not give a monotone potential.
    m=Q(4)
    seq=[Q(1),Q(0)]
    sums=direct_sums(seq)
    bad=[(c+m*b)/n for n,(b,c) in enumerate(sums,1)]
    assert bad[1]<bad[0]
    return {'wrong_ratio_denominator':True,'omitted_old_mass_budget':True,
            'wrong_potential_denominator':True}

def run():
    return {'status':'independent_exact_controls_passed','binding':integrity(),
            'potential':potential_checks(),'blocks':blocks(),'negative_controls':negative_controls(),
            'limits':'No finite control proves the infinite or analytic statements; see the independent written audit.'}

if __name__=='__main__':
    print(json.dumps(run(),indent=2,sort_keys=True))
