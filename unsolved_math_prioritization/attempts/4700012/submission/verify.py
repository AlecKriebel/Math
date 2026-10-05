#!/usr/bin/env python3
"""Portable scope and consistency checks. Does not certify a published theorem."""
from pathlib import Path
from fractions import Fraction
import json

ROOT=Path(__file__).resolve().parent
checks=0

def require(test, message):
    global checks
    checks += 1
    if not test:
        raise RuntimeError(message)

# Every monomial of ordinary degree d has (1,1) weighted degree d.
# Exact rational samples also test the implementation, not the universal theorem.
monomials=0
for d in range(2, 41):
    for i in range(d+1):
        j=d-i
        require(i+j==d, 'weighted degree')
        x,y=Fraction(2,3),Fraction(-3,5)
        for lam in [Fraction(-2),Fraction(0),Fraction(3,2)]:
            require((lam*x)**i*(lam*y)**j == lam**d*x**i*y**j,
                    'ordinary to weighted scaling')
        if i:
            require((i-1)+j==d-1, 'x derivative degree')
        if j:
            require(i+(j-1)==d-1, 'y derivative degree')
        monomials += 1

pairs=0
for n in range(1, 21):
    for m in range(2*n+1, 4*n+5):
        require(2*n < m, 'distinct Hamiltonian degrees')
        require((2*n-1) < (m-1), 'distinct vector-field degrees')
        pairs += 1
residual=[(n,m) for n in range(1,10) for m in range(2*n+1,4*n-2)]
require(residual[0]==(2,5), 'first historical residual pair')
require(not any(n==1 for n,m in residual), 'empty n=1 residual degree band')

s=json.loads((ROOT/'STATUS.json').read_text())
a=json.loads((ROOT/'SOURCE_MANIFEST.json').read_text())
require(s['problem_id']==a['problem_id']==4700012, 'ID match')
require(s['status']=='already_solved', 'bibliographic classification')
require(s['turns_used']==0, 'no proof search turns')
require(not s['full_published_proof_inspected'], 'full-proof limitation retained')
require(not s['complete_candidate_proof'], 'no invented new proof')
require(not s['new_mathematical_result'], 'no novelty claim')
require((ROOT/'turns.jsonl').read_text()=='', 'empty proof attempt history')
require(a['sources'][1]['full_paper_pdf_hash'] is None, 'no false PDF hash')
require(a['sources'][1]['publication_date']==s['literature_resolution_date'],
        'publication date consistency')
require(a['sources'][1]['doi']==s['doi'], 'DOI consistency')
require(a['corpora'][0]['sha256']=='04128381e42a5e312326d74adb0947ee02062ade70229e02d3060ac4ef9942cf',
        'pinned corpus hash')
require(all(not x.get('full_source_redistributed',False) for x in a['sources']),
        'source distribution constraint')
require('nonsimple' in (ROOT/'LITERATURE_STATUS.md').read_text(),
        'simple-zero ambiguity documented')
print(json.dumps({'checks_passed':checks,'ordinary_monomials_tested':monomials,
                  'degree_pairs_tested':pairs,'historical_first_residual_pair':[2,5],
                  'published_proof_certified':False,
                  'scope':'Exact arithmetic degree-mapping controls and packet metadata consistency only.'},
                 indent=2,sort_keys=True))
