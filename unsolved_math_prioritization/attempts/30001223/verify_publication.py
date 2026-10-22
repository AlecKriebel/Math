#!/usr/bin/env python3
"""Strict publication integrity, immutable archive equality, and actual replay."""
import argparse,hashlib,json,os,stat,subprocess,sys,zipfile
from pathlib import Path
PINS={
 'author':('YOUNG_TOPS_30001223_AUTHOR_SAFE_FREEZE.zip',12753,'e82e3a8349c00e74199090c3463918f5a83b915d85003438fa030adabf797978',8),
 'first_audit':('YOUNG_TOPS_30001223_INDEPENDENT_AUDIT_SAFE.zip',18009,'a795cf78699d7dc0a87bf0b04c15f9ec5f5afb02869ab9cb1432a1824e86c572',11),
 'second_review':('YOUNG_TOPS_30001223_SECOND_ADVERSARIAL_REVIEW_SAFE.zip',16256,'29e1e6af5a33593bab04caf3228e02a76ec2853f19d27303bef42da357e8e4e3',11)}
DIRS={'author','first_audit','second_review','archives'}
ROOT_FILES={'README.md','RESEARCH_LOG.md','CORPUS_VERIFICATION.json','QUEUE_DELTA.json','PUBLICATION_METADATA.json','PUBLICATION_MANIFEST.json','PUBLICATION_TEST_RESULTS.json','verify_publication.py'}
def require(ok,why):
 if not ok:raise ValueError(why)
def digest(b):return hashlib.sha256(b).hexdigest()
def inventory(root):
 require(stat.S_ISDIR(root.lstat().st_mode),'nonregular root')
 files={};dirs=set()
 for current,ds,fs in os.walk(root,followlinks=False):
  for name in ds+fs:
   p=Path(current)/name;rel=p.relative_to(root).as_posix();mode=p.lstat().st_mode
   if stat.S_ISDIR(mode):dirs.add(rel)
   else:
    require(stat.S_ISREG(mode),'nonregular entry: '+rel);files[rel]=p
 require(dirs==DIRS,'directory inventory mismatch')
 require({x for x in files if '/' not in x}==ROOT_FILES,'root inventory mismatch')
 return files

def run(root,path,args=(),optimized=False):
 cmd=[sys.executable,'-I','-B']+(['-O'] if optimized else [])+[str(root/path),*map(str,args)]
 out=subprocess.run(cmd,cwd=root.parent,text=True,capture_output=True,timeout=180)
 require(out.returncode==0,'replay failed: '+path+' '+out.stderr)
 data=json.loads(out.stdout);require(data.get('status')=='PASS','non-PASS result: '+path)
 return data

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--expected-manifest',required=True);ap.add_argument('--integrity-only',action='store_true');a=ap.parse_args()
 root=Path(__file__).absolute().parent;files=inventory(root)
 raw=files['PUBLICATION_MANIFEST.json'].read_bytes();require(digest(raw)==a.expected_manifest,'external manifest pin mismatch')
 m=json.loads(raw);require(set(m)=={'schema','files'} and m['schema']=='young-tops-publication-v1','manifest schema mismatch')
 require(set(m['files'])==set(files)-{'PUBLICATION_MANIFEST.json'},'manifest inventory mismatch')
 for name,meta in m['files'].items():
  require(set(meta)=={'bytes','sha256'},'manifest entry keys')
  b=files[name].read_bytes();require(type(meta['bytes']) is int and len(b)==meta['bytes'],'byte-count mismatch: '+name);require(digest(b)==meta['sha256'],'hash mismatch: '+name)
 for folder,(name,size,sha,count) in PINS.items():
  archive=files['archives/'+name];b=archive.read_bytes();require((len(b),digest(b))==(size,sha),'external archive pin mismatch')
  with zipfile.ZipFile(archive) as z:
   infos=z.infolist();names=[x.filename for x in infos]
   require(len(names)==len(set(names))==count,'archive inventory count')
   require({folder+'/'+n for n in names}=={n for n in files if n.startswith(folder+'/')},'archive member inventory')
   for info in infos:
    require('/' not in info.filename and info.filename not in ('.','..') and not info.is_dir() and stat.S_IFMT(info.external_attr>>16) in (0,stat.S_IFREG),'nonregular archive member')
    require(z.read(info)==files[folder+'/'+info.filename].read_bytes(),'archive/extracted bytes differ')
 report={'status':'PASS','regular_files':len(files),'archive_count':3,'archive_members':30,'integrity_only':a.integrity_only}
 if not a.integrity_only:
  for path in ['author/audit.py','first_audit/audit_gate.py','second_review/verify_second_review.py']:
   run(root,path,optimized=bool(sys.flags.optimize))
  author=root/'archives'/PINS['author'][0];audit=root/'archives'/PINS['first_audit'][0]
  counts=[]
  for optimized in (False,True):
   prior=run(root,'second_review/replay_frozen_inputs.py',[author,audit],optimized)
   cs=prior['checks'];require(len(cs)==8 and all(x['status']=='PASS' for x in cs),'frozen replay outcomes')
   ac=[x['control_count'] for x in cs if x['test']=='author_adversarial_controls'];fc=[x['control_count'] for x in cs if x['test']=='first_audit_adversarial_controls']
   require(ac==[34,34] and fc==[28,28],'prior controls count')
   second=run(root,'second_review/test_second_gate.py',optimized=optimized)
   require(len(second['checks'])==24 and all(x['passed'] is True for x in second['checks']),'second controls count')
   counts.append({'driver_optimized':optimized,'author_controls_per_inner_driver':34,'first_audit_controls_per_inner_driver':28,'second_review_controls':24})
  weights=json.loads(files['second_review/weight_graph_results.json'].read_bytes())
  require(len(weights['family'])==24 and weights['family'][-1]['p']==97,'formal prime support')
  report.update({'three_gates':'PASS','prior_relocation_and_controls':'PASS','controls':counts,'formal_odd_primes':24,'largest_tested_prime':97})
 print(json.dumps(report,sort_keys=True,indent=2))
if __name__=='__main__':
 try:main()
 except (ValueError,TypeError,KeyError,OSError,subprocess.TimeoutExpired,zipfile.BadZipFile) as e:
  print('REJECT: '+str(e),file=sys.stderr);sys.exit(1)
