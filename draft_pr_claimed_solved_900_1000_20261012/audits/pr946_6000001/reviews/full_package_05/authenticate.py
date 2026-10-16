"""Independent read-only PR946 candidate05 authenticity gate; writes own receipt only."""
import hashlib, io, json, os, stat, subprocess, sys, zipfile
from pathlib import Path
from datetime import datetime, timezone
R=Path('/Users/alec/Documents/Math'); P=R/'draft_pr_claimed_solved_900_1000_20261012'; A=P/'audits/pr946_6000001'; D=A/'preprint'; O=Path(__file__).resolve().parent
HEAD='7d3adb0e500b0414a49a449e7981d34ade329427'
FP='adf39584e2645b7b530447523f690ca7e2bf68587c647f7bd5b218b758fa8068'
IP='e592834f80025eaf825f2808d7cceedfd3aa6cfbe26a5ba5c7c027e4fe2c0e8a'
MP='52165ba2410fa32238244feef20820e5bca9971f60c90542a2360f4d44e6c4ec'
ENV=dict(os.environ,GIT_CONFIG_COUNT='1',GIT_CONFIG_KEY_0='gc.auto',GIT_CONFIG_VALUE_0='0')
def run(*args):return subprocess.check_output(args,cwd=R,env=ENV)
def h(b):return hashlib.sha256(b).hexdigest()
def pin(p,v):
 b=p.read_bytes(); assert len(b)==v['bytes'] and h(b)==v['sha256'],str(p);return b
def j(b):return json.loads(b)
def blob(ref,path):return run('git','show',ref+':'+path)
def row(b):
 lines=b.splitlines(keepends=True); k=[i for i,x in enumerate(lines) if b'| 6000001 /' in x];assert len(k)==1
 i=k[0];cells=lines[i].decode().split('|');assert cells[8].strip()=='claimed_solved' and cells[9].strip()=='4/5'
 return b''.join(lines[:i]+lines[i+1:]),lines[i].decode()
