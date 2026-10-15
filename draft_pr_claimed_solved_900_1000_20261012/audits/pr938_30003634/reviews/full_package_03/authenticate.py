import base64,hashlib,json,os,stat,subprocess,sys,zipfile
from pathlib import Path
from datetime import datetime,timezone
ROOT=Path('/Users/alec/Documents/Math');P=ROOT/'draft_pr_claimed_solved_900_1000_20261012';A=P/'audits/pr938_30003634';D=A/'publication';R=A/'reviews/full_package_03'
HEAD='2b3ea2de7a9a9ea4fa8cba9a34cbdb01063bda3b';FREEZE='9bcbbb293acffa58d3f0ce81b51607463a5c3a093703647b62c4904e5ef89503';MAN='5f86b1126a90ffa4a7d9725a039b89e5ab1653f8a6c3fcd1f96a4b11e4553fa4'
def run(args):return subprocess.check_output(args,cwd=ROOT)
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
def fp(p):
 assert stat.S_ISREG(p.lstat().st_mode);b=p.read_bytes();return dict(bytes=len(b),sha256=sha(b))
label=sys.argv[1];now=datetime.now(timezone.utc).isoformat()
if label=='START':
 (R/'private/start.json').write_text(json.dumps({'started_utc':now}))
 (R/'RESEARCH_LOG.md').write_text('# Reviewer03 research log\n\n'+now+' — Started clean-context independent whole-package audit; 0% complete. Audit-only: zero substantive proof turns. No external communications or operational actions.\n')
f=load(D/'PREPUBLICATION_FREEZE.json');assert sha((D/'PREPUBLICATION_FREEZE.json').read_bytes())==FREEZE
for n,r in f['files'].items():assert fp(D/n)==r and fp(D/'reviewed_candidates/candidate03'/n)==r,n
for n,r in f['future_helpers'].items():assert fp(P/n)==r and fp(D/'reviewed_candidates/candidate03/future_helpers'/n)==r,n
pr=json.loads(run(['gh','pr','view','938','--repo','AlecKriebel/Math','--json','number,state,isDraft,headRefOid,headRefName,baseRefName,title,body,url']))
assert pr['number']==938 and pr['state']=='OPEN' and pr['isDraft'] is True and pr['headRefOid']==HEAD and pr['baseRefName']=='main'
assert sha(pr['body'].encode())==f['pr_description_sha256']
queue=run(['git','show',HEAD+':unsolved_math_prioritization/QUEUE.md']);rows=[s for s in queue.decode().splitlines() if '| 30003634 /' in s];assert len(rows)==1
cells=rows[0].split('|');assert cells[8].strip()=='claimed_solved' and cells[9].strip()=='1/5'
remote=run(['git','ls-remote','origin','refs/heads/main']).decode().split()[0]
try:catalog=json.loads(run(['git','show',remote+':unsolved_math_prioritization/catalog.json']))
except subprocess.CalledProcessError:
 content=json.loads(run(['gh','api','repos/AlecKriebel/Math/contents/unsolved_math_prioritization/catalog.json?ref='+remote]));catalog=json.loads(base64.b64decode(content['content']))
target=[t for t in catalog if str(t['id'])=='30003634'];assert len(target)==1;target=target[0]
assert target['statement_hash']=='2302f06ebd156e0ce9f1728964208380752184dcd932a117b8b397e409c15d6b' and target['review_hash']=='eebfb186fc2eefe2cb9756aec0572e127127fc1be6e248d6abad78a4fe298bd9' and target['present'] is True and target['holds']==[]
base=run(['git','merge-base',HEAD,remote]).decode().strip()
def other(b):return b''.join(s for s in b.splitlines(keepends=True) if b'| 30003634 /' not in s)
assert other(queue)==other(run(['git','show',base+':unsolved_math_prioritization/QUEUE.md']))
snap=load(A/'ORIGINAL_SNAPSHOT.json');assert snap['head']==HEAD and len(snap['files'])==44
originals={};prefix='unsolved_math_prioritization/attempts/30003634/'
assert set(run(['git','ls-tree','-r','--name-only',HEAD,'--',prefix]).decode().splitlines())==set(snap['files'])
with zipfile.ZipFile(D/'deep-derived-pure-braids-source-verification-v1.0.zip') as z:
 raw=z.read('PACKAGE_MANIFEST.json');assert sha(raw)==MAN;m=json.loads(raw);assert len(m['files'])==206 and len(z.namelist())==207 and len(set(z.namelist()))==207
 assert set(z.namelist())==set(m['files'])|{'PACKAGE_MANIFEST.json'}
 for i in z.infolist():
  assert stat.S_ISREG(i.external_attr>>16)
  if i.filename!='PACKAGE_MANIFEST.json':assert dict(bytes=len(z.read(i)),sha256=sha(z.read(i)))==m['files'][i.filename]
 for n,pin in snap['files'].items():
  b=run(['git','show',HEAD+':'+n]);tree=run(['git','ls-tree',HEAD,'--',n]).decode().split();assert tree[0]=='100644' and tree[1]=='blob'
  disk=A/'original'/n;arc='original_packet/'+n[len(prefix):];info=z.getinfo(arc)
  assert sha(b)==pin and disk.read_bytes()==b and z.read(arc)==b
  assert stat.S_IMODE(disk.lstat().st_mode)==0o644 and (info.external_attr>>16)==0o100644
  item=dict(git_blob=tree[2],git_mode=tree[0],bytes=len(b),sha256=pin,disk_and_archive_match=True)
  if label=='END':item.update(disk_mode='0644',archive_mode='100644')
  originals[n]=item
 assert z.read('note.pdf')==(D/'output/pdf/note.pdf').read_bytes()
changed=run(['gh','api','repos/AlecKriebel/Math/pulls/938/files','--paginate','--jq','.[].filename']).decode().splitlines();assert set(changed)<=set(snap['files'])|{'unsolved_math_prioritization/QUEUE.md'}
assert run(['git','branch','--show-current']).decode().strip()=='main'
record=dict(utc=datetime.now(timezone.utc).isoformat(),status='PASS',original_pr_head=HEAD,freeze_sha256=FREEZE,package_manifest_sha256=MAN,candidate_files=f['files'],future_helpers=f['future_helpers'],archive_members=207,payloads=206,originals=originals,live_gate={k:v for k,v in pr.items() if k!='body'},live_description_sha256=sha(pr['body'].encode()),queue_row=rows[0],remote_main=remote,base_commit=base,source_identity=target,other_queue_rows_unchanged=True)
(R/('AUTHENTICATION_'+label+'.json')).write_text(json.dumps(record,indent=2)+'\n')
print(json.dumps(dict(status='PASS',label=label,utc=record['utc'],remote_main=remote,originals=len(originals),payloads=206,members=207)))
