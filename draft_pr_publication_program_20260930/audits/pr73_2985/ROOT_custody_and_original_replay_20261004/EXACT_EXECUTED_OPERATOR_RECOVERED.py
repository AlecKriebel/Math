#!/usr/bin/env python3
"""Read-only custody validation and isolated replays of already read original code.

This verifies existing proofs and evidence; it does not start a proof-search turn.
The original source namespace and all shared Git/native state remain untouched.
"""
from pathlib import Path
from collections import defaultdict
from datetime import datetime, timezone
import hashlib
import json
import os
import shutil
import sqlite3
import stat
import subprocess
import sys

A = Path(__file__).resolve().parent
S = A / 'original_source_authentication_20261004'
O = S / 'original/unsolved_math_prioritization/attempts/2985'
D = Path('/Users/alec/.cache/codex-pr73-audit-20261004/ROOT_primary_sources')
OUT = A / 'ROOT_custody_and_original_replay_20261004'
HEAD = '6f82e81631fd43abc0140a831acfb43c150f4210'
def utc(): return datetime.now(timezone.utc).isoformat()
def sha(b): return hashlib.sha256(b).hexdigest()
def j(p): return json.loads(p.read_text())
def save(p, value): p.write_text(json.dumps(value, indent=2, sort_keys=True)+'\n')
def pin(p):
    b = p.read_bytes()
    return dict(path=str(p), bytes=len(b), sha256=sha(b), POSIX_mode=oct(p.lstat().st_mode))
def git_hash(kind, b): return hashlib.sha1(kind.encode()+b' '+str(len(b)).encode()+b'\0'+b).hexdigest()

assert sys.flags.optimize == 0 and sys.flags.ignore_environment == 1 and sys.dont_write_bytecode
OUT.mkdir(exist_ok=False)
started = utc()
save(OUT/'OPERATOR_AND_RUNTIME.json', dict(operator=pin(Path(__file__)), PID=os.getpid(),
    cwd=os.getcwd(), argv=sys.argv, executable=sys.executable, version=sys.version,
    flags=str(sys.flags), dont_write_bytecode=sys.dont_write_bytecode, started_utc=started))

# Verify every member of the custodian's complete filesystem inventory.
manifest = j(S/'DEEP_CUSTODY_MANIFEST.json')
member_count = 0
for row in manifest['inventory']:
    p = S/row['path']
    assert p.lstat().st_mode == int(row['POSIX_mode'], 8), row['path']
    if row['kind'] == 'regular_file':
        b = p.read_bytes()
        assert len(b) == row['bytes'] and sha(b) == row['sha256'], row['path']
        member_count += 1
    elif row['kind'] == 'directory': assert p.is_dir()
    else: raise AssertionError(('unexpected inventory type', row))
assert member_count == manifest['regular_file_count'] == 184
actual_files = {str(p.relative_to(S)) for p in S.rglob('*') if p.is_file()}
manifest_files = {r['path'] for r in manifest['inventory'] if r['kind']=='regular_file'}
assert actual_files-manifest_files == set(manifest['exclusions'])
assert not (manifest_files-actual_files)

# Independently serialize all original Git trees, commit and retained blobs.
tree = j(S/'ORIGINAL_RECURSIVE_TREE.json')
assert tree['sha'] == '9b5a3402b56f97aeeb9435ffa388eef6bbc1edfb' and not tree['truncated']
children = defaultdict(list)
for row in tree['tree']:
    parent, _, basename = row['path'].rpartition('/')
    children[parent].append((basename, row))
expected_trees = {'':tree['sha']}
expected_trees.update({r['path']:r['sha'] for r in tree['tree'] if r['type']=='tree'})
for parent, expected in expected_trees.items():
    entries = sorted(children[parent], key=lambda x:(x[0]+('/' if x[1]['type']=='tree' else '')).encode())
    body = b''.join((r['mode'].lstrip('0')+' '+name).encode()+b'\0'+bytes.fromhex(r['sha']) for name,r in entries)
    assert git_hash('tree',body) == expected, parent
