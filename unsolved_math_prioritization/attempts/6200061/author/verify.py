#!/usr/bin/env python3
"""Fail-closed package and exact-algebra verifier; not a geometry proof assistant."""
import hashlib
import json
import math
from fractions import Fraction as F
from pathlib import Path
import re
import sys

FILES = {'README.md', 'PROOF.md', 'APPROACHES.md', 'IDENTITY.json', 'SOURCES.json',
         'RESULTS.json', 'verify.py', 'test_suite.py'}
REVIEW = '19d550c8dd1630a33ab9f57396a75f3ff318fe849cdf8d4a4ad32469fe9fb258'

class VerificationError(Exception):
    pass

def need(value, message):
    if not value:
        raise VerificationError(message)

def load(root, name):
    def unique_pairs(pairs):
        out = {}
        for k, v in pairs:
            need(k not in out, 'duplicate JSON key: ' + k)
            out[k] = v
        return out
    return json.loads((root/name).read_text(), object_pairs_hook=unique_pairs,
                      parse_constant=lambda x: (_ for _ in ()).throw(VerificationError('nonfinite JSON')))

def rat(v):
    need(isinstance(v, list) and len(v) == 2 and all(type(x) is int for x in v), 'bad rational encoding')
    need(v[1] > 0, 'nonpositive denominator')
    f = F(*v)
    need(v == [f.numerator, f.denominator], 'noncanonical rational')
    return f

def pair(f):
    f = F(f)
    return [f.numerator, f.denominator]

def mul(a,b):
    out=[F(0)]*(len(a)+len(b)-1)
    for i,x in enumerate(a):
        for j,y in enumerate(b):
            out[i+j] += x*y
    return out

def poly_pow(a,n):
    out=[F(1)]
    for _ in range(n):
        out=mul(out,a)
    return out

def model_ratio_square(t):
    need(0 < t <= 1, 'model t outside domain')
    # Derived directly from squared chordal distances, separately from simplified expression.
    source_square=t**4/(1+t**4)
    image_square=(((1+2*t)**2-1)**2)/(2*(1+(1+2*t)**4))
    return image_square/source_square

def expected_results():
    a=mul(poly_pow([F(1),F(1)],2),[F(1),0,0,0,F(1)])
    b=poly_pow([F(1),F(2)],4);b[0]+=1
    coeff=[82*a[i]-(b[i] if i<len(b) else 0) for i in range(7)]
    bern=[sum(coeff[k]*F(math.comb(i,k), math.comb(6,k)) for k in range(i+1)) for i in range(7)]
    samples=[]
    for k in range(1,81):
        t=F(1,2**k); r2=model_ratio_square(t)
        samples.append({'k':k,'t':pair(t),'ratio_squared':pair(r2),'t_squared_ratio_squared':pair(t*t*r2)})
    trees=[]
    for r in range(2,9):
        for n in range(1,13):
            cylinders=2*r*(2*r-1)**(n-1)
            mass=F(1,cylinders); diameter_to_Q=F(1,(2*r-1)**n)
            trees.append({'rank':r,'depth':n,'cylinder_count':cylinders,'cylinder_mass':pair(mass),
                          'diameter_to_Q':pair(diameter_to_Q),'regularity_ratio':pair(mass/diameter_to_Q)})
    coords=[0,1,3,7,8];m=len(coords)
    d0=[[abs(x-y) for y in coords] for x in coords]
    d=[[max(d0[(i+h)%m][(j+h)%m] for h in range(m)) for j in range(m)] for i in range(m)]
    defect=max(abs(d0[(i+h)%m][(j+h)%m]-d0[i][j]) for h in range(m) for i in range(m) for j in range(m))
    return {'schema':1,'claim_scope':'PARTIAL_NOT_SOLVED','sample_role':'regression_only',
            'certificate':{'domain':'0<t<=1','model_multiplier':2,'model_translation':1,'squared_growth_lower_bound':pair(F(4,41)),
                           'polynomial_monomial_coefficients':[pair(v) for v in coeff],
                           'polynomial_bernstein_coefficients':[pair(v) for v in bern]},
            'dyadic_samples':samples,'free_tree_cylinders':trees,
            'finite_supremum_example':{'group':'cyclic_order_5','coordinates':coords,'additive_defect':defect,'invariant_metric':d}}

