#!/usr/bin/env python3
from pathlib import Path
import subprocess,json,hashlib,shutil,sys
from datetime import datetime,timezone
P=Path(__file__).resolve().parent; AUDIT=P.parent; ROOT=Path('/Users/alec/Documents/Math');PREFIX='unsolved_math_prioritization/attempts/30004106/'
HEAD='1747a651d5865cfbbe3c4eef7ab3c8142fc117f4';OLD='682f6fd29dce0c9ca5625d14461d0e6e1eb2e6d6';MAIN='264c26d539d616b0da6f8df76478a213d20939e4';WIP='59ecabf2953d6c0d39e51a341a554152927b7b6c';Q='unsolved_math_prioritization/QUEUE.md'
def git(*args):return subprocess.check_output(['git',*args],cwd=ROOT)
def sha(b):return hashlib.sha256(b).hexdigest()
m=json.loads((AUDIT/'repaired_snapshot_manifest.json').read_text());entries=[]
for e in m['files']:
 b=(AUDIT/'repaired_snapshot'/e['path']).read_bytes();g=git('show',HEAD+':'+e['path']);o=git('show',OLD+':'+e['path'])
 assert len(b)==e['bytes'] and sha(b)==e['sha256'] and b==g
 if e['path'].startswith(PREFIX):assert b==o
 entries.append(dict(e,git_head_equal=True,original_target_equal=b==o))
assert len(entries)==52 and sum(e['path'].startswith(PREFIX) for e in entries)==51
live_target=git('ls-tree','-r','--name-only',HEAD,'--',PREFIX).decode().splitlines();assert sorted(live_target)==sorted(e['path'] for e in entries if e['path'].startswith(PREFIX))
parents=git('show','-s','--format=%P',HEAD).decode().strip().split();assert parents==[OLD,MAIN]
assert git('show','-s','--format=%T',HEAD).decode().strip()==json.loads((AUDIT/'queue_repair_receipt.json').read_text())['tree']
old_vs_head=git('diff','--name-only',OLD,HEAD).decode().splitlines()
# Queue-only integration means candidate artifact preservation, NOT literally only queue vs OLD: main updates are merged too.
assert git('diff','--name-only',OLD,HEAD,'--',PREFIX)==b''
qmain=git('show',MAIN+':'+Q);qhead=git('show',HEAD+':'+Q);ql=qmain.splitlines(keepends=True);qh=qhead.splitlines(keepends=True)
assert len(ql)==len(qh);changes=[(i+1,a,b) for i,(a,b) in enumerate(zip(ql,qh)) if a!=b];assert len(changes)==1
line,a,b=changes[0];ac=a.decode().split('|');bc=b.decode().split('|');cellchanges=[i for i,(x,y) in enumerate(zip(ac,bc)) if x!=y];assert cellchanges==[8,9]
assert '30004106 / OWR-16776-002' in bc[2] and bc[8].strip()=='unsolved' and bc[9].strip()=='5/5';assert line==421
(P/'QUEUE_ACTUAL_DIFF.patch').write_bytes(git('diff',MAIN,HEAD,'--',Q))
(P/'INTEGRITY.json').write_text(json.dumps({'utc':datetime.now(timezone.utc).isoformat(),'head':HEAD,'parents':parents,'workspace_branch':git('branch','--show-current').decode().strip(),'workspace_head':git('rev-parse','HEAD').decode().strip(),'all52_exact_head_snapshot_bindings':entries,'all51_original_target_bytes_preserved':True,'old_to_repaired_paths':old_vs_head,'current_main_relative_queue_changed_lines':[line],'changed_cells':cellchanges,'all_other_current_main_queue_bytes_preserved':True},indent=2)+'\n')
private=P/'private'/'packet';shutil.copytree(AUDIT/'repaired_snapshot'/PREFIX,private,dirs_exist_ok=True)
bindings=[]
for f in sorted(private.rglob('*MANIFEST.json')):
 d=json.loads(f.read_text());base=f.parent
 if 'files' not in d:continue
 for e in d['files']:
  b=(base/e['path']).read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256'],(f,e['path'])
  bindings.append({'manifest':str(f.relative_to(private)),'path':e['path'],'bytes':len(b),'sha256':sha(b)})
final=json.loads((private/'FINAL_AUTHOR_MANIFEST.json').read_text());assert len(final['files'])==41
preserved_author=[]
for f in list(e['path'] for e in final['files'])+['FINAL_AUTHOR_MANIFEST.json']:
 b=(private/f).read_bytes();assert b==git('show',WIP+':'+PREFIX+f);preserved_author.append({'path':f,'sha256':sha(b)})
reviewfiles=[str(f.relative_to(private)) for f in sorted((private/'review').glob('*')) if f.is_file()];assert len(reviewfiles)==6
old_review=[]
for f in reviewfiles:
 b=(private/f).read_bytes();assert b==git('show',OLD+':'+PREFIX+f);old_review.append({'path':f,'sha256':sha(b)})
replays=[]
for name in [f'verify_turn{i}.py' for i in range(1,6)]+['replay_author.py','review/independent_check.py','verify_publication.py']:
 run=subprocess.run([sys.executable,str(private/name)],cwd=private,capture_output=True)
 stem=Path(name).stem; (P/(stem+'.stdout')).write_bytes(run.stdout);(P/(stem+'.stderr')).write_bytes(run.stderr)
 assert run.returncode==0 and not run.stderr
 receipt=(private/('TURN_'+str(name[len('verify_turn')])+ '_CHECKS.json')).read_bytes() if name.startswith('verify_turn') else (private/'AUTHOR_REPLAY.json').read_bytes() if name=='replay_author.py' else (private/'review/INDEPENDENT_CHECKS.json').read_bytes() if name.startswith('review/') else None
 if receipt is not None:assert run.stdout==receipt
 replays.append({'script':name,'exit_code':run.returncode,'stdout_sha256':sha(run.stdout),'stderr_sha256':sha(run.stderr),'byte_exact_to_frozen_receipt':True if receipt is not None else None,'complete_stdout_file':stem+'.stdout','result':json.loads(run.stdout)})
# Copies are not allowed to corrupt the source or historical receipts.
for e in m['files']:
 if not e['path'].startswith(PREFIX):continue
 b=(private/e['path'][len(PREFIX):]).read_bytes();assert sha(b)==e['sha256']
(P/'REPLAY_BINDINGS.json').write_text(json.dumps({'utc':datetime.now(timezone.utc).isoformat(),'private_replay_packet_preserved':True,'nested_manifest_entries':bindings,'nested_manifest_entry_count':len(bindings),'42_frozen_author_files_preserved_against_wip':preserved_author,'six_old_review_files_preserved':old_review,'replays':replays},indent=2)+'\n')
print(json.dumps({'exact_head_snapshot_paths':len(entries),'historical_and_final_nested_entries':len(bindings),'author_files_preserved':len(preserved_author),'old_review_files_preserved':len(old_review),'private_complete_scripts_replayed':len(replays),'author_assertions':184604,'old_review_assertions':14871,'queue_current_main_relative_changed_lines':[line],'queue_changed_cells':cellchanges},indent=2))
