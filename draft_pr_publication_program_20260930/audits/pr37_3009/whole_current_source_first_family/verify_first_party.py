#!/usr/bin/env python3
"""Strict recursive self-excluding manifest, plus real private corruption tests.

Default verification writes nothing. --negative-controls-output NEWDIR keeps
every private testcase/stream outside the frozen first-party directory.
"""
from pathlib import Path,PurePosixPath
import argparse,hashlib,json,shutil,subprocess,sys
sys.dont_write_bytecode=True
def rows(root):
 result=[]
 for p in sorted(root.rglob('*')):
  rel=p.relative_to(root)
  if rel.parts[0]=='primary' or '__pycache__'in rel.parts or str(rel)=='FIRST_PARTY_MANIFEST.json':continue
  if p.is_symlink():raise AssertionError('symlink first-party member: '+str(rel))
  if p.is_file():
   b=p.read_bytes();result.append({'path':str(rel),'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
 return result
def verify(root,pin=None):
 p=root/'FIRST_PARTY_MANIFEST.json';assert p.is_file()and not p.is_symlink()
 if pin:assert hashlib.sha256(p.read_bytes()).hexdigest()==pin,'manifest byte pin'
 m=json.loads(p.read_bytes());assert m['self_excluded']==['FIRST_PARTY_MANIFEST.json'];assert m['foreign_excluded_prefixes']==['primary/'];assert m['bytecode_excluded_component']=='__pycache__'
 advertised=m['files'];assert m['files_count']==len(advertised);seen=set()
 for r in advertised:
  q=PurePosixPath(r['path']);assert not q.is_absolute()and '..'not in q.parts and str(q)==r['path']and q.parts[0]!='primary'and r['path']!='FIRST_PARTY_MANIFEST.json'
  assert r['path']not in seen,'duplicate member';seen.add(r['path'])
 assert rows(root)==advertised,'recursive first-party inventory/bytes mismatch'
 return len(advertised)
def main():
 a=argparse.ArgumentParser();a.add_argument('--root',type=Path,default=Path(__file__).resolve().parent);a.add_argument('--manifest-pin');a.add_argument('--negative-controls-output',type=Path);x=a.parse_args();root=x.root.resolve();n=verify(root,x.manifest_pin)
 if x.negative_controls_output:
  out=x.negative_controls_output.resolve();assert not out.exists();out.mkdir(parents=True);cases=[]
  def malformed(d):
   p=d/'FIRST_PARTY_MANIFEST.json';m=json.loads(p.read_bytes());m['files'].append(dict(m['files'][0]));m['files_count']+=1;p.write_text(json.dumps(m))
  frozen=json.loads((root/'FIRST_PARTY_MANIFEST.json').read_bytes())
  for label,edit in [('byte',lambda d:(d/'REPORT.md').write_bytes((d/'REPORT.md').read_bytes()+b'\n')),('missing',lambda d:(d/'REPORT.md').unlink()),('unlisted',lambda d:(d/'nested').mkdir()or(d/'nested/REPORT.md').write_text('unlisted')),('duplicate',malformed)]:
   d=out/label;d.mkdir()
   for r in frozen['files']+[{'path':'FIRST_PARTY_MANIFEST.json'}]:
    dst=d/r['path'];dst.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(root/r['path'],dst)
   edit(d)
   cp=subprocess.run(['/usr/bin/python3',str(d/'verify_first_party.py'),'--root',str(d)],capture_output=True)
   for ch in ['stdout','stderr']:(out/(label+'.'+ch)).write_bytes(getattr(cp,ch))
   assert cp.returncode!=0 and b'AssertionError'in cp.stderr;cases.append({'label':label,'exit':cp.returncode})
   shutil.copy2(d/'FIRST_PARTY_MANIFEST.json',out/(label+'.tested_manifest.json'))
   if (d/'REPORT.md').exists():shutil.copy2(d/'REPORT.md',out/(label+'.tested_report.md'))
   shutil.rmtree(d)
  (out/'RESULT.json').write_text(json.dumps({'baseline_files':n,'all_rejected':True,'cases':cases},indent=2)+'\n')
 print(json.dumps({'verified':True,'files':n,'self_excluding':True}))
if __name__=='__main__':main()
