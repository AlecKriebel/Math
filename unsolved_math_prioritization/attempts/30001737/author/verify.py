#!/usr/bin/env python3
"""Pinned package verifier. Checks are active under -O; no mathematical oracle."""
import argparse
import hashlib
import importlib.util
import json
from pathlib import Path
import stat

PAYLOAD={'REPORT.md','PUBLIC_METADATA.json','SOURCES.json','math_checks.py','verify.py','audit_checks.py','VERIFICATION.json','verify_corpora.py'}
def need(ok,message):
    if not ok: raise ValueError(message)
def sha(b): return hashlib.sha256(b).hexdigest()
def unique(pairs):
    d={}
    for k,v in pairs:
        need(k not in d,'Duplicate JSON key')
        d[k]=v
    return d
def parse(b): return json.loads(b,object_pairs_hook=unique)
def verify(root,pin):
    need(not root.is_symlink() and root.is_dir(),'Invalid root')
    entries=list(root.iterdir())
    need({p.name for p in entries}==PAYLOAD|{'MANIFEST.json'},'Unexpected inventory')
    for p in entries:
        st=p.lstat();need(stat.S_ISREG(st.st_mode) and st.st_nlink==1,'Nonregular or aliased entry')
    raw=(root/'MANIFEST.json').read_bytes();need(sha(raw)==pin,'External manifest pin mismatch')
    manifest=parse(raw)
    need(set(manifest)=={'schema','files'} and manifest['schema']=='strict-flat-sha256-v1','Manifest schema')
    need(set(manifest['files'])==PAYLOAD,'Manifest inventory')
    for name in sorted(PAYLOAD):
        b=(root/name).read_bytes();need(manifest['files'][name]=={'bytes':len(b),'sha256':sha(b)},'Payload mismatch '+name)
    m=parse((root/'PUBLIC_METADATA.json').read_bytes())
    need(m['problem_id']==30001737 and m['problem_number']=='OWR-4804-005','Identity')
    need(m['disposition']=='not_solved_here_status_correction_and_expository_partial','Disposition')
    for key in ['full_resolution_claim','novel_mathematical_result_claim','target_counterexample_claim']:
        need(m[key] is False,'Invalid result claim '+key)
    need(m['actual_substantive_approaches']==3 and m['maximum_substantive_approaches']==5,'Approach count')
    target={'base_field':'R','extension_field':'C','ambient_group':'GL_n(C)','subgroup':'U(p,q)','representation_category':'irreducible_Casselman_Wallach','functional_category':'continuous_complex_linear','parameter_conjugation':'(k,s)->(-k,s)','symmetry':'pi_tau_isomorphic_pi','induction':'normalized_standard_Langlands_order','signature':'p,q_nonnegative_integers_p_plus_q_equals_n','orbit_count':'nonfixed_pairs_counted_with_multiplicity','extra_parity_restriction':False}
    need(m['exact_target']==target,'Target scope changed')
    for key in ['formula_is_period_dimension','positive_upper_bound_proves_distinction','quotient_example_is_target_counterexample']:
        need(m['partial_results'][key] is False,'Unsupported mathematical inference '+key)
    need(m['statement_identity']=={'bytes':len_of_statement(),'sha256':'89d6225abbe19de7352c6960382ec2a36ca00cd192d8c48cfc3e743c072fe08e','matches_catalog':True},'Statement pin')
    r=m['full_record_review'];need(r['bytes']==4195 and r['sha256']=='8ba2836d652463cffa7f4d58ad97db568547c48217eb4dc4b6a77b326ff8336d' and r['matches_catalog'] is True and r['report_present'] is False,'Full record review pin')
    c=m['public_dataset_fingerprints']['catalog'];need(c=={'bytes':21735099,'sha256':'891938878f1e395de77f6829d5d5d13cb5d5393f85efaa7941fb14bd3e3d7566'},'Catalog pin')
    sources=parse((root/'SOURCES.json').read_bytes());need(sources['target_live_fetch']['live_statement_verified'] is False,'Live status overclaimed')
    need({x['id'] for x in sources['sources']}=={'OWR2011','FLO2012','GUREVICH2015','ZOU2024','BEUZART_PLESSIS2025'},'Source inventory')
    spec=importlib.util.spec_from_file_location('unitary_counting_checks',root/'math_checks.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
    result=module.run();need(result['status']=='pass' and result['stable_multiplicity_patterns']==174 and result['signature_cases']==1266,'Math regression counts')
    return {'status':'pass','payload_files':len(PAYLOAD),'math_checks':result,'scope':'Integrity, exact scope, and finite combinatorial regression checks; general converse unresolved.'}
def len_of_statement():
    return 291
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--root',type=Path,default=Path(__file__).resolve().parent);p.add_argument('--manifest-sha256',required=True);a=p.parse_args()
    print(json.dumps(verify(a.root,a.manifest_sha256),sort_keys=True))
