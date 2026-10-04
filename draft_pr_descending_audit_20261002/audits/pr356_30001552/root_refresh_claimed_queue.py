"""Reconcile only this reviewed PR with current main, preserving shared checkout/index."""
from pathlib import Path
import datetime,hashlib,json,os,subprocess,time
A=Path(__file__).resolve().parent; P=A.parents[1]; R=P.parent
N=356; H='12fc989f8635fd202eb66b553b9599f0546d05d3'
BRANCH='math/30001552-antimorphic-periods-wip'; Q='unsolved_math_prioritization/QUEUE.md'
PROBLEM=b'30001552'; TARGET='problems/30001552_antimorphic_periods'
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
def window():assert not load(P/'SHARED_GIT_WINDOW_STATUS.json')['shared_git_writes_paused']
window()
assert not (A/'queue_repair_receipt.json').exists(),'Preserve previous/uncertain refresh; investigate before another mutation.'
c=load(A/'PUBLISHING_CLEARANCE.json')
assert c['status']=='READY_AFTER_TWO_SEQUENTIAL_FRESH_PREPRINT_REVIEWS' and c['second_review_mandatory_findings']==0
assert len(c['fresh_reviews'])==2 and len(c['sealed_submission_files'])==4
for e in c['sealed_submission_files']:
 b=(A/'preprint'/e['path']).read_bytes();assert len(b)==e['bytes'] and sha(b)==e['sha256']
for n in (1,2):
 v=load(A/f'ROOT_PREPRINT_REVIEW0{n}_VERIFICATION.json')
 assert v['mandatory_findings']==0 and v['closed_namespace_unchanged'] and v['whole_verifier_output_compared']
 assert {e['path']:(e['bytes'],e['sha256']) for e in v['sealed_submission_files']}=={e['path']:(e['bytes'],e['sha256']) for e in c['sealed_submission_files']}
 assert sha((A/f'preprint_review_0{n}'/v['review_seal_path']).read_bytes())==v['review_seal_sha256']
