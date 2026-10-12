#!/usr/bin/env python3
"""Verify this fixed audit package and reproduce its complete exact outputs.

Writes only ignored private_replay/VERIFY_runtime. Git use is read-only.
No source downloads, candidate mutations, external contacts or service calls.
"""
from pathlib import Path
import hashlib, json, os, subprocess, sys

P = Path(__file__).resolve().parent
ROOT = P.parents[3]
HEAD = '89d5f156c4a2846d6ef0b840cd24c854677d07ca'
ORIGINAL = '5b7bd8db9f34294d10862fed0f723055da864df6'
BASE = '859a836402f92f3a78dd7aecd9199e973ab666fb'
MERGE382 = '568e2f38888221aa2ff9c5e86b940a309db2ddde'
TARGET = 'problems/30003853_thompson_subgroup_abelianization'
ENV = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')

def sha(b):
    return hashlib.sha256(b).hexdigest()

def validate(e, b):
    assert len(b) == e['bytes'] and sha(b) == e['sha256'], e['path']
    if 'git_blob_sha' in e:
        assert hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest() == e['git_blob_sha'], e['path']

def git(*args):
    return subprocess.check_output(['git', *args], cwd=ROOT)

out = {'head': HEAD, 'scope': 'fixed audit reproduction, not universal proof or later-head approval'}
manifest = json.loads((P/'OUTPUT_MANIFEST.json').read_text())
assert manifest['head'] == HEAD
for e in manifest['files']:
    validate(e, (P/e['path']).read_bytes())
out['public_output_bindings'] = len(manifest['files'])
for name in ['INITIAL_SEAL.json', 'PRE_COMPARISON_SEAL.json']:
    entries = json.loads((P/name).read_text())['entries']
    for e in entries:
        validate(e, (P/e['path']).read_bytes())
    out[name] = len(entries)

receipt = json.loads((P/'INPUT_RECEIPT.json').read_text())
assert receipt['head'] == HEAD and receipt['base'] == BASE
assert git('show', '-s', '--format=%P', HEAD).decode().strip().split() == [ORIGINAL, BASE]
assert git('show', '-s', '--format=%P', BASE).decode().strip() == MERGE382
for anc in [ORIGINAL, BASE, MERGE382]:
    assert subprocess.run(['git', 'merge-base', '--is-ancestor', anc, HEAD], cwd=ROOT).returncode == 0
out['ancestry_checks'] = 5
RUNTIME = P/'private_replay'/'VERIFY_runtime'
for e in receipt['inputs']:
    b = git('show', HEAD+':'+e['path'])
    validate(e, b)
    if e['path'].startswith(TARGET+'/'):
        assert b == git('show', ORIGINAL+':'+e['path'])
    q = RUNTIME/e['path']
    q.parent.mkdir(parents=True, exist_ok=True)
    q.write_bytes(b)
out['git_input_bindings'] = len(receipt['inputs'])
out['unchanged_target_files'] = sum(e['original_target_unchanged'] is True for e in receipt['inputs'])
assert out['git_input_bindings'] == 45 and out['unchanged_target_files'] == 44
qp = 'unsolved_math_prioritization/QUEUE.md'
before = git('show', BASE+':'+qp).splitlines(keepends=True)
after = git('show', HEAD+':'+qp).splitlines(keepends=True)
assert len(before) == len(after)
assert [i+1 for i, (a,b) in enumerate(zip(before, after)) if a != b] == [419]
old, new = before[418].split(b'|'), after[418].split(b'|')
assert len(old) == len(new)
assert [i for i, (a,b) in enumerate(zip(old,new)) if a != b] == [8,9]
assert [old[i].strip() for i in [8,9]] == [b'queued',b'0/5']
assert [new[i].strip() for i in [8,9]] == [b'unsolved',b'5/5']
replacement = b'|'.join(old[:8]+[new[8],new[9]]+old[10:])
assert replacement == after[418]
assert b''.join(before[:418]+[replacement]+before[419:]) == b''.join(after)
out['queue'] = {'line':419,'cells':[8,9],'all_other_bytes_preserved':True}

