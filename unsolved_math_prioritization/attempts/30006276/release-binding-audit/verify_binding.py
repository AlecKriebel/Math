#!/usr/bin/env python3
"""Read-only binding/replay checks for the corrected release; no release writes."""
from pathlib import Path
import difflib
import hashlib
import json
import subprocess
import sys

BASE=Path(__file__).resolve().parent.parent
RELEASE=BASE/'release'
EXPECTED_RELEASE='6e530df04a9bf69747646de41c6dfb3b7410576a2388843b6b754895a17339c6'
EXPECTED_AUTHOR='83549a36a97a878966348ab32cdfe0798e235e299b6841973e21c63434afec08'
EXPECTED_AUDIT='e9514f008b747812b43947ee71dc7818d3df20a775e78c7cb7ffeb4505ab0d98'
checks=0

def check(x):
    global checks
    checks+=1
    if not x: raise AssertionError(checks)

def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()

def inventory(root):
    result={}
    for p in sorted(root.rglob('*')):
        check(not p.is_symlink())
        if p.is_file(): result[p.relative_to(root).as_posix()]=sha(p)
        else: check(p.is_dir())
    return result

def check_manifest(root,expected):
    check(sha(root/'SHA256SUMS')==expected)
    listed={}
    for line in (root/'SHA256SUMS').read_text().splitlines():
        h,name=line.split()
        check(name not in listed)
        check(not Path(name).is_absolute() and '..' not in Path(name).parts)
        check(sha(root/name)==h)
        listed[name]=h
    return listed

before=inventory(RELEASE)
listed=check_manifest(RELEASE,EXPECTED_RELEASE)
check(set(before)==set(listed)|{'SHA256SUMS'})
for name in before:
    check(Path(name).suffix in {'.md','.json','.py','.patch'} or Path(name).name=='SHA256SUMS')
    check(not any(part in {'private','.git','.codex','.agents','__pycache__'} for part in Path(name).parts))
for sub,expected in [('author',EXPECTED_AUTHOR),('audit',EXPECTED_AUDIT)]:
    check_manifest(BASE/sub,expected)
    check_manifest(RELEASE/sub,expected)
    original=inventory(BASE/sub); copy=inventory(RELEASE/sub)
    check(original==copy)

ledger=json.loads((RELEASE/'CORRECTION_LEDGER.json').read_text())
changed=['PROOF.md','README.md','RESEARCH_LOG.md','RESULT.json','SOURCES.md']
check([d['file'] for d in ledger['changed_files']]==changed)
diff=''
for name in changed:
    d=next(d for d in ledger['changed_files'] if d['file']==name)
    check(d['original_sha256']==sha(RELEASE/'author'/name))
    check(d['corrected_sha256']==sha(RELEASE/name))
    diff+=''.join(difflib.unified_diff((RELEASE/'author'/name).read_text().splitlines(keepends=True),
             (RELEASE/name).read_text().splitlines(keepends=True),
             fromfile='author/'+name,tofile=name))
check(diff==(RELEASE/'CORRECTION_DIFF.patch').read_text())
check(sha(RELEASE/'CORRECTION_DIFF.patch')==ledger['exact_diff_sha256'])
for d in ledger['preserved_files']:
    check(sha(RELEASE/d['file'])==d['sha256'])
    check((RELEASE/d['file']).stat().st_size==d['bytes'])
    check(d['byte_identical'] is True)
manifest=json.loads((RELEASE/'RELEASE_MANIFEST.json').read_text())
check(set(d['file'] for d in manifest['files'])==set(before)-{'RELEASE_MANIFEST.json','SHA256SUMS'})
for d in manifest['files']:
    check(sha(RELEASE/d['file'])==d['sha256'])
    check((RELEASE/d['file']).stat().st_size==d['bytes'])

proof=(RELEASE/'PROOF.md').read_text()
old=(RELEASE/'author/PROOF.md').read_text()
check('In the following annihilator calculation assume g >= 2.' in proof)
check('nonsimple locus is empty, I=0' in proof)
check('lambda_0=1.' in proof)
check("Deligne's Proposition 8.2.7 [S7] identifies the kernels" in proof)
check('X is smooth, D is proper, D_tilde is proper and smooth,' in proof)
check('and q is surjective.' in proof)
check('H_c^(2g)(U,Q)' in proof)
check('Divide by the level-cover degree' in proof)
check('Arbitrary smooth compactifications' in proof)
check('need not themselves carry an extension from bar(M_g).' in proof)
check('pullback by this compatible extended morphism.' in proof)
# All unamended mathematical sections remain exactly the reviewed originals.
for start,end in [('## 1.','## 3.'),('### 5.1','## 6.'),('## 6.',None)]:
    x=proof[proof.index(start):]; y=old[old.index(start):]
    if end: x=x[:x.index(end)]; y=y[:y.index(end)]
    check(x==y)
new_result=json.loads((RELEASE/'RESULT.json').read_text())
old_result=json.loads((RELEASE/'author/RESULT.json').read_text())
for key,value in old_result.items(): check(new_result[key]==value)
check(new_result['status']=='unsolved')
check(new_result['full_resolution'] is False)
check(new_result['novelty_claim'] is False)
check(new_result['geometric_Torelli_left_hand_integrals_computed']==0)
check([d['id'] for d in new_result['corrections_applied']]==['C1','C2','C3'])
for p,q in [('verify_controls.py','author/verify_controls.py'),
            ('control_results.json','author/control_results.json')]:
    check((RELEASE/p).read_bytes()==(RELEASE/q).read_bytes())

replays=[]
for program,fixture,assertion_key,expected_assertions in [
    ('verify_controls.py','control_results.json','exact_assertions',5250),
    ('audit/independent_checks.py','audit/independent_results.json','independent_exact_assertions',2736)]:
    proc=subprocess.run([sys.executable,str(RELEASE/program)],cwd=RELEASE,capture_output=True,check=True)
    check(proc.stderr==b'')
    check(proc.stdout==(RELEASE/fixture).read_bytes())
    obj=json.loads(proc.stdout)
    check(obj[assertion_key]==expected_assertions)
    cases=obj['codimension_controls']['partitions_examined'] if program=='verify_controls.py' else obj['partition_check']['cases']
    check(cases==(215267 if program=='verify_controls.py' else 1295920))
    replays.append({'program':program,'fixture':fixture,'byte_identical':True,
        'assertions':expected_assertions,'partition_cases':cases,
        'result_sha256':hashlib.sha256(proc.stdout).hexdigest()})
check(before==inventory(RELEASE))
check(sha(RELEASE/'SHA256SUMS')==EXPECTED_RELEASE)
output={'problem_id':30006276,'verdict':'accepted_corrected_release','target_status':'unsolved',
    'release_manifest_sha256':EXPECTED_RELEASE,'original_author_manifest_sha256':EXPECTED_AUTHOR,
    'original_audit_sha256sums_sha256':EXPECTED_AUDIT,'binding_assertions':checks,
    'release_file_count':len(before),'release_sha256_entries':len(listed),
    'exact_diff_recomputed':True,'ledger_hashes_verified':True,'manifest_inventory_exact':True,
    'safe_inventory_verified':True,'original_author_and_audit_byte_preserved':True,
    'corrections_closed':['C1','C2','C3'],'new_geometric_claims':False,
    'geometric_Torelli_left_hand_integrals_computed':0,'full_resolution':False,
    'replays':replays,'release_unchanged_before_after':True,
    'release_inventory':before,'remote_writes_performed':False}
print(json.dumps(output,indent=2,sort_keys=True))
