"""Read-only custody/scope checker for round03; not a formal proof or priority oracle."""
from pathlib import Path,PurePosixPath
import argparse,hashlib,json,os,stat,subprocess,sys
SOURCE_PIN='50baca75de83bb4959f52b88762b020a65181428d200dffc4f343db8e026f9de'
SOURCE_CHECKER='700eaab42e6d98589fb2f1c6fa4a3077b4dd74cad4f336a00cb53bd6dfe47489'
HEAD='aa44dec3baf8c1cd179cf8b55f32be95c74ee81a'
def need(v,m):
 if not v:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def strict(b):
 def pairs(items):
  out={}
  for k,v in items:
   need(k not in out,'duplicate JSON key');out[k]=v
  return out
 def bad(v):raise ValueError('nonfinite JSON')
 return json.loads(b,object_pairs_hook=pairs,parse_constant=bad)
def safe(n):
 need(type(n)is str and n and '\\'not in n,'invalid path')
 p=PurePosixPath(n)
 need(not p.is_absolute() and str(p)==n and all(c not in ('','.','..') for c in n.split('/')),'unsafe relative path')
 return n
def absolute(p):return Path(os.path.abspath(os.fspath(p)))
def ancestry(p):
 p=absolute(p)
 for q in [p,*p.parents]:need(stat.S_ISDIR(q.lstat().st_mode),'directory or ancestor symlink/non-directory')
 return p
def read(p):
 p=absolute(p);ancestry(p.parent);before=p.lstat()
 need(stat.S_ISREG(before.st_mode)and before.st_nlink==1,'not singly linked regular input')
 fd=os.open(p,os.O_RDONLY|os.O_NONBLOCK|os.O_NOFOLLOW)
 with os.fdopen(fd,'rb')as stream:
  opened=os.fstat(stream.fileno())
  need((opened.st_dev,opened.st_ino)==(before.st_dev,before.st_ino),'changed before open')
  data=stream.read();after=os.fstat(stream.fileno())
 need((before.st_ino,before.st_size,before.st_mtime_ns)==(after.st_ino,after.st_size,after.st_mtime_ns)and len(data)==before.st_size,'changed during read')
 return data
def rows(root,records):
 ancestry(root);out={}
 need(type(records)is list,'records not list')
 for r in records:
  need(set(r)=={'path','bytes','sha256'},'row schema')
  n=safe(r['path']);need(n not in out,'duplicate row')
  need(type(r['bytes'])is int and r['bytes']>=0,'invalid size')
  h=r['sha256'];need(type(h)is str and len(h)==64 and all(c in '0123456789abcdef' for c in h),'invalid digest')
  data=read(root/n);need(len(data)==r['bytes']and sha(data)==h,'bound bytes differ: '+n);out[n]=data
 return out
def closed(root,files):
 observed=set();directories=set()
 for base,ds,fs in os.walk(root,followlinks=False):
  for n in ds+fs:
   p=Path(base)/n;st=p.lstat();rel=p.relative_to(root).as_posix()
   if stat.S_ISDIR(st.st_mode):directories.add(rel)
   else:
    need(stat.S_ISREG(st.st_mode)and st.st_nlink==1,'nonregular/linked entry');observed.add(rel)
 expected_dirs={str(p) for n in files for p in PurePosixPath(n).parents if str(p)!='.'}
 need(observed==set(files)and directories==expected_dirs,'closed inventory differs')
