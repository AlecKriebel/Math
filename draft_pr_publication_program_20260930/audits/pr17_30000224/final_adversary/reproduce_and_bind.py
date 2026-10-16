#!/usr/bin/env python3
"""Validation only: exact immutable-input binding and isolated script replay."""
from pathlib import Path
import concurrent.futures as cf
import datetime as dt
import hashlib
import json
import shutil
import subprocess
import sys

HERE = Path(__file__).resolve().parent
BASE = HERE.parent
ROOT = BASE.parents[2]
def sha(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def utc(): return dt.datetime.now(dt.timezone.utc).isoformat()
def read(p): return json.loads(p.read_text())

input_paths = sorted(p for p in BASE.rglob('*') if p.is_file() and HERE not in p.parents)
before = {str(p.relative_to(ROOT)): {'sha256':sha(p),'bytes':p.stat().st_size} for p in input_paths}

candidate = read(BASE/'reviewed_candidate/MANIFEST.json')
assert all(sha(BASE/'reviewed_candidate'/name)==digest for name,digest in candidate['sha256'].items())
assert sha(BASE/'reviewed_candidate/PARTIAL_RESULTS.md')=='5e4e60e433a714f333709af2f1a59c1f33c22b374acad2740e3a57517fc143de'
assert sha(BASE/'reviewed_candidate/MANIFEST.json')=='8041f6d02c6b5586c4e5d10b354d7dd3f8b6bbd8af26eed16ad20d96602a5390'

snapshot = read(BASE/'snapshot_manifest.json')
frozen = []
for item in snapshot['files']:
    local=BASE/'source_snapshot'/item['path']
    historical=subprocess.check_output(['git','show',snapshot['head']+':unsolved_math_prioritization/attempts/30000224/'+item['path']],cwd=ROOT)
    blob=hashlib.sha256(historical).hexdigest()
    assert sha(local)==blob==item['sha256']
    frozen.append({'path':item['path'],'sha256':blob,'git_blob':item['git_blob'],'head_bytes_identical':True})
assert len(frozen)==14

families = read(BASE/'FAMILY_MANIFEST.json')
for family,files in families['sha256'].items():
    for name,digest in files.items(): assert sha(BASE/family/name)==digest,(family,name)
cache=read(BASE/'geometry_family/cache_relocation.json')
for item in cache['files']:
    path=ROOT/item['ignored_cache_path']
    assert sha(path)==item['sha256'] and path.stat().st_size==item['bytes']
    assert subprocess.run(['git','check-ignore','--quiet',str(path)],cwd=ROOT).returncode==0
    assert not (ROOT/item['original_family_cache_path']).exists()

jobs = [
 ('author','reviewed_candidate/verify.py','verification.json','reviewed_candidate/verification.json',shutil.which('python3')),
 ('historical_reviewer','reviewed_candidate/independent_checks.py','independent_results.json','reviewed_candidate/independent_results.json',str(ROOT/'.venv/bin/python')),
 ('algebra','algebra_family/exact_probes.py','evidence/exact_probe_results.json','algebra_family/evidence/exact_probe_results.json',shutil.which('python3')),
 ('geometry','geometry_family/independent_probes.py','probe_results.json','geometry_family/probe_results.json',shutil.which('python3')),
 ('primary','primary_scope_family/independent_replay.py','replay_results.json','primary_scope_family/replay_results.json',shutil.which('python3')),
]

def replay(job):
    name,source,receipt,prior,python=job
    work=HERE/'tmp'/'replays'/name
    work.mkdir(parents=True,exist_ok=True)
    (work/'evidence').mkdir(exist_ok=True)
    script=work/Path(source).name
    shutil.copyfile(BASE/source,script)
    assert sha(script)==sha(BASE/source)
    proc=subprocess.run([python,str(script)],cwd=work,text=True,capture_output=True,timeout=300)
    (work/'stdout.txt').write_text(proc.stdout)
    (work/'stderr.txt').write_text(proc.stderr)
    assert proc.returncode==0,(name,proc.stderr)
    fresh=work/receipt
    original=BASE/prior
    a,b=read(fresh),read(original)
    ignored=[]
    if name=='algebra':
        ignored=['checked_at_utc']
        a.pop('checked_at_utc',None); b.pop('checked_at_utc',None)
    assert a==b,(name,'receipt differs beyond documented timestamp')
    return {'name':name,'source_script':source,'source_script_sha256':sha(BASE/source),
            'isolated_script_sha256':sha(script),'source_receipt_sha256':sha(original),
            'fresh_receipt_path':str(fresh.relative_to(HERE)), 'fresh_receipt_sha256':sha(fresh),
            'exit_code':proc.returncode,'byte_identical':fresh.read_bytes()==original.read_bytes(),
            'all_math_fields_equal':True,'ignored_fields':ignored,
            'assertions':a.get('assertions',a.get('assertions_passed',a.get('independent_check_groups'))),
            'stdout_sha256':sha(work/'stdout.txt'),'stderr_sha256':sha(work/'stderr.txt')}

with cf.ThreadPoolExecutor(max_workers=5) as pool:
    results=list(pool.map(replay,jobs))
for p in input_paths: assert before[str(p.relative_to(ROOT))]['sha256']==sha(p),str(p)

status=read(BASE/'reviewed_candidate/status.json')
assert status['turns_used']==4 and status['turn_limit']==5 and status['full_target_solved'] is False
turns=(BASE/'reviewed_candidate/turns.jsonl').read_bytes()
assert turns==(BASE/'source_snapshot/turns.jsonl').read_bytes()
assert len(turns.splitlines())==4
review=read(BASE/'reviewed_candidate/review_summary.json')
assert review['reviewed_sha256']==sha(BASE/'source_snapshot/PARTIAL_RESULTS.md')
assert review['reviewed_sha256']!=sha(BASE/'reviewed_candidate/PARTIAL_RESULTS.md')
queue=(ROOT/'unsolved_math_prioritization/QUEUE.md').read_text()
row=next(line for line in queue.splitlines() if '30000224 / OWR-824-008' in line)
assert '| queued | 0/5 |' in row
binding={'checked_at_utc':utc(),'candidate_proof_sha256':sha(BASE/'reviewed_candidate/PARTIAL_RESULTS.md'),
 'candidate_manifest_sha256':sha(BASE/'reviewed_candidate/MANIFEST.json'),
 'frozen_head':snapshot['head'],'original14files_verified':frozen,
 'family_manifest_all_entries_match':True,'geometry_cache_relocation_all_bytes_match_and_ignored':True,
 'first_pass_seal_valid':sha(HERE/'FIRST_PASS.md')==read(HERE/'FIRST_PASS_SEAL.json')['first_pass_sha256'],
 'all_inputs_before_and_after_identical':True,'all_input_files':before,
 'actual_main_queue_row_during_audit':row,'proposed_status':'unsolved4/5 after parent integration in PR order',
 'historical_review_current_hash_different':True,'turns4of5_preserved':True,
 'branch_during_audit':subprocess.check_output(['git','branch','--show-current'],cwd=ROOT,text=True).strip()}
(HERE/'INPUT_BINDING.json').write_text(json.dumps(binding,indent=2)+'\n')
(HERE/'REPRODUCTION.json').write_text(json.dumps({'checked_at_utc':utc(),'replays':results,'all_math_fields_equal':True,'all_inputs_untouched':True},indent=2)+'\n')
print(json.dumps({'replays':[{k:r[k] for k in ('name','exit_code','byte_identical','all_math_fields_equal','assertions')} for r in results], 'original_files':len(frozen),'input_files_bound':len(before)},indent=2))