assert len(expected_trees) == 3547
commit = (S/'ORIGINAL_GIT_COMMIT_BODY.bin').read_bytes()
assert git_hash('commit',commit) == HEAD
assert b'tree '+tree['sha'].encode()+b'\n' in commit
blobs = j(S/'ORIGINAL_BLOB_MANIFEST.json')['artifacts']
for row in blobs:
    p=S/row['retained_path']; b=p.read_bytes()
    assert len(b)==row['bytes'] and sha(b)==row['sha256']
    assert git_hash('blob',b)==row['git_blob_SHA1']
    assert p.lstat().st_mode == int(row['mode'],8)
assert len(blobs)==29
incoming={r['path'] for r in blobs if r['incoming_changed_domain']}
attempts={r['path'] for r in blobs if r['path'].startswith('unsolved_math_prioritization/attempts/2985/')}
assert len(attempts)==19 and incoming==attempts|{'unsolved_math_prioritization/QUEUE.md'}

# Retain exact typed source null/absent/empty distinctions, including raw/SQL.
source=j(O/'source_record.json')
assert set(source)=={'dataset','dataset_revision','license','problem','exact_separate_prior_report'}
assert source['exact_separate_prior_report'] is None
assert not (O/'status.json').exists()
readiness=j(O/'readiness.json')
assert readiness['substantive_attempts']==1 and readiness['attempt_limit']==5
ledger=[json.loads(l) for l in (O/'turns.jsonl').read_text().splitlines()]
assert len(ledger)==1 and ledger[0]['turn']==1
pair=S/'current_sourcepair'
local_manifest=j(pair/'local_manifest.json')
assert local_manifest==j(S/'original/unsolved_math_prioritization/manifest.json')
for name in ['problems.json','research_results.json']:
    b=(pair/name).read_bytes()
    assert dict(bytes=len(b),sha256=sha(b))==local_manifest['files'][name]
problems=j(pair/'problems.json'); reports=j(pair/'research_results.json')
assert isinstance(problems,list) and isinstance(reports,dict)
targets=[p for p in problems if type(p.get('id')) is int and p['id']==2985]
assert len(targets)==1 and targets[0]==source['problem']
assert sum(p.get('problem_number')=='KP-4.109' for p in problems)==1
assert 'KP-4.109' not in reports
db=pair/'catalog.sqlite'
db_before=pin(db)
connection=sqlite3.connect(db.as_uri()+'?mode=ro&immutable=1',uri=True)
connection.execute('PRAGMA query_only=ON')
sql_row=connection.execute('SELECT key,payload,report,typeof(key),typeof(payload),typeof(report) FROM records WHERE key=?',('2985',)).fetchall()
assert len(sql_row)==1 and sql_row[0][0]=='2985' and sql_row[0][3:]==('text','text','text')
assert json.loads(sql_row[0][1])==source['problem']
assert json.loads(sql_row[0][2])=={} and type(json.loads(sql_row[0][2])) is dict
assert connection.execute('SELECT revision FROM metadata').fetchall()==[(source['dataset_revision'],)]
assert connection.execute('SELECT count(*) FROM records').fetchall()==[(15458,)]
assert connection.execute('PRAGMA integrity_check').fetchall()==[('ok',)]
connection.close(); assert pin(db)==db_before
state=S/'original/unsolved_math_prioritization/state.json'
history=S/'original/unsolved_math_prioritization/assessment_history.jsonl'
assert j(state)=={} and history.read_bytes()==b''

# Check every actual command stream independently, preserving the failed lookup.
commands=[json.loads(l) for l in (S/'ACTUAL_COMMANDS.jsonl').read_text().splitlines()]
for r in commands:
    assert isinstance(r['actual_pid'],int) and r['actual_pid']>0
    assert r['argv'] and r['cwd'] and r['started_UTC'] and r['finished_UTC']
    for stream in ['stdout','stderr']:
        b=(S/r[stream+'_path']).read_bytes()
        assert len(b)==r[stream+'_bytes'] and sha(b)==r[stream+'_sha256']
assert len(commands)==43
failures=[r for r in commands if r['exit_code']!=0]
assert len(failures)==1 and failures[0]['exit_code']==128

