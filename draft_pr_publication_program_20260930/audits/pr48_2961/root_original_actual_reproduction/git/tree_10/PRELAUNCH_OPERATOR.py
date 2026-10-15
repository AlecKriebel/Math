#!/usr/bin/env python3
"""ROOT's independent full original-body and historical/final receipt reproduction."""
from pathlib import Path
import datetime as dt
import hashlib
import json
import os
import stat
import subprocess

assert __debug__ and not os.environ.get('PYTHONOPTIMIZE')
A=Path(__file__).absolute().parent
R=A.parents[2]
S=A/'source_snapshot'
D=A/'root_original_actual_reproduction'
assert R==Path('/Users/alec/Documents/Math') and not D.exists()
D.mkdir()

def sha(b):
    return hashlib.sha256(b).hexdigest()

def stamp():
    return dt.datetime.now(dt.timezone.utc).isoformat()

def encode(o):
    return (json.dumps(o,indent=2,ensure_ascii=False,allow_nan=False)+'\n').encode()

def write(p,b):
    with p.open('xb') as h:
        h.write(b); h.flush(); os.fsync(h.fileno())

def read(p):
    assert not p.is_symlink() and not any(q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode)
    return p.read_bytes()

def row(p):
    b=read(p)
    return dict(path=p.relative_to(R).as_posix(),bytes=len(b),sha256=sha(b))

def equal(a,b):
    if type(a) is not type(b): return False
    if type(a) is dict: return set(a)==set(b) and all(equal(a[k],b[k]) for k in a)
    if type(a) is list: return len(a)==len(b) and all(equal(x,y) for x,y in zip(a,b))
    return a==b

captures=[]
def run(label,argv,source=None):
    c=D/label; c.mkdir(parents=True)
    write(c/'PRELAUNCH_OPERATOR.py',read(Path(__file__)))
    if source is not None: write(c/'PRELAUNCH_SOURCE.py',read(source))
    rec=dict(schema='pr48-root-readonly-git-actual-capture/v1' if source is None else 'pr48-root-unchanged-helper-actual-capture/v1',
        argv=argv,cwd=str(R),actual_operator_pid=os.getpid(),started_utc=stamp(),actual_execution=False,completed=False,pid=None,exit_code=None,stdin_supplied=False,
        source=None if source is None else row(source),operator_sha256=sha(read(Path(__file__))))
    write(c/'PRELAUNCH.json',encode(rec))
    with (c/'stdout.bin').open('xb') as out,(c/'stderr.bin').open('xb') as err:
        child=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=out,stderr=err,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
        rec.update(actual_execution=True,pid=child.pid,exit_code=child.wait(timeout=60),completed=True)
    rec.update(finished_utc=stamp(),source_unchanged=None if source is None else read(source)==read(c/'PRELAUNCH_SOURCE.py'),operator_unchanged=sha(read(Path(__file__)))==rec['operator_sha256'])
    for channel in ('stdout','stderr'): rec[channel]=row(c/(channel+'.bin'))
    write(c/'CAPTURE.json',encode(rec)); captures.append(rec)
    assert type(rec['exit_code']) is int and rec['exit_code']==0 and not read(c/'stderr.bin')
    assert rec['operator_unchanged'] is True and (source is None or rec['source_unchanged'] is True)
    return read(c/'stdout.bin')

def git(label,*argv):
    assert argv[0] in {'show','ls-tree','diff','merge-base'}
    return run('git/'+label,['git',*argv])

write(D/'PRELAUNCH_ROOT_REPRODUCTION_SOURCE.py',read(Path(__file__)))
mf=json.loads(read(A/'ORIGINAL_PREPARATION_MANIFEST.json'))
assert sha(read(A/'ORIGINAL_PREPARATION_MANIFEST.json'))=='278e4fd39b5a13c7a181e3f7d494420c41ea4082fa8ab9add34229671a1be3b4'
for r in mf['files']:
    p=A/r['path']; b=read(p)
    assert len(b)==r['bytes'] and sha(b)==r['sha256'] and stat.S_IMODE(p.stat().st_mode)==0o444
snapshot=json.loads(read(A/'snapshot_manifest.json'))
head='e2e5c8c3e5ad218f867fa753c465bb96b3687bda'
base='60292bed09f59236aa192cb17aa138f7b4750e1a'
assert snapshot['head']==head and snapshot['merge_base']==base and len(snapshot['files'])==17
for i,r in enumerate(snapshot['files']):
    b=read(S/r['relative_path'])
    assert len(b)==r['bytes'] and sha(b)==r['sha256']
    assert git('body_'+str(i),'show',head+':'+r['path'])==b
    assert git('tree_'+str(i),'ls-tree',head,'--',r['path']).decode().strip()=='100644 blob '+r['git_object']+'\t'+r['path']
