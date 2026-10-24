"""Classify exploratory factor patterns; does not certify irreducibility."""
import json,math,collections,hashlib
from fractions import Fraction
from pathlib import Path
P=Path(__file__).resolve().parent
rows=[json.loads(l)for l in (P/'artifacts/all_factors.ndjson').read_text().splitlines()]
def key(f):
    assert f['terms'][0][0]==1 and f['terms'][0][1]>0
    return tuple(map(tuple,f['terms']))
weights={}
for g in rows:
    if g['radical_free'] and sum(f['multiplicity']for f in g['factors'])==1:
        k=key(g['factors'][0])
        if k in weights:assert weights[k]==g['content']
        weights[k]=g['content']
for g in rows:
    if g['radical_free']:
        assert all(key(f)in weights for f in g['factors'])
        assert g['content']==math.prod(weights[key(f)]**f['multiplicity']for f in g['factors'])
private=[];penalties=[]
for g in rows:
    if g['radical_free']:continue
    if any(key(f)not in weights for f in g['factors']):private.append(g['names'][0]);continue
    den=math.prod(weights[key(f)]**f['multiplicity']for f in g['factors'])
    penalty=Fraction(g['content'],den)
    assert penalty>1
    penalties.append({'table':g['names'][0],'scalar_penalty':str(penalty)})
r={'unique_spectra':len(rows),'radical_free_spectra':sum(g['radical_free']for g in rows),'primitive_radical_free_factor_types':len(weights),'nontrivial_radical_spectra_with_new_factor':len(private),'nontrivial_radical_spectra_using_old_factors':len(penalties),'scalar_penalty_histogram':dict(collections.Counter(p['scalar_penalty']for p in penalties)),'old_factor_cases':penalties,'input_sha256':hashlib.sha256((P/'artifacts/all_factors.ndjson').read_bytes()).hexdigest(),'status':'EXPLORATORY, NOT A VERIFIED ARBITRARY-PRODUCT EXCLUSION','missing_verification':'All factorizations reconstruct exactly, but independent irreducibility certificates for the factor polynomials have not been supplied. Unique-factorization reasoning cannot be promoted without that step.','conditional_conclusion':'If the factor outputs are irreducible over Q, no product of these radical-free spectra can equal a product containing a nontrivial-radical spectrum: a new irreducible factor obstructs equality; otherwise the scalar penalty is >1 while all radical-free products have penalty 1.'}
(P/'artifacts/exploratory_factor_report.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({k:v for k,v in r.items() if k!='old_factor_cases'},indent=2))