# Prepare exact isolated replay copies, never execute in the frozen original.
rep=OUT/'isolated_replay';rep.mkdir()
copied=[]
for old,new in [('CANDIDATE.md','CANDIDATE.md'),('verify.py','verify.py'),('review/independent_checks.py','independent_checks.py')]:
    shutil.copyfile(O/old,rep/new)
    assert (rep/new).read_bytes()==(O/old).read_bytes()
    copied.append(dict(original=pin(O/old),copy=pin(rep/new)))
save(OUT/'PRELAUNCH_REPLAY_PINS.json',copied)
replay_receipts=[]
for name, expected in [('verify.py','verification.json'),('independent_checks.py','review/independent_results.json')]:
    argv=['/usr/bin/python3','-E','-B',str(rep/name)]
    begin=utc(); child=subprocess.Popen(argv,cwd=rep,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    stdout,stderr=child.communicate(); end=utc()
    label=name.removesuffix('.py') if hasattr(name,'removesuffix') else name[:-3]
    (OUT/(label+'.stdout.bin')).write_bytes(stdout); (OUT/(label+'.stderr.bin')).write_bytes(stderr)
    record=dict(PID=child.pid,argv=argv,cwd=str(rep),started_utc=begin,finished_utc=end,exit_code=child.returncode,
        stdout=dict(path=label+'.stdout.bin',bytes=len(stdout),sha256=sha(stdout)),
        stderr=dict(path=label+'.stderr.bin',bytes=len(stderr),sha256=sha(stderr)),
        script_before_and_after_identical=pin(rep/name)==next(x['copy'] for x in copied if x['copy']['path']==str(rep/name)))
    save(OUT/(label+'.ACTUAL_RECEIPT.json'),record)
    assert child.returncode==0 and not stderr and record['script_before_and_after_identical']
    assert stdout==(O/expected).read_bytes(), ('historical stdout differs',name)
    result=json.loads(stdout); assert result['status']=='PASS'
    replay_receipts.append(dict(record=record,assertions=result['exact_assertions']))

# Authenticate newly fetched primary PDF bytes against original declarations.
pdfs={'kirby2026.pdf':D/'K3_author.pdf','giroux2017.pdf':D/'giroux1803.05929.pdf'}
primary=[]
for row in j(O/'source_manifest.json')['sources']:
    p=pdfs[row['name']]; v=pin(p)
    assert v['bytes']==row['bytes'] and v['sha256']==row['sha256']
    primary.append(dict(actual=v,declared_url=row['url']))
for p in D.glob('*.txt'):primary.append(dict(private_extracted_text=pin(p)))
for p in D.glob('*.png'):primary.append(dict(private_rendered_page=pin(p)))
result=dict(status='PASS',started_utc=started,finished_utc=utc(),actual_PID=os.getpid(),head=HEAD,
    source_manifest=pin(S/'DEEP_CUSTODY_MANIFEST.json'),validated_inventory_regular_files=member_count,
    original_Git_tree_serializations=len(expected_trees),original_Git_blobs=len(blobs),incoming_paths=len(incoming),
    custody_command_stream_receipts=len(commands),preserved_failed_lookup_exit=128,
    native_prior_report='present JSON null',raw_prior_report='lookup absent',SQL_report='normalized empty object',
    original_budget='1/5',original_ledger_events=1,new_substantive_proof_search_turns=0,
    exact_replays=replay_receipts,primary_private_artifacts=primary,
    root_primary_read_scope='K3 complete printed p.281, text and pixels; Giroux complete manuscript pp.1-2 and pp.8-10 text, pp.8-10 pixels. Not a whole-book or whole-paper reading.',
    limitations=['The wrapper background triage exposure before ROOT FIRST is separately disclosed.',
        'Original shell-launcher PID/argv/UTC unavailable; preserved custodian disclosure.',
        'This pins private source bodies; it does not authorize their redistribution.',
        'Finite checkers supplement continuous smoothing and covering-space proofs, and do not certify those proofs.'],
    shared_Git_native_PR_editor_publication_tracker_mutations=False)
save(OUT/'READBACK_AND_REPLAY.json',result)
print(json.dumps({k:result[k] for k in ['status','finished_utc','actual_PID','original_Git_tree_serializations','original_Git_blobs','custody_command_stream_receipts','original_budget']}))
print(json.dumps({'replay_assertions':[r['assertions'] for r in replay_receipts]}))
