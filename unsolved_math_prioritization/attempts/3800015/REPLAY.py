#!/usr/bin/env python3
"""Complete-output replay; authenticate with external BOOTSTRAP.py first."""
from pathlib import Path
import argparse,errno,hashlib,json,math,os,stat,subprocess,sys,tempfile
EXPECTED_SHA='c326afcf4ad1d54783957a178f0da79e6a99a5eae52cee552e45a517f5bbed5a'
class Reject(Exception):pass
def need(ok,text):
 if not ok:raise Reject(text)
def sha(b):return hashlib.sha256(b).hexdigest()
def pairs(items):
 out={}
 for k,v in items:
  need(k not in out,'duplicate JSON key');out[k]=v
 return out
def nonfinite(s):raise Reject('nonfinite JSON constant')
def floating(s):
 x=float(s);need(math.isfinite(x),'nonfinite JSON number');return x
def load(b):return json.loads(b,object_pairs_hook=pairs,parse_constant=nonfinite,parse_float=floating)
def same(a,b):
 if type(a) is not type(b):return False
 if type(a) is dict:return set(a)==set(b) and all(same(a[k],b[k]) for k in a)
 if type(a) is list:return len(a)==len(b) and all(same(x,y) for x,y in zip(a,b))
 return a==b
def run(script,args,cwd):
 flags=[] if sys.flags.optimize==0 else ['-O' if sys.flags.optimize==1 else '-OO']
 env={'PATH':'/usr/bin:/bin','HOME':str(cwd),'LANG':'C.UTF-8','PYTHONNOUSERSITE':'1','PYTHONDONTWRITEBYTECODE':'1'}
 p=subprocess.run([sys.executable,'-I','-S','-B',*flags,str(script),*map(str,args)],cwd=cwd,env=env,capture_output=True,timeout=240)
 need(p.returncode==0 and p.stderr==b'','replay child failed: '+script.name)
 return {'exit_code':p.returncode,'stdout':p.stdout.decode(),'stderr':p.stderr.decode(),'result':load(p.stdout)}
def probe(file,new):
 output=[]
 for label,target,flags in [('existing_file',file,os.O_WRONLY|os.O_APPEND),('new_file',new,os.O_WRONLY|os.O_CREAT|os.O_EXCL)]:
  try:fd=os.open(target,flags,0o600)
  except OSError as e:
   need(e.errno in (errno.EACCES,errno.EROFS),'write denied for unrelated reason');output.append({'target':label,'denied':True,'errno':e.errno})
  else:os.close(fd);raise Reject('write succeeded')
 return output
def collect(root):
 need(os.getuid()==1000 and os.geteuid()==1000,'genuine UID/EUID 1000 required');need(sys.version.split()[0]=='3.12.14','exact-output replay requires Python 3.12.14')
 for p in [root,*root.rglob('*')]:need(p.stat().st_mode&0o222==0,'input has write bits')
 with tempfile.TemporaryDirectory(prefix='line-arrangement-replay-') as td:
  cwd=Path(td)/'cwd';cwd.mkdir();sentinel=cwd/'sentinel';sentinel.write_text('read-only probe\n');sentinel.chmod(0o444);cwd.chmod(0o555)
  try:
   probes={'delivery':probe(root/'REPLAY.py',root/'.write-probe'),'audit':probe(root/'audit/independent_checks.py',root/'audit/.write-probe'),'cwd':probe(sentinel,cwd/'new')}
   native=run(root/'author/verify.py',['--require-readonly'],cwd)
   independent=run(root/'audit/independent_checks.py',[root/'author/verify.py'],cwd)
   original_mutations=run(root/'audit/mutation_checks.py',[root/'author/verify.py'],cwd)
   complete_mutations=run(root/'REPLAY_MUTATIONS.py',[root/'author/verify.py'],cwd)
  finally:cwd.chmod(0o755)
 need(native['result']['all_pairs_queries']==6531 and independent['result']['independent_ordered_distance_queries']==7828 and independent['result']['all_tied_geodesic_paths_checked']==890,'unexpected mathematical counts')
 return {'native':native,'independent':independent,'original_mutations':original_mutations,'complete_mutations':complete_mutations,'write_probes':probes,'uid':os.getuid(),'euid':os.geteuid(),'optimization':sys.flags.optimize}
def optional(root,a):
 out={'fresh_source_bytes':'NOT_RUN','fresh_corpus_bytes':'NOT_RUN','fresh_source_retrieval':'NOT_RUN','fresh_source_inspection':'NOT_RUN','fresh_record_join':'NOT_RUN'}
 def match(p,n,size,digest):
  need(not p.is_symlink() and p.is_file() and stat.S_ISREG(p.stat().st_mode),'missing or nonregular optional input: '+n);need(p.stat().st_size==size,'optional input size: '+n)
  h=hashlib.sha256()
  with p.open('rb') as f:
   for block in iter(lambda:f.read(1048576),b''):h.update(block)
  need(h.hexdigest()==digest,'optional input hash: '+n);return {'id':n,'bytes':size,'sha256':digest,'match':True}
 if a.source_dir is not None:
  need(not a.source_dir.is_symlink() and a.source_dir.is_dir(),'invalid source directory')
  rows=load((root/'author/SOURCES.json').read_bytes())['sources'];need(len(rows)==8,'source count')
  out['source_matches']=[match(a.source_dir/r['id'],r['id'],r['retrieved_bytes'],r['sha256']) for r in rows];out['fresh_source_bytes']='PASS_CURRENT_BYTE_REHASH'
 if a.problems is not None:
  rows=load((root/'CORPUS_METADATA.json').read_bytes())['datasets'];need([r['name'] for r in rows]==['problems.json','research_results.json'],'corpus order')
  out['corpus_matches']=[match(p,r['name'],r['bytes'],r['sha256']) for p,r in zip([a.problems,a.research_results],rows)];out['fresh_corpus_bytes']='PASS_CURRENT_BYTE_REHASH'
 return out
def main():
 ap=argparse.ArgumentParser();ap.add_argument('root',type=Path);ap.add_argument('--source-dir',type=Path);ap.add_argument('--problems',type=Path);ap.add_argument('--research-results',type=Path);a=ap.parse_args()
 need((a.problems is None)==(a.research_results is None),'both corpus inputs required');root=a.root.absolute();raw=(root/'EXPECTED_OUTPUTS.json').read_bytes();need(sha(raw)==EXPECTED_SHA,'fixed expected-output pin')
 expected=load(raw);need(type(expected) is dict and set(expected)=={'schema','python_version','normalization','modes'},'expected schema')
 need(expected['schema']=='line-arrangement-complete-outputs-v1' and expected['python_version']=='3.12.14' and set(expected['modes'])=={'0','1','2'},'expected identity')
 observed=collect(root);need(same(observed,expected['modes'][str(sys.flags.optimize)]),'complete fresh output mismatch')
 return {'schema':'line-arrangement-public-replay-v1','status':'PASS_ACCEPTED_PARTIALS','problem_id':3800015,'rank':1060,'disposition':'exhausted','turns':5,'full_target_resolved':False,'novelty_claimed':False,'formal_proof':False,'complete_expected_output_comparison':'PASS','expected_outputs_sha256':EXPECTED_SHA,'normalization':expected['normalization'],'observed':observed,'optional':optional(root,a)}
if __name__=='__main__':
 try:print(json.dumps(main(),sort_keys=True,indent=2))
 except (Reject,OSError,ValueError,TypeError,KeyError,UnicodeError,subprocess.SubprocessError) as e:print('REJECT: '+str(e),file=sys.stderr);sys.exit(1)
