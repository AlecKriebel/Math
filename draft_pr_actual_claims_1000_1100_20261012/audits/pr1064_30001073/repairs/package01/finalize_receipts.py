#!/usr/bin/env python3
"""Check bounded mutation/protected bytes, then issue noncircular current pins."""
from pathlib import Path
import datetime,hashlib,json,zipfile
from resolve_preparation_stage import resolve
HERE=Path(__file__).resolve().parent;AUDIT=HERE.parent.parent;PACKAGE=AUDIT/'preprint_v1_0'
ALLOWED={'build_pdf.py','verify_package.py','README.md','COPY_MAP.json','SAFE_INPUT_PINS.json','EXCLUSION_LEDGER.json','SUPPORT_ALLOWLIST.json','SUPPORT_MANIFEST.json','support.zip','publication/DEPOSIT_BINDING.json'}
def require(c,m):
 if not c:raise ValueError(m)
def sha(data):return hashlib.sha256(data).hexdigest()
def record(path,root):
 data=path.read_bytes();return {'path':path.relative_to(root).as_posix(),'bytes':len(data),'sha256':sha(data)}
def match(path,r):return path.is_file() and not path.is_symlink() and path.stat().st_size==r['bytes'] and sha(path.read_bytes())==r['sha256']
def write(name,data):(HERE/name).write_text(json.dumps(data,indent=2)+'\n')
def main():
 utc=datetime.datetime.now(datetime.timezone.utc).isoformat()
 inputs=json.loads((HERE/'INPUT_PINS.json').read_text())['records'];changed=[];unchanged=[]
 for r in inputs:
  path=AUDIT/r['path']
  if match(path,r):unchanged.append(r)
  else:
   require(r['path'].startswith('preprint_v1_0/') and r['path'][len('preprint_v1_0/'):] in ALLOWED,'unexpected protected mutation '+r['path'])
   preserved=HERE/'before'/r['path'];require(match(preserved,r),'old bytes not preserved '+r['path'])
   changed.append({'path':r['path'],'before':r,'after':record(path,AUDIT),'preserved_path':preserved.relative_to(AUDIT).as_posix()})
 require({r['path'][len('preprint_v1_0/'):] for r in changed}==ALLOWED,'unexpected change inventory')
 before=json.loads((HERE/'BEFORE_PINS.json').read_text())['entries']
 for r in before:require(match(HERE/r['preserved_path'],r),'before-file mismatch '+r['preserved_path'])
 original_seal=json.loads((PACKAGE/'OUTPUT_PINS.json').read_text())
 require(len(original_seal['entries'])==103,'old output count changed')
 for r in original_seal['entries']:resolve(r)
 original_inputs=json.loads((PACKAGE/'INPUT_PINS.json').read_text())['records']
 for r in original_inputs:require(match(AUDIT/r['path'],r),'preparation input changed '+r['path'])
 copies=json.loads((PACKAGE/'COPY_MAP.json').read_text())['copies'];oldcopies=json.loads((HERE/'before/preprint_v1_0/COPY_MAP.json').read_text())['copies']
 require(len(oldcopies)==72 and copies[:72]==oldcopies,'old 72 copy records changed')
 require(len(copies)==91,'current copy count wrong')
 for r in copies:
  require(match(AUDIT/r['source_path'],r) and match(PACKAGE/r['package_path'],r),'source/copy mismatch '+r['source_path'])
 require(json.loads((PACKAGE/'SAFE_INPUT_PINS.json').read_text())['records']==copies,'safe copy pins differ')
 review_seal=json.loads((AUDIT/'reviews/package_01/OUTPUT_PINS.json').read_text())
 require(len(review_seal['entries'])==17,'old review count changed')
 for r in review_seal['entries']:require(match(AUDIT/'reviews/package_01'/r['path'],r),'review01 output changed')
 require(sum(r['source_path'].startswith('submitted/') for r in copies)==9,'original count wrong')
 protected_names=['paper.tex','paper.pdf','metadata.json','publication/release_metadata.json','publication/zenodo.json','STATUS.json','OUTPUT_PINS.json','FINAL_VERIFICATION.json','PREPARATION_REPORT.md','fresh_guard_checker.py','run_checks.py','build_archive.py','ATTRIBUTION.md','SOURCE_LEDGER.json','LICENSE.txt']
 lookup={r['path']:r for r in inputs}
 protected=[lookup['preprint_v1_0/'+n] for n in protected_names]
 for r in protected:require(match(AUDIT/r['path'],r),'explicit protected mismatch')
 meta=json.loads((PACKAGE/'metadata.json').read_text())
 require(all(json.loads((PACKAGE/n).read_text())['metadata']==meta for n in ['publication/release_metadata.json','publication/zenodo.json']),'normalized metadata differ')
 allow=json.loads((PACKAGE/'SUPPORT_ALLOWLIST.json').read_text())['members']
 require(len(allow)==117 and allow==sorted(set(allow)),'allowlist members wrong')
 manifest=json.loads((PACKAGE/'SUPPORT_MANIFEST.json').read_text())
 require([r['path'] for r in manifest['entries']]==[n for n in allow if n!='SUPPORT_MANIFEST.json'],'manifest coverage wrong')
 for r in manifest['entries']:require(match(PACKAGE/r['path'],r),'manifest pin mismatch')
 for n in allow:
  require((PACKAGE/n).is_file() and not (PACKAGE/n).is_symlink(),'nonregular allowlist')
  if n!='paper.pdf':(PACKAGE/n).read_bytes().decode('utf-8')
 require('publication/DEPOSIT_BINDING.json' not in allow,'binding included in ZIP')
 with zipfile.ZipFile(PACKAGE/'support.zip') as z:
  infos=z.infolist();require([i.filename for i in infos]==allow,'ZIP members wrong')
  for i in infos:
   require(i.create_system==3 and i.external_attr==0o100644<<16 and i.date_time==(2026,10,14,0,0,0) and i.compress_type==zipfile.ZIP_DEFLATED and not i.flag_bits&1,'ZIP attributes wrong')
   require(z.read(i)==(PACKAGE/i.filename).read_bytes(),'ZIP bytes differ')
 binding=json.loads((PACKAGE/'publication/DEPOSIT_BINDING.json').read_text())
 oldbinding=json.loads((HERE/'before/preprint_v1_0/publication/DEPOSIT_BINDING.json').read_text())
 require(binding['schema_version']==oldbinding['schema_version'] and binding['paper_pdf']==oldbinding['paper_pdf'] and binding['support_archive']['path']==oldbinding['support_archive']['path']=='support.zip','binding scope broadened')
 for key,n in [('paper_pdf','paper.pdf'),('support_archive','support.zip')]:require(match(PACKAGE/n,binding[key]),'binding mismatch')
 require(sha((PACKAGE/'paper.pdf').read_bytes())=='67f07f64a5b06c9a4372c285ed438e735fb780d8477b25652bea4f7f6c72e072','PDF differs')
 current_status=json.loads((PACKAGE/'CURRENT_STATUS.json').read_text())
 require(current_status['stage']=='PENDING_NEW_WHOLE_02' and current_status['whole_package_reviews_completed']==1 and current_status['whole_package_reviews_required']>=2 and current_status['publication_ready'] is False and current_status['issues_updated'] is False,'current stage wrong')
 write('PROTECTED_BYTE_RECEIPT.json',{'checked_utc':utc,'pass':True,'immediate_inputs':len(inputs),'unchanged_immediate_inputs':len(unchanged),'allowed_modified_inputs':len(changed),'exact_preserved_before_files':len(before),'original_preparation_inputs_unchanged':len(original_inputs),'original_preparation_output_pins_resolved':103,'original_copy_records_and_bytes_unchanged':72,'current_source_equal_copies':91,'original_submitted_copies':9,'review01_terminal_outputs_unchanged':17,'explicit_protected_records':protected,'all_other_immediate_inputs_unchanged':unchanged,'bibliographic_objects_identical':True,'old_dated_snapshot_and_seals_unchanged':True})
 additions=[record(f,AUDIT) for f in sorted(PACKAGE.rglob('*')) if f.is_file() and 'tmp' not in f.relative_to(PACKAGE).parts and '__pycache__' not in f.parts and f.relative_to(AUDIT).as_posix() not in lookup and f.name!='CURRENT_OUTPUT_PINS.json']
 write('CHANGE_INVENTORY.json',{'checked_utc':utc,'scope':'Only two CLI/verifier guards and necessary current package admin/history/integrity updates. No source, math, TeX, canonical PDF, metadata, prior history/report/verdict or original stage change.','modified':changed,'added_package_members':additions,'unchanged_old_copy_records':72,'added_exact_history_copies':19,'current_status':'PENDING_NEW_WHOLE_02; count1; minimum2; ready/issues false','old_output_pins':'Immutable original103 preserve their meanings via resolve_preparation_stage.py and exact before bytes.'})
 current_entries=[record(f,PACKAGE) for f in sorted(PACKAGE.rglob('*')) if f.is_file() and 'tmp' not in f.relative_to(PACKAGE).parts and '__pycache__' not in f.parts and f.name!='CURRENT_OUTPUT_PINS.json']
 (PACKAGE/'CURRENT_OUTPUT_PINS.json').write_text(json.dumps({'sealed_utc':utc,'scope':'Current repaired non-temporary package stage only. Original OUTPUT_PINS.json is included unchanged and retains original103-stage meanings through preserved before resolver. Excludes this current seal itself; independently pinned in repair FINAL_CURRENT_PINS/OUTPUT_PINS. Not all records are ZIP members.','stage':'PENDING_NEW_WHOLE_02','publication_ready':False,'issues_updated':False,'whole_package_reviews_completed':1,'whole_package_reviews_required':2,'entries':current_entries},indent=2)+'\n')
 write('FINAL_CURRENT_PINS.json',{'sealed_utc':utc,'scope':'Every current non-temporary package file including CURRENT_OUTPUT_PINS; excludes repair outputs to avoid cycles.','records':[record(f,PACKAGE) for f in sorted(PACKAGE.rglob('*')) if f.is_file() and 'tmp' not in f.relative_to(PACKAGE).parts and '__pycache__' not in f.parts]})
 print(json.dumps({'pass':True,'protected_inputs':len(inputs)-len(changed),'allowed_modifications':len(changed),'current_output_entries':len(current_entries),'package_files':len(current_entries)+1,'archive_members':len(allow)},indent=2))
if __name__=='__main__':main()
