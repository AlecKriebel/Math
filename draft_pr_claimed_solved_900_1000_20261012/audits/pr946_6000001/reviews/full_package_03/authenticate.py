import sys
if not sys.flags.isolated: raise RuntimeError('requires -I')
import json,hashlib,pathlib,subprocess,stat,zipfile,datetime,os
R=pathlib.Path('/Users/alec/Documents/Math'); A=R/'draft_pr_claimed_solved_900_1000_20261012/audits/pr946_6000001'; D=A/'preprint'; O=A/'reviews/full_package_03'
H='7d3adb0e500b0414a49a449e7981d34ade329427'; FP='fdff50b3a1c77523b1b1b7c3da42b2dfdbb1bc17ada7b19abfcbfbbd40d4c505'; OP='ab02441054348e6f88a5478396a838157411015a82996daa7f77f11f81c7a494'
def sha(b): return hashlib.sha256(b).hexdigest()
def call(a): return subprocess.check_output(a,cwd=R)
def regular(p):
 s=p.lstat(); assert stat.S_ISREG(s.st_mode) and not p.is_symlink(); return p.read_bytes()
def pin(p,v):
 b=regular(p);assert len(b)==v['bytes'] and sha(b)==v['sha256'],str(p);return b
fraw=regular(D/'FREEZE.json'); assert sha(fraw)==FP; f=json.loads(fraw);assert f['revision_candidate']==3
opraw=regular(A/'OPERATIONS_INVENTORY.json');assert sha(opraw)==OP;op=json.loads(opraw)
for n,v in op['files'].items():pin(R/n,v)
for n,v in f['files'].items():pin(D/n,v)
for n,v in f['evidence_files'].items():pin(R/n,v)
pr=json.loads(call(['gh','pr','view','946','--repo','AlecKriebel/Math','--json','number,state,isDraft,headRefOid,headRefName,baseRefName,title,body,url,mergeCommit,mergedAt']))
assert pr['number']==946 and pr['state']=='OPEN' and pr['isDraft'] is True and pr['headRefOid']==H and pr['baseRefName']=='main'
assert sha(pr['body'].encode())==f['pr_description_sha256']
main=call(['git','ls-remote','origin','refs/heads/main']).decode().split()[0]
def blob(ref,p):return call(['git','show',ref+':'+p])
source=json.loads(regular(A/'TARGET_IDENTITY_PREFLIGHT.json'));target=[x for x in json.loads(blob(main,'unsolved_math_prioritization/catalog.json')) if str(x.get('id'))=='6000001'];assert len(target)==1; t=target[0]
assert t['present'] is True and t['holds']==[] and t['statement_hash']==source['statement_hash']=='04707260f4ed2585125f1da57279c9cf1da447cd99a9010d463e5be43dc945cd' and t['review_hash']==source['review_hash']=='f8584e1f273da5d42d94704da74c51cf5aa9f0100b44e2bc9b2096c45eabf4fb'
groups=json.loads(blob(main,'unsolved_math_prioritization/review_v2/related_target_groups.json'))['groups'];membership={str(i):g for i,g in enumerate(groups) if '6000001' in list(map(str,g.get('ids',[])))};assert membership==source['related_target_groups']=={}
q='unsolved_math_prioritization/QUEUE.md'
def parts(raw):
 l=raw.splitlines(keepends=True); idx=[i for i,b in enumerate(l) if b'| 6000001 /' in b];assert len(idx)==1;i=idx[0];return b''.join(l[:i]+l[i+1:]),l[i]
other,row=parts(blob(H,q));cells=row.decode().split('|');assert cells[8].strip()=='claimed_solved' and cells[9].strip()=='4/5'
base=call(['git','merge-base',H,main]).decode().strip();assert parts(blob(base,q))[0]==other
snap=json.loads(regular(A/'ORIGINAL_SNAPSHOT.json')); assert snap['head']==H and len(snap['files'])==33
orig={}; zipname=D/'global_hessian_verification.zip'
with zipfile.ZipFile(zipname) as z:
 infos=z.infolist();assert len(infos)==220 and len(set(i.filename for i in infos))==220
 am=json.loads(z.read('ARCHIVE_MANIFEST.json'));records=am['files'];assert len(records)==219
 assert set(records)|{'ARCHIVE_MANIFEST.json'}=={i.filename for i in infos}
 for i in infos:
  pp=pathlib.PurePosixPath(i.filename);assert not pp.is_absolute() and '..' not in pp.parts and '\\' not in i.filename and stat.S_ISREG(i.external_attr>>16)
  if i.filename!='ARCHIVE_MANIFEST.json': b=z.read(i);assert len(b)==records[i.filename]['bytes'] and sha(b)==records[i.filename]['sha256']
 for n,v in snap['files'].items():
  b=blob(H,n); d=regular(A/'original'/n); entry=call(['git','ls-tree',H,'--',n]).decode().strip().split(None,3);oid=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest();i=z.getinfo('package/original/'+n);zb=z.read(i)
  assert sha(b)==v and d==b==zb and entry[:3]==['100644','blob',oid] and stat.S_IMODE((A/'original'/n).lstat().st_mode)==0o644 and i.external_attr>>16==0o100644
  orig[n]={'bytes':len(b),'sha256':v,'git_blob':oid,'git_mode':'100644','disk_mode':'0644','archive_mode':'100644','disk_and_archive_match':True}
files=call(['gh','api','repos/AlecKriebel/Math/pulls/946/files','--paginate','--jq','.[].filename']).decode().splitlines();assert set(files)<=set(snap['files'])|{q}
result={'status':'PASS','utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'pr':946,'problem_id':'6000001','head':H,'original_pr_head':H,'payloads':219,'freeze_sha256':FP,'package_manifest_sha256':f['package_manifest_sha256'],'future_helpers':f['future_helpers'],'candidate_files':f['files'],'originals':orig,'archive_payloads':219,'archive_members':220,'disk_and_archive_match':True,'source_gate':{'remote_main':main,'present':True,'holds':[],'statement_hash':t['statement_hash'],'review_hash':t['review_hash'],'related_target_membership':membership},'operations_inventory_sha256':OP,'evidence_files_verified':len(f['evidence_files']),'live_pr':pr,'immutable_queue_row':row.decode(),'remote_base':base,'live_changed_paths':files,'actual_external_mutations':0}
name=sys.argv[1] if len(sys.argv)>1 else 'AUTHENTICATION_START.json';(O/name).write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':'PASS','utc':result['utc'],'main':main,'originals':len(orig),'candidate_files':len(f['files']),'archive':len(infos)}))
