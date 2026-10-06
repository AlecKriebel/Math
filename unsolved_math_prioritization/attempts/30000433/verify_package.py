#!/usr/bin/env python3
"""Pinned publication replay; A1 is mandatory, and immutable freezes stay unchanged."""
import argparse,hashlib,json,pathlib,subprocess,sys,zipfile
ROOT=pathlib.Path(__file__).resolve().parent
ARCHIVES={
 'author':('EDGE_DEGREE_30000433_AUTHOR_SAFE_FREEZE.zip',21187,'b64c3b92a96f180b51d22ddd343e9458fc7181f7d8117d5117a4b6a7215dcdf7','ac8006591dde3c8d85cbf2bc47dcb375f7b572107c159bc9a4118e16b8ed0873'),
 'audit':('EDGE_DEGREE_30000433_INDEPENDENT_AUDIT_SAFE.zip',21573,'01d37b0a09da4e568444a3121dd103c773a06ae656333b3d3c8cfc8d6c77de6f','bf2ac5ab05d4235f6a1bf815b14ab438eac2f3b623cf2670bd062b736669b5db')}
def need(c,m):
 if not c: raise ValueError(m)
def digest(b): return hashlib.sha256(b).hexdigest()
def files(root): return {str(p.relative_to(root)) for p in root.rglob('*') if p.is_file() and '__pycache__' not in p.parts}
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--manifest-sha256',required=True);ap.add_argument('--integrity-only',action='store_true');args=ap.parse_args()
 raw=(ROOT/'PUBLICATION_MANIFEST.json').read_bytes();need(digest(raw)==args.manifest_sha256,'publication manifest anchor mismatch');m=json.loads(raw)
 need(files(ROOT)==set(m['files'])|{'PUBLICATION_MANIFEST.json'},'publication inventory mismatch')
 for n,x in m['files'].items():
  p=ROOT/n;need(not p.is_symlink(),'symlink forbidden');b=p.read_bytes();need(len(b)==x['bytes'] and digest(b)==x['sha256'],'publication member mismatch: '+n)
 archives={}
 for folder,(name,size,pin,mpin) in ARCHIVES.items():
  p=ROOT/'archives'/name;b=p.read_bytes();need(len(b)==size and digest(b)==pin,'archive mismatch: '+folder)
  with zipfile.ZipFile(p) as z:
   names=z.namelist();need(len(set(names))==len(names),'duplicate archive member');need(all('/' not in n and '\\' not in n and n not in ('.','..') for n in names),'unsafe archive name');need(files(ROOT/folder)==set(names),'extracted inventory mismatch')
   manifest=z.read('MANIFEST.json');need(digest(manifest)==mpin,'frozen manifest mismatch');memb=json.loads(manifest)['files'];need(set(names)==set(memb)|{'MANIFEST.json'},'frozen inventory mismatch')
   for n in names:
    b=z.read(n);need((ROOT/folder/n).read_bytes()==b,'extracted bytes differ: '+folder+'/'+n)
    if n in memb:need(len(b)==memb[n]['bytes'] and digest(b)==memb[n]['sha256'],'frozen member mismatch')
   archives[folder]={'bytes':size,'sha256':pin,'members':len(names),'extracted_bytes_match':True}
 need((ROOT/'audit/CORRECTION.md').is_file() and (ROOT/'audit/verify_quotient_guard.patch').is_file(),'A1 missing')
 verdict=json.loads((ROOT/'VERDICT.json').read_text());need(verdict['audit_verdict']=='accept_scoped_partial_with_A1_supplement' and verdict['full_source_solved'] is False and verdict['approaches_used']==4,'verdict drift')
 result={'schema':1,'problem_id':30000433,'status':'pass','full_source_solved':False,'approaches_used':4,'archives':archives,'A1_mandatory':True}
 if not args.integrity_only:
  cmd=[sys.executable]+(['-O'] if sys.flags.optimize else [])+[str(ROOT/'audit/audit_replay.py'),str(ROOT/'archives'/ARCHIVES['author'][0])]
  r=subprocess.run(cmd,cwd=ROOT.parent,capture_output=True,text=True,timeout=900);need(r.returncode==0,'audit replay failed: '+r.stderr);a=json.loads(r.stdout)
  expected=json.loads((ROOT/'audit/AUDIT_REPLAY_NORMAL.json').read_text());need(a==expected,'audit replay output drift');result['audit_replay']=a
 print(json.dumps(result,sort_keys=True,indent=2))
if __name__=='__main__':
 try:main()
 except Exception as e:print('FAIL: '+str(e),file=sys.stderr);sys.exit(1)
