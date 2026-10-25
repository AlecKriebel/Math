"""Direct root check of the printed repaired cores and the bound false row.

No submitted Python modules, descriptors or pickles are imported.
"""
from pathlib import Path
import datetime, gzip, hashlib, json

HERE = Path(__file__).resolve().parent
PACKAGE = HERE / 'sources/published-source/K2P_SAME_Reproducibility_Package_v1.0.5-r1/k2p_same_reproducibility_v1.0.5-r1'
ledger = PACKAGE / 'work/corrected_composite_ledgers/artifacts/raw4_corrected_composite_ledger.jsonl.gz'
digest = hashlib.sha256(ledger.read_bytes()).hexdigest()
assert digest == '7cf3f953fca695d612387143818843650498f84f55cf0a776f90c9afdd95eef6'

# Main article's theta1 and theta0 templates, with segments 2 and 3 repaired.
# The ordinary suppressed-root edge is included; the last item is the head.
source = [('S','U',''),('S','X','X'),('V','P2',''),('P2','X','X'),
          ('P2','L1',''),('U','P3',''),('P3','V','V'),('P3','L2',''),
          ('U','V','V'),('S','L0',''),('X','L3','')]
target = [('S','U',''),('S','V','V'),('U','P2',''),('P2','X','X'),
          ('P2','L1',''),('V','P3',''),('P3','X','X'),('P3','L2',''),
          ('U','V','V'),('S','L0',''),('X','L3','')]
port = {'L0':'L2','L1':'L0','L2':'L1','L3':'L3'}
iso = {'S':'P3','U':'U','V':'V','X':'X','P2':'S','P3':'P2',
       **{f'L{i}':f'L{i}' for i in range(4)}}
def canonical(a,b,head):
    return (*sorted((a,b)),head)
def transported(edge):
    a,b,h = (port.get(v,v) for v in edge)
    return canonical(iso[a],iso[b],iso[h] if h else '')
assert len(iso) == len(set(iso.values())) == 10
assert all(iso[f'L{i}'] == f'L{i}' for i in range(4))
assert len(source) == len(target) == 11
assert {canonical(*e) for e in source} == {transported(e) for e in target}

with gzip.open(ledger, 'rt') as f:
    row = next(json.loads(line) for line in f if json.loads(line).get('raw_id') == 137124)
assert (row['source_index'],row['target_index'],row['port_permutation']) == (2,85,[2,0,1,3])
assert row['corrected_category'] == 'exact_rank_exclusion'
assert row['evidence_binding']['source_exact_rank'] == 14
assert row['evidence_binding']['target_exact_rank'] == 13
result = {
    'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'status':'FALSE_EXCLUSION_CONFIRMED_BY_DIRECT_SOURCE_CHECK',
    'ledger_sha256':digest,'published_row':row,'edge_count':11,
    'target_port_transport':[2,0,1,3],'label_and_head_preserving_bijection':iso,
    'interpretation':'The same labelled mixed network admits both root presentations. Main Lemma6.1 explicitly permits independent incoming boundaries. Full physical maps agree by reversible rerooting and strict serial splitting, so the incidence-quotient germ cannot be excluded by the arm-fixed ranks.',
    'affected_claim':'Validity/completeness of the finite proof object and its rank-exclusion census; no counterexample to the structural classification statement is asserted.',
    'source_locations':['Main p9 quotient relation','Main pp13-14 core/repair table','Main Lemma6.1 incoming-boundary independence','Main pp14-16 finite termination and Theorem6.3'],
    'source_repair_performed':False,
}
(HERE/'root-defect-check.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'status':result['status'],'raw_id':137124,'edges':11,'source_repair':False}))