def main(out):
 started=datetime.now(timezone.utc).isoformat()
 fr=D/'FREEZE.json';assert h(fr.read_bytes())==FP; f=j(fr.read_bytes());assert f['revision_candidate']==5
 ir=A/'OPERATIONS_INVENTORY.json';assert h(ir.read_bytes())==IP; inv=j(ir.read_bytes());assert len(inv['files'])==7
 for n,v in inv['files'].items():pin(R/n,v)
 assert len(f['files'])==223 and len(f['evidence_files'])==65
 for n,v in f['files'].items():pin(D/n,v)
 for n,v in f['evidence_files'].items():pin(R/n,v)
 assert f['package_manifest_sha256']==MP
 pr=j(run('gh','pr','view','946','--repo','AlecKriebel/Math','--json','number,state,isDraft,headRefOid,baseRefName,headRefName,body,title,mergeCommit,mergedAt,url'))
 assert pr['number']==946 and pr['state']=='OPEN' and pr['isDraft'] is True and pr['headRefOid']==HEAD and pr['baseRefName']=='main'
 assert h(pr['body'].encode())==f['pr_description_sha256'] and pr['body']==(D/'ORIGINAL_PR_DESCRIPTION.md').read_text()
 fresh=run('git','ls-remote','origin','refs/heads/main').decode().split()[0]
 run('git','fetch','--no-write-fetch-head','origin',fresh);run('git','fetch','--no-write-fetch-head','origin',HEAD)
 q='unsolved_math_prioritization/QUEUE.md';other,selected=row(blob(HEAD,q));base=run('git','merge-base',HEAD,fresh).decode().strip();assert row(blob(base,q))[0]==other if b'| 6000001 /' in blob(base,q) and b'claimed_solved' in [x for x in blob(base,q).splitlines() if b'| 6000001 /' in x][0] else True
 # The base row may have a different status; compare all literal nonselected bytes.
 base_lines=blob(base,q).splitlines(keepends=True);assert b''.join(x for x in base_lines if b'| 6000001 /' not in x)==other
 source=j(blob(fresh,'unsolved_math_prioritization/catalog.json'));t=[x for x in source if str(x.get('id'))=='6000001'];assert len(t)==1;t=t[0]
 assert t['present'] is True and t['holds']==[] and t['statement_hash']=='04707260f4ed2585125f1da57279c9cf1da447cd99a9010d463e5be43dc945cd' and t['review_hash']=='f8584e1f273da5d42d94704da74c51cf5aa9f0100b44e2bc9b2096c45eabf4fb'
 groups=j(blob(fresh,'unsolved_math_prioritization/review_v2/related_target_groups.json'))['groups'];membership={str(i):g for i,g in enumerate(groups) if '6000001' in [str(x) for x in g.get('ids',[])]};assert membership=={}
 rawsource=j((A/'source_record_private.txt').read_bytes());assert rawsource['review_hash']==t['review_hash'] and h(rawsource['problem']['statement'].encode())==t['statement_hash']
 snap=j((A/'ORIGINAL_SNAPSHOT.json').read_bytes());assert snap['head']==HEAD and len(snap['files'])==33
 changed=run('gh','api','repos/AlecKriebel/Math/pulls/946/files','--paginate','--jq','.[].filename').decode().splitlines();assert set(changed)==set(snap['files'])|{q}
 originals={}
 layout=f['archive_layout'];zipraw=(D/'global_hessian_verification.zip').read_bytes()
 with zipfile.ZipFile(io.BytesIO(zipraw)) as z:
  names=z.namelist();assert len(names)==len(set(names))==220
  am=j(z.read(layout['manifest']));assert len(am['files'])==219 and set(names)==set(am['files'])|{layout['manifest']}
  for zi in z.infolist():
   assert not zi.filename.startswith('/') and '..' not in zi.filename.split('/') and stat.S_ISREG(zi.external_attr>>16)
   if zi.filename in am['files']:assert {'bytes':len(z.read(zi)),'sha256':h(z.read(zi))}==am['files'][zi.filename]
  for n,sh in snap['files'].items():
   b=blob(HEAD,n);disk=A/'original'/n;member=layout['original_prefix']+n.split('/6000001/',1)[1];zb=z.read(member);entry=run('git','ls-tree',HEAD,'--',n).decode().split(None,3);gitblob=hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()
   assert h(b)==sh and b==disk.read_bytes()==zb and entry[:3]==['100644','blob',gitblob] and stat.S_IMODE(disk.stat().st_mode)==0o644 and z.getinfo(member).external_attr>>16==0o100644
   originals[n]={'bytes':len(b),'sha256':sh,'git_blob':gitblob,'git_mode':'100644','disk_mode':'0644','archive_mode':'100644','disk_and_archive_match':True}
  assert h(z.read(layout['package_manifest']))==MP
 receipt={'status':'PASS','utc':datetime.now(timezone.utc).isoformat(),'started_utc':started,'original_pr_head':HEAD,'freeze_sha256':FP,'package_manifest_sha256':MP,'operations_inventory_sha256':IP,'future_helpers':f['future_helpers'],'candidate_files':f['files'],'external_evidence_files':65,'payloads':219,'archive_members':220,'originals':originals,'fresh_main':fresh,'actual_live_pr':pr,'live_paths':changed,'source':{'present':True,'holds':[],'statement_hash':t['statement_hash'],'review_hash':t['review_hash'],'related_target_membership':membership},'immutable_queue_row':selected,'all_7_operational_dependencies_verified':True,'raw_statement_hash_verified':True,'external_mutations':0}
 (O/out).write_text(json.dumps(receipt,indent=2)+'\n');print(json.dumps({'status':receipt['status'],'utc':receipt['utc'],'fresh_main':fresh,'candidate_file_count':len(f['files']),'external_evidence_files':65}))
if __name__=='__main__':main(sys.argv[1])
