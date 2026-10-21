#!/usr/bin/env python3
"""Publication wrapper controls; all mutations remain in disposable copies."""
import argparse,hashlib,json,os,shutil,subprocess,sys,tempfile
from pathlib import Path
def need(ok,msg):
 if not ok:raise ValueError(msg)
def pin(root):return hashlib.sha256((root/'PUBLICATION_MANIFEST.json').read_bytes()).hexdigest()
def run(root,expected,opt=False,entry='verify_publication.py',integrity=True):
 return subprocess.run([sys.executable,'-I','-B']+(['-O'] if opt else [])+[str(root/entry),'--expected-manifest',expected]+(['--integrity-only'] if integrity else []),cwd=root.parent,text=True,capture_output=True,timeout=480)
def rehash(root):
 p=root/'PUBLICATION_MANIFEST.json';m=json.loads(p.read_text())
 for n in m['files']:
  b=(root/n).read_bytes();m['files'][n]={'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
 p.write_text(json.dumps(m,sort_keys=True,indent=2)+'\n')
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--expected-manifest',required=True);ap.add_argument('--full-relocation',action='store_true');a=ap.parse_args();root=Path(__file__).absolute().parent;expected=a.expected_manifest;tests=[]
 for opt in (False,True):
  p=run(root,expected,opt);need(p.returncode==0,'baseline '+p.stderr)
 tests.append('normal_optimized_integrity_baseline')
 with tempfile.TemporaryDirectory(prefix='prime publication controls ') as d:
  t=Path(d);rel=t/'relocated tree with spaces';shutil.copytree(root,rel)
  for opt in (False,True):
   p=run(rel,expected,opt,integrity=not a.full_relocation);need(p.returncode==0,'relocation '+p.stderr)
  tests.append('normal_optimized_relocation')
  for kind in ['extra_file','extra_directory','bytecode','nested_bytecode','missing_file','unrehashed_edit','fifo','symlink_document','symlink_wrapper','symlink_author_verifier','symlink_audit_verifier','symlink_nested_author_verifier','symlink_review_verifier','symlink_directory','wrong_manifest_pin','duplicate_manifest_key','extra_manifest_key','corrupt_archive','rehash_source_metadata','rehash_source_corpus_metadata']:
   w=t/kind;shutil.copytree(root,w);used=expected
   if kind=='extra_file':(w/'extra.txt').write_text('extra')
   elif kind=='extra_directory':(w/'extra').mkdir()
   elif kind=='bytecode':(w/'__pycache__').mkdir()
   elif kind=='nested_bytecode':(w/'first_audit/author/__pycache__').mkdir()
   elif kind=='missing_file':(w/'README.md').unlink()
   elif kind=='unrehashed_edit':(w/'README.md').write_text('edited')
   elif kind=='fifo':(w/'README.md').unlink();os.mkfifo(w/'README.md')
   elif kind.startswith('symlink_'):
    target={'symlink_document':'README.md','symlink_wrapper':'verify_publication.py','symlink_author_verifier':'author/verify.py','symlink_audit_verifier':'first_audit/verify_audit.py','symlink_nested_author_verifier':'first_audit/author/verify.py','symlink_review_verifier':'second_review/verify_review.py','symlink_directory':'author'}[kind]
    p=w/target
    if p.is_dir():shutil.rmtree(p)
    else:p.unlink()
    p.symlink_to(root/target,target_is_directory=kind=='symlink_directory')
   elif kind=='wrong_manifest_pin':used='0'*64
   elif kind=='duplicate_manifest_key':
    p=w/'PUBLICATION_MANIFEST.json';p.write_text(p.read_text().replace('"schema": "prime-quotient-publication-v1"','"schema": "prime-quotient-publication-v1", "schema": "prime-quotient-publication-v1"'));used=pin(w)
   elif kind=='extra_manifest_key':
    p=w/'PUBLICATION_MANIFEST.json';m=json.loads(p.read_text());m['extra']=True;p.write_text(json.dumps(m));used=pin(w)
   elif kind=='corrupt_archive':
    p=next((w/'archives').iterdir());b=p.read_bytes();p.write_bytes(b[:-1]+bytes([b[-1]^1]));rehash(w);used=pin(w)
   elif kind=='rehash_source_metadata':
    p=w/'second_review/source_verification.json';m=json.loads(p.read_text());m['source_display_matches_author_certificate']=False;p.write_text(json.dumps(m));rehash(w);used=pin(w)
   elif kind=='rehash_source_corpus_metadata':
    p=w/'author/provenance.json';m=json.loads(p.read_text());m['review_pair']['sha256']='0'*64;p.write_text(json.dumps(m));rehash(w);used=pin(w)
   for opt in (False,True):
    p=run(w,used,opt);need(p.returncode!=0 and 'REJECT:' in p.stderr,'accepted malformed tree: '+kind)
   tests.append(kind)
  for kind in ['root_symlink','ancestor_symlink']:
   if kind=='root_symlink':w=t/'root link';w.symlink_to(root,target_is_directory=True)
   else:
    parent=t/'ordinary parent';parent.mkdir();shutil.copytree(root,parent/'package');link=t/'ancestor link';link.symlink_to(parent,target_is_directory=True);w=link/'package'
   for opt in (False,True):
    p=run(w,expected,opt);need(p.returncode!=0 and 'nonregular invocation ancestry' in p.stderr,'accepted '+kind)
   tests.append(kind)
 print(json.dumps({'status':'PASS','named_control_count':len(tests),'tests':tests,'all_controls_normal_and_optimized':True,'relocation_full_replay':a.full_relocation},sort_keys=True,indent=2))
if __name__=='__main__':
 try:main()
 except Exception as e:print('FAIL: '+str(e),file=sys.stderr);sys.exit(1)
