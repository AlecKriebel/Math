#!/usr/bin/env python3
"""Replay every historical/family computation from ignored copies, no source writes."""
import datetime,hashlib,json,pathlib,shutil,subprocess,sys
OUT=pathlib.Path(__file__).resolve().parent
AUDIT=OUT.parent
REPO=OUT.parents[3]
TMP=OUT/'tmp/replays'
sha=lambda b:hashlib.sha256(b).hexdigest()
receipts=[]
def run(name,source,expected,json_compare=False,ignore=()):
    dest=TMP/name
    dest.mkdir(parents=True,exist_ok=True)
    copied=dest/source.name
    shutil.copy2(source,copied)
    p=subprocess.run([sys.executable,str(copied)],cwd=dest,capture_output=True)
    (dest/'stdout.txt').write_bytes(p.stdout);(dest/'stderr.txt').write_bytes(p.stderr)
    assert p.returncode==0,(name,p.stderr.decode())
    old=expected.read_bytes()
    ok=p.stdout==old
    if json_compare:
        newj=json.loads(p.stdout);oldj=json.loads(old)
        for key in ignore: newj.pop(key,None);oldj.pop(key,None)
        assert newj==oldj,(name,'JSON mismatch')
    else: assert ok,(name,'byte mismatch')
    receipts.append({'name':name,'script_sha256':sha(source.read_bytes()),'copied_script_identical':source.read_bytes()==copied.read_bytes(),'returncode':p.returncode,'stdout_sha256':sha(p.stdout),'expected_sha256':sha(old),'byte_identical':ok,'mathematical_fields_match':True,'ignored_fields':list(ignore),'stderr':p.stderr.decode()})
    print(name+': PASS',flush=True)

run('original8',AUDIT/'reviewed_candidate/verify.py',AUDIT/'reviewed_candidate/verification.txt')
run('historical11',AUDIT/'reviewed_candidate/review/independent_checks.py',AUDIT/'reviewed_candidate/review/independent_results.json')
run('compatibility19',AUDIT/'compatibility_family/exact_falsification_controls.py',AUDIT/'compatibility_family/exact_control_results.json')
run('signed19',AUDIT/'signed_measure_family/fresh_controls.py',AUDIT/'signed_measure_family/fresh_results.json')
run('primary10',AUDIT/'primary_scope_family/check_source_domain_types.py',AUDIT/'primary_scope_family/source_domain_type_results.json',True,('timestamp_utc','python'))

# Path-only adaptation: the original script assumes its original family depth.
# A scratch copy and complete scratch source_snapshot keep all writes local.
dest=TMP/'provenance/primary_scope_family';dest.mkdir(parents=True,exist_ok=True)
shutil.copytree(AUDIT/'source_snapshot',dest.parent/'source_snapshot',dirs_exist_ok=True)
shutil.copy2(AUDIT/'snapshot_manifest.json',dest.parent/'snapshot_manifest.json')
source=AUDIT/'primary_scope_family/check_pinned_sources.py'
text=source.read_text();assert text.count('REPO=ROOT.parents[3]')==1
patched=text.replace('REPO=ROOT.parents[3]','REPO=Path('+repr(str(REPO))+')')
copy=dest/source.name;copy.write_text(patched)
p=subprocess.run([sys.executable,str(copy)],cwd=dest,capture_output=True)
(dest/'stdout.txt').write_bytes(p.stdout);(dest/'stderr.txt').write_bytes(p.stderr)
assert p.returncode==0,p.stderr.decode()
new=json.loads((dest/'pinned_corpus_receipt.json').read_bytes())
old=json.loads((AUDIT/'primary_scope_family/pinned_corpus_receipt.json').read_bytes())
for j in (new,old):
    for key in ('checked_at_utc','script_sha256'):j.pop(key,None)
assert new==old,'pinned provenance fields differ'
receipts.append({'name':'pinned_provenance','original_script_sha256':sha(source.read_bytes()),'scratch_path_adapted_script_sha256':sha(copy.read_bytes()),'adaptation':'one REPO path assignment; no mathematical/source query change','excluded_fields':['checked_at_utc','script_sha256'],'returncode':0,'all_pinned_fields_equal':True,'stderr':p.stderr.decode()})
print('pinned provenance: PASS',flush=True)
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pass':True,'python':sys.version,'sympy':__import__('sympy').__version__,'original_controls':8,'historical_controls':11,'family_controls':48,'receipts':receipts,'scope':'Complete replay plus independently sealed universal proof audit; finite tests are supplemental.'}
(OUT/'REPLAY_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print('All replays complete.',flush=True)
