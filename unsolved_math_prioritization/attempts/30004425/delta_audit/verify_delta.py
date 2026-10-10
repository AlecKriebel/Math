#!/usr/bin/env python3
"""Read-only exact delta audit. Arguments: original corrected independent-audit."""
from pathlib import Path
import difflib
import hashlib
import json
import subprocess
import sys
import zipfile

old, new, audit = map(Path, sys.argv[1:4])

def require(test, label):
    if not test:
        raise AssertionError(label)

def pin(path):
    b = path.read_bytes()
    return {'bytes':len(b), 'sha256':hashlib.sha256(b).hexdigest()}

def run(path, *args):
    return subprocess.check_output([sys.executable, str(path), *map(str,args)])

original_archive = old.parent / 'TROPICAL_WALL_30004425_AUTHOR_SAFE_FREEZE.zip'
corrected_archive = new.parent / 'TROPICAL_WALL_30004425_CORRECTED_SAFE_FREEZE.zip'
expected_original = {'bytes':17849,'sha256':'8297f9480c92cf9a736468cfeefc008b62a04b7e4674c8851b9e72fb6c99a446'}
expected_corrected = {'bytes':25136,'sha256':'a53534d916ae974461131d47fab6589d80bfc1799ecffad4c6b3f56691d303c8'}
expected_diff = {'bytes':9236,'sha256':'ae6cd7dd45c4192d050fb123d7de6c81f881504557bfaf854fe5c88f9cdd2407'}
expected_manifest = {'bytes':1500,'sha256':'bd3994c0ff3a51c3695135291206af0e50455c461a482f1738b0939fe3eb5a82'}
require(pin(original_archive)==expected_original,'Original archive pin')
require(pin(corrected_archive)==expected_corrected,'Corrected archive pin')
require(pin(new/'CORRECTIONS.diff')==expected_diff,'Correction diff pin')
require(pin(new/'MANIFEST.json')==expected_manifest,'Corrected manifest pin')
require(pin(audit/'MANIFEST.json')['sha256']=='a52431e654bd7354f89867de09c823a3b0010768cb9ad1c3a4a35f253097e413','Original audit preserved')

for folder, archive, count in [(old,original_archive,8),(new,corrected_archive,11)]:
    with zipfile.ZipFile(archive) as z:
        require(len(z.namelist())==count,'Archive member count')
        require(set(z.namelist())=={folder.name+'/'+p.name for p in folder.iterdir() if p.is_file()},'Exact archive membership')
        for name in z.namelist():
            require(z.read(name)==(folder/Path(name).name).read_bytes(),'Archive member bytes')

manifest_checks = {
    'original':json.loads(run(old/'verify_manifest.py')),
    'corrected':json.loads(run(new/'verify_manifest.py')),
    'independent_audit':json.loads(run(audit/'verify_audit_manifest.py')),
}
old_names = {p.name for p in old.iterdir() if p.is_file()}
new_names = {p.name for p in new.iterdir() if p.is_file()}
added = new_names-old_names
changed = {name for name in old_names & new_names if (old/name).read_bytes()!=(new/name).read_bytes()}
require(added=={'PUBLICATION_SCOPE.md','CORRECTIONS.diff','CORRECTION_RESULTS.json'},'Only authorized added files')
require(changed=={'REPORT.md','SOURCE_VERIFICATION.json','MANIFEST.json'},'Only authorized changed originals')
require(not old_names-new_names,'No original removed')
unchanged = old_names-changed
old_report=(old/'REPORT.md').read_text()
require(old_report.count('and finite semigroups S_i')==1,'Unique terminology correction')
require(old_report.replace('and finite semigroups S_i','and finitely generated semigroups S_i')==(new/'REPORT.md').read_text(),'Report only required terminology correction')

