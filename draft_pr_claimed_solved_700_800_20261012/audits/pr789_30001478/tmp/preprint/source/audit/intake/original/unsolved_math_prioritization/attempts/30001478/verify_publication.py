#!/usr/bin/env python3
"""Verify invocation path, externally pinned inventory, frozen bytes, then replay."""
import argparse,hashlib,json,os,stat,subprocess,sys,zipfile
from pathlib import Path,PurePosixPath
PINS={
'author':('PRIME_IDEALS_30001478_AUTHOR_SAFE_FREEZE.zip',13202,'018f641c1425c6cb28e09b5cf8cc17a0848f928bdd3f37ea57e64c7a70f6d0a9',9),
'first_audit':('PRIME_IDEALS_30001478_INDEPENDENT_AUDIT_SAFE.zip',30566,'075159f6da95ded37cbeb3aab31aa8cd26a441b3e2e1f53e18fcd1a41f0d8ae6',22),
'second_review':('PRIME_IDEALS_30001478_SECOND_ADVERSARIAL_REVIEW_SAFE.zip',19255,'7fdefb9a9b5560d871429e08f029fde389b16b175098659152985940f15faac1',13)}
DIRS={'archives','author','first_audit','first_audit/author','second_review'}
ROOT_FILES={'README.md','RESEARCH_LOG.md','SOURCE_CORPUS_CHECKS.json','QUEUE_DELTA.json','PUBLICATION_METADATA.json','PUBLICATION_MANIFEST.json','PUBLICATION_TEST_RESULTS.json','PATH_PATCH_TEST_RESULTS.json','verify_publication.py','test_publication.py','test_path_patch.py'}
def need(ok,msg):
 if not ok:raise ValueError(msg)
def digest(b):return hashlib.sha256(b).hexdigest()
def unique(pairs):
 out={}
 for k,v in pairs:
  need(k not in out,'duplicate JSON key: '+k);out[k]=v
 return out
def js(b):return json.loads(b,object_pairs_hook=unique)
def inventory(root):
 # Do not resolve: preserve and reject every symlink component before reads.
 for p in [root,*root.parents]:need(stat.S_ISDIR(p.lstat().st_mode),'nonregular invocation ancestry')
 files={};dirs=set()
 for current,ds,fs in os.walk(root,followlinks=False):
  for name in ds+fs:
   p=Path(current)/name;rel=p.relative_to(root).as_posix();mode=p.lstat().st_mode
   if stat.S_ISDIR(mode):dirs.add(rel)
   else:need(stat.S_ISREG(mode),'nonregular entry: '+rel);files[rel]=p
 need(dirs==DIRS,'directory inventory mismatch')
 need({n for n in files if '/' not in n}==ROOT_FILES,'root inventory mismatch')
 return files

def execute(root,path,optimized=False):
 p=subprocess.run([sys.executable,'-I','-B']+(['-O'] if optimized else [])+[str(root/path)],cwd=root.parent,capture_output=True,text=True,timeout=240)
 need(p.returncode==0,'replay failure: '+path+' '+p.stderr);out=js(p.stdout);need(out.get('status')=='PASS','non-PASS '+path);return out

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--expected-manifest',required=True);ap.add_argument('--integrity-only',action='store_true');a=ap.parse_args()
 root=Path(__file__).absolute().parent;files=inventory(root)
 raw=files['PUBLICATION_MANIFEST.json'].read_bytes();need(digest(raw)==a.expected_manifest,'external manifest pin mismatch');m=js(raw)
 need(set(m)=={'schema','files'} and m['schema']=='prime-quotient-publication-v1','manifest schema')
 need(set(m['files'])==set(files)-{'PUBLICATION_MANIFEST.json'},'manifest inventory mismatch')
 for name,meta in m['files'].items():
  need(set(meta)=={'bytes','sha256'} and type(meta['bytes']) is int,'manifest entry schema');b=files[name].read_bytes();need((len(b),digest(b))==(meta['bytes'],meta['sha256']),'manifest content mismatch: '+name)
 for folder,(name,size,sha,count) in PINS.items():
  b=files['archives/'+name].read_bytes();need((len(b),digest(b))==(size,sha),'immutable archive pin mismatch')
  with zipfile.ZipFile(files['archives/'+name]) as z:
   infos=z.infolist();names=[i.filename for i in infos];need(len(names)==len(set(names))==count,'archive count')
   need({folder+'/'+n for n in names}=={n for n in files if n.startswith(folder+'/')},'archive inventory mismatch')
   for info in infos:
    p=PurePosixPath(info.filename);need(not p.is_absolute() and '..' not in p.parts and str(p)==info.filename and not info.is_dir() and stat.S_IFMT(info.external_attr>>16) in (0,stat.S_IFREG),'unsafe archive entry')
    need(z.read(info)==files[folder+'/'+info.filename].read_bytes(),'frozen member mismatch: '+folder+'/'+info.filename)
 out={'status':'PASS','regular_files':len(files),'immutable_archives':3,'immutable_archive_members':44,'strict_path_inventory_before_execution':True,'integrity_only':a.integrity_only}
 if not a.integrity_only:
  for path in ['author/verify.py','first_audit/verify_audit.py','second_review/verify_review.py']:
   normal=execute(root,path);optimized=execute(root,path,True);need(normal==optimized,'optimized gate mismatch')
  controls=[]
  for path,key,count in [('author/test_suite.py','test_count',47),('first_audit/test_audit.py','named_test_count',16),('second_review/test_review.py','named_test_count',20)]:
   normal=execute(root,path);optimized=execute(root,path,True);need(normal==optimized and normal[key]==count,'suite output/count mismatch: '+path);controls.append({'suite':path,'named_controls':count,'normal_optimized_agree':True})
  patch=execute(root,'test_path_patch.py',bool(sys.flags.optimize));need(patch==js(files['PATH_PATCH_TEST_RESULTS.json'].read_bytes()),'patch saved output mismatch')
  out.update({'three_gates_normal_optimized':'PASS','control_suites':controls,'actual_ephemeral_patch_test':'PASS'})
 print(json.dumps(out,sort_keys=True,indent=2))
if __name__=='__main__':
 try:main()
 except Exception as e:print('REJECT: '+str(e),file=sys.stderr);sys.exit(1)
