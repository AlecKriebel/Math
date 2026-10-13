"""Read-only original PR305 custody intake during the peer's exclusive Git window."""
from pathlib import Path
from datetime import datetime,timezone
import subprocess,json,hashlib,base64,stat
A=Path(__file__).resolve().parent;R=A.parents[2];P=A.parents[1];H='cc083024dbd00de06ad444cd4070f51f60d209eb';BASE='c315d14e8d1ad1d3aea4d042c40388f5551f93d7';PREFIX='problems/5100034_focal_pedal_equality/';QUEUE='unsolved_math_prioritization/QUEUE.md'
sha=lambda b:hashlib.sha256(b).hexdigest();utc=lambda:datetime.now(timezone.utc).isoformat()
D=A/'root_custody_private_v02';D.mkdir(exist_ok=False)
def api(label,path):
 argv=['/opt/homebrew/bin/gh','api','repos/AlecKriebel/Math/'+path];rec=dict(argv=argv,cwd=str(R),started_utc=utc(),read_only=True)
 run=subprocess.run(argv,cwd=R,capture_output=True)
 for k,b in [('stdout',run.stdout),('stderr',run.stderr)]: (D/(label+'.'+k)).write_bytes(b);rec[k]=dict(bytes=len(b),sha256=sha(b))
 rec.update(ended_utc=utc(),exit_code=run.returncode);(D/(label+'.json')).write_text(json.dumps(rec,indent=2)+'\n');assert run.returncode==0,run.stderr;return json.loads(run.stdout)
inv=json.loads((P/'inventory.json').read_bytes());row=next(x for x in inv['items'] if x['number']==305);assert row['headRefOid']==H
live=api('live_pr','pulls/305');assert live['state']=='open' and live['draft'] and live['head']['sha']==H and live['head']['ref']==row['headRefName']
files=api('live_files','pulls/305/files?per_page=100');assert len(files)==live['changed_files'] and len(files)<100
compare=api('immutable_compare','compare/'+BASE+'...'+H);assert len(compare['files'])==len(files) and {x['filename'] for x in files}=={x['filename'] for x in compare['files']}
assert all(x['filename']==QUEUE or x['filename'].startswith(PREFIX) for x in files)
head=api('original_git_commit','git/commits/'+H);entries=[];snap=A/'snapshot';snap.mkdir()
for n,e in enumerate(files):
 assert e['status'] in ['added','modified'] and e['filename']!='' and not Path(e['filename']).is_absolute() and '..' not in Path(e['filename']).parts
 blob=api('blob_'+str(n),'git/blobs/'+e['sha']);assert blob['encoding']=='base64' and blob['sha']==e['sha']
 raw=base64.b64decode(blob['content']);assert len(raw)==blob['size'] and hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==e['sha']
 path=snap/e['filename'];path.parent.mkdir(parents=True,exist_ok=True);path.write_bytes(raw);path.chmod(0o444)
 entries.append(dict(path=e['filename'],bytes=len(raw),sha256=sha(raw),git_blob_sha=e['sha'],mode='0444',change_status=e['status']))
queue=(snap/QUEUE).read_bytes();lines=[x for x in queue.splitlines(keepends=True) if len(x.split(b'|'))>12 and x.split(b'|')[2].strip().split(b' / ')[0]==b'5100034'];assert len(lines)==1
cells=lines[0].split(b'|');assert cells[8].strip()==b'claimed_solved' and cells[9].strip()==b'1/5'
m=dict(utc=utc(),pr=305,problem='5100034',head=H,original_submitted_status='claimed_solved',original_author_turn_count='1/5',live_head_equals_original_inventory=True,live_draft_open=True,current_main_reference_read_only=BASE,original_merge_base=compare['merge_base_commit']['sha'],original_tree=head['tree']['sha'],files=entries,original_queue_row=lines[0].decode(),source_custody_only_no_math_review=True,shared_branch_refs_index_tracked_files_unmodified=True,peer_checkpoint_window_respected=True,mathematical_verification_percent=0,bounded_priority_percent=0,workflow_percent=5)
(A/'snapshot_manifest.json').write_text(json.dumps(m,indent=2)+'\n')
(A/'RESEARCH_LOG.md').write_text('# PR305 original claimed-result audit\n\n'+utc()+' — Original claimed_solved1/5 source frozen at '+H+' with '+str(len(entries))+' exact Git blobs, independently verified sizes/blob SHA1/SHA256 and readonly native snapshot modes. Live PR remains open/draft at the original head. Read-only/untracked custody intake while ascending PR80 owns shared writes; no mathematical claims accepted, no shared tracked/index/ref mutation. Completion estimate: math0%,priority0%,workflow5%.\n')
print(json.dumps({k:v for k,v in m.items() if k!='files'},indent=2));print('Frozen original file paths:',*[e['path'] for e in entries],sep='\n')
