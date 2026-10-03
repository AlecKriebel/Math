#!/usr/bin/env python3
"""Complete root replay of the current, pre-final and superseded PR379 packets."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, shutil, subprocess, sys

A = Path(__file__).resolve().parent
D = A / 'clean_corrected_final_adversary'
W = A / 'tmp/root_clean_final_packets'
assert not W.exists(), 'Do not overwrite a completed or failed run.'
W.mkdir(parents=True)
TARGET = 'problems/30000590_group_ring_cohomology'
CURRENT = W / 'current'
shutil.copytree(A / 'scope_repaired_snapshot' / TARGET, CURRENT)
PRE = W / 'pre_final'
shutil.copytree(CURRENT, PRE)
(PRE / 'FINAL_AUTHOR_MANIFEST.json').unlink()
OLD = W / 'original'
OLD.mkdir()
oldhead = '90794508688ec07f598e0871bbd1eb38aaf466ce'
for p in subprocess.check_output(['git','ls-tree','-r','--name-only',oldhead,'--',TARGET],text=True).splitlines():
    out = OLD / Path(p).relative_to(TARGET)
    out.parent.mkdir(parents=True,exist_ok=True)
    out.write_bytes(subprocess.check_output(['git','show',oldhead+':'+p]))
SOURCES = A / 'root_raw_sources'
source_checks = []
fresh = json.loads((D / 'FRESH_SIX_SOURCE_BINDINGS.json').read_text())['fresh_fetches']
for e in fresh:
    for p in [SOURCES/e['candidate_filename'], D/'raw_sources'/e['fresh_private_filename']]:
        b=p.read_bytes()
        assert len(b)==e['bytes'] and hashlib.sha256(b).hexdigest()==e['sha256'], str(p)
    source_checks.append(e)

def inventory(root):
    return {str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest()
            for p in root.rglob('*') if p.is_file()}
before={str(p):inventory(p) for p in [CURRENT, PRE, OLD]}
jobs=[]
for n in range(1,6): jobs.append((f'author_turn_{n}',CURRENT/f'check_turn_{n}.py',[],CURRENT))
jobs += [
 ('prior_independent_controls',CURRENT/'review/independent_checks.py',[],CURRENT),
 ('packet_no_sources',CURRENT/'verify_packet.py',[],CURRENT),
 ('packet_with_fresh_sources',CURRENT/'verify_packet.py',['--source-dir',str(SOURCES)],CURRENT),
 ('review_wrapper',CURRENT/'review/verify_review.py',['--author',str(CURRENT)],CURRENT),
 ('publication_no_sources',CURRENT/'verify_publication.py',[],CURRENT),
 ('publication_with_fresh_sources',CURRENT/'verify_publication.py',['--source-dir',str(SOURCES)],CURRENT),
 ('historical_pre_final_receipt',PRE/'verify_packet.py',['--author-dir',str(PRE),'--source-dir',str(SOURCES),'--allow-unfrozen'],PRE),
 ('original_publication_no_sources',OLD/'verify_publication.py',[],OLD),
 ('original_publication_with_fresh_sources',OLD/'verify_publication.py',['--source-dir',str(SOURCES)],OLD),
]
records=[]
for label,script,args,cwd in jobs:
    p=subprocess.run([sys.executable,'-B',str(script),*args],cwd=cwd,
                     env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'),capture_output=True)
    (A/f'root_clean_{label}.stdout').write_bytes(p.stdout)
    (A/f'root_clean_{label}.stderr').write_bytes(p.stderr)
    assert p.returncode==0 and not p.stderr,(label,p.returncode,p.stderr.decode())
    expected=D/'replay_outputs'/f'{label}.stdout.txt'
    assert p.stdout==expected.read_bytes(), label+' full output differs'
    records.append({'label':label,'returncode':p.returncode,'stdout_bytes':len(p.stdout),
                    'stdout_sha256':hashlib.sha256(p.stdout).hexdigest(),'stderr_bytes':len(p.stderr),
                    'full_stream_byte_exact':True})
    print(label+': PASS',flush=True)
assert before=={str(p):inventory(p) for p in [CURRENT,PRE,OLD]}, 'Private inputs changed'
for label,expected in [('baseline','baseline_controls.stdout.txt'),
                       ('new_controls','fresh_adversarial_controls.stdout.json'),
                       ('exact_head','exact_head.stdout.json')]:
    assert (A/f'root_clean_{label}.stdout').read_bytes()==(D/expected).read_bytes()
receipt={'status':'PASS','created_utc':datetime.now(timezone.utc).isoformat(),
         'head':'4ee3016a755bb3553e712716dcd26b3d031836d0','completion_percent':95,
         'root_new_controls':14427,'baseline_S3_equations':360,
         'separate_exact_head_verifier_full_stream_match':True,'actual_git_bindings':58,
         'runs':records,'fresh_source_checks':source_checks,'private_inputs_unchanged':True,
         'scope':'Full mathematical/source/current/historical execution gate; final public whitelist and actual merge gates still required',
         'original_problem_status':'unsolved','original_problem_resolution_percent':0}
(A/'root_clean_final_reproduction_receipt.json').write_text(json.dumps(receipt,indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':'PASS','full_candidate_modes':len(records),'source_identities':len(source_checks)},sort_keys=True))
