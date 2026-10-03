"""Authenticate the pinned original PR52 scientific package using read-only GitHub API calls."""
from pathlib import Path
import base64,datetime,hashlib,json,os,subprocess,sys
F=Path(__file__).resolve().parent
R=Path('/Users/alec/Documents/Math')
HEAD='d40d2dae4cff2a5e5a1e12e9a2f8bc3987431c1a'
def sha(b):return hashlib.sha256(b).hexdigest()
def ident(p):
 b=p.read_bytes();return {'path':str(p),'bytes':len(b),'sha256':sha(b),'mode':format(p.stat().st_mode&0o7777,'04o')}
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
commands=[]
D=F/'retrieval_streams';D.mkdir(exist_ok=False)
def run(argv):
 n=len(commands);started=utc();child=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE);out,err=child.communicate()
 op=D/('%03d.stdout.bin'%n);ep=D/('%03d.stderr.bin'%n);op.write_bytes(out);ep.write_bytes(err)
 rec={'ordinal':n,'argv':argv,'cwd':str(R),'started_utc':started,'finished_utc':utc(),'actual_execution':True,'pid':child.pid,'exit_code':child.returncode,'completed':True,'operator_source':ident(Path(__file__)),'stdout':ident(op),'stderr':ident(ep)};commands.append(rec);(F/'RETRIEVAL_COMMANDS.json').write_text(json.dumps(commands,indent=2,sort_keys=True)+'\n');assert child.returncode==0,(argv,err.decode(errors='replace'));return out
def api(path):return json.loads(run(['gh','api','repos/AlecKriebel/Math/'+path]))
def tree(tree_sha):
 obj=api('git/trees/'+tree_sha);assert obj['sha']==tree_sha and obj.get('truncated') is False
 payload=b''
 for x in sorted(obj['tree'],key=lambda x:x['path']+('/' if x['type']=='tree' else '')):
  mode='40000' if x['type']=='tree' else x['mode'];payload+=mode.encode()+b' '+x['path'].encode()+b'\0'+bytes.fromhex(x['sha'])
 computed=hashlib.sha1(b'tree '+str(len(payload)).encode()+b'\0'+payload).hexdigest();assert computed==tree_sha,(computed,tree_sha)
 return obj['tree']
meta=json.loads((F/'captures/fresh_github_metadata/STDOUT.bin').read_bytes());assert meta['number']==52 and meta['head']['sha']==HEAD
commit=json.loads((F/'captures/github_commit/STDOUT.bin').read_bytes());assert commit['sha']==HEAD
root=tree(commit['tree']['sha']);ut=next(x for x in root if x['path']=='unsolved_math_prioritization');u=tree(ut['sha']);at=next(x for x in u if x['path']=='attempts');a=tree(at['sha']);target=next(x for x in a if x['path']=='30000644')
allrows=[]
def walk(tree_sha,prefix):
 for x in tree(tree_sha):
  path=prefix+'/'+x['path']
  if x['type']=='tree':walk(x['sha'],path)
  else:allrows.append({'repository_path':path,'git_mode':x['mode'],'git_blob_sha1':x['sha']})
walk(target['sha'],'unsolved_math_prioritization/attempts/30000644')
changed=json.loads((F/'captures/github_changed_files/STDOUT.bin').read_bytes());assert len(changed)==meta['changed_files']==20
science=[x for x in changed if x['filename'].startswith('unsolved_math_prioritization/attempts/30000644/')]
assert len(science)==19 and {x['filename'] for x in science}=={x['repository_path'] for x in allrows}
rows=[]
for x in sorted(allrows,key=lambda x:x['repository_path']):
 entry=next(q for q in science if q['filename']==x['repository_path']);assert entry['sha']==x['git_blob_sha1'] and entry['status']=='added' and entry['deletions']==0
 obj=api('git/blobs/'+x['git_blob_sha1']);assert obj['sha']==x['git_blob_sha1'] and obj['encoding']=='base64'
 body=base64.b64decode(obj['content']);assert len(body)==obj['size'];assert hashlib.sha1(b'blob '+str(len(body)).encode()+b'\0'+body).hexdigest()==x['git_blob_sha1']
 dest=F/'original'/'/'.join(x['repository_path'].split('/')[3:]);dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(body);dest.chmod(int(x['git_mode'][-4:],8))
 rows.append(dict(x,local_identity=ident(dest),all_full_body_bytes_authenticated=True))
q=[x for x in changed if x['filename']=='unsolved_math_prioritization/QUEUE.md'];assert len(q)==1 and q[0]['status']=='modified' and q[0]['additions']==q[0]['deletions']==1
(F/'ORIGINAL_AUTHENTICATION.json').write_text(json.dumps({'schema':'pr52-original-scientific-authentication/v1','head':HEAD,'root_tree':commit['tree']['sha'],'primary_science_files':rows,'science_file_count':len(rows),'queue_changed_file':q[0],'queue_body_independently_downloaded':False,'queue_scope':'complete PR diff and literal target row amendment; no mutable current native authority','git_tree_hashes_independently_reconstructed':True,'git_blob_hashes_independently_reconstructed':True,'github_api_authority_not_signed_commit_certificate':True,'preparation_only':True},indent=2,sort_keys=True)+'\n')
print(json.dumps({'status':'PASS','head':HEAD,'science_files':len(rows),'science_bytes':sum(x['local_identity']['bytes'] for x in rows),'commands':len(commands),'no_git_mutations':True},sort_keys=True))
