from pathlib import Path
import datetime,hashlib,json
R=Path(__file__).resolve().parent;M=R/'FREEZE_MANIFEST.json'
def main():
 entries=[]
 for p in sorted(R.iterdir()):
  if p.is_dir():
   if p.name!='scratch_local':raise RuntimeError('Unexpected authored child directory '+p.name)
   continue
  if p==M:continue
  if p.is_symlink():raise RuntimeError('Symlink in authored root')
  b=p.read_bytes();entries.append({'path':p.name,'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()})
 d={'schema':'independent-whole-package-authored-output-freeze-v1','at_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'review':'package_round3','status':'CLEAN','root':str(R),'input_freeze_sha256':hashlib.sha256((R/'INPUT_FREEZE.json').read_bytes()).hexdigest(),'authored_files':entries,'self_exclusion':'FREEZE_MANIFEST.json excludes itself; its exact SHA256 is delivered outside the manifest together with report/verdict digests.','excluded':'Only ignored scratch_local copied inputs/fixtures, third-party bodies, renders, compiled copies. Every root file, including scripts, research log, receipts, supplied .gitignore and INPUT_FREEZE.json, is included.','no_input_changed':True,'external_mutations':False}
 M.write_text(json.dumps(d,indent=2)+'\n')
 for e in entries:
  b=(R/e['path']).read_bytes()
  if len(b)!=e['bytes'] or hashlib.sha256(b).hexdigest()!=e['sha256']:raise RuntimeError('Output changed during seal')
 print(json.dumps({'members':len(entries),'manifest_sha256':hashlib.sha256(M.read_bytes()).hexdigest(),'report_sha256':hashlib.sha256((R/'REPORT.md').read_bytes()).hexdigest(),'verdict_sha256':hashlib.sha256((R/'VERDICT.json').read_bytes()).hexdigest()}))
if __name__=='__main__':main()
