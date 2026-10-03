#!/usr/bin/env python3
"""PR373 complete live gate. Reads Git/GitHub; writes only explicit private output.

Never edits a PR, ref, source snapshot, queue or publication record. Expected
inputs are explicit, exact objects. Failures remain failures, with no normalizing.
No acceptance of future/refreshed metadata is inferred from a historical PASS.
"""
import argparse,hashlib,json,os,subprocess,sys,traceback,urllib.request,shutil
from pathlib import Path
from datetime import datetime,timezone

PR=373;F='unsolved_math_prioritization/attempts/30004435';Q='unsolved_math_prioritization/QUEUE.md'
ORIGINAL_HEAD='4e635c77d7399d671ea58700e41bbd92cbdeeb46';ORIGINAL_BASE='efd29c05204703acca9a0860812f54b94fae54b1'
AUTHOR_MANIFEST='48fce3e6630fd1bfd81c49054ab4c5640eeb7079f2bd6cc62b65ea479750d78c'
REVIEW_MANIFEST='fd9fdd983fc29b09fad2d2cc9c5264db782f0a6748404a639d837335f28aa5eb'
OLD=b'| 398 | 30004435 / OWR-17474-009 | Probabilistic Equality of Left and Right Tail Fields | 0.1435 | 4.5 | 3 | 2020 | queued | 0/5 |  |  |  |'
NEW=OLD.replace(b'| queued | 0/5 |',b'| unsolved | 5/5 |')
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_bytes())
def demand(v,msg):
 if not v:raise AssertionError(msg)
