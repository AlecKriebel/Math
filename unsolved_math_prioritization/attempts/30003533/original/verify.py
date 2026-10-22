#!/usr/bin/env python3
"""Strict source-free packet verifier. No assertions, network, or in-place writes."""
import sys
sys.dont_write_bytecode=True
import hashlib,json
from pathlib import Path
from controls import run

FILES={'CLAIMS.json','GATE.md','LEDGER.json','PROOFS.md','RESULT.md','SOURCES.md','SOURCE_METADATA.json','controls.py','verify.py','selftest.py','REPLAY.json','VALIDATION.md'}
FALSE_FIELDS={'original_target_resolved','novelty_claim','independent_audit_passed','finite_checks_prove_pde','smooth_counterexample_proved','polyhedral_counterexample_is_smooth','uniform_inverse_implies_coercivity','star_combined_equals_standard','deformation_bound_is_fixed_domain_high_frequency','acyclicity_without_contraction_suffices','source_liminf_display_is_well_formed','source_strong_nontrapping_is_formally_defined','full_current_literature_exhausted','publication_payload_contains_third_party_source_text'}
EXPECTED_CLAIMS={'schema_version':1,'problem_id':30003533,'status':'unsolved','substantive_attempts':5,'operator':'0.5 I + Dprime_k - i k eta S_k','space':'complex L2(Gamma, ds)','coupling':'eta > 0 fixed before k varies','coercivity':'inf over unit v of abs(inner(A_k v, v))','geometric_controls':{'r_min':'3/4','support_ball_radius':'3/8','curvature_at_pi_over_3':'-8/3','curvature_numerator_at_pi_over_3':'-9/8'},'matrix_A':[[1,2],[0,1]],'matrix_P':[[1,-1],[-1,3]],'zero_vector':[1,-1],'nilpotent_N2_counterexample_weight':2,'deformation_dimension':3,'deformation_growth_power':2}
EXPECTED_CLAIMS.update({k:False for k in FALSE_FIELDS})

def need(ok,msg):
    if not ok: raise ValueError(msg)

def pairs(items):
    d={}
    for k,v in items:
        need(k not in d,'duplicate JSON key: '+k)
        d[k]=v
    return d

def bad_constant(s): raise ValueError('non-finite JSON constant: '+s)

def readjson(path):
    return json.loads(path.read_text(encoding='utf-8'),object_pairs_hook=pairs,parse_constant=bad_constant)

def typed_equal(a,b):
    if type(a) is not type(b): return False
    if isinstance(a,dict): return a.keys()==b.keys() and all(typed_equal(a[k],b[k]) for k in a)
    if isinstance(a,list): return len(a)==len(b) and all(typed_equal(x,y) for x,y in zip(a,b))
    return a==b

def main():
    root=Path(__file__).resolve().parent
    actual={p.name for p in root.iterdir()}
    need(actual==FILES|{'MANIFEST.json'},'inventory mismatch')
    for name in actual:
        p=root/name
        need(not p.is_symlink() and p.is_file(),'nonregular or symlink payload: '+name)
    manifest=readjson(root/'MANIFEST.json')
    need(isinstance(manifest,dict) and set(manifest)=={'schema_version','files'} and type(manifest['schema_version']) is int and manifest['schema_version']==1,'manifest schema')
    need(isinstance(manifest['files'],dict) and set(manifest['files'])==FILES,'manifest file set')
    for name in sorted(FILES):
        item=manifest['files'][name];data=(root/name).read_bytes()
        need(isinstance(item,dict) and set(item)=={'bytes','sha256'},'manifest entry schema')
        need(type(item['bytes']) is int and item['bytes']==len(data),'byte count mismatch: '+name)
        need(type(item['sha256']) is str and item['sha256']==hashlib.sha256(data).hexdigest(),'hash mismatch: '+name)
    claims=readjson(root/'CLAIMS.json')
    need(typed_equal(claims,EXPECTED_CLAIMS),'unsupported, false or malformed claim')
    ledger=readjson(root/'LEDGER.json')
    need(type(ledger.get('problem_id')) is int and ledger['problem_id']==30003533,'ledger problem identity')
    need(ledger.get('status')=='unsolved' and ledger.get('turns')=='5/5' and ledger.get('original_target_resolved') is False and ledger.get('independent_review')=='pending','ledger scope')
    attempts=ledger.get('attempts');need(type(attempts) is list and len(attempts)==5,'ledger attempts')
    need([a.get('turn') for a in attempts]==[1,2,3,4,5],'ledger order')
    need(all(all(type(a.get(k)) is str and a[k] for k in ['method','derived_result','gap']) for a in attempts),'ledger gaps')
    result=run(claims)
    need(typed_equal(result,readjson(root/'REPLAY.json')),'replay receipt mismatch')
    print(json.dumps(result,sort_keys=True,separators=(',',':')))

if __name__=='__main__':
    try: main()
    except (ValueError,OSError,KeyError,TypeError) as exc:
        print('VERIFICATION_FAILED: '+str(exc),file=sys.stderr)
        sys.exit(1)
