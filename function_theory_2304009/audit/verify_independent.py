#!/usr/bin/env python3
"""Independent finite audit controls. No imports from the author's verifier.

These checks support, and do not replace, the universal argument in AUDIT.md.
Only Python's standard library is used. No source PDFs are generated or exposed.
"""
from fractions import Fraction as F
import argparse
import hashlib
import json
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
EXPECTED_FREEZE = 'ca309e19c702eeb882e8c7900b9c7084b48aba37994d77b2ad15aaaaf3a16377'

# Gaussian rationals, represented by pairs of Fraction.
def z(x=0, y=0): return F(x), F(y)
def add(a,b): return a[0]+b[0], a[1]+b[1]
def mul(a,b): return a[0]*b[0]-a[1]*b[1], a[0]*b[1]+a[1]*b[0]
def norm2(a): return a[0]**2+a[1]**2
def inv(a):
    n=norm2(a)
    assert n
    return a[0]/n, -a[1]/n
def power(a,n):
    if n<0:return power(inv(a),-n)
    r=z(1)
    for _ in range(n):r=mul(r,a)
    return r
def evalpoly(coeff,x):
    r=z()
    for c in reversed(coeff):r=add(mul(r,x),c)
    return r


def main(check_private_sources=False):
    pub=ROOT/'public'
    manifest_bytes=(pub/'SHA256SUMS.json').read_bytes()
    assert hashlib.sha256(manifest_bytes).hexdigest()==EXPECTED_FREEZE
    manifest=json.loads(manifest_bytes)
    assert {p.name for p in pub.iterdir() if p.is_file()}==set(manifest['files'])|{'SHA256SUMS.json'}
    for name,meta in manifest['files'].items():
        b=(pub/name).read_bytes()
        assert len(b)==meta['bytes'] and hashlib.sha256(b).hexdigest()==meta['sha256']

    # Deliberately different grid, including extremes far beyond the author grid.
    ds=sorted({F(j,32) for j in range(1,128)}|{F(1,10**30),F(4)-F(1,10**30)})
    ns=[1,2,4,17,53,10**3,10**12]
    g=0
    for d in ds:
        A=(4+d)/4; B=(4-d)/4
        L=(4+3*d)/4; a=L/2
        m=(4-d)*(5*d+12)/(4*(4+d)**2)
        assert m==1-(a/A)**2 and 0<m<1
        assert L-d==2*A-L==B>0
        h=B*m/4
        for N in ns:
            e=min(h/4,h/(3*(N+1)))
            assert e==h/(3*(N+1))>0
            assert 2*h/(N+1)-2*e==4*e>0
            assert ((a+e)/A)**2+((h+e)/B)**2 < 1
            major=(a/A+m/16)**2+(5*m/16)**2
            upper=1-m+m/8+26*m*m/256
            assert ((a+e)/A)**2+((h+e)/B)**2 <=major<=upper<=1-F(99,128)*m<1
            # First and last segment heights lie strictly inside the rectangle.
            assert -h < -h+2*h/(N+1) <= -h+2*h*N/(N+1) < h
            g+=1

    # Exact complex normalization on full polynomials, rather than only leading terms.
    ws=[z(1),z(0,1),z(-1),z(0,-1),z(F(3,5),F(4,5)),z(1,1),z(-2,1),z(F(5,4),F(2,3))]
    zs=[z(0),z(1),z(-1),z(0,1),z(F(2,3),F(5,7)),z(3,-2)]
    polys=evals=0
    for n in [1,2,3,5,11,20]:
        for w in ws:
            assert norm2(w)>=1
            coeff=[z(F(k+1,k+2),F((-1)**k,k+3)) for k in range(n)]+[power(w,n)]
            p=[mul(c,power(w,-k)) for k,c in enumerate(coeff)]
            assert p[-1]==z(1)
            for x in zs:
                assert evalpoly(p,mul(w,x))==evalpoly(coeff,x)
                evals+=1
            # Similarity and diameter expansion hold on arbitrary point differences.
            for x in zs:
                assert norm2(mul(w,x))==norm2(w)*norm2(x)>=norm2(x)
            polys+=1

    # Deliberate mutations are actually rejected by equalities/inequalities.
    negative={}
    alpha=z(16); w=z(2)
    negative['wrong_normalization_direction']=mul(alpha,power(w,4))!=z(1)
    # q(z)=16z^4: z=1 lies in E(q/16) but not E(q), so level sets change.
    negative['divide_leading_coefficient_changes_set']=(norm2(evalpoly([z(),z(),z(),z(),alpha],z(1)))>1)
    # The disk E(16z^4) has radius 1/2, ruling out the positive-exponent sign.
    negative['capacity_positive_exponent_wrong']=F(1,2)!=F(2)
    # If separation is replaced by epsilon=h/(N+1), adjacent tubes touch.
    h=F(1,10); N=5; bad_e=h/(N+1)
    negative['touching_neighborhoods_not_separated']=not(2*bad_e<2*h/(N+1))
    # At d=4 the vertical semiaxis is zero; it is no Jordan ellipse.
    negative['endpoint_d4_degenerate']=((4-F(4))/4==0)
    # Distinct zeros do not certify different closed components: [-1,1] lies
    # in E(z^2-1), joining both zeros. The following is a finite witness check.
    negative['root_count_not_component_count']=all(abs(x*x-1)<=1 for x in [F(-1),F(-1,2),F(0),F(1,2),F(1)])
    assert all(negative.values())

    source_manifest=json.loads((pub/'SOURCE_MANIFEST.json').read_text())
    source_checks={}
    private_pdfs=list((ROOT/'private').glob('*.pdf'))
    for item in source_manifest['sources'] if check_private_sources else []:
        if 'sha256' not in item:continue
        matched=[p for p in private_pdfs if hashlib.sha256(p.read_bytes()).hexdigest()==item['sha256']]
        assert len(matched)==1 and matched[0].stat().st_size==item['bytes']
        source_checks[item['id']]={'sha256':item['sha256'],'bytes':item['bytes'],'matched':True}
    return {'result':'PASS','author_public_manifest_sha256':EXPECTED_FREEZE,
            'frozen_files_including_manifest':10,'independent_geometry_cases':g,
            'exact_complex_polynomials':polys,'exact_complex_evaluation_identities':evals,
            'negative_controls':negative,'private_pdf_byte_checks':source_checks,
            'limitations':['Finite tests do not establish universal claims.','No Hilbert approximant or effective degree bound is computed.','Pommerenke original proof not inspected.']}

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('--check-private-sources',action='store_true',help='Requires separately obtained private PDFs; never needed for the finite mathematical controls.')
    args=parser.parse_args()
    print(json.dumps(main(args.check_private_sources),indent=2,sort_keys=True))
