"""Reconcile only this reviewed PR with current main, preserving shared checkout/index."""
from pathlib import Path
import datetime,hashlib,json,os,subprocess,time
A=Path(__file__).resolve().parent; P=A.parents[1]; R=P.parent
N=344; H='86a758b1cc9c94322ce6afc3d17150fa2c90327a'
BRANCH='math/30005649-qss-self-duality-wip'; Q='unsolved_math_prioritization/QUEUE.md'
PROBLEM=b'30005649'; TARGET='problems/30005649_qss_self_duality'
def utc():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
def window():assert not load(P/'SHARED_GIT_WINDOW_STATUS.json')['shared_git_writes_paused']
window()
assert not (A/'queue_repair_receipt.json').exists(),'Preserve previous/uncertain refresh; investigate before another mutation.'
from root_submission_gate import current_clearance
c=current_clearance()
assert len(c['sealed_author_inputs'])==8 and len(c['sealed_submission_files'])==4
original=load(A/'snapshot_manifest.json');assert original['head']==H and len(original['files'])==16
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
def dirty_bodies():
 result={}
 for raw in git('diff','--name-only','-z').split(b'\0'):
  if raw:
   p=R/raw.decode();result[raw.decode()]={'exists':p.exists(),'bytes':p.read_bytes() if p.is_file() else None,'mode':p.stat().st_mode&0o7777 if p.exists() else None}
 return result
dirty_before=dirty_bodies()
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
cells[11]=b' '+cells[11].strip()+b' Verified negative answer to Takao higher-rank self-duality question: all p>3, n>=3, qss special fiber and Witt lift both non-self-dual; research note and repaired verification package ready after third fresh full AI review; bounded priority, unrefereed. '
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
release=('Verified research note for OWR-14297740-021 (30005649)\n\n'
 'For every prime p>3 and n>=3 over k=an algebraic closure of F_p, there is a p-killed finite flat commutative W(k)-group of rank p^(2n) with quasi-supersingular special fiber, such that both special fiber and Witt-ring lift fail Cartier self-duality. '
 'This gives an explicit negative answer to the higher-rank question after Proposition2 on printed2479 of Naotake Takao\'s contribution to OWR42/2023. '
 'Quasi-supersingularity here requires actual supersingular elliptic p-torsion factors over k; no quasi-supersingular Witt-ring filtration or descent to every perfect field is asserted. '
 'The six-dimensional Dieudonne module has a three-factor elliptic filtration, is distinguished from its dual by dim(im(F^2) intersect im(V^2)), and admits an explicit finite Honda complement. Standard elliptic factors extend the example to all n>=3.\n\n'
 'Established cyclic-word, supersingular and finite Honda theory is credited, including Pries-Ulmer, Oort, Fontaine-Laffaille, Hoshi and Takao. '
 'A focused audit also supplies an integral supersingular flag for the classical cyclic completion. The bounded priority audit records inspected-source and version limits; no first-discovery, first-application or worldwide continuing-openness certificate is claimed.\n\n'
 'Three independent mathematical approach families and three successive NEW full preprint adversaries were used. Historical first-review B1 and second-review F01/root B2 remain adverse as dated records. '
 'B1 was repaired by separating interpreter provenance from deterministic mathematical output. F01/root B2 was repaired by the opposite squared-Frobenius twists in the generic dual kernel formula, with dense nonprime basis controls and targeted negative tests. '
 'The third NEW full adversary of the complete repaired v04 packet closed with zero unresolved mandatory findings, independently reproduced by the root review. '
 'Main theorem, TeX, PDF and exact deposit metadata were unchanged by those software repairs. Extensive AI use; this is an unrefereed preprint without independent external human peer review.\n\n'
 'All15 original problem files remain byte-identical to submitted head '+H+'. Their dated author and review history is preserved. '
 'Current qualifications and the corrected generic supporting helper are in the cleared public verification package; historical acceptance statements must be read with the root qualification. '
 'The package contains33 ordinary files,32 payloads, with standard-library verification on Python3.12 and3.14. The characteristic-two arithmetic tests concern generic semilinear algebra only and do not extend the p>3 theorem. '
 'Production Zenodo publication and tracker registration will be recorded separately after their successful execution.\n\n'
 'Cleared formal submission files:\n'+''.join('- '+e['path']+': '+str(e['bytes'])+' bytes; SHA256 '+e['sha256']+'\n' for e in c['sealed_submission_files'])+'\n'
 'Author: Alec Kriebel, Independent researcher, ORCID0009-0001-9320-500X. LicenseCC BY4.0.\n').encode()
added[TARGET+'/PREPRINT_RELEASE.md']=release;assert len(added)==5
for path,b in added.items():tree=replace(tree,path.split('/'),git('hash-object','-w','--stdin',input=b).decode().strip())
expected={e['path'] for e in original['files']}|set(added);assert len(expected)==21
assert set(git('diff','--name-only',main,tree).decode().splitlines())==expected
for e in original['files']:
 if e['path']==Q:continue
 b=git('show',tree+':'+e['path']);assert len(b)==e['bytes'] and sha(b)==e['sha256']
 assert git('ls-tree',tree,'--',e['path']).split(b'\t',1)[0].split()==[b'100644',b'blob',e['git_blob_sha'].encode()]
for path,b in added.items():assert git('show',tree+':'+path)==b
assert git('show',tree+':'+Q)==new
assert git('rev-parse','HEAD').decode().strip()==local and ix.read_bytes()==index
assert dirty_bodies()==dirty_before
current_clearance()
remote=json.loads(run('main_before_push',['gh','api','repos/AlecKriebel/Math/git/ref/heads/main']).stdout);assert remote['object']['sha']==main
window();commit=git('commit-tree',tree,'-p',H,'-p',main,input=b'Refresh PR344 on current main, preserve original proof and add reviewed repaired preprint\n').decode().strip()
run('branch_push',['git','push','origin',commit+':refs/heads/'+BRANCH])
assert git('rev-parse','HEAD').decode().strip()==local and ix.read_bytes()==index
assert dirty_bodies()==dirty_before
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
 'all_original_target_files_unchanged':15,'new_submission_files':5,'changed_queue_line':i+1,'changed_queue_pipe_cells':[8,9,11],
 'accepted_status':'claimed_solved','author_turns':'1/5','old_row':before.decode(),'new_row':lines[i].decode(),
 'all_other_queue_bytes_preserved':True,'checkout_and_entire_index_unchanged':True,'all_dirty_tracked_bodies_modes_preserved':True,'nonforce_branch_push_succeeded':True,
 'captures':captures,'program_sha256':sha(Path(__file__).read_bytes()),'workflow_percent':80}
(A/'queue_repair_receipt.json').write_text(json.dumps(r,indent=2)+'\n')
print(json.dumps({k:v for k,v in r.items() if k!='captures'},indent=2))
