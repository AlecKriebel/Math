#!/usr/bin/env python3
"""Bounded adversarial wrapper tests. Not mathematical validation."""
import hashlib,json,pathlib,shutil,subprocess,sys,tempfile
ROOT=pathlib.Path(__file__).absolute().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def need(c,m):
 if not c:raise ValueError(m)
def resign(p):
 m=json.loads((p/'PUBLICATION_MANIFEST.json').read_bytes())
 for e in m['files']:
  f=p/e['path'];e['bytes']=f.stat().st_size;e['sha256']=sha(f.read_bytes())
 (p/'PUBLICATION_MANIFEST.json').write_text(json.dumps(m,indent=2)+'\n')
def main():
 rows=[]
 with tempfile.TemporaryDirectory(prefix='quadratic wrapper tests ') as td:
  td=pathlib.Path(td)
  def case(name,change=None,flags=(),expected=2,anchor_override=None):
   p=td/name;shutil.copytree(ROOT,p)
   if change:change(p)
   anchor=anchor_override or sha((p/'PUBLICATION_MANIFEST.json').read_bytes())
   r=subprocess.run([sys.executable,'-I','-S','-B',*flags,str(p/'verify_publication.py'),'--expected-manifest',anchor],cwd=td,capture_output=True,text=True,timeout=180)
   rows.append({'test':name,'expected_exit':expected,'exit_code':r.returncode});need(r.returncode==expected,name+': '+r.stderr)
  case('relocated normal with spaces',expected=0)
  case('optimized rejection',flags=('-O',),expected=1)
  case('doubly optimized rejection',flags=('-OO',),expected=1)
  case('wrong anchor',anchor_override='0'*64)
  case('missing member',lambda p:(p/'corrected/README.md').unlink())
  case('unexpected member',lambda p:(p/'unexpected').write_text('x'))
  case('unexpected directory',lambda p:(p/'unexpected').mkdir())
  def mutate(p):
   f=p/'corrected/PROOF.md';b=f.read_bytes();f.write_bytes(bytes([b[0]^1])+b[1:])
  case('same-size member mutation',mutate)
  def symlink(p):
   f=p/'corrected/PROOF.md';f.unlink();f.symlink_to(ROOT/'corrected/PROOF.md')
  case('symlink member',symlink)
  def symlinkmf(p):
   f=p/'PUBLICATION_MANIFEST.json';f.unlink();f.symlink_to(ROOT/'PUBLICATION_MANIFEST.json')
  case('symlink manifest',symlinkmf)
  def dup(p):
   f=p/'PUBLICATION_MANIFEST.json';f.write_text(f.read_text().replace('"problem_id": 2931','"problem_id": 2931, "problem_id": 2931',1))
  case('duplicate manifest key',dup)
  def nonfinite(p):
   f=p/'PUBLICATION_MANIFEST.json';f.write_text(f.read_text().replace('"problem_id": 2931','"problem_id": NaN',1))
  case('nonfinite JSON',nonfinite)
  def boolean(p):
   f=p/'PUBLICATION_MANIFEST.json';m=json.loads(f.read_bytes());m['files'][0]['bytes']=True;f.write_text(json.dumps(m))
  case('boolean byte count',boolean)
  def traversal(p):
   f=p/'PUBLICATION_MANIFEST.json';m=json.loads(f.read_bytes());m['files'][0]['path']='../outside';f.write_text(json.dumps(m))
  case('manifest traversal path',traversal)
  def tamperpin(p):
   f=p/'audit/CORRECTIONS.patch';f.write_bytes(f.read_bytes()+b'\n');resign(p)
  case('reanchored frozen patch tamper',tamperpin)
  def claim(p):
   f=p/'PUBLICATION_METADATA.json';m=json.loads(f.read_bytes());m['full_solution']=True;f.write_text(json.dumps(m));resign(p)
  case('reanchored solution scope tamper',claim)
  def provenance(p):
   f=p/'audit/EXACT_ACCEPTANCE.json';m=json.loads(f.read_bytes());m['human_peer_review_performed']=True;f.write_text(json.dumps(m));resign(p)
  case('reanchored review provenance tamper',provenance)
  def extracted(p):mutate(p);resign(p)
  case('reanchored extracted member mismatch',extracted)
 print(json.dumps({'result':'pass','test_count':len(rows),'all_expected_exits':True,'tests':rows,'mathematical_validation':False},indent=2))
if __name__=='__main__':main()
