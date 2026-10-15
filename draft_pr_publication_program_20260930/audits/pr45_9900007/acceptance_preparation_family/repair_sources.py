"""Own final precision adaptation: bind full native mode capture, preserve failed lexical assumption."""
from pathlib import Path
import datetime as dt,difflib,json,os
H=Path(__file__).resolve().parent
folder=H/'PRE_FINAL_MODE_SOURCE';folder.mkdir();patch=[]
for n in ['pr45_guards.py','capture_root_final_operation.py']:
 p=H/n;before=p.read_text();(folder/n).write_text(before);after=before
 if n=='pr45_guards.py':
  # The actual source already has the correct single-backslash stream literals.
  literal="require(raw.endswith(b'\\n') and raw.count(b'\\n')==1,'One whole direct ls-tree line');fields,literal=raw.decode().rstrip('\\n').split('\\t')"
  if after.count(literal)!=1:raise ValueError('Exact correct original stream literal required')
  marker="    require(len(rows(cap['native13_before']))==13 and {z['path'] for z in rows(cap['native13_before'])}==NATIVE,'Exact thirteen actual final capture native references')"
  if after.count(marker)!=1:raise ValueError('Exact final native13 check')
  after=after.replace(marker,marker+"\n    for z in cap['native13_before']:\n        keyset(z,{'path','bytes','sha256','worktree_mode'},'Exact sealer captured native row/mode');require(type(z['worktree_mode']) is int and 0<=z['worktree_mode']<=0o7777,'Complete full native mode')")
 else:
  after=after.replace('import traceback','import traceback\nimport stat')
  st=after.index('    native_paths = ');en=after.index('    def native():',st)
  paths=['draft_pr_publication_program_20260930/inventory.json']+['unsolved_math_prioritization/'+n for n in ['QUEUE.md','assessments.json','cache/catalog.sqlite','cache/problems.json','cache/research_results.json','catalog.json','history.jsonl','manifest.json','policy.json','queue.py','review_v2/related_target_groups.json','state.json']]
  after=after[:st]+'    native_paths = '+repr(sorted(paths))+'\n'+after[en:]
  after=after.replace("rows.append({'path': name, 'bytes': len(raw), 'sha256': sha(raw)})","rows.append({'path': name, 'bytes': len(raw), 'sha256': sha(raw), 'worktree_mode':stat.S_IMODE(path.stat().st_mode)})")
 p.write_text(after);patch.extend(difflib.unified_diff(before.splitlines(keepends=True),after.splitlines(keepends=True),fromfile='PRE_FINAL_MODE_SOURCE/'+n,tofile=n))
(H/'FINAL_MODE_CAPTURE_DELTA.patch').write_text(''.join(patch))
with (H/'RESEARCH_LOG.md').open('a') as f:f.write('\n'+dt.datetime.now(dt.timezone.utc).isoformat()+' — Final mode adaptation checkpoint:90% preparation,0% acceptance/discovery. Failed63648 assumed double-escaped literals but actual source already had correct single-backslash newline/tab. Failure retained; no lexical repair was necessary. Failed63650 correctly rejected the still-missing prospective sealer full native modes. This successful new mode adaptation removes obsolete frozen row values from path-only operator declaration and adds before/after full native13 modes. Both failures and pre-change sources remain. No production runtime execution.\n')
print(json.dumps({'status':'OWN_NATIVE_MODE_SOURCE_ADAPTATION','actual_pid':os.getpid(),'source_literals_already_correct':True,'production_executed':False,'source_preparation_percent':90}))