assert git('merge_base','merge-base',head,snapshot['github_base']).decode().strip()==base
diff=git('full_diff','diff','--no-ext-diff','--no-textconv','--binary',base,head,'--')
assert diff==read(A/'original_diff.patch') and len(diff)==80679 and sha(diff)=='994b4bbd4993227d1100cbd9d7493de776c6619c9daa379dca7f4ef3b3a26698'
tree=git('scientific_tree','ls-tree','-r','-z',head,'--','unsolved_math_prioritization/attempts/2961/').decode().split('\0')
assert {r.split('\t',1)[1] for r in tree if r}=={r['path'] for r in snapshot['files']}
historical=git('historical_note','show','2c32c34e6ddfa52ce067805afd3e2157dc32a130:unsolved_math_prioritization/attempts/2961/PARTIAL.md')
final=read(S/'PARTIAL.md')
assert sha(historical)=='0036b78ba3164a52c15a7a24ea73fe4438a3db3c9a206f2882070c23e91cd3b2'
assert sha(final)=='196568d2029fd378dfa43919efbf49dcbd11244a2de8c525483f84484f00e5fa'
old=b'Separate adversarial review is pending.'
new=b'Separate adversarial AI review passed; see [the report](review/REVIEW.md).'
assert final.count(new)==1 and historical==final.replace(new,old)
author=read(S/'check_algebra.py'); submitted=read(S/'review/author_replay/check_algebra.py')
assert author==submitted
saved=read(S/'check_results.json'); saved_obj=json.loads(saved)
results={}
for name,source,partial in [('author_historical',author,historical),('identical_submitted_historical',submitted,historical),('author_final',author,final)]:
    d=D/name; d.mkdir(); write(d/'check_algebra.py',source); write(d/'PARTIAL.md',partial)
    out=run(name+'_capture',['/usr/bin/python3','-B',str(d/'check_algebra.py')],d/'check_algebra.py')
    b=read(d/'check_results.json'); value=json.loads(b)
    assert out==b and value['all_passed'] is True and type(value['assertions']) is int and value['assertions']==6570
    if partial==historical: assert b==saved and equal(value,saved_obj)
    else:
        expected=dict(saved_obj,partial_sha256=sha(final))
        assert equal(value,expected)
    results[name]=value
d=D/'historical_independent'; d.mkdir(); source=read(S/'review/independent_checks.py'); write(d/'independent_checks.py',source)
b=run('historical_independent_capture',['/usr/bin/python3','-B',str(d/'independent_checks.py')],d/'independent_checks.py')
write(d/'independent_results.json',b); independent=json.loads(b)
assert b==read(S/'review/independent_results.json') and equal(independent,json.loads(read(S/'review/independent_results.json')))
assert independent['status']=='PASS' and type(independent['assertions']) is int and independent['assertions']==228 and len(independent['checks'])==24 and sum(independent['checks'].values())==228
ledger=[json.loads(b) for b in read(S/'turns.jsonl').splitlines()]
assert len(ledger)==2 and all(type(r['turn']) is int for r in ledger) and [r['turn'] for r in ledger]==[1,2]
record=dict(schema='pr48-root-original-complete-reproduction/v1',status='PASS_ROOT_ORIGINAL_AND_HISTORICAL_FINAL_REPRODUCTION',utc=stamp(),actual_operator_pid=os.getpid(),
    original_head=head,actual_merge_base=base,github_base=snapshot['github_base'],original_scientific_files=17,original_closure_members_read=574,
    whole_diff_bytes=len(diff),whole_diff_sha256=sha(diff),complete_actual_Git_captures=[r for r in captures if r['source'] is None],complete_actual_helper_captures=[r for r in captures if r['source'] is not None],
    entire_original_author_result=saved_obj,entire_historical_independent_result=independent,entire_historical_and_final_replayed_results=results,
    complete_original_turns=ledger,original_substantive_attempts=2,turn_limit=5,new_substantive_attempts=0,audit_turns=0,
    original_author_and_identical_submitted_historical_receipts_byte_type_exact=True,identical_submitted_counted_independent=False,
    final_author_receipt_only_partial_sha256_changes=True,historical_note_genuine_Git_body=True,only_review_status_sentence_changed=True,
    mathematical_partial_read_and_checked_separately=True,full_problem_solved=False,novelty_claimed=False,
    original_primary_PDF_hashes_freshly_authenticated_by_ROOT=False,ROOT_complete_raw_SQL_audit='PENDING_SEPARATE_OPERATION',
    future_acceptance_approved=False,foreign_source_cache_SQL_bodies_copied=False)
write(D/'ROOT_REPRODUCTION_RESULT.json',encode(record))
print(json.dumps(dict(status=record['status'],actual_operator_pid=os.getpid(),git_children=len(record['complete_actual_Git_captures']),helper_children=4,original_turns='2/5',historical6570_receipts_byte_exact=True,independent228_byte_exact=True,final6570_only_note_hash_changes=True,future_acceptance_approved=False),indent=2))