def main():
    need(len(sys.argv)==1, 'unexpected arguments')
    root=Path(__file__).resolve().parent
    names={p.name for p in root.iterdir()}
    need(names==FILES|{'MANIFEST.json'}, 'unexpected or missing package files')
    for p in root.iterdir():
        need(p.is_file() and not p.is_symlink(), 'nonregular package member')
    man=load(root,'MANIFEST.json')
    need(set(man)=={'schema','algorithm','files','public_content_only','status'}, 'manifest schema mismatch')
    need(man['schema']==1 and man['algorithm']=='sha256' and man['public_content_only'] is True, 'manifest flags')
    need(man['status']=='PARTIAL_NOT_SOLVED', 'manifest claim inflation')
    need(set(man['files'])==FILES, 'manifest file roster')
    for name in sorted(FILES):
        record=man['files'][name];data=(root/name).read_bytes()
        need(set(record)=={'sha256','bytes'}, 'bad manifest entry')
        need(type(record['bytes']) is int and record['bytes']==len(data), 'byte count mismatch: '+name)
        need(record['sha256']==hashlib.sha256(data).hexdigest(), 'hash mismatch: '+name)
    ident=load(root,'IDENTITY.json')
    need(ident['problem_id']==6200061 and ident['problem_number']=='AMR-061-0061' and ident['rank']==810, 'wrong target')
    need(ident['status']=='PARTIAL_NOT_SOLVED' and ident['general_conjecture_solved'] is False and ident['novelty_claim'] is False, 'claim inflation')
    need(ident['full_review_sha256']==REVIEW and ident['review_hash_matches_catalog'] is True, 'record review identity')
    need(ident['reviewed_full_record_and_report'] is True, 'unreviewed record')
    need((ident['catalog_year'],ident['survey_date'],ident['survey_problem'],ident['survey_pdf_page'])==(2005,'2007-10-24',61,17),'source identity')
    expected_flags={'marked_obstruction_proved_in_text':True,'universal_equality_proved':False,
                    'existential_attainment_disproved':False,'finite_samples_are_general_proof':False,
                    'algebra_certificate_is_universal_on_stated_interval':True}
    need(ident['scope_flags']==expected_flags, 'scope flags changed')
    need(len(ident['source_corpora'])==3, 'corpus metadata incomplete')
    for entry in ident['source_corpora']:
        need(re.fullmatch('[0-9a-f]{64}',entry['sha256']) is not None and type(entry['bytes']) is int and entry['bytes']>0,'invalid corpus metadata')
    src=load(root,'SOURCES.json')
    need({x['key'] for x in src['sources']}=={'K07','C93','BS00','HMT20','HMT22','HM25'}, 'source roster')
    for entry in src['sources']:
        need(entry['included_in_package'] is False, 'source-content inclusion')
        need(entry['url'].startswith('https://') and bool(entry['inspection']), 'source provenance missing')
    results=load(root,'RESULTS.json');expected=expected_results()
    need(results==expected, 'results differ from independently recomputed algebra/data')
    cert=results['certificate']
    need(all(rat(x)>0 for x in cert['polynomial_bernstein_coefficients']), 'Bernstein positivity failed')
    for row in results['dyadic_samples']:
        t=rat(row['t']);r2=rat(row['ratio_squared'])
        simple=8*(1+t)**2*(1+t**4)/(t*t*(1+(1+2*t)**4))
        need(r2==simple and t*t*r2>=F(4,41),'ratio formula/lower bound failed')
    for row in results['free_tree_cylinders']:
        r=row['rank'];need(rat(row['regularity_ratio'])==F(2*r-1,2*r),'cylinder identity failed')
    ex=results['finite_supremum_example'];d=ex['invariant_metric'];coords=ex['coordinates'];m=len(d)
    for i in range(m):
        for j in range(m):
            base=abs(coords[i]-coords[j])
            need(d[i][j]==d[j][i] and (d[i][j]==0)==(i==j),'metric symmetry/positivity failed')
            need(base<=d[i][j]<=base+ex['additive_defect'],'defect bound failed')
            for k in range(m):
                need(d[i][j]<=d[i][k]+d[k][j], 'triangle failed')
                need(d[i][j]==d[(i+k)%m][(j+k)%m], 'invariance failed')
    print(json.dumps({'verification':'PASS','problem_id':6200061,'status':'PARTIAL_NOT_SOLVED',
                      'exact_bernstein_coefficients_checked':7,'rational_samples_checked':80,
                      'tree_cylinders_checked':84,'finite_supremum_group_order':5,
                      'geometry_formalized':False,'literature_search_exhaustive':False},sort_keys=True))

if __name__=='__main__':
    try:
        main()
    except Exception as exc:
        print('VERIFICATION FAILED: '+str(exc),file=sys.stderr)
        sys.exit(1)
