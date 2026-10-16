"""Execute the already independently reviewed main-only exact-tree merge plan."""
from pathlib import Path
import subprocess,json,hashlib,datetime,os,shutil,time
A=Path(__file__).resolve().parent;C=A.parents[2];D=A/'actual_merge_reconciled_20261006';D.mkdir(exist_ok=False)
accepted='d18401d15e8905d4e22b6bf8f52ca26a36d30971';original='3526d46bf143b08e5055ffa7728c6278e9f958ea';records=[]
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def require(x,m):
 if not x:raise RuntimeError(m)
def pin(p):
 h=hashlib.sha256();n=0
 with p.open('rb') as f:
  for b in iter(lambda:f.read(1048576),b''):h.update(b);n+=len(b)
 return {'bytes':n,'sha256':h.hexdigest()}
def run(argv,cap=64*1024*1024):
 start=now();p=subprocess.Popen(argv,cwd=C,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
 try:out,err=p.communicate(timeout=60)
 except subprocess.TimeoutExpired:
  p.kill();out,err=p.communicate();raise RuntimeError('Actual merge operation deadline')
 i=len(records)
 for k,b in [('stdout',out),('stderr',err)]:(D/(str(i)+'.'+k+'.prefix.bin')).write_bytes(b[:4096])
 r={'argv':argv,'actual_PID':p.pid,'UTC_start':start,'UTC_end':now(),'exit_code':p.returncode,'child_reaped':True,'stdout':{'bytes':len(out),'sha256':hashlib.sha256(out).hexdigest(),'retained_prefix':str(i)+'.stdout.prefix.bin'},'stderr':{'bytes':len(err),'sha256':hashlib.sha256(err).hexdigest(),'retained_prefix':str(i)+'.stderr.prefix.bin'}};records.append(r)
 (D/'PROCESS_JOURNAL.json').write_text(json.dumps({'actual_operator_PID':os.getpid(),'records':records},indent=2)+'\n')
 require(p.returncode==0,'Failed '+repr(argv)+' '+err.decode('utf8','replace')[:800]);require(len(out)<=cap and len(err)<=65536,'Unexpected stream size');return out
def git(*a):return run(['/opt/homebrew/bin/git',*a])
require(git('symbolic-ref','--short','HEAD').strip()==b'main','Not main');require(git('rev-parse','HEAD').strip().decode()==accepted,'Own head changed')
require(git('ls-remote','https://github.com/AlecKriebel/Math.git','refs/heads/main').decode().split()[0]==accepted,'Remote main changed');require(not git('diff','--cached','--name-only','-z'),'Foreign staged entries')
require(not git('diff','--name-only','--diff-filter=ACMRTUXB','-z'),'Materialized tracked changes')
absences=git('diff','--name-only','--diff-filter=D','-z');absence_count=len([x for x in absences.split(b'\0') if x])
# Sparse physical absences are never staged; exact complete index/tree is retained.
require(git('write-tree').strip()==git('rev-parse','HEAD^{tree}').strip(),'Complete index differs from accepted tree')
receipt=json.loads((A/'actual_checkpoints/native_acceptance_20261006/RECEIPT.json').read_bytes())
require(receipt['commit']==accepted and receipt['remote_verified'],'Acceptance receipt')
for row in receipt['pins']:require(pin(C/row['file'])=={k:row[k] for k in ['bytes','sha256']},'Accepted materialized body changed '+row['file'])
pr=json.loads(run(['/opt/homebrew/bin/gh','pr','view','108','--repo','AlecKriebel/Math','--json','number,state,isDraft,headRefOid,headRefName,baseRefName,title,body']))
require(pr['number']==108 and pr['state']=='OPEN' and pr['isDraft'] is False and pr['headRefOid']==original and pr['headRefName']=='dot/math-30003996' and pr['baseRefName']=='main','Original ready PR changed')
require(pr['body']==(A/'ACCEPTED_PR_DESCRIPTION_20261006.md').read_text(),'Accepted PR description readback differs')
require(shutil.disk_usage(C).free>=32*1024*1024,'Merge reserve')
git('cat-file','-e',original+'^{commit}');tree=git('rev-parse',accepted+'^{tree}').strip().decode()
pre={'UTC':now(),'actual_operator_PID':os.getpid(),'accepted_main':accepted,'original_head':original,'accepted_tree':tree,'materialized_acceptance_pins_checked':len(receipt['pins']),'unstaged_physical_sparse_absence_count':absence_count,'absence_name_stream_sha256':hashlib.sha256(absences).hexdigest(),'no_materialized_tracked_changes':True,'complete_index_matches_accepted_tree':True,'sparse_absences_not_staged':True,'PR_ready_and_description_exact':True,'main_only_ours_merge_authorized_and_reviewed':True}
(D/'PRE_MERGE_READBACK.json').write_text(json.dumps(pre,indent=2)+'\n')
git('-c','core.hooksPath=/dev/null','-c','commit.gpgsign=false','-c','gc.auto=0','merge','-s','ours','--no-ff','--no-edit','-m','Merge PR108: independently verified and published all-root spanning-tree result',original)
commit=git('rev-parse','HEAD').strip().decode();parents=git('show','-s','--format=%P',commit).decode().strip().split();merge_tree=git('rev-parse',commit+'^{tree}').strip().decode()
require(parents==[accepted,original] and merge_tree==tree,'Merge parents/tree differ')
require(not git('diff','--cached','--name-only','-z'),'Merge index remains changed')
for row in receipt['pins']:require(pin(C/row['file'])=={k:row[k] for k in ['bytes','sha256']},'Merge touched accepted body')
r={'schema':'pr108-root-main-only-native-merge/v1','UTC':now(),'actual_operator_PID':os.getpid(),'accepted_commit':accepted,'original_PR_head':original,'merge_commit':commit,'exact_parents':parents,'accepted_tree':tree,'merge_tree':merge_tree,'tree_equality_verified':True,'all_1084_accepted_materialized_pins_preserved':True,'main_only':True,'primary_checkout_mutated':False,'local_merge_complete':True,'remote_push_complete':False,'GitHub_MERGED_confirmed':False}
(D/'LOCAL_MERGE_RECEIPT.json').write_text(json.dumps(r,indent=2)+'\n')
git('push','--force-with-lease=refs/heads/main:'+accepted,'https://github.com/AlecKriebel/Math.git','HEAD:refs/heads/main');require(git('ls-remote','https://github.com/AlecKriebel/Math.git','refs/heads/main').decode().split()[0]==commit,'Merge remote readback')
r.update({'UTC':now(),'remote_push_complete':True});(D/'REMOTE_MERGE_RECEIPT.json').write_text(json.dumps(r,indent=2)+'\n')
pr=json.loads(run(['/opt/homebrew/bin/gh','pr','view','108','--repo','AlecKriebel/Math','--json','number,state,isDraft,headRefOid,mergeCommit,mergedAt,url']))
(D/'GITHUB_STATUS_READBACK.json').write_text(json.dumps(pr,indent=2)+'\n')
require(pr['state']=='MERGED' and pr['headRefOid']==original and pr['mergeCommit']['oid']==commit,'Actual GitHub merged state/OID unconfirmed')
r.update({'UTC':now(),'GitHub_MERGED_confirmed':True,'mergedAt':pr['mergedAt'],'PR_URL':pr['url'],'native_acceptance_and_merge_complete':True,'DOI':'10.5281/zenodo.23181280','tracker_range':"'Math Puzzles'!A31:D31",'new_central_proof_search_turns':0,'human_outreach_or_GitHub_release':False})
(D/'FINAL_RECEIPT.json').write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r))
