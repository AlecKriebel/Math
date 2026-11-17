"""Passive finite final closure with actual source/INITIAL/native/primary schemas."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json
import os
import stat
P=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024')
A=P/'papers/23318851/reviews/adversarial-continuation-20261117'
S=P/'papers/23318851/sources'
I=P/'papers/23318851/reviews/adversarial-sol'
TERMINALS={'FINAL_MANIFEST.json','FINAL_SEAL.json'}
def sha(b):return hashlib.sha256(b).hexdigest()
def enc(v):return (json.dumps(v,indent=2,ensure_ascii=False)+'\n').encode()
def snap(root):
    rows=[]
    for p in [root,*sorted(root.rglob('*'))]:
        st=p.lstat();r={'path':'.' if p==root else str(p.relative_to(root)),
            'mode':oct(stat.S_IMODE(st.st_mode)),'hidden':any(x.startswith('.') for x in p.relative_to(root).parts)}
        if stat.S_ISDIR(st.st_mode):r.update(kind='directory',empty=not any(p.iterdir()))
        elif stat.S_ISREG(st.st_mode):
            b=p.read_bytes();r.update(kind='file',bytes=len(b),SHA256=sha(b))
        else:r.update(kind='other',target=os.readlink(p) if p.is_symlink() else None)
        rows.append(r)
    return rows
def omap(root):return {r['path']:{k:v for k,v in r.items() if k not in ['path','hidden']} for r in snap(root)}
def counts(rows):return {'files':sum(r['kind']=='file' for r in rows),
    'child_directories':sum(r['kind']=='directory' for r in rows)-1,
    'hidden_paths':sum(r['hidden'] for r in rows),
    'empty_directories':[r['path'] for r in rows if r['kind']=='directory' and r['empty']],
    'empty_files':[r['path'] for r in rows if r['kind']=='file' and r['bytes']==0]}
assert not (A/'FINAL.json').exists() and not any((A/n).exists() for n in TERMINALS)
before=json.loads((A/'CUSTODY_BEFORE.json').read_text());after=json.loads((A/'CUSTODY_AFTER.json').read_text())
assert before['source']==after['source']==snap(S)
assert before['INITIAL']==after['INITIAL']==snap(I)
assert counts(before['source'])['files']==95 and counts(before['source'])['child_directories']==16
assert counts(before['INITIAL'])['files']==18 and counts(before['INITIAL'])['child_directories']==1
assert sha((S/'SOURCE_FINAL.json').read_bytes())=='c61fb0473f0954877ab5af49e7b6139732eb4afab7cfab3377864a91dd98b317'
assert sha((S/'SOURCE_MANIFEST.json').read_bytes())=='ed5c217040b7a0d72df7de7ef1d5cbce9bc516ab32c1f20ed6466ef153a6bac8'
assert sha((I/'INITIAL_MANIFEST.json').read_bytes())=='dbb198866601fd68216f11628a508407e5a98d90c8228204f2e3d72ae39c20e6'
assert sha((I/'INITIAL_SEAL.json').read_bytes())=='9e314a96b491a96f18ad3cdaa1cdcc9c1c3c125e69a16bbb3a60fae5e8cf4d86'
nb=json.loads((A/'NATIVE_INPUT_BEFORE.json').read_text());na=json.loads((A/'NATIVE_INPUT_AFTER.json').read_text())
assert nb['source']==na['source']==omap(S/'archives/02-gram_locus_support.zip.extracted')
assert nb['isolated']==na['isolated']==omap(A/'native-isolated')
assert na['source_exact'] and na['added_paths']==[] and na['removed_paths']==[] and na['changed_records']=={}
run=json.loads((A/'NATIVE_RUN.json').read_text())
assert run['attempts']==1 and run['exit']==0 and run['repairs_retries_installs_interpreter_switches']==0
for stem in ['stdout','stderr']:
    b=(A/('NATIVE.'+stem+'.bin')).read_bytes()
    assert len(b)==run[stem+'_bytes'] and sha(b)==run[stem+'_SHA256']
assert run['stdout_bytes']==216 and run['stderr_bytes']==0
primary=json.loads((A/'PRIMARY_RECEIPT.json').read_text())
assert len(primary['primary_files'])==6
for r in primary['primary_files']:
    b=(A/r['path']).read_bytes();assert len(b)==r['bytes'] and sha(b)==r['SHA256']
now=datetime.now(timezone.utc).isoformat()
final={'UTC':now,'row':194,'record':'23318851','phase':'FINAL_ADVERSARIAL_SCIENTIFIC_REVIEW',
    'completion_percent':100,'interpretation':'Assigned bounded mathematical family; not formal certainty or independent priority clearance',
    'mathematical_status':'Supported ordinary independent written-proof review; no verified central gap found',
    'core_claim':'Closed-ball real binary Gram locus has no single determinant-polynomial nonnegativity definition in cube or stated hull for each n>=3',
    'positive_witness_and_primary_Q_direction_verified':True,'printed_GHZ_caution_verified':True,
    'priority_status':'Not cleared by this family; current priority-family/root findings unread',
    'central_gap':None,'follow_up':None,'root_owns_final_adoption':True,
    'source_files':95,'source_child_directories':16,'INITIAL_files':18,'INITIAL_child_directories':1,
    'complete_source_INITIAL_byte_mode_hidden_empty_topology_exact':True,
    'native_attempts':1,'native_exit':0,'native_stdout_bytes':216,'native_stderr_bytes':0,
    'native_elapsed_seconds':run['elapsed_seconds'],'native_original_isolated_whole_tree_exact':True,
    'native_nested_stream_time_limit':run['internal_stream_time_limit'],
    'native_repairs_retries_installs_interpreter_switches':0,
    'primary_files_authenticated':6,'actual_primary_read_scope':'EXPOSURE_AND_PRIMARY_LEDGER.md',
    'historical_packaged_audit_bodies_or_current_peer_root_reports_read':False,
    'original_author_version':'1.0.0','original_declared_date':'2026-10-12',
    'website_Sheet_Git_release_Zenodo_mutations':0,'external_contact_outreach':0,'children':0,
    'report':'FINAL_REPORT.md','checkpoint':'CHECKPOINT.md',
    'mechanisms_verdicts_withheld_from_messages_until_root_request':True,'stop':True}
(A/'FINAL.json').write_bytes(enc(final))
for n in TERMINALS:(A/n).write_bytes(b'')
rows=snap(A);assert not any(r['kind']=='other' for r in rows)
for r in rows:
    if r['path'] in TERMINALS:r['SHA256']='EXCLUDED_TERMINAL_RECURSIVE_HASH'
scope=counts(rows);scope['empty_files']=[n for n in scope['empty_files'] if n not in TERMINALS]
manifest={'UTC':now,'root':str(A),**scope,'all_actual_bytes_modes_hidden_empty_topology':True,
    'only_recursive_hash_exclusions':sorted(TERMINALS),'entries':rows}
seal={'UTC':now,'frozen':True,'root':str(A),**scope,'manifest_bytes':0,'manifest_SHA256':'0'*64,
    'FINAL_SHA256':sha((A/'FINAL.json').read_bytes()),'FINAL_REPORT_SHA256':sha((A/'FINAL_REPORT.md').read_bytes()),
    'CUSTODY_BEFORE_SHA256':sha((A/'CUSTODY_BEFORE.json').read_bytes()),
    'CUSTODY_AFTER_SHA256':sha((A/'CUSTODY_AFTER.json').read_bytes()),
    'source95_16_INITIAL18_1_exact':True,'native_attempts':1,'native_exit':0,
    'only_recursive_hash_exclusions':sorted(TERMINALS),'seal_SHA256':'EXCLUDED_TERMINAL_RECURSIVE_HASH',
    'completion_percent':100,'follow_up':None,'stop':True}
for _ in range(20):
    mb=enc(manifest);seal['manifest_bytes']=len(mb);seal['manifest_SHA256']=sha(mb);sb=enc(seal)
    sizes={'FINAL_MANIFEST.json':len(mb),'FINAL_SEAL.json':len(sb)}
    if all(r['bytes']==sizes[r['path']] for r in rows if r['path'] in TERMINALS):break
    for r in rows:
        if r['path'] in TERMINALS:r['bytes']=sizes[r['path']]
else:raise AssertionError('Terminal size fixed point failed')
(A/'FINAL_MANIFEST.json').write_bytes(mb);(A/'FINAL_SEAL.json').write_bytes(sb)
actual=snap(A)
for r in actual:
    if r['path'] in TERMINALS:r['SHA256']='EXCLUDED_TERMINAL_RECURSIVE_HASH'
assert actual==rows and counts(actual)==scope
assert before['source']==snap(S) and before['INITIAL']==snap(I)
print(json.dumps({'UTC':now,'frozen':True,**scope,'FINAL_SHA256':seal['FINAL_SHA256'],
    'report_SHA256':seal['FINAL_REPORT_SHA256'],'manifest_bytes':len(mb),'manifest_SHA256':sha(mb),
    'seal_bytes':len(sb),'seal_SHA256':sha(sb),'source95_16_INITIAL18_1_exact':True,
    'native_attempts':1,'native_exit':0,'completion_percent':100}))