def verify(a):
 root=ancestry(a.packet_root);invocation=absolute(__file__)
 need(invocation==root/'verify_review.py','entrypoint/root mismatch')
 need(sha(read(invocation))==a.expected_checker_sha256,'external checker pin')
 raw=read(root/'MANIFEST.json');need(sha(raw)==a.expected_manifest_sha256,'external manifest pin')
 mf=strict(raw);need(set(mf)=={'schema','problem','pr','files'}and mf['schema']=='pr789-whole-preprint-round03/v1'and mf['problem']==30001478 and mf['pr']==789,'review manifest target')
 data=rows(root,mf['files']);need('MANIFEST.json'not in data,'self manifest');closed(root,set(data)|{'MANIFEST.json'})
 v=strict(data['VERDICT.json'])
 need(v['verdict']=='PASS_NO_REQUIRED_REPAIRS'and v['actionable_findings']==[],'verdict scope')
 need(v['severity_counts']=={'critical':0,'high':0,'medium':0,'low':0}and v['completion_percent']==100,'count/completion scope')
 need(v['historical_priority']=='UNRESOLVED'and v['firstness_certified']is False and v['exhaustive_absence_certified']is False and v['current_worldwide_open_certified']is False,'unsupported priority promotion')
 need(v['candidate_head']==HEAD and v['source_manifest_sha256']==SOURCE_PIN,'target binding')
 source=ancestry(a.source_root);release=ancestry(a.release_root)
 need(sha(read(source/'MANIFEST.json'))==SOURCE_PIN and sha(read(source/'verify_source.py'))==SOURCE_CHECKER,'source external pins')
 bindings=strict(data['INPUT_VERIFICATION.json']);source_files=rows(source,bindings['source_inventory']);closed(source,source_files)
 need(len(source_files)==151,'source count')
 release_files=rows(release,bindings['release_files']);need(len(release_files)==6,'distribution count')
 for name in ['CORE_0_normal','CORE_0_O','CORE_1_normal','CORE_1_O','OPTIONAL_BODIES']:
  result=strict(data[name+'.json']);need(result['returncode']==0 and result['stderr']=='','core execution failed')
  output=strict(result['stdout']);need(output['result']=='PASS'and output['source_files']==151 and output['original_files']==58,'core output')
  need(output['external_evidence_files_rehashed']==(139 if name=='OPTIONAL_BODIES'else 0),'body count scope')
 need(strict(data['PACKAGE_CONTROLS.json'])['negative_control_count']==19,'package controls')
 need(strict(data['REPRODUCTION.json'])['result']=='PASS','reproduction')
 pdf=strict(data['PDF_REVIEW.json']);need(pdf['frozen_pages']==pdf['fresh_pages']==4 and pdf['visual_findings']==[]and pdf['extracted_text_identical']is True,'PDF scope')
 primary=0
 if a.primary_root:
  bank=ancestry(a.primary_root);primary=len(rows(bank,strict(data['PRIMARY_BINDINGS.json'])['files']))
 replay=False
 if a.replay:
  p=subprocess.run([sys.executable,'-I','-B']+(['-O']if sys.flags.optimize else[])+[str(root/'check_math.py')],cwd='/',capture_output=True,text=True,timeout=30)
  need(p.returncode==0 and not p.stderr and strict(p.stdout)==strict(data['MATH_RESULTS.json']),'independent math replay');replay=True
 # Recheck authenticated packet bytes after optional execution.
 rows(root,mf['files']);closed(root,set(data)|{'MANIFEST.json'})
 return {'result':'PASS','problem':30001478,'pr':789,'review_files':len(data)+1,'source_files':151,'original_files':58,'distribution_files':6,'fresh_primary_files_rehashed':primary,'independent_math_replayed':replay,'actionable_findings':0,'priority':'UNRESOLVED','scope':'Read-only static custody, recorded execution evidence, and optional exact math diagnostics; not formal proof, firstness, exhaustive search, or race-free filesystem certification.'}
def main():
 p=argparse.ArgumentParser(description=__doc__)
 for n in ('packet-root','expected-manifest-sha256','expected-checker-sha256','source-root','release-root'):p.add_argument('--'+n,required=True)
 p.add_argument('--primary-root');p.add_argument('--replay',action='store_true');a=p.parse_args()
 try:r=verify(a)
 except Exception as e:print(json.dumps({'result':'FAIL','error':str(e)},sort_keys=True));return 1
 print(json.dumps(r,indent=2,sort_keys=True));return 0
if __name__=='__main__':raise SystemExit(main())
