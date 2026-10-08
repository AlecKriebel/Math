#!/usr/bin/env python3
"""Fail-closed source-free replay of accepted corrected critical-value partials."""
from pathlib import Path, PurePosixPath
import argparse,hashlib,json,math,os,re,shutil,stat,subprocess,sys,tempfile
MANIFEST='9ea0fcf80bfb4775769e45c700bb78a4845ab44623d2b079c0548a9307448064'
ORIGINAL='90f41824fce3c028993e1dcd12651dbeb86c8b2728527e61052da9b54c2e33a7'
CORRECTED='9ddef9ad585717ca652952fddceef1d3cf0f753f2e23c59a5cdc581ff92e5850'
AUDIT='a7126bb7e29e485efc506de3b6994e8e0daf59d64fa77e6e34279f0b43d74da6'
PROOF='23c088a87ef91827d94ca2aee040892c46a2492166901810586d75c49669df41'
class Reject(Exception):pass
def need(c,m):
 if not c:raise Reject(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def pairs(ps):
 d={}
 for k,v in ps:need(k not in d,'duplicate JSON key');d[k]=v
 return d
def nonfinite(x):raise Reject('nonfinite JSON constant')
def finite(s):
 x=float(s);need(math.isfinite(x),'nonfinite JSON number');return x
def load(b):return json.loads(b,object_pairs_hook=pairs,parse_constant=nonfinite,parse_float=finite)
def safe(n):return type(n) is str and bool(n) and '\\' not in n and not n.startswith('/') and all(x not in ('','.','..') for x in n.split('/'))
def inventory(root):
 need(not root.is_symlink() and root.is_dir(),'nonsymlink root required')
 files={};dirs=set()
 def visit(d,prefix):
  need(stat.S_IMODE(d.stat().st_mode) in (0o555,0o755),'directory mode')
  for e in os.scandir(d):
   n=prefix+e.name;s=e.stat(follow_symlinks=False);mode=s.st_mode
   need(not stat.S_ISLNK(mode),'symlink: '+n)
   if stat.S_ISDIR(mode):dirs.add(n);visit(Path(e.path),n+'/')
   else:
    need(stat.S_ISREG(mode),'nonregular member: '+n)
    need(stat.S_IMODE(mode) in (0o444,0o644),'file mode: '+n)
    need(s.st_size<=2000000,'oversized member: '+n);files[n]=Path(e.path).read_bytes()
 visit(root,'');return files,dirs
def authenticate(root):
 f,dirs=inventory(root);need('PUBLICATION_MANIFEST.json' in f,'missing manifest')
 need(sha(f['PUBLICATION_MANIFEST.json'])==MANIFEST,'publication manifest trust anchor')
 m=load(f['PUBLICATION_MANIFEST.json']);need(type(m) is dict and set(m)=={'schema','problem_id','rank','status','approaches','files'},'manifest schema')
 for k,v in [('schema','critical-collision-publication-v1'),('problem_id',10800003),('rank',1011),('status','unsolved'),('approaches',5)]:need(type(m[k]) is type(v) and m[k]==v,'manifest identity: '+k)
 need(type(m['files']) is list and bool(m['files']),'manifest files')
 expected={'PUBLICATION_MANIFEST.json','VERIFY_PUBLICATION.py','BOOTSTRAP.py'}
 for e in m['files']:
  need(type(e) is dict and set(e)=={'path','bytes','sha256'},'entry schema');n=e['path']
  need(safe(n) and n not in expected,'unsafe or duplicate member');expected.add(n)
  need(n in f,'missing: '+n)
  need(type(e['bytes']) is int and e['bytes']>=0 and len(f[n])==e['bytes'],'byte count: '+n)
  need(type(e['sha256']) is str and re.fullmatch('[0-9a-f]{64}',e['sha256']) is not None and sha(f[n])==e['sha256'],'hash: '+n)
  if n.endswith('.json'):load(f[n])
 need(set(f)==expected,'file inventory mismatch')
 need(dirs=={str(p) for n in expected for p in PurePosixPath(n).parents if str(p)!='.'},'directory inventory mismatch')
 need(f['VERIFY_PUBLICATION.py']==Path(__file__).read_bytes(),'different verifier copy')
 return f
def inner(f,manifest,prefix,extra=()):
 seen=set(extra);m=load(f[manifest]);need(type(m['files']) is list,'inner files')
 for e in m['files']:
  n=prefix+e['path'];need(safe(n) and n not in seen,'inner path');seen.add(n)
  need(type(e['bytes']) is int and len(f[n])==e['bytes'] and sha(f[n])==e['sha256'],'inner binding')
 need({n for n in f if n.startswith(prefix)}==seen,'inner inventory')
def semantics(f):
 pins={'freeze/AUTHOR_MANIFEST.json':ORIGINAL,'freeze/bootstrap.py':'747e0a67d88e4adb8818077394a132f80b0c8f30ed5c5b1877ea536708ab624f','audit/AUDIT_MANIFEST.json':AUDIT,'audit/corrected/freeze/AUTHOR_MANIFEST.json':CORRECTED,'audit/corrected/freeze/bootstrap.py':'e75b15d966850e2097412032b18c243cd068aa7750d20191121236671802a161','audit/corrected/author/PROOF_AND_STATUS.md':PROOF}
 for n,h in pins.items():need(sha(f[n])==h,'accepted byte pin: '+n)
 inner(f,'freeze/AUTHOR_MANIFEST.json','author/')
 inner(f,'audit/corrected/freeze/AUTHOR_MANIFEST.json','audit/corrected/author/')
 inner(f,'audit/AUDIT_MANIFEST.json','audit/',('audit/AUDIT_MANIFEST.json',))
 inner(f,'VALIDATION_MANIFEST.json','validation/')
 a=load(f['audit/ACCEPTANCE.json']);c=load(f['audit/corrected/author/CLAIMS.json'])
 need(a['disposition']=='ACCEPT_CORRECTED_UNSOLVED_RESEARCH_PACKET' and a['corrections_applied']==3,'audit acceptance')
 need(a['corrected_manifest_sha256']==CORRECTED and a['corrected_bootstrap_sha256']==pins['audit/corrected/freeze/bootstrap.py'],'audit accepted pins')
 for x in (a,c):
  need(type(x['problem_id']) is int and x['problem_id']==10800003 and type(x['rank']) is int and x['rank']==1011,'identity')
  need(type(x['approaches_used']) is int and x['approaches_used']==5,'approaches')
 for k in ['accept_target_resolution','accept_target_counterexample','claim_novelty','formal_verification','human_peer_review']:need(a[k] is False,'audit scope: '+k)
 need(c['status']=='unsolved','corrected disposition')
 for k in ['complete_original_resolution','target_counterexample','novelty_claim','formal_verification_claim','human_peer_review_claim']:need(c[k] is False,'corrected scope: '+k)
 need(len([n for n in f if n.startswith('author/')])==10,'original count')
 need(len([n for n in f if n.startswith('audit/corrected/author/')])==10,'corrected count')
def invoke(root,script,*args):
 flags=[] if sys.flags.optimize==0 else ['-O' if sys.flags.optimize==1 else '-OO']
 r=subprocess.run([sys.executable,'-I','-S','-B',*flags,str(root/script),*map(str,args)],cwd=root,capture_output=True,timeout=240)
 need(r.returncode==0 and not r.stderr,'replay failed '+script+': '+r.stderr.decode('utf8','replace'));return load(r.stdout)
def optional(f,a):
 out={'sources':'NOT_RUN','corpora':'NOT_RUN','fresh_download':'NOT_RUN','fresh_source_inspection':'NOT_RUN','fresh_record_join':'NOT_RUN'}
 def match(p,e):
  need(not p.is_symlink() and stat.S_ISREG(p.stat().st_mode),'optional input must be regular')
  h=hashlib.sha256();size=0
  with p.open('rb') as handle:
   for b in iter(lambda:handle.read(1048576),b''):size+=len(b);h.update(b)
  need(type(e['bytes']) is int and size==e['bytes'] and h.hexdigest()==e['sha256'],'optional byte mismatch')
  return {'bytes':size,'sha256':h.hexdigest()}
 if a.source_dir is not None:
  names={'problem_published':'vassiliev2015-published.pdf','problem_preprint':'vassiliev2015.pdf','quartic_current':'quartic-v12.pdf','j10_current':'j10v5.pdf','parabolic_current':'parabolic-v6.pdf','problem_html':'vassiliev2015.html'}
  out['source_matches']=[{'alias':e['alias'],**match(a.source_dir/names[e['alias']],e)} for e in load(f['audit/corrected/author/SOURCE_METADATA.json'])['sources']]
  need(len(out['source_matches'])==6,'source count');out['sources']='PASS_CURRENT_BYTE_REHASH'
 if a.problems is not None:
  entries=load(f['audit/corrected/author/CORPUS_VERIFICATION.json'])['datasets'];paths={'problems.json':a.problems,'research_results.json':a.research_results}
  out['corpus_matches']=[{'name':e['dataset_name'],**match(paths[e['dataset_name']],e)} for e in entries]
  need(len(out['corpus_matches'])==2,'corpus count');out['corpora']='PASS_CURRENT_BYTE_REHASH'
 return out
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('--integrity-only',action='store_true');p.add_argument('--source-dir',type=Path);p.add_argument('--problems',type=Path);p.add_argument('--research-results',type=Path);a=p.parse_args()
 need((a.problems is None)==(a.research_results is None),'both complete corpus files required')
 need(not a.integrity_only or (a.source_dir is None and a.problems is None),'optional inputs require full replay')
 root=a.root.absolute();before=authenticate(root);semantics(before)
 if a.integrity_only:return {'status':'PASS_PUBLICATION_INTEGRITY','problem_id':10800003}
 need(os.geteuid()==1000,'exact preserved receipt replay requires non-root UID 1000')
 author=invoke(root,'audit/corrected/freeze/bootstrap.py',root/'audit/corrected/author')
 need(author['status']=='PASS' and author['files']==10 and author['manifest_sha256']==CORRECTED,'corrected replay')
 with tempfile.TemporaryDirectory(prefix='critical-collision-publication-') as temp:
  work=Path(temp);copy=work/'packet';shutil.copytree(root,copy)
  for part in ['author','freeze']:
   d=copy/part;d.chmod(0o555)
   for q in d.iterdir():q.chmod(0o444)
  vr=work/'validation.json';ar=work/'audit.json'
  v=invoke(copy,'validation/run_controls.py',vr);r=load(vr.read_bytes())
  need(r==load(before['validation/REPLAY_CONTROLS.json']),'original 120-case receipt differs')
  audit=invoke(copy,'audit/independent_controls.py','--receipt',ar);araw=load(ar.read_bytes())
  historical=load(before['audit/INDEPENDENT_CONTROLS.json'])
  need(araw==historical,'independent audit receipt differs')
  need(v['total_cases']==120 and audit['total_cases']==115 and audit['independent_math']['total']==405,'replay counts')
  need(audit['hostile_sentinels_created']==0 and audit['immutable_bytes_and_modes_preserved'] is True,'audit integrity')
  for part in ['author','freeze']:
   d=copy/part;d.chmod(0o755)
   for q in d.iterdir():q.chmod(0o644)
 inputs=optional(before,a);need(authenticate(root)==before,'publication changed during replay')
 return {'schema':'critical-collision-publication-replay-v1','status':'PASS_CORRECTED_UNSOLVED_REPLAY','problem_id':10800003,'rank':1011,'disposition':'unsolved','approaches':5,'original_cases':120,'independent_cases':115,'independent_exact_checks':405,'author_exact_checks':390,'patch_reconstruction':'PASS','corrected_proof_sha256':PROOF,'optional_inputs':inputs,'formal_verification':False,'human_peer_review':False,'novelty_claim':False,'github_ci':False,'publication_manifest_sha256':MANIFEST}
if __name__=='__main__':
 try:print(json.dumps(main(),sort_keys=True))
 except (Reject,OSError,ValueError,KeyError,TypeError,UnicodeError,subprocess.SubprocessError) as e:
  print('REJECT: '+str(e),file=sys.stderr);sys.exit(1)