original=load(A/'snapshot_manifest.json');assert original['head']==H and len(original['files'])==17
D=A/'root_replay_private'/('queue_refresh_'+datetime.datetime.now(datetime.timezone.utc).strftime('%Y%m%dT%H%M%S%f'))
D.mkdir(parents=True,exist_ok=False);captures=[]
def run(tag,args,input=None,ok=(0,)):
 if args[0]=='git' and args[1] in {'fetch','hash-object','mktree','commit-tree','push'}:window()
 started=utc()
 (D/(tag+'.preexecution.json')).write_text(json.dumps({'utc':started,'argv':args,'cwd':str(R),'orchestrator_sha256':sha(Path(__file__).read_bytes())},indent=2)+'\n')
 r=subprocess.run(args,cwd=R,input=input,capture_output=True,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0',GIT_NO_LAZY_FETCH='1'))
 streams={}
 for kind,b in [('stdout',r.stdout),('stderr',r.stderr)]:
  f=D/(tag+'.'+kind);f.write_bytes(b);streams[kind]={'path':str(f.relative_to(A)),'bytes':len(b),'sha256':sha(b)}
 e={'tag':tag,'argv':args,'started_utc':started,'finished_utc':utc(),'exit_code':r.returncode,'streams':streams}
 captures.append(e);(D/(tag+'.json')).write_text(json.dumps(e,indent=2)+'\n');assert r.returncode in ok,(tag,r.stderr.decode(errors='replace'));return r
counter=0
def git(*args,input=None):
 global counter
 counter+=1;return run('git_'+str(counter),['git',*args],input=input).stdout
assert git('branch','--show-current').strip()==b'main'
assert run('merge_head',['git','rev-parse','-q','--verify','MERGE_HEAD'],ok=(1,)).returncode==1
ix=Path(git('rev-parse','--git-path','index').decode().strip());ix=ix if ix.is_absolute() else R/ix;index=ix.read_bytes()
local=git('rev-parse','HEAD').decode().strip()
pr=load(A/'snapshot_manifest.json')
api=json.loads(run('pr_before',['gh','pr','view',str(N),'--json','state,headRefOid,headRefName,isDraft']).stdout)
assert api['state']=='OPEN' and api['isDraft'] and api['headRefOid']==H and api['headRefName']==BRANCH
for e in original['files']:
 if e['path']==Q:continue
 b=git('show',H+':'+e['path']);assert len(b)==e['bytes'] and sha(b)==e['sha256']
 assert git('ls-tree',H,'--',e['path']).split(b'\t',1)[0].split()==[b'100644',b'blob',e['git_blob_sha'].encode()]
run('main_fetch',['git','fetch','origin','main'])
main=git('rev-parse','origin/main').decode().strip();assert main==local
m=run('merge_tree',['git','merge-tree','--write-tree',H,main],ok=(0,1));tree=m.stdout.decode().splitlines()[0]
if m.returncode:
 conflicts=[line.rsplit('\t',1)[1] for line in m.stdout.decode().splitlines() if '\t' in line]
 assert conflicts and set(conflicts)=={Q},conflicts
def row(lines):
 found=[i for i,b in enumerate(lines) if len(b.split(b'|'))>11 and b.split(b'|')[2].strip().split(b' / ')[0]==PROBLEM]
 assert len(found)==1;return found[0]
frozen=git('show',H+':'+Q).splitlines(keepends=True);fc=frozen[row(frozen)].split(b'|')
assert [fc[j].strip() for j in (8,9)]==[b'claimed_solved',b'1/5']
raw=git('show',main+':'+Q);lines=raw.splitlines(keepends=True);i=row(lines);before=lines[i];cells=before.split(b'|')
assert [cells[j].strip() for j in (8,9)]==[b'queued',b'0/5']
for j in (8,9):cells[j]=fc[j]
cells[11]=b' '+cells[11].strip()+b' Verified exact alternating antimorphic gcd bound; concise research note and public verification supplement ready; bounded priority and two fresh AI preprint reviews passed (unrefereed). '
assert [j for j,(x,y) in enumerate(zip(before.split(b'|'),cells)) if x!=y]==[8,9,11]
lines[i]=b'|'.join(cells);new=b''.join(lines)
def replace(tree,parts,blob):
 entries={}
 for item in git('ls-tree','-z',tree).split(b'\0'):
  if item:
   meta,name=item.split(b'\t',1);entries[name]=tuple(meta.split())
 name=parts[0].encode();prior=entries.get(name)
 if len(parts)==1:
  if prior:assert prior[:2]==(b'100644',b'blob')
  entries[name]=(b'100644',b'blob',blob.encode())
 else:
  if prior:assert prior[:2]==(b'040000',b'tree');child=prior[2].decode()
  else:child=git('mktree','-z',input=b'').decode().strip()
  entries[name]=(b'040000',b'tree',replace(child,parts[1:],blob).encode())
 return git('mktree','-z',input=b''.join(b' '.join(entries[n])+b'\t'+n+b'\0' for n in sorted(entries))).decode().strip()
blob=git('hash-object','-w','--stdin',input=new).decode().strip();tree=replace(tree,Q.split('/'),blob)
added={TARGET+'/preprint/'+e['path']:(A/'preprint'/e['path']).read_bytes() for e in c['sealed_submission_files']}
release=('Verified research note for OWR-4425-007 (30001552)\n\n'
 'The exact unnumbered conjecture afterTheorem23 on printed2220 of OWR37/2010 is proved for arbitrary antimorphic involutions: alternating periods p,q at length p+q-gcd(p,q) force alternating gcd(p,q). '
 'A canonical common finite extension theta(w)w supplies ordinary periods2p,2q; classical Fine-Wilf and central reflection recover the alternating phase. '
 'Fine-Wilf, the Nowotka/Bischoff originating contribution and Bischoff thesis reflections/doubled periods are credited. '
 'The abb example gives only uniform one-letter-lower obstruction, not all-pair optimality.\n\n'
 'Three independent mathematical approach families, an in-depth bounded primary-literature audit, and two sequential new full preprint adversaries are complete. '
 'No earlier exact theorem was found in inspected sources; the public audit retains access/version gaps and does not certify global novelty or first discovery. '
 'Extensive AI use; unrefereed, without independent external human peer review.\n\n'
 'All16 original problem files remain byte-identical to submitted head '+H+'. Historical source/check/review claims are preserved as dated history. '
 'The currently reproduced public portable mode has68408 checks; the optional historical five-source68413 mode is not reproduced. '
 'Current accepted scope and qualifications are in the cleared note and supplement below. Production Zenodo publication and tracker registration will be dated separately after completion.\n\n'
 'Cleared files:\n'+''.join('- '+e['path']+': '+str(e['bytes'])+' bytes; SHA256 '+e['sha256']+'\n' for e in c['sealed_submission_files'])+'\n'
 'Author: Alec Kriebel, Independent researcher, ORCID0009-0001-9320-500X. LicenseCC BY4.0.\n').encode()
added[TARGET+'/PREPRINT_RELEASE.md']=release;assert len(added)==5
for path,b in added.items():tree=replace(tree,path.split('/'),git('hash-object','-w','--stdin',input=b).decode().strip())
expected={e['path'] for e in original['files']}|set(added);assert len(expected)==22
assert set(git('diff','--name-only',main,tree).decode().splitlines())==expected
for e in original['files']:
 if e['path']==Q:continue
 b=git('show',tree+':'+e['path']);assert len(b)==e['bytes'] and sha(b)==e['sha256']
 assert git('ls-tree',tree,'--',e['path']).split(b'\t',1)[0].split()==[b'100644',b'blob',e['git_blob_sha'].encode()]
for path,b in added.items():assert git('show',tree+':'+path)==b
assert git('show',tree+':'+Q)==new
assert git('rev-parse','HEAD').decode().strip()==local and ix.read_bytes()==index
remote=json.loads(run('main_before_push',['gh','api','repos/AlecKriebel/Math/git/ref/heads/main']).stdout);assert remote['object']['sha']==main
window();commit=git('commit-tree',tree,'-p',H,'-p',main,input=b'Refresh PR356 on current main, preserve original proof and add reviewed preprint\n').decode().strip()
run('branch_push',['git','push','origin',commit+':refs/heads/'+BRANCH])
assert git('rev-parse','HEAD').decode().strip()==local and ix.read_bytes()==index
for n in range(6):
 after=json.loads(run('pr_after_'+str(n),['gh','pr','view',str(N),'--json','state,headRefOid,headRefName']).stdout)
 if after['headRefOid']==commit:break
 time.sleep(.5)
assert after['state']=='OPEN' and after['headRefOid']==commit and after['headRefName']==BRANCH
S=A/'repaired_snapshot';assert not S.exists();files=[]
for path in sorted(expected):
 b=git('show',commit+':'+path);f=S/path;f.parent.mkdir(parents=True,exist_ok=True);f.write_bytes(b)
 mode=git('ls-tree',commit,'--',path).split(b'\t',1)[0].split();assert mode[:2]==[b'100644',b'blob']
 files.append({'path':path,'bytes':len(b),'sha256':sha(b),'git_blob_sha':mode[2].decode(),'mode':'100644'})
manifest={'pr':N,'head':commit,'base':main,'original_frozen_head':H,'frozen_utc':utc(),'files':files}
(A/'repaired_snapshot_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
r={'utc':utc(),'status':'PASS_CLAIMED_SOLVED_QUEUE_REFRESH','pr':N,'original_head':H,'repaired_head':commit,'current_main_parent':main,'parents':[H,main],'tree':tree,
 'all_original_target_files_unchanged':16,'new_submission_files':5,'changed_queue_line':i+1,'changed_queue_pipe_cells':[8,9,11],
 'accepted_status':'claimed_solved','author_turns':'1/5','old_row':before.decode(),'new_row':lines[i].decode(),
 'all_other_queue_bytes_preserved':True,'checkout_and_entire_index_unchanged':True,'nonforce_branch_push_succeeded':True,
 'captures':captures,'program_sha256':sha(Path(__file__).read_bytes()),'workflow_percent':80}
(A/'queue_repair_receipt.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({k:v for k,v in r.items() if k!='captures'},indent=2))
