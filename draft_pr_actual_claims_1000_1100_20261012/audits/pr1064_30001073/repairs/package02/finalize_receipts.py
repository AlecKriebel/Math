#!/usr/bin/env python3
"""Protect prior stages and issue separate current repaired-stage pins."""
from pathlib import Path
import datetime,difflib,hashlib,json,zipfile
from resolve_prior_stages import require,match,resolve_package
HERE=Path(__file__).resolve().parent;AUDIT=HERE.parent.parent;PACKAGE=AUDIT/'preprint_v1_0'
ALLOWED={'build_archive.py','verify_package.py','README.md','COPY_MAP.json','SAFE_INPUT_PINS.json','EXCLUSION_LEDGER.json','SUPPORT_ALLOWLIST.json','SUPPORT_MANIFEST.json','support.zip','publication/DEPOSIT_BINDING.json'}
def record(p,root):
 data=p.read_bytes();return {'path':p.relative_to(root).as_posix(),'bytes':len(data),'sha256':hashlib.sha256(data).hexdigest()}
def write(p,d):p.write_text(json.dumps(d,indent=2)+'\n')
def main():
 utc=datetime.datetime.now(datetime.timezone.utc).isoformat();frozen=json.loads((HERE/'INPUT_PINS.json').read_text())['records'];changed=[];unchanged=[]
 for r in frozen:
  p=AUDIT/r['path']
  if match(p,r):unchanged.append(r)
  else:
   require(r['path'].startswith('preprint_v1_0/') and r['path'][len('preprint_v1_0/'):] in ALLOWED,'unexpected protected mutation '+r['path'])
   require(match(HERE/'before'/r['path'],r),'missing exact before bytes')
   changed.append({'path':r['path'],'before':r,'after':record(p,AUDIT),'preserved_path':(HERE/'before'/r['path']).relative_to(AUDIT).as_posix()})
 require({r['path'][len('preprint_v1_0/'):] for r in changed}==ALLOWED,'unexpected changed set')
 before=json.loads((HERE/'BEFORE_PINS.json').read_text())['entries']
 for r in before:require(match(HERE/r['preserved_path'],r),'before-byte mismatch')
 for seal,count,key in [('OUTPUT_PINS.json',103,'entries'),('CURRENT_OUTPUT_PINS.json',124,'entries')]:
  records=json.loads((PACKAGE/seal).read_text())[key];require(len(records)==count,'stage count changed')
  for r in records:resolve_package(r)
 repair01=AUDIT/'repairs/package01'
 for r in json.loads((repair01/'FINAL_CURRENT_PINS.json').read_text())['records']:resolve_package(r)
 for r in json.loads((repair01/'OUTPUT_PINS.json').read_text())['entries']:require(match(repair01/r['path'],r),'repair01 terminal changed')
 original_inputs=json.loads((PACKAGE/'INPUT_PINS.json').read_text())['records']
 for r in original_inputs:require(match(AUDIT/r['path'],r),'original preparation input changed')
 copies=json.loads((PACKAGE/'COPY_MAP.json').read_text())['copies'];old=json.loads((HERE/'before/preprint_v1_0/COPY_MAP.json').read_text())['copies'];require(len(old)==91 and len(copies)==122 and copies[:91]==old,'old/current copy records differ')
 for r in copies:require(match(AUDIT/r['source_path'],r) and match(PACKAGE/r['package_path'],r),'copy/source byte mismatch')
 require(sum(r['source_path'].startswith('submitted/') for r in copies)==9,'original nine count changed')
 require(json.loads((PACKAGE/'SAFE_INPUT_PINS.json').read_text())['records']==copies,'safe input pins differ')
 for folder,count in [('package_01',17),('package_02',28)]:
  records=json.loads((AUDIT/'reviews'/folder/'OUTPUT_PINS.json').read_text())['entries'];require(len(records)==count,'review count changed')
  for r in records:require(match(AUDIT/'reviews'/folder/r['path'],r),'review output changed')
 protected_names=['paper.tex','paper.pdf','metadata.json','publication/release_metadata.json','publication/zenodo.json','STATUS.json','CURRENT_STATUS.json','OUTPUT_PINS.json','CURRENT_OUTPUT_PINS.json','PREPARATION_REPORT.md','FINAL_VERIFICATION.json','RESEARCH_LOG.md','build_pdf.py','fresh_guard_checker.py','run_checks.py','ATTRIBUTION.md','SOURCE_LEDGER.json','LICENSE.txt']
 lookup={r['path']:r for r in frozen};protected=[lookup['preprint_v1_0/'+n] for n in protected_names]
 for r in protected:require(match(AUDIT/r['path'],r),'explicit protected byte changed')
 meta=json.loads((PACKAGE/'metadata.json').read_text())
 require(all(json.loads((PACKAGE/n).read_text())['metadata']==meta for n in ['publication/release_metadata.json','publication/zenodo.json']),'normalized metadata differ')
 allow=json.loads((PACKAGE/'SUPPORT_ALLOWLIST.json').read_text())['members'];require(len(allow)==149 and allow==sorted(set(allow)),'allowlist count/order wrong')
 manifest=json.loads((PACKAGE/'SUPPORT_MANIFEST.json').read_text())['entries'];require([r['path'] for r in manifest]==[n for n in allow if n!='SUPPORT_MANIFEST.json'],'manifest coverage wrong')
 for r in manifest:require(match(PACKAGE/r['path'],r),'manifest hash differs')
 for name in allow:
  if name!='paper.pdf':(PACKAGE/name).read_bytes().decode('utf-8')
 with zipfile.ZipFile(PACKAGE/'support.zip') as z:
  infos=z.infolist();require([i.filename for i in infos]==allow,'archive order/members wrong')
  for i in infos:
   require(i.date_time==(2026,10,14,0,0,0) and i.create_system==3 and i.external_attr==(0o100644<<16) and i.compress_type==zipfile.ZIP_DEFLATED and not i.flag_bits&1,'archive attributes wrong')
   require(z.read(i)==(PACKAGE/i.filename).read_bytes(),'archive/source byte mismatch')
 binding=json.loads((PACKAGE/'publication/DEPOSIT_BINDING.json').read_text());oldbinding=json.loads((HERE/'before/preprint_v1_0/publication/DEPOSIT_BINDING.json').read_text())
 require(binding['schema_version']==oldbinding['schema_version'] and binding['paper_pdf']==oldbinding['paper_pdf'] and binding['support_archive']['path']==oldbinding['support_archive']['path']=='support.zip','binding scope changed')
 for key,n in [('paper_pdf','paper.pdf'),('support_archive','support.zip')]:require(match(PACKAGE/n,binding[key]),'binding hash differs')
 require('publication/DEPOSIT_BINDING.json' not in allow,'circular descriptor membership')
 latest=json.loads((PACKAGE/'CURRENT_STATUS_WHOLE03.json').read_text());require(latest['stage']=='PENDING_NEW_WHOLE_03' and latest['whole_package_reviews_completed']==2 and latest['whole_package_reviews_required']>=2 and latest['publication_ready'] is False and latest['issues_updated'] is False and latest['ascending_publication_hold_after_pr']==1032,'latest gate altered')
 write(HERE/'PROTECTED_BYTE_RECEIPT.json',{'checked_utc':utc,'pass':True,'immediate_inputs':len(frozen),'unchanged_immediate_inputs':len(unchanged),'allowed_modified_inputs':len(changed),'exact_before_files':len(before),'original_preparation_inputs_unchanged':len(original_inputs),'original103_stage_resolved':True,'repair01_current124_all125_stage_resolved':True,'repair01_all37_terminal_outputs_unchanged':True,'whole01_17_whole02_28_outputs_unchanged':True,'old91_copy_records_and_bytes_unchanged':True,'current_source_equal_copies':122,'original_nine_exact_copies':True,'explicit_protected_records':protected,'other_unchanged_inputs':unchanged,'bibliographic_objects_unchanged_and_equal':True})
 additions=[record(p,AUDIT) for p in sorted(PACKAGE.rglob('*')) if p.is_file() and 'tmp' not in p.relative_to(PACKAGE).parts and '__pycache__' not in p.parts and p.relative_to(AUDIT).as_posix() not in lookup]
 write(HERE/'CHANGE_INVENTORY.json',{'checked_utc':utc,'scope':'Sole whole02 P3 archive-output aliases; minimal necessary code/admin/history/integrity changes.','modified':changed,'added_package_files':additions,'old91_copies_preserved':True,'added_exact_history_copies':31,'old_status_current_seals_immutable':True,'current_stage':'PENDING_NEW_WHOLE_03/count2/minimum2/false flags/held1032','prior_stage_resolver':'resolve_prior_stages.py; byte-exact before02/before01/current matching only'})
 diff=[]
 for name in ['build_archive.py','verify_package.py']:
  diff.extend(difflib.unified_diff((HERE/'before/preprint_v1_0'/name).read_text().splitlines(True),(PACKAGE/name).read_text().splitlines(True),fromfile='before/preprint_v1_0/'+name,tofile='preprint_v1_0/'+name))
 (HERE/'CODE_DIFF.patch').write_text(''.join(diff))
 latest_entries=[record(p,PACKAGE) for p in sorted(PACKAGE.rglob('*')) if p.is_file() and 'tmp' not in p.relative_to(PACKAGE).parts and '__pycache__' not in p.parts and p.name!='CURRENT_OUTPUT_PINS_WHOLE03.json']
 require(len(latest_entries)==157,'latest file count wrong')
 write(PACKAGE/'CURRENT_OUTPUT_PINS_WHOLE03.json',{'sealed_utc':utc,'scope':'Latest repaired stage; every non-temporary package file except this seal. Old CURRENT_OUTPUT_PINS/OUTPUT_PINS retain their dated meanings through preserved-stage resolver. Separately pinned by repair02 FINAL_CURRENT_PINS and output seal.','stage':'PENDING_NEW_WHOLE_03','publication_ready':False,'issues_updated':False,'whole_package_reviews_completed':2,'whole_package_reviews_required':2,'entries':latest_entries})
 write(HERE/'FINAL_CURRENT_PINS.json',{'sealed_utc':utc,'scope':'All158 current non-temporary package files including latest current seal; no repair-output cycle.','records':[record(p,PACKAGE) for p in sorted(PACKAGE.rglob('*')) if p.is_file() and 'tmp' not in p.relative_to(PACKAGE).parts and '__pycache__' not in p.parts]})
 print(json.dumps({'pass':True,'frozen_inputs':len(frozen),'protected_inputs':len(unchanged),'allowed_changes':len(changed),'current_package_files':158,'latest_seal_entries':157,'archive_members':len(allow)},indent=2))
if __name__=='__main__':main()
