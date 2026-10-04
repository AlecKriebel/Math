from pathlib import Path
import datetime as dt,hashlib,json,os,stat
F=Path(__file__).absolute().parent;A=F.parent;C=A/'reviewed_candidate';R=A.parents[2];bind=[]
sha=lambda b:hashlib.sha256(b).hexdigest()
def read(p):assert p.is_file()and not p.is_symlink();b=p.read_bytes();bind.append(dict(path=str(p),bytes=len(b),sha256=sha(b)));return b
def load(p):return json.loads(read(p))
def time(x):z=dt.datetime.fromisoformat(x.replace('Z','+00:00'));assert z.tzinfo and z.utcoffset()==dt.timedelta(0);return z
# Byte-exact literal historical helper output, not merely matching JSON.
for name,expected in [('author_historical','check_results.json'),('duplicate_historical','review/author_replay/check_results.json'),('independent','review/independent_results.json')]:assert read(F/'literal_replays'/name/'stdout.bin')==read(C/expected)
final=load(F/'private_science/author_final/check_results.json');old=load(C/'check_results.json');assert set(final)==set(old)and all(final[k]==old[k]for k in old if k!='partial_sha256')
# Full18-path diff, reconstruct all17 new scientific hunks independently.
patch=read(A/'original_diff.patch');blocks=patch.split(b'diff --git ')[1:];assert len(blocks)==18;science=0
for block in blocks:
 lines=block.splitlines(keepends=True);header=lines[0].decode().strip();path=header.split(' b/',1)[1]
 if path.startswith('unsolved_math_prioritization/attempts/2961/'):
  n=path.split('attempts/2961/',1)[1];assert b'new file mode 100644\n'in lines
  hunk=False;out=b''
  for line in lines[1:]:
   if line.startswith(b'@@'):hunk=True;continue
   if hunk:
    assert line.startswith(b'+');out+=line[1:]
  assert out==read(A/'source_snapshot'/n);science+=1
 else:
  assert path=='unsolved_math_prioritization/QUEUE.md';removed=[x[1:]for x in lines if x.startswith(b'-|')];added=[x[1:]for x in lines if x.startswith(b'+|')];assert len(removed)==len(added)==1 and b'2961 / KP-4.85'in removed[0]and b'2961 / KP-4.85'in added[0]
assert science==17
# Complete original103 command captures, actual sources/full streams, failed executions retained.
m=load(A/'ORIGINAL_PREPARATION_MANIFEST.json');original=[]
for r in m['complete_prior_actual_captures']:
 p=A/r['path'];c=load(p);assert c['actual_execution']is True and c['completed']is True and type(c['pid'])is int and c['pid']==r['pid']and type(c['exit_code'])is int and c['exit_code']==r['exit_code']and c['argv']==r['argv']and c['cwd']==r['cwd']and c['stdin_supplied']is False
 assert time(c['started_utc'])<=time(c['finished_utc'])<=dt.datetime.now(dt.timezone.utc)
 for k in ['stdout','stderr']:
  s=c[k];q=p.parent/s['path'];b=read(q);assert len(b)==s['bytes']and sha(b)==s['sha256']
 assert c['operator_unchanged']is True and sha(read(p.parent/'prelaunch_operator.py'))==c['operator_sha256']
 pre=load(p.parent/'PRELAUNCH.json');assert pre['argv']==c['argv']and pre['cwd']==c['cwd']
 if 'target_source'in c:
  t=c['target_source'];b=read(p.parent/'prelaunch_target.py');assert len(b)==t['bytes']and sha(b)==t['sha256']and c['target_unchanged']is True
 original.append(dict(path=r['path'],pid=c['pid'],exit_code=c['exit_code'],source_operator_streams_checked=True))
assert len(original)==103
# Original genuine closing event separately; no invention about old operator choice.
p=A/'original_preparation_closure_actual_capture';c=load(p/'CAPTURE.json');assert c['operator_pid']==87064 and c['pid']==87065 and c['actual_execution']is True and c['completed']is True and c['exit_code']==0 and c['operator_unchanged']is True and c['target_unchanged']is True
assert sha(read(p/'prelaunch_operator.py'))==c['operator_sha256']and sha(read(p/'prelaunch_target.py'))==c['target_source']['sha256']
for k in ['stdout','stderr']:
 s=c[k];b=read(p/s['path']);assert len(b)==s['bytes']and sha(b)==s['sha256']
assert time(c['started_utc'])<=time(m['created_utc'])<=time(c['finished_utc']);assert load(p/'stdout.bin')['manifest_sha256']==sha(read(A/'ORIGINAL_PREPARATION_MANIFEST.json'))
# All completed own previous outer captures and nested literal/Git children, full sources and streams.
own=[]
for cp in sorted(F.rglob('CAPTURE.json')):
 if cp.parent==F/'captures/final_evidence_controls':continue
 c=load(cp);assert c['actual_execution']is True and c['completed']is True and type(c['pid'])is int and type(c['exit_code'])is int and c['stdin_supplied']is False;assert time(c['started_utc'])<=time(c['finished_utc'])
 for key in ['stdout','stderr']:
  x=c[key];b=read(cp.parent/x['path']);assert len(b)==x['bytes']and sha(b)==x['sha256']
 op=cp.parent/'PRELAUNCH_OPERATOR.py';assert op.is_file()
 if 'operator_sha256'in c:assert sha(read(op))==c['operator_sha256']
 if c.get('source_sha256')is not None:assert sha(read(cp.parent/'PRELAUNCH_SOURCE.py'))==c['source_sha256']
 pre=load(cp.parent/'PRELAUNCH.json');assert pre['argv']==c['argv']and pre['cwd']==c['cwd']and pre['operator_pid']==c['operator_pid']
 own.append(dict(capture=str(cp.relative_to(F)),actual_child=c['pid'],exit_code=c['exit_code']))
D=load(C/'CURRENT_DEPENDENCIES.json');native4={'unsolved_math_prioritization/'+n for n in ['QUEUE.md','state.json','history.jsonl']}|{'draft_pr_publication_program_20260930/inventory.json'}
for r in D['current_native13']:
 if r['path']not in native4:b=read(R/r['path']);assert len(b)==r['bytes']and sha(b)==r['sha256']and stat.S_IMODE((R/r['path']).stat().st_mode)==r['full_mode']
result=dict(status='PASS_COMPLETE_DIFF_BYTE_REPLAYS_ORIGINAL103_AND_OWN_ACTUAL_EVIDENCE',actual_pid=os.getpid(),UTC=dt.datetime.now(dt.timezone.utc).isoformat(),all17_scientific_hunks_reconstructed=True,all18_paths_accounted=True,original103_actual_captures=original,original_true_closing_capture=c,own_completed_actual_captures=own,stable9_live=True,bindings=bind,no_future_child_or_acceptance_certified=True)
(F/'FINAL_EVIDENCE_CONTROL_RESULT.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items()if k not in {'bindings','original103_actual_captures','original_true_closing_capture'}},indent=2))