candidate = RUNTIME/TARGET
local_count = 0
for name in [f'TURN_{i}_MANIFEST.json' for i in range(1,6)] + ['FINAL_AUTHOR_MANIFEST.json','PUBLICATION_MANIFEST.json','independent_review/REVIEW_MANIFEST.json']:
    d = json.loads((candidate/name).read_text())
    prefix = candidate/'independent_review' if name.startswith('independent_review/') else candidate
    for e in d['files']:
        validate(e, (prefix/e['path']).read_bytes())
        local_count += 1
    if 'previous_manifest_sha256' in d:
        assert sha((candidate/f"TURN_{d['turn']-1}_MANIFEST.json").read_bytes()) == d['previous_manifest_sha256']
assert local_count == len(receipt['nested_local_bindings']) == 108
out['nested_local_bindings'] = local_count

names = {'bieri-geoghegan-kochloukova2010.pdf':'bgk.pdf','bleak2006-algebraic.pdf':'bleak.pdf','kassabov-matucci.pdf':'km.pdf','guba-sapir2003.pdf':'gs.pdf','golan2026.pdf':'golan.pdf','farley2026.pdf':'farley.pdf','owr2018-26.pdf':'ems46748.pdf'}
source_checked = 0
for e in receipt['source_bindings']:
    basename = Path(e['path']).name
    if basename in names:
        q = P/'private_sources'/names[basename]
        if q.exists():
            validate(e, q.read_bytes())
            source_checked += 1
out['private_fresh_PDFs_rechecked_if_retained'] = source_checked
out['optional_public_raw_source_bindings'] = 0
out['historical_processed_source_bindings_unreproduced'] = 13

results = []
for entry in json.loads((P/'REPLAY_RECEIPT.json').read_text())['replays']:
    name = entry['name']
    label = name.replace('/','_').replace('.py','')
    r = subprocess.run([sys.executable, str(candidate/name)], cwd=candidate, env=ENV, capture_output=True)
    assert r.returncode == 0 and not r.stderr, name
    assert r.stdout == (P/'replay_outputs'/(label+'.stdout')).read_bytes(), name
    assert sha(r.stdout) == entry['stdout_sha256'], name
    if name.startswith('verify_turn'):
        assert r.stdout == (candidate/f"TURN_{name[len('verify_turn')]}_CHECKS.json").read_bytes()
    elif name == 'independent_review/independent_check.py':
        assert r.stdout == (candidate/'independent_review/INDEPENDENT_CHECKS.json').read_bytes()
    elif name == 'REPLAY_ALL.py':
        expected = json.loads((candidate/'FINAL_REPLAY.json').read_text())
        expected['local_source_bindings'] = 0
        assert json.loads(r.stdout) == expected
        expected = json.loads((candidate/'independent_review/AUTHOR_REPLAY.json').read_text())
        expected['local_source_bindings'] = 0
        assert json.loads(r.stdout) == expected
    results.append({'name':name,'stdout_bytes':len(r.stdout),'stdout_sha256':sha(r.stdout),'byte_exact':True,'stderr_bytes':0})
out['candidate_complete_stream_replays'] = results
out['author_assertions'] = sum(json.loads((P/'replay_outputs'/f'verify_turn{i}.stdout').read_text())['assertions'] for i in range(1,6))
out['historical_assertions'] = json.loads((P/'replay_outputs'/'independent_review_independent_check.stdout').read_text())['assertions']
assert out['author_assertions'] == 562635 and out['historical_assertions'] == 110736

controls = []
for stem, field, count in [('independent_controls','assertions_passed',53439),('post_candidate_controls','assertions',233751)]:
    r = subprocess.run([sys.executable, str(P/'controls'/(stem+'.py'))], cwd=P, env=ENV, capture_output=True)
    assert r.returncode == 0 and not r.stderr, stem
    assert r.stdout == (P/'controls'/(stem+'.stdout.json')).read_bytes(), stem
    assert json.loads(r.stdout)[field] == count
    controls.append({'name':stem,'assertions':count,'stdout_bytes':len(r.stdout),'stdout_sha256':sha(r.stdout),'byte_exact':True,'stderr_bytes':0})
out['independent_complete_stream_replays'] = controls
out['distinct_independent_assertions'] = 287190
out['required_current_scope_repairs'] = 1
out['candidate_date_repairs'] = 0
out['original_status'] = 'unsolved5/5'
out['result'] = 'PASS reproducibility; HOLD current promotion pending diagram-group scope correction and new-head gate'
print(json.dumps(out, indent=2, sort_keys=True))