s0=json.loads((old/'SOURCE_VERIFICATION.json').read_bytes())
s1=json.loads((new/'SOURCE_VERIFICATION.json').read_bytes())
queue=s1['repository']['queue']
require(queue['complete_content_bytes']==389371 and queue['sha256']=='6b37d1112c4223ae1c39156a98a745389112a7b129080dcd3a6439c334ebf2c2','Correct queue byte evidence')
require(queue['git_blob_sha1']==queue['tree_blob_sha']=='483de6795be8c12bacc3d18e1ef04900eddedf04','Correct queue blob')
require(queue['matches_git_tree_blob_and_size'] and queue['embedded_header_is_file_text_not_transport_metadata'] and not queue['repair_required'],'No false queue mismatch')
require(s1['publication_disposition']['status']=='unsolved' and s1['publication_disposition']['turns_used']==1 and s1['publication_disposition']['turn_limit']==5,'Root disposition')
require(not s1['new_solution_claim'] and not s1['novelty_claim'],'No resolution upgrade')
normalized=json.loads(json.dumps(s1))
for key in ['checked_at_utc','independent_audit']:
    normalized[key]=s0[key]
normalized['repository']['queue']=s0['repository']['queue']
normalized['retrieval_history'][-1]=s0['retrieval_history'][-1]
del normalized['publication_disposition']
require(normalized==s0,'No other source-metadata changes')

expected_diff_text=''
for name in ['REPORT.md','SOURCE_VERIFICATION.json','PUBLICATION_SCOPE.md']:
    before=(old/name).read_text().splitlines(keepends=True) if (old/name).exists() else []
    after=(new/name).read_text().splitlines(keepends=True)
    expected_diff_text+=''.join(difflib.unified_diff(before,after,fromfile='original/'+name,tofile='corrected/'+name))
require(expected_diff_text==(new/'CORRECTIONS.diff').read_text(),'Diff exact for declared prose/metadata scope')

scope=(new/'PUBLICATION_SCOPE.md').read_text()
require('**unsolved, 1/5**' in scope and 'no new theorem, new counterexample, or universal resolution' in scope,'Publication-scope qualification')
receipt=json.loads((new/'CORRECTION_RESULTS.json').read_bytes())
require(receipt['old_archive']==expected_original,'Author correction receipt original pin')
require(set(receipt['unchanged_files'])==unchanged,'Author receipt unchanged file membership')
require(all(receipt['unchanged_files'][name]==pin(new/name) for name in unchanged),'Author receipt unchanged file pins')
require(set(receipt['added_files'])==added,'Author receipt additions')
require(set(receipt['changed_original_files'])==changed-{'MANIFEST.json'},'Author receipt changes')

replay=run(new/'verify.py')
require(replay==(new/'VERIFICATION_RESULTS.json').read_bytes()==(old/'VERIFICATION_RESULTS.json').read_bytes(),'Corrected exact replay')
mutations=run(audit/'mutation_verify.py',new)
require(mutations==(audit/'MUTATION_RESULTS.json').read_bytes(),'All four negative mutations still rejected')

print(json.dumps({
    'delta_verdict':'PASS',
    'problem_id':30004425,
    'scope':'Acceptance of the bounded publication corrections, not a universal mathematical resolution',
    'required_corrections':{'finitely_generated_terminology':'FIXED','queue_embedded_header_interpretation':'FIXED'},
    'root_publication_disposition':{'status':'unsolved','turns_used':1,'turn_limit':5},
    'original_archive':pin(original_archive),'corrected_archive':pin(corrected_archive),
    'corrected_manifest':pin(new/'MANIFEST.json'),'corrections_diff':pin(new/'CORRECTIONS.diff'),
    'publication_scope':pin(new/'PUBLICATION_SCOPE.md'),
    'original_audit_manifest':pin(audit/'MANIFEST.json'),
    'manifest_checks':manifest_checks,
    'changed_original_files':sorted(changed),'added_files':sorted(added),
    'unchanged_original_files':{name:pin(new/name) for name in sorted(unchanged)},
    'exact_diff_matches':'PASS','source_metadata_change_allowlist':'PASS',
    'corrected_arithmetic_replay':'PASS, byte-identical to original results',
    'negative_mutations':json.loads(mutations),
    'source_clarifications':'Independently re-read against already-refetched pinned EH v2 equation 2.4, choices before 2.7, and Lemmas 3.7-3.8',
    'original_freeze_and_audit_preserved':True,
    'remote_writes':False
},indent=2))
