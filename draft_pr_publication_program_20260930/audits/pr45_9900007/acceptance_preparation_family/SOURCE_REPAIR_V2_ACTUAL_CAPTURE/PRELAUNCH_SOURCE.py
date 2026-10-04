"""Second own precision repair: literal stream escapes and full native mode capture; retained versions."""
from pathlib import Path
import datetime as dt,difflib,json,os
H=Path(__file__).resolve().parent
folder=H/'PRE_FINAL_PRECISION_SOURCE';folder.mkdir();patch=[]
for n in ['pr45_guards.py','capture_root_final_operation.py']:
 p=H/n;before=p.read_text();(folder/n).write_text(before);after=before
 if n=='pr45_guards.py':
  # Only the actual ROOT query branch acquired double-escaped control characters.
  old="require(raw.endswith(b'\\\\n') and raw.count(b'\\\\n')==1,'One whole direct ls-tree line');fields,literal=raw.decode().rstrip('\\\\n').split('\\\\t')"
  new="require(raw.endswith(b'\\n') and raw.count(b'\\n')==1,'One whole direct ls-tree line');fields,literal=raw.decode().rstrip('\\n').split('\\t')"
  if after.count(old)!=1:raise ValueError('Exact own drafted stream literal expected once')
  after=after.replace(old,new)
  marker="    require(len(rows(cap['native13_before']))==13 and {z['path'] for z in rows(cap['native13_before'])}==NATIVE,'Exact thirteen actual final capture native references')"
  after=after.replace(marker,marker+"\n    for z in cap['native13_before']:\n        keyset(z,{'path','bytes','sha256','worktree_mode'},'Exact sealer captured native row/mode');require(type(z['worktree_mode']) is int and 0<=z['worktree_mode']<=0o7777,'Complete full native mode')")
 elif n=='capture_root_final_operation.py':
  after=after.replace('import traceback','import traceback\nimport stat')
  st=after.index('    native_paths = ');en=after.index('    def native():',st)
  paths=['draft_pr_publication_program_20260930/inventory.json']+['unsolved_math_prioritization/'+n for n in ['QUEUE.md','assessments.json','cache/catalog.sqlite','cache/problems.json','cache/research_results.json','catalog.json','history.jsonl','manifest.json','policy.json','queue.py','review_v2/related_target_groups.json','state.json']]
  after=after[:st]+'    native_paths = '+repr(sorted(paths))+'\n'+after[en:]
  after=after.replace("rows.append({'path': name, 'bytes': len(raw), 'sha256': sha(raw)})","rows.append({'path': name, 'bytes': len(raw), 'sha256': sha(raw), 'worktree_mode':stat.S_IMODE(path.stat().st_mode)})")
 p.write_text(after);patch.extend(difflib.unified_diff(before.splitlines(keepends=True),after.splitlines(keepends=True),fromfile='PRE_FINAL_PRECISION_SOURCE/'+n,tofile=n))
(H/'FINAL_PRECISION_DELTA.patch').write_text(''.join(patch))
with (H/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+dt.datetime.now(dt.timezone.utc).isoformat()+' — Final drafting precision checkpoint:90% preparation,0% acceptance/discovery. Fixed double-escaped newline/tab in newly handwritten query source and bound full native13 permission modes in prospective sealer capture. Prior source/control PASS is text-only evidence, never a production runtime claim; originals/deltas retained. Final private recheck follows.\n')
print(json.dumps({'status':'OWN_FINAL_PRECISION_REPAIR','actual_pid':os.getpid(),'production_executed':False,'source_preparation_percent':90}))
