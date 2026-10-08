#!/usr/bin/env python3
"""Publication integrity controls. Authenticate this script before execution."""
from pathlib import Path
import hashlib,importlib.util,json,os,re,shutil,stat,subprocess,sys,tempfile

def need(c,m):
 if not c:raise RuntimeError(m)
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 need(len(sys.argv)==2,'usage: TEST_MUTATIONS.py PACKET');root=Path(sys.argv[1]).absolute();need(os.geteuid()!=0,'non-root required')
 boot=root/'BOOTSTRAP.py';bootpin=sha(boot);text=boot.read_text();vp=re.search("VERIFIER_SHA='([0-9a-f]{64})'",text)[1];mp=re.search("MANIFEST_SHA='([0-9a-f]{64})'",text)[1]
 need(sha(root/'VERIFY_PUBLICATION.py')==vp and sha(root/'PUBLICATION_MANIFEST.json')==mp,'initial anchors')
 spec=importlib.util.spec_from_file_location('trusted_publication',root/'VERIFY_PUBLICATION.py');module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
 module.semantics(module.authenticate(root))
 for raw in [b'{"a":1,"a":2}',b'{"a":NaN}',b'{"a":Infinity}',b'{"a":-Infinity}',b'{"a":1e999}',b'\xff']:
  try:module.load(raw)
  except (ValueError,UnicodeError,module.Reject):pass
  else:raise RuntimeError('strict parser accepted malformed JSON')
 before={str(p.relative_to(root)):sha(p) for p in root.rglob('*') if p.is_file()};cases=[]
 with tempfile.TemporaryDirectory(prefix='critical-publication-controls-') as tmp:
  work=Path(tmp)
  def cp(name):
   d=work/name;shutil.copytree(root,d)
   for p in [d,*d.rglob('*')]:p.chmod(0o755 if p.is_dir() else 0o644)
   return d
  def run(d,flags,extra=()):
   if sha(d/'BOOTSTRAP.py')!=bootpin:return None
   return subprocess.run([sys.executable,'-I','-S','-B',*flags,str(d/'BOOTSTRAP.py'),str(d),*extra],capture_output=True,timeout=300)
  for mode,flags in [('normal',[]),('O',['-O']),('OO',['-OO'])]:
   r=run(root,flags);need(r is not None and r.returncode==0 and not r.stderr,'baseline '+mode);baseline=json.loads(r.stdout)
   cases.append({'mode':mode,'case':'baseline_full_replay','result':'PASS'})
   ro=cp(mode+'-readonly')
   for p in [ro,*ro.rglob('*')]:p.chmod(0o555 if p.is_dir() else 0o444)
   for p,how in [(ro/'new-file','wb'),(ro/'README.md','ab')]:
    try:
     with p.open(how) as h:h.write(b'x')
    except PermissionError:pass
    else:raise RuntimeError('read-only write succeeded')
   r=run(ro,flags);need(r is not None and r.returncode==0 and not r.stderr and json.loads(r.stdout)==baseline,'read-only full replay '+mode)
   cases.append({'mode':mode,'case':'nonroot_readonly_full_replay_create_append_denied','result':'PASS','uid':os.geteuid()})
   for p in [ro,*ro.rglob('*')]:p.chmod(0o755 if p.is_dir() else 0o644)
   for tag in ['missing','extra_file','extra_directory','symlink','fifo','writable','executable','changed_proof','duplicate_manifest','nan_manifest','bad_utf8','forged_manifest','hostile_author','hostile_audit','hostile_wrapper','hostile_bootstrap','extra_import']:
    d=cp(mode+'-'+tag);sentinel=work/(mode+'-'+tag+'-EXECUTED');payload='from pathlib import Path\nPath('+repr(str(sentinel))+').write_text("bad")\n'
    target=d/'audit/corrected/author/PROOF_AND_STATUS.md'
    if tag=='missing':target.unlink()
    elif tag=='extra_file':(d/'extra.txt').write_text('not part of payload')
    elif tag=='extra_directory':(d/'extra').mkdir()
    elif tag=='symlink':target.unlink();target.symlink_to(root/'audit/corrected/author/PROOF_AND_STATUS.md')
    elif tag=='fifo':target.unlink();os.mkfifo(target)
    elif tag=='writable':target.chmod(0o664)
    elif tag=='executable':target.chmod(0o755)
    elif tag=='changed_proof':target.write_text('false proof')
    elif tag=='duplicate_manifest':(d/'PUBLICATION_MANIFEST.json').write_text('{"schema":0,"schema":1}')
    elif tag=='nan_manifest':(d/'PUBLICATION_MANIFEST.json').write_text('{"schema":NaN}')
    elif tag=='bad_utf8':(d/'PUBLICATION_MANIFEST.json').write_bytes(b'\xff')
    elif tag=='forged_manifest':
     target.write_text('false proof');p=d/'PUBLICATION_MANIFEST.json';m=json.loads(p.read_text())
     for e in m['files']:
      if e['path']=='audit/corrected/author/PROOF_AND_STATUS.md':e.update(bytes=target.stat().st_size,sha256=sha(target))
     p.write_text(json.dumps(m))
    elif tag=='extra_import':(d/'sitecustomize.py').write_text(payload)
    else:
     path={'hostile_author':'audit/corrected/author/verify.py','hostile_audit':'audit/independent_controls.py','hostile_wrapper':'VERIFY_PUBLICATION.py','hostile_bootstrap':'BOOTSTRAP.py'}[tag];(d/path).write_text(payload)
    r=run(d,flags,('--integrity-only',));need((r is None or r.returncode!=0) and not sentinel.exists(),'control accepted '+mode+' '+tag)
    cases.append({'mode':mode,'case':tag,'result':'PASS','rejection_layer':'external_bootstrap_pin' if r is None else 'authenticated_boundary'})
   for tag,args in [('incomplete_corpus',['--problems',str(work/'absent')]),('optional_with_integrity',['--integrity-only','--source-dir',str(work/'absent')])]:
    r=run(root,flags,args);need(r is not None and r.returncode!=0,tag);cases.append({'mode':mode,'case':tag,'result':'PASS'})
  after={str(p.relative_to(root)):sha(p) for p in root.rglob('*') if p.is_file()};need(before==after,'original packet changed')
 return {'schema':'critical-collision-publication-controls-v1','status':'PASS','uid':os.geteuid(),'strict_parser_negative_cases':6,'cases':cases,'total_cases':len(cases),'hostile_sentinels_created':0,'packet_unchanged':True,'limits':['Boundary mutations primarily test authenticated byte rejection; independent audit tests semantic mutations separately.','No arbitrary-code sandbox or race-resistance claim.']}
if __name__=='__main__':print(json.dumps(main(),sort_keys=True,indent=2))
