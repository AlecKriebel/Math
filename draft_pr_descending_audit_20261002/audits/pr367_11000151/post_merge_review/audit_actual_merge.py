"""Complete read-only actual-merge scope audit; no heavy mathematical rerun."""
from pathlib import Path
from datetime import datetime,timezone
import base64,gzip,hashlib,json,os,subprocess,traceback
D=Path(__file__).resolve().parent
A=D.parent
REPO=Path('/Users/alec/Documents/Math')
PREFIX='problems/11000151_artin_a5_quotient'
QUEUE='unsolved_math_prioritization/QUEUE.md'
CHECKS=[];CAPTURES=[]
def utc():return datetime.now(timezone.utc).isoformat()
def sha(b):return hashlib.sha256(b).hexdigest()
def bind(b):return {'bytes':len(b),'sha256':sha(b)}
def load(p):return json.loads(p.read_bytes())
def save(n,o):(D/'receipts'/n).write_text(json.dumps(o,indent=2)+'\n')
def check(c,label):
 CHECKS.append({'check':label,'pass':bool(c)})
 if not c:raise AssertionError(label)
def run(label,args,public=False):
 start=utc();r=subprocess.run(list(map(str,args)),cwd=REPO,capture_output=True,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1'))
 folder=D/'fullstreams' if public else D/'private_runtime'
 streams={}
 for channel,data in [('stdout',r.stdout),('stderr',r.stderr)]:
  p=folder/(label+'.'+channel+'.gz');stored=gzip.compress(data,mtime=0);p.write_bytes(stored)
  streams[channel]={'path':p.relative_to(D).as_posix(),**bind(data),'stored_bytes':len(stored),'stored_sha256':sha(stored)}
 CAPTURES.append({'label':label,'args':list(map(str,args)),'started_utc':start,'finished_utc':utc(),'exit_code':r.returncode,**streams});save('EXECUTIONS.json',CAPTURES)
 check(r.returncode==0,label+' successful');check(r.stderr==b'',label+' complete empty stderr')
 return r.stdout
def git(label,*args):return run('git_'+label,['git',*args])
def api(label,route):return json.loads(run('api_'+label,['gh','api','--method','GET','-H','Cache-Control: no-cache','repos/AlecKriebel/Math/'+route]))
def manifest(row):
 p=A/row['path'];data=p.read_bytes();check(bind(data)=={'bytes':row['bytes'],'sha256':row['sha256']},'exact earlier manifest '+row['path'])
 obj=json.loads(data);rows=[];names=[]
 for r in obj['files']:
  q=p.parent/r['path'];check(not q.is_symlink() and q.resolve().is_relative_to(p.parent.resolve()),'confined earlier binding '+row['path']+':'+r['path'])
  check(bind(q.read_bytes())=={'bytes':r['bytes'],'sha256':r['sha256']},'complete earlier binding '+row['path']+':'+r['path']);names.append(r['path']);rows.append({'manifest':row['path'],**r})
 check(len(names)==len(set(names)),'unique earlier manifest scope '+row['path'])
 return rows
def queue(before,after):
 old=before.splitlines(keepends=True);new=after.splitlines(keepends=True)
 assert len(old)==len(new) and [i for i,(a,b) in enumerate(zip(old,new),1) if a!=b]==[400]
 cells=old[399].split(b'|');assert b'11000151 / AMR-109-0151' in cells[2]
 assert cells[8:10]==[b' queued ',b' 0/5 ']
 cells[8:10]=[b' claimed_solved ',b' 4/5 '];old[399]=b'|'.join(cells);assert after==b''.join(old)
def validate_pr(pr,b,body):
 assert pr['merged'] is True and pr['state']=='closed' and not pr['draft']
 assert pr['merge_commit_sha']==b['merge'] and pr['head']['sha']==b['head']
 assert pr['body'].encode()==body and pr['merged_at']==b['merged_at']
 assert pr['base']['ref']=='main' and pr['base']['repo']['full_name']=='AlecKriebel/Math'
def refs(label,b):
 remote=api(label+'_main','git/ref/heads/main');local=git(label+'_local','rev-parse','main').decode().strip();tracking=git(label+'_tracking','rev-parse','origin/main').decode().strip()
 git(label+'_ancestor_local','merge-base','--is-ancestor',b['merge'],local);git(label+'_ancestor_tracking','merge-base','--is-ancestor',b['merge'],tracking)
 compared=api(label+'_remote_ancestry','compare/'+b['merge']+'...'+remote['object']['sha'])
 check(compared['merge_base_commit']['sha']==b['merge'] and compared['status'] in ('ahead','identical') and compared['behind_by']==0,'actual merge ancestor of current API main '+label)
 return {'utc':utc(),'local_main':local,'origin_main':tracking,'api_main':remote,'actual_merge_ancestor_of_all':True}
def negative(label,call):
 try:call()
 except AssertionError:
  (D/'fullstreams'/('negative_'+label+'.txt')).write_text(traceback.format_exc());check(True,'negative '+label+' rejected')
 else:raise AssertionError('negative accepted '+label)
def main():
 b=load(D/'BASELINE.json')
 for r in load(D/'CODE_READY_SEAL.json')['programs']:check(bind((D/r['path']).read_bytes())=={'bytes':r['bytes'],'sha256':r['sha256']},'fully read unchanged program '+r['path'])
 body=(A/b['body_file']).read_bytes();check(bind(body)=={'bytes':b['body_bytes'],'sha256':b['body_sha256']},'entire accepted body')
 original=load(A/'root_original_reproduction_receipt.json');targets=[r for r in original['all44_actual_files'] if r['path'].startswith(PREFIX+'/')];expected=sorted([r['path'] for r in targets]+[QUEUE])
 check(len(targets)==43 and len(expected)==44,'complete original43 plus queue')
 bindings=[]
 for r in b['manifests']:bindings+=manifest(r)
 for r in b['other_immutable_files']:check(bind((A/r['path']).read_bytes())=={'bytes':r['bytes'],'sha256':r['sha256']},'entire earlier immutable file '+r['path'])
 for label,path,expected_out in [('original127','clean_final_adversary/verify_audit.py',b'PASS: complete self-excluded public audit, earlier/final seals and44 raw execution-output streams\n'),('prior110','clean_final_adversary/final_live/verify_live_audit.py',b'PASS: complete additive audit, final seal, every binding and all full retained execution outputs\n'),('refresh104','final_live_refresh_02/verify_live_audit.py',b'PASS: complete additive audit, final seal, every binding and all full retained execution outputs\n')]:
  check(run('closed_'+label,['python3','-B',A/path],public=True)==expected_out,'entire prior closed validator stdout '+label)
 pr=api('start_pr','pulls/367');validate_pr(pr,b,body)
 actual=api('actual_merge','git/commits/'+b['merge']);check(actual['sha']==b['merge'] and actual['tree']['sha']==b['tree'] and [p['sha'] for p in actual['parents']]==[b['base'],b['head']],'actual API merge identity parents tree')
 raw=git('raw_merge','cat-file','commit',b['merge']);check(hashlib.sha1(b'commit '+str(len(raw)).encode()+b'\0'+raw).hexdigest()==b['merge'],'full actual Git raw commit identity')
 header=raw.split(b'\n\n',1)[0].splitlines();parents=[line.split()[1].decode() for line in header if line.startswith(b'parent ')];tree=[line.split()[1].decode() for line in header if line.startswith(b'tree ')]
 check(parents==[b['base'],b['head']] and tree==[b['tree']],'actual complete Git parents/tree equal API')
 check(git('actual_tree','rev-parse',b['merge']+'^{tree}').decode().strip()==b['tree']==git('reviewed_head_tree','rev-parse',b['head']+'^{tree}').decode().strip(),'actual merge and reviewed head exact tree')
 check(git('branch','branch','--show-current')==b'main\n','remained main')
 current=refs('start',b)
 check(git('actual_delta','diff','--name-only',b['base'],b['merge']).decode().splitlines()==expected,'entire actual Git delta44')
 comparison=api('actual_delta','compare/'+b['base']+'...'+b['merge'])
 check(comparison['merge_base_commit']['sha']==b['base'] and sorted(r['filename'] for r in comparison['files'])==expected,'entire actual API delta44 from exact parent')
 prfiles=api('all_pr_files','pulls/367/files?per_page=100&page=1');check(api('pr_files_end','pulls/367/files?per_page=100&page=2')==[],'PR files exhausted')
 check(sorted(r['filename'] for r in prfiles)==expected,'entire merged PR API44 scope')
 bypath={r['filename']:r for r in comparison['files']};prbypath={r['filename']:r for r in prfiles};files=[];data_by={}
 for i,row in enumerate(targets+[{'path':QUEUE}]):
  p=row['path'];data=git('blob_'+str(i),'show',b['merge']+':'+p);mode,kind,blob,_=git('mode_'+str(i),'ls-tree',b['merge'],'--',p).decode().split(None,3)
  check(mode=='100644' and kind=='blob','actual mode '+p)
  check(bypath[p]['sha']==blob==prbypath[p]['sha'] and bypath[p]['status']==prbypath[p]['status']==('modified' if p==QUEUE else 'added'),'actual Git/two API full file status/blob '+p)
  api_blob=api('blob_'+str(i),'git/blobs/'+blob);check(base64.b64decode(api_blob['content'])==data and api_blob['size']==len(data),'entire actual API/Git blob '+p)
  if p!=QUEUE:check(bind(data)=={'bytes':row['bytes'],'sha256':row['sha256']},'entire original43 bytes '+p)
  data_by[p]=data;files.append({'path':p,'mode':mode,'git_blob_sha':blob,'status':bypath[p]['status'],**bind(data)})
 before=git('base_queue','show',b['base']+':'+QUEUE);queue(before,data_by[QUEUE]);check(True,'whole queue only own line400 cells8/9')
 for r in original['nested_bindings']:
  p=(Path(PREFIX)/Path(r['manifest']).parent/r['path']).as_posix();check(bind(data_by[p])=={'bytes':r['bytes'],'sha256':r['sha256']},'actual106 nested binding '+r['manifest']+':'+r['path'])
 repair=load(A/'preprint/REPAIRED_REVIEW_PACKAGE_02.json');submission=[]
 for row in repair['sealed_files']:
  data=(A/'preprint'/row['path']).read_bytes();check(bind(data)=={'bytes':row['bytes'],'sha256':row['sha256']},'unchanged reviewed submission '+row['path']);submission.append(row)
 import copy
 mutant=copy.deepcopy(pr);mutant['merged']=False;negative('unmerged',lambda:validate_pr(mutant,b,body))
 mutant=copy.deepcopy(pr);mutant['body']+='altered';negative('body',lambda:validate_pr(mutant,b,body))
 negative('queue_extra_byte',lambda:queue(before,data_by[QUEUE]+b'altered\n'))
 endpr=api('end_pr','pulls/367');validate_pr(endpr,b,body);endrefs=refs('end',b)
 for r in b['manifests']:manifest(r)
 for r in b['other_immutable_files']:check(bind((A/r['path']).read_bytes())=={'bytes':r['bytes'],'sha256':r['sha256']},'end earlier immutable file '+r['path'])
 for row in submission:check(bind((A/'preprint'/row['path']).read_bytes())=={'bytes':row['bytes'],'sha256':row['sha256']},'end unchanged reviewed submission '+row['path'])
 save('ALL44_ACTUAL_FILES_AND_QUEUE.json',{'files':files,'queue_physical_line':400,'only_queue_pipe_cells':[8,9],'all_other_queue_bytes_identical':True,'base_queue':bind(before),'merged_queue':bind(data_by[QUEUE])})
 save('ACTUAL_COMMIT_PR_REFS.json',{'actual_commit':actual,'start_pr':pr,'end_pr':endpr,'start_refs':current,'end_refs':endrefs,'full_git_raw_commit':bind(raw)})
 save('EARLIER_BINDINGS_AND_SUBMISSION.json',{'all_manifest_bindings':bindings,'submission':submission,'all106_actual_nested_bindings':original['nested_bindings']})
 save('CHECKS.json',CHECKS)
 result={'utc':utc(),'status':'QUALIFIED_ACTUAL_MERGE_SCOPE_PASS','merge':b['merge'],'parents':[b['base'],b['head']],'tree':b['tree'],'head':b['head'],'body':bind(body),'all_actual_files':44,'unchanged_original_target_files':43,'checks':len(CHECKS),'complete_captures':len(CAPTURES),'prior127_110_104_unchanged':True,'fresh_heavy_mathematical_replays':False,'reason_no_new_math_replay':'Exact original43 mathematical bytes, sources/review/replay manifests and four reviewed submission bindings remain unchanged; all three prior complete closed validators pass.','workflow_completion_percent':100,'remaining_gap':'Historical full orbit-classification priority and external human peer review remain unverified. Zenodo/DOI/tracker/release publication status is outside this actual-merge audit.','mutations':False}
 save('FINAL_RECEIPT.json',result)
 (D/'FINAL_REPORT.md').write_text('# Actual merge adversarial audit of PR367\n\nQualified PASS for actual merge '+b['merge']+', with exact parents '+b['base']+' and '+b['head']+' and tree '+b['tree']+'. The actual Git object, API commit, merged PR/head/body, all44 changed files/modes/blobs, all43 original bytes, whole queue and all106 nested bindings agree. Only own queue physical line400 cells8/9 became claimed_solved4/5. Current local main, origin/main and API main contain the merge. All reviewed four-file submission bindings and earlier127/110/104/family/priority/preprint manifests remain intact.\n\nComplete Git/API and validator outputs are retained. No heavy mathematical replay was repeated: all mathematical/source/submission bytes remain bound to the already complete independent replays. This audit checks actual-merge scope, not historical novelty, external human peer review or Zenodo/DOI/tracker/release completion. No candidate, Git, service or person was modified or contacted.\n')
 with (D/'RESEARCH_LOG.md').open('a') as log:log.write('- '+utc()+': Complete actual-merge scope and earlier evidence pass; three adversarial local controls reject changed state/body/queue. No new mathematical/source/submission bytes and no heavy rerun. Completion100%.\n')
 sealed=[D/'FINAL_REPORT.md',D/'CODE_READY_SEAL.json']+sorted((D/'receipts').glob('*'))
 def record(p):return {'path':p.relative_to(D).as_posix(),**bind(p.read_bytes())}
 (D/'FINAL_SEAL.json').write_text(json.dumps({'utc':utc(),'status':result['status'],'sealed_artifacts':[record(p) for p in sealed]},indent=2)+'\n')
 public=[p for p in D.rglob('*') if p.is_file() and p.name!='PUBLIC_MANIFEST.json' and not any(x in {'private_runtime','__pycache__'} for x in p.relative_to(D).parts)]
 (D/'PUBLIC_MANIFEST.json').write_text(json.dumps({'utc':utc(),'self_excluded':True,'files':[record(p) for p in sorted(public)]},indent=2)+'\n')
 print(json.dumps(result,indent=2))
if __name__=='__main__':
 try:main()
 except BaseException:
  save('FAILURE.json',{'utc':utc(),'status':'FAIL_NO_ACCEPTANCE','traceback':traceback.format_exc(),'checks':CHECKS,'captures':CAPTURES})
  raise
