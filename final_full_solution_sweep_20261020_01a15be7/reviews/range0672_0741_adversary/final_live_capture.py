from pathlib import Path
import base64, datetime as dt, hashlib, json, os, shutil, subprocess
os.environ['GIT_OPTIONAL_LOCKS']='0'
Q=Path(__file__).resolve().parent;R=Q.parent.parent;REPO=R.parent
def now():return dt.datetime.now(dt.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def save(rel,obj):
 p=Q/rel;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(obj,indent=2)+'\n')
def run(args,**kw):return subprocess.run(args,cwd=REPO,capture_output=True,check=True,**kw).stdout
if (Q/'final_live_recheck.json').exists():
 history=Q/'private/final_capture_history'/dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S%fZ');history.mkdir(parents=True)
 for p in list((Q/'private').glob('final_*'))+[Q/'final_live_recheck.json',Q/'final_input_recheck.json']:
  if p.is_file():shutil.copyfile(p,history/p.name)
query='query { repository(owner:"AlecKriebel",name:"Math") {'+' '.join(f'p{n}:pullRequest(number:{n}){{number title body state isDraft mergedAt updatedAt headRefOid baseRefOid mergeCommit{{oid}}}}' for n in range(672,742))+'} }'
wire=run(['gh','api','--hostname','github.com','graphql','--input','-'],input=json.dumps({'query':query}).encode());(Q/'private/final_live_wire.json').write_bytes(wire);live=json.loads(wire);save('private/final_live_prs.json',live)
if 'errors' in live:raise RuntimeError('Live metadata provider error')
initial=json.loads((Q/'private/initial_live_prs.json').read_text());diffs=[]
for n in range(672,742):
 a=initial['data']['repository'][f'p{n}'];b=live['data']['repository'][f'p{n}'];fields=[k for k in a if a[k]!=b[k]]
 if fields:diffs.append(dict(pr=n,fields=fields))
inputs=json.loads((Q/'INPUT_MANIFEST.json').read_text())['files'];changes=[]
for v in inputs:
 p=Path(v['source'])
 if not p.is_file() or sha(p.read_bytes())!=v['sha256']:changes.append(v['source'])
dispositions=[v for v in changes if Path(v).name.startswith('PR') and Path(v).name.endswith('_DISPOSITION.json')]
for name in ['STATE.json','rest_inventory.json','COVERAGE_SNAPSHOT.json','dispositions.jsonl']:(Q/'private'/('final_'+name)).write_bytes((R/name).read_bytes())
state=json.loads((R/'STATE.json').read_text());inventory=json.loads((R/'rest_inventory.json').read_text())
main=run(['gh','api','repos/AlecKriebel/Math/commits/main']);(Q/'private/final_main_wire.json').write_bytes(main);mainsha=json.loads(main)['sha']
raw=run(['gh','api','repos/AlecKriebel/Math/contents/unsolved_math_prioritization/QUEUE.md?ref='+mainsha]);(Q/'private/final_main_queue_wire.json').write_bytes(raw);queue=base64.b64decode(json.loads(raw)['content']);(Q/'private/final_main_QUEUE.md').write_bytes(queue)
target=[s for s in queue.decode().splitlines() if s.startswith('| 766 | 2515 / KOU-21.6 |')];initial_target=json.loads((Q/'withdrawal_current_binding.json').read_text())['source_line']
if target!=[initial_target]:raise RuntimeError('PR734 current withdrawal changed')
comment=run(['gh','api','repos/AlecKriebel/Math/issues/comments/6160164376']);(Q/'private/final_withdrawal_comment_wire.json').write_bytes(comment)
if json.loads(comment)['body']!=json.loads((Q/'private/withdrawal_comment_wire.json').read_text())['body']:raise RuntimeError('PR734 correction body changed')
save('final_input_recheck.json',dict(at=now(),captured_inputs=len(inputs),changed_source_paths=changes,unchanged_dispositions=not dispositions,scope='Global cursor/inventory may legitimately advance outside the assigned range; captured bytes are never overwritten to follow them.'))
save('final_live_recheck.json',dict(at=now(),count=70,wire_bytes=len(wire),wire_sha256=sha(wire),differences_from_initial=diffs,changed_canonical_dispositions=dispositions,final_next_pr=state['next_pr'],final_last_processed=state['last_completely_processed_pr'],final_inventory_highest=max(p['number'] for p in inventory['pull_requests']),final_main=mainsha,PR734_withdrawal_unchanged=True,PR734_correction_body_unchanged=True,scope='Start/end actual live metadata and current withdrawal; no assertion about later provider changes.'))
if diffs or dispositions:raise RuntimeError('Range metadata/disposition changes require review')
print(json.dumps(dict(status='PASS',live_changes=0,changed_input_sources=len(changes),cursor=state['next_pr'],highest=max(p['number'] for p in inventory['pull_requests']))))