def checked(cmd,cwd=None):return subprocess.check_output(cmd,cwd=cwd,stderr=subprocess.PIPE)
def main():
 ap=argparse.ArgumentParser(description=__doc__)
 ap.add_argument('--repo',type=Path,required=True);ap.add_argument('--snapshot',type=Path,required=True)
 ap.add_argument('--expected-head',required=True);ap.add_argument('--expected-main',required=True)
 ap.add_argument('--expected-target-count',type=int,required=True);ap.add_argument('--prepared-body',type=Path,required=True)
 ap.add_argument('--out',type=Path,required=True);a=ap.parse_args()
 a.repo=a.repo.resolve();a.snapshot=a.snapshot.resolve();a.out=a.out.resolve();a.prepared_body=a.prepared_body.resolve()
 own=Path(__file__).resolve().parent.parent
 demand(a.out.is_relative_to(own),'output must be inside assigned clean_final_adversary folder')
 demand(not a.out.exists(),'fresh output directory required; do not overwrite/normalize previous gate run')
 demand(not a.snapshot.is_relative_to(a.out) and not a.out.is_relative_to(a.snapshot),'snapshot and output must be separate')
 a.out.mkdir(parents=True);private=a.out/'private';private.mkdir();streams=a.out/'streams';streams.mkdir()
 result={'at_utc':datetime.now(timezone.utc).isoformat(),'status':'FAIL','expected_head':a.expected_head,'expected_main':a.expected_main,'expected_target_count':a.expected_target_count,'checks':[],'gate_code_sha256':sha(Path(__file__).read_bytes())}
 def ck(v,msg):demand(v,msg);result['checks'].append(msg)
 def git(*x):return checked(['git',*x],a.repo)
 def api(name,endpoint):
  b=checked(['gh','api',endpoint],a.repo);(private/(name+'.json')).write_bytes(b);return json.loads(b)
 try:
  body=a.prepared_body.read_bytes();body_text=body.decode('utf-8');result['prepared_body_sha256']=sha(body)
  ck(git('symbolic-ref','--short','HEAD').decode().strip()=='main','calling repository stays on main')
  pr=api('pr_start',f'repos/AlecKriebel/Math/pulls/{PR}');mainapi=api('main_start','repos/AlecKriebel/Math/git/ref/heads/main')
  ck(pr['state']=='open' and not pr['merged'],'actual PR open and unmerged')
  ck(pr['head']['sha']==a.expected_head,'actual API head exactly expected head')
  ck(pr['base']['ref']=='main' and pr['base']['sha']==a.expected_main,'actual API base is expected current main')
  ck(mainapi['object']['sha']==a.expected_main,'actual remote main exactly expected main')
  ck(git('rev-parse','main').decode().strip()==a.expected_main,'actual local main exactly expected main')
  ck((pr.get('body') or '')==body_text,'actual API body exactly prepared literal body')
  ck(subprocess.run(['git','merge-base','--is-ancestor',a.expected_main,a.expected_head],cwd=a.repo).returncode==0,'current main is ancestor of actual candidate head')
  for key,obj in [('candidate_commit',a.expected_head),('current_main_commit',a.expected_main),('original_commit',ORIGINAL_HEAD)]:
   remote=api(key,'repos/AlecKriebel/Math/git/commits/'+obj);ck(remote['sha']==obj,key+' remote object exists exactly')
   ck(git('rev-parse',obj+'^{commit}').decode().strip()==obj,key+' local object exists exactly')
  ck(pr['mergeable'] is True,'actual API reports mergeable true')
  ck(pr['mergeable_state']=='clean','actual API reports clean mergeability')
  merge=api('test_merge','repos/AlecKriebel/Math/git/commits/'+pr['merge_commit_sha'])
  ck([x['sha'] for x in merge['parents']]==[a.expected_main,a.expected_head],'actual cached test merge binds expected current main and head')
  # Literal entire-tree scope, not a count or normalizing replacement.
  snapshot_paths=sorted(str(p.relative_to(a.snapshot)) for p in a.snapshot.rglob('*') if p.is_file())
  target=[p for p in snapshot_paths if p.startswith(F+'/')]
  ck(snapshot_paths==sorted(target+[Q]),'snapshot contains only target files plus full literal queue')
  ck(len(target)==a.expected_target_count,'exact expected target-file count')
  headtarget=git('ls-tree','-r','--name-only',a.expected_head,'--',F).decode().splitlines()
  ck(headtarget==target,'entire actual target tree equals exact snapshot inventory')
  diff=git('diff','--name-only',a.expected_main,a.expected_head).decode().splitlines()
  ck(diff==snapshot_paths,'complete current-main diff is exactly target inventory plus queue')
  bindings=[]
  for p in snapshot_paths:
   b=(a.snapshot/p).read_bytes();ck(git('show',a.expected_head+':'+p)==b,'actual head exact bytes: '+p)
   bindings.append({'path':p,'bytes':len(b),'sha256':sha(b),'git_blob':git('rev-parse',a.expected_head+':'+p).decode().strip()})
  result['snapshot_bindings']=bindings
  mainqueue=git('show',a.expected_main+':'+Q);headqueue=(a.snapshot/Q).read_bytes()
  ck(mainqueue.count(OLD)==1,'current-main target queue row occurs exactly once in original state')
  ck(headqueue==mainqueue.replace(OLD,NEW),'entire candidate queue equals literal two-cell change and preserves all other bytes')
  # Every other path identical, with complete tree maps including modes/types.
  def treemap(ref):
   return {x.split('\t',1)[1]:x.split('\t',1)[0] for x in git('ls-tree','-r',ref).decode().splitlines()}
  mt=treemap(a.expected_main);ht=treemap(a.expected_head);allow=set(snapshot_paths)
  ck({k:v for k,v in mt.items() if k not in allow}=={k:v for k,v in ht.items() if k not in allow},'all other complete tree paths/modes/types/blob identities preserved')
  api_files_b=checked(['gh','api','--paginate','--slurp',f'repos/AlecKriebel/Math/pulls/{PR}/files?per_page=100'],a.repo)
  (private/'api_files.json').write_bytes(api_files_b);api_files=[r for page in json.loads(api_files_b) for r in page]
  ck(sorted(r['filename'] for r in api_files)==snapshot_paths,'complete actual API file list exactly snapshot inventory')
  ck(pr['changed_files']==len(snapshot_paths),'actual API changed-file count equals exact complete inventory')
  P=a.snapshot/F
  ck(sha((P/'FINAL_FROZEN_MANIFEST.json').read_bytes())==AUTHOR_MANIFEST,'unchanged original final author manifest')
  ck(sha((P/'final_review/REVIEW_MANIFEST.json').read_bytes())==REVIEW_MANIFEST,'unchanged original review manifest')
  author=load(P/'FINAL_FROZEN_MANIFEST.json');review=load(P/'final_review/REVIEW_MANIFEST.json')
  frozen=[r['path'] for r in author['files']]+['FINAL_FROZEN_MANIFEST.json']+['final_review/'+r['path'] for r in review['files']]+['final_review/REVIEW_MANIFEST.json']
  ck(len(frozen)==49 and len(set(frozen))==49,'exact42author plus7review frozen-file inventory')
  for path in frozen:ck(git('show',ORIGINAL_HEAD+':'+F+'/'+path)==(P/path).read_bytes(),'original frozen preservation: '+path)
  mcounts={}
  for f in sorted(P.rglob('*.json')):
   j=load(f)
   if 'files' not in j:continue
   for r in j['files']:
    rel=Path(r['path']);ck(not rel.is_absolute() and '..' not in rel.parts,'manifest relative confined path: '+str(f.relative_to(P))+' / '+r['path'])
    base=f.parent if f.name=='REVIEW_MANIFEST.json' and f.parent.name=='final_review' else P
    p=base/r['path'];ck(p.is_file(),'manifest target exists: '+str(f.relative_to(P))+' / '+r['path'])
    b=p.read_bytes();ck(len(b)==r.get('bytes',r.get('size')),'manifest exact length: '+str(f.relative_to(P))+' / '+r['path'])
    if 'sha256' in r:ck(sha(b)==r['sha256'],'manifest exact sha256: '+str(f.relative_to(P))+' / '+r['path'])
    if 'sha' in r:ck(hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()==r['sha'],'manifest exact Gitblob: '+r['path'])
   mcounts[str(f.relative_to(P))]=len(j['files'])
  result['manifest_counts']=mcounts
  pub=load(P/'PUBLICATION_MANIFEST.json')
  ck(sorted(r['path'] for r in pub['files'])==sorted(p[len(F)+1:] for p in target if p!=F+'/PUBLICATION_MANIFEST.json'),'publication manifest binds every actual target file except itself')
  # All four sources fetched independently on this run; raw assets remain private.
  sources=private/'sources';sources.mkdir();items=load(P/'SOURCE_MANIFEST.json')['primary_pdfs'];e=load(P/'TURN_3_SOURCE.json');items=items+[{'file':e['local_source'],'url':e['url'],'bytes':e['bytes'],'sha256':e['sha256']}]
  source_results=[]
  for r in items:
   b=urllib.request.urlopen(r['url'],timeout=90).read();(sources/r['file']).write_bytes(b)
   ck(len(b)==r['bytes'] and sha(b)==r['sha256'],'separate fresh primary-source exact bytes: '+r['file'])
   source_results.append({'name':r['file'],'url':r['url'],'bytes':len(b),'sha256':sha(b)})
  result['source_results']=source_results
  # Dedicated private clone; known code is executed only in the copied candidate.
  clone=private/'clone';checked(['git','clone','--shared','--no-checkout',str(a.repo),str(clone)])
  replay=clone/'candidate';shutil.copytree(a.snapshot,replay);AP=replay/F
  def run(name,args,expected=None):
   r=subprocess.run([sys.executable,*map(str,args)],cwd=clone,stdout=subprocess.PIPE,stderr=subprocess.PIPE,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
   (streams/(name+'.stdout')).write_bytes(r.stdout);(private/(name+'.stderr')).write_bytes(r.stderr)
   ck(r.returncode==0,'complete replay zero exit: '+name)
   if expected is not None:ck(r.stdout==expected,'complete replay exact literal output: '+name)
   return r.stdout
  counts=[]
  for n in range(1,6):counts.append(json.loads(run('turn'+str(n),[AP/f'verify_turn{n}.py'],(P/f'TURN_{n}_CHECKS.json').read_bytes()))['assertions'])
  ck(counts==[5527,25404,25455,123026,31562] and sum(counts)==210974,'actual per-turn counts and total remain exact')
  authorstream=run('author_replay',[AP/'REPLAY_ALL.py','--sources',sources],(P/'final_review/AUTHOR_REPLAY.json').read_bytes())
  run('old_independent',[AP/'final_review/independent_checks.py'],(P/'final_review/INDEPENDENT_CHECKS.json').read_bytes())
  run('review_wrapper',[AP/'final_review/verify_review.py','--author-dir',AP],b'PASS: review, frozen author/remote bindings and independent exact replay\n')
  result['author_replay']=json.loads(authorstream)
  # Final read guarantees no unnoticed head/body/main transition during checks.
  endpr=api('pr_end',f'repos/AlecKriebel/Math/pulls/{PR}');endmain=api('main_end','repos/AlecKriebel/Math/git/ref/heads/main')
  ck(endpr['head']['sha']==a.expected_head and endpr['base']['sha']==a.expected_main and endmain['object']['sha']==a.expected_main,'final actual head/base/main unchanged during gate')
  ck((endpr.get('body') or '')==body_text,'final actual API body remains exact')
  ck(endpr['state']=='open' and not endpr['merged'],'final actual PR remains open/unmerged')
  result['status']='PASS_LIVE_SCOPED_UNSOLVED_5_OF_5';result['scope']='Source-first scoped mathematics; complete byte replays and actual Git/API metadata. No novelty/external peer review/formal proof/full resolution claim.'
 except BaseException as e:
  result['failure']=repr(e);result['traceback']=traceback.format_exc();result['scope']='Gate failed honestly. No input normalized, metadata rewritten, source count weakened, or future acceptance asserted.'
 finally:
  result['finished_at_utc']=datetime.now(timezone.utc).isoformat();(a.out/'VERDICT.json').write_text(json.dumps(result,indent=2,sort_keys=True)+'\n')
  print(json.dumps({'status':result['status'],'out':str(a.out),'checks_passed':len(result['checks']),'failure':result.get('failure')},indent=2))
 return 0 if result['status'].startswith('PASS') else 1
if __name__=='__main__':sys.exit(main())
