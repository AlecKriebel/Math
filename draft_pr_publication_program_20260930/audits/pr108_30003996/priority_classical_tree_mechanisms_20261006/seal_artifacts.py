"""Verify custody receipts and seal first-party metadata in this directory only."""
from pathlib import Path
import json,hashlib,datetime,os
B=Path(__file__).resolve().parent
def h(p):
    d=p.read_bytes();return {'bytes':len(d),'sha256':hashlib.sha256(d).hexdigest()}
now=datetime.datetime.now(datetime.timezone.utc).isoformat()
receipt_checks=0
for line in (B/'CLI_LEDGER.jsonl').read_text().splitlines():
    c=json.loads(line)
    for stream in ['stdout','stderr']:
        p=B/'_private'/(c['label']+'.'+stream)
        actual=h(p)
        assert actual['bytes']==c[stream+'_bytes'],p
        assert actual['sha256']==c[stream+'_sha256'],p
        receipt_checks+=1
for p in B.glob('*.json'):
    if 'MANIFEST' not in p.name and p.name!='SEAL.json':json.loads(p.read_text())
bind=json.loads((B/'INPUT_BINDINGS.json').read_text())
for key in ['candidate_proof','original_source_pdf','gate']:
    x=bind[key];actual=h(B/x['path'])
    assert actual['bytes']==x['bytes'] and actual['sha256']==x['sha256'],key
comp=json.loads((B/'COMPARISON_RESULTS.json').read_text())
assert comp['trees_checked']==16 and comp['exact_cut_identity_checked']
assert comp['fixed_core_leaf_comparison']['identity_verified']
assert comp['fixed_core_leaf_comparison']['literal_mixed_difference']==0
assert comp['fixed_core_leaf_comparison']['routing_mixed_difference']==-4
v=json.loads((B/'VERDICT.json').read_text())
assert v['priority_established_percent']==0 and not v['novelty_cleared']
assert v['new_central_proof_search_approaches']==0
with (B/'RESEARCH_LOG.md').open('a') as f:
    f.write(f'\n- {now}: Checkpoint5. Scope extended to concrete MINCCA antecedent: retrieved revised2013 author preprint, checked both complete hardness reductions and exact quadratic model; original2011 chronology version remains unavailable. Reassessed family review95% during extension, then sealed bounded packet100%. Independent GO to fresh combined review/narrow2018-question note if it passes; NO-GO for absolute-priority/novelty certification. Broader novelty establishment0%; original2/5 and extra proof routes0 retained.\n')
seal={'UTC':now,'operator_PID':os.getpid(),'receipt_stream_checks':receipt_checks,'input_bindings_verified':True,'JSON_validated':True,'comparative_checks_validated':True,'recommendation':'Independent source-priority review recommendation, not publication authority.','hash_algorithm':'SHA256','manifests_exclude':'PUBLIC_MANIFEST.json excludes itself; SEAL.json and PRIVATE_CUSTODY_MANIFEST.json are included. Private files are only hash metadata in public custody manifest.'}
(B/'SEAL.json').write_text(json.dumps(seal,indent=2)+'\n')
private={'UTC':now,'custody':'private third-party/raw material; metadata-only inventory','files':[{'private_relative_path':str(p.relative_to(B)),**h(p)} for p in sorted((B/'_private').iterdir()) if p.is_file()]}
(B/'PRIVATE_CUSTODY_MANIFEST.json').write_text(json.dumps(private,indent=2)+'\n')
public={'UTC':now,'files':[{'relative_path':p.name,**h(p)} for p in sorted(B.iterdir()) if p.is_file() and p.name!='PUBLIC_MANIFEST.json'],'self_excluded':'PUBLIC_MANIFEST.json','private_inventory':'PRIVATE_CUSTODY_MANIFEST.json','authority':'No novelty/publication/closure authority.'}
(B/'PUBLIC_MANIFEST.json').write_text(json.dumps(public,indent=2)+'\n')
print(json.dumps({'UTC':now,'operator_PID':os.getpid(),'receipt_stream_checks':receipt_checks,'public_files':len(public['files']),'private_files':len(private['files']),'public_manifest':h(B/'PUBLIC_MANIFEST.json'),'verdict':h(B/'VERDICT.json'),'report':h(B/'REPORT.md')}))
