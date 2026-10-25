"""Read-only final audit custody/outcome verifier; no controls or generators run."""
from pathlib import Path
import hashlib,json
E=Path(__file__).resolve().parent
def read(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def matches(p,r):return p.is_file() and p.stat().st_size==r['bytes'] and sha(p)==r['sha256']
def main():
 issues=[];seal=read(E/'FINAL_SEAL.json');manifest=read(E/'FINAL_MANIFEST.json')
 for name,r in seal['bindings'].items():
  if not matches(E/name,r):issues.append('seal:'+name)
 for r in manifest['files']:
  if not matches(E/r['path'],r):issues.append('owned:'+r['path'])
 actual={str(p.relative_to(E)) for p in E.rglob('*') if p.is_file() and 'private' not in p.relative_to(E).parts and p.name not in ['FINAL_MANIFEST.json','FINAL_SEAL.json']}
 if actual!={r['path'] for r in manifest['files']}:issues.append('owned_file_set')
 original=read(E/'preservation-before.json')
 for r in original['files']:
  if not matches(Path(r['path']),r):issues.append('original:'+r['path'])
 controls=read(E/'CHECKER_CONTROLS.json');rows=controls['rows']
 if len(rows)!=68 or any(x['accepted'] is None for x in rows):issues.append('control_count_or_exception')
 false=[]
 for x in rows:
  result=read(E/x['mode']/(x['record']+'-'+x['case']+'.json'))
  if (result['status']=='PASS')!=x['accepted'] or result['issues']!=x['issues']:issues.append('recorded_control:'+str(x))
  if x['case']=='pristine' and not x['accepted']:issues.append('pristine_failed')
  if x['case']!='pristine' and x['accepted']:false.append(x)
 if len(false)!=14 or {x['case'] for x in false}!={'wrong_visible_h1','unapproved_body_claim','Gin_TeX_link_mislabelled'}:issues.append('false_negative_set')
 child=read(E/'schema-lane/SEAL.json')
 for name,r in child['owned_output_bindings'].items():
  if not matches(E/'schema-lane'/name,r):issues.append('child_owned:'+name)
 if sha(E/'schema-lane/SEAL.json')!=(E/'schema-lane/SEAL.sha256').read_text().split()[0]:issues.append('child_detached_seal')
 cc=read(E/'schema-lane/CONTROLS.json')
 if cc['control_count']!=145 or cc['passed']!=145 or cc['failed']:issues.append('child_controls')
 after=read(E/'preservation-after.json')
 if after['issues'] or after['bindings_rehashed']!=1708:issues.append('final_preservation')
 print(json.dumps({'status':'PASS_CUSTODY_AND_RECORDED_FINDINGS' if not issues else 'FAIL','owned_bindings':len(manifest['files']),'original_bindings':len(original['files']),'sealed_stage_files':original['stage_files'],'checker_runs':len(rows),'demonstrated_checker_false_negatives':len(false),'independent_schema_controls':cc['control_count'],'issues':issues,'disposition':'Exact stage content passes; three checker false-negative classes and caller numeric-type equality caveat remain recorded for root; no integration authority.'},indent=2))
 return bool(issues)
if __name__=='__main__':raise SystemExit(main())
