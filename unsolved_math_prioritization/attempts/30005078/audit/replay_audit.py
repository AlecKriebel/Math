"""Replay the frozen author and independent numerical audit without editing inputs.
Usage: python replay_audit.py AUTHOR_SAFE_FREEZE.zip
"""
from pathlib import Path
import hashlib,json,subprocess,sys,tempfile,zipfile

HERE=Path(__file__).resolve().parent

def main():
 archive=Path(sys.argv[1]).resolve(); original=archive.read_bytes()
 assert len(original)==23313 and hashlib.sha256(original).hexdigest()=='fac44aee178ad76fbeb347c1bab796ed5b877a470a4bd69ca63777886dd6012d'
 with tempfile.TemporaryDirectory(prefix='regularity-audit-') as work:
  out=Path(work)
  with zipfile.ZipFile(archive) as z:
   assert hashlib.sha256(z.read('AUTHOR_MANIFEST.json')).hexdigest()=='ac613e4ee58fa4a7fe816e6c67995742af775e09e4bab4a9aa0cf417b02e37b9'
   assert all('/' not in n and '\\' not in n for n in z.namelist())
   z.extractall(out)
  m=json.loads((out/'AUTHOR_MANIFEST.json').read_text())
  def check_original_files():
   for f in m['files']:
    data=(out/f['path']).read_bytes()
    assert len(data)==f['bytes'] and hashlib.sha256(data).hexdigest()==f['sha256']
  check_original_files()
  p=subprocess.run([sys.executable,'test_regularity.py'],cwd=out,text=True,capture_output=True,check=True)
  author=json.loads(p.stdout);check_original_files()
  p=subprocess.run([sys.executable,str(HERE/'independent_checks.py'),str(out)],cwd=out,text=True,capture_output=True,check=True)
  independent=json.loads(p.stdout)
 assert archive.read_bytes()==original
 report={'status':'PASS','author_freeze_unchanged':True,'author_manifest_files_byte_identical_after_replay':True,
         'author_replay':author,'independent_counts':independent['counts'],
         'characteristic_torsion_controls':independent['characteristic_torsion_controls'],
         'general_problem_solved':False,'proof_search_families_used':5,'proof_search_limit':5,
         'verdict':'PASS for scoped results; general finite-presentation module target unresolved'}
 (HERE/'AUDIT_REPLAY.json').write_text(json.dumps(report,indent=2)+'\n')
 print(json.dumps(report,indent=2))

if __name__=='__main__':main()
