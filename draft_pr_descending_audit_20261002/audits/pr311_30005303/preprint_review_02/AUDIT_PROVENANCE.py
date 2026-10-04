"""Authenticate corrected orchestration labels and preserved native streams."""
import datetime,hashlib,json,pathlib
base=pathlib.Path(__file__).resolve().parent;D=base/'private';P=D/'released_package';H=D/'historical_build'
sha=lambda b:hashlib.sha256(b).hexdigest()
r=json.loads((P/'BUILD_RECEIPT.json').read_bytes());script=(H/'root_build_preprint_v01.py').read_bytes();script_hash=sha(script)
assert script_hash=='85020339f2a629d3aafb62f63699c4e9c17be2997e910aaeb6630886663a5d03'
assert b'program_sha256=sha(Path(__file__).read_bytes())' in script
rawjobs=[];checks=[]
for label,newjob in zip(['compile','pdfinfo','extract','render'],r['native_jobs']):
 raw=json.loads((H/(label+'_execution.json')).read_bytes());rawjobs.append(raw)
 assert raw['program_sha256']==script_hash==newjob['orchestration_script_sha256']
 assert {k:v for k,v in raw.items() if k!='program_sha256'}=={k:v for k,v in newjob.items() if k!='orchestration_script_sha256'}
 for stream in ['stdout','stderr']:
  b=(H/(label+'.'+stream)).read_bytes();assert len(b)==raw[stream+'_bytes'] and sha(b)==raw[stream+'_sha256']
 checks.append({'label':label,'all_native_fields_and_full_streams_agree':True,'exit_code':raw['exit_code'],'orchestration_hash':script_hash})
old={k:v for k,v in r.items() if k!='provenance_label_correction'};old['native_jobs']=rawjobs
old_bytes=(json.dumps(old,indent=2)+'\n').encode();old_hash=sha(old_bytes)
assert old_hash==r['provenance_label_correction']['original_receipt_sha256']
(D/'reconstructed_original_BUILD_RECEIPT.json').write_bytes(old_bytes)
assert r['source_sha256']==sha((P/'mtp2_edge_closure.tex').read_bytes())
pdf=(P/'output/pdf/mtp2_edge_closure.pdf').read_bytes();assert len(pdf)==r['pdf']['bytes'] and sha(pdf)==r['pdf']['sha256']
render_checks=[]
for i,record in enumerate(r['rendered_pages'],1):
 p=D/('manuscript-'+str(i)+'.png');assert sha(p.read_bytes())==record['sha256'];render_checks.append({'page':i,'fresh_render_equals_historical_pin':True})
assert (D/'manuscript_pdfinfo.stdout').read_bytes()==(H/'pdfinfo.stdout').read_bytes()
assert all(not (H/(label+'.stderr')).read_bytes() for label in ['pdfinfo','extract','render'])
result={'verified_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'status':'PASS_CORRECTED_PROVENANCE','orchestration_script_sha256':script_hash,'what_hash_measures':'The Python orchestration file bytes, through Path(__file__).read_bytes(), not a compiler/renderer executable.','historical_native_checks':checks,'reconstructed_original_receipt_sha256':old_hash,'all_five_render_pins_reproduced':render_checks,'source_pdf_and_pdfinfo_pins_agree':True,'historical_limits':['The original script Git commit was not independently inspected because Git/ref operations and additional files were outside this review release.','The historical desktop compiler statement has no released purpose-built-tool capture; native compile/render evidence is directly authenticated.','The original law-checker authorship-independence statement is historical testimony; current label edits are transparently attributed. No new firsthand certification of that authorship history is inferred.','No historical executable-binary fingerprints are asserted. Current command records include current executable fingerprints.']}
(base/'PROVENANCE_CHECK_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps(result,indent=2))
