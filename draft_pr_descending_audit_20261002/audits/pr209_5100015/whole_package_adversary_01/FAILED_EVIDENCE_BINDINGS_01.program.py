from pathlib import Path
import datetime,hashlib,json,zipfile
B=Path('/Users/alec/Documents/Math/draft_pr_descending_audit_20261002/audits/pr209_5100015/preprint');O=B.parent/'whole_package_adversary_01';D=B.parent/'initial_review_20261016';R=D/'root_reproduction_04_portable_zip_01';X=R/'k303b_outer_center_pedal_product';V=B/'verification'
def pin(p):
 d=p.read_bytes();return dict(path=str(p),bytes=len(d),sha256=hashlib.sha256(d).hexdigest())
primary=[]
for folder,names in [
 (D/'priority_classical_general_01/private_reading',['kls_cyclic_II_v1.pdf','kls_cyclic_II_v1.txt','kls_cyclic_II.pdf','kls_cyclic_II.txt','ks_landen.pdf','ks_landen.txt','ast_revisited_v2.pdf','ast_revisited_v2.txt','bt_reznik_v2.pdf','bt_reznik_v2.txt','chavez_areas_final.pdf','chavez_areas_final.txt']),
 (D/'priority_author_updates_01/private_reading',['invariants_v11.pdf','invariants_v11.txt','stachel_published.txt','ferudun_v11.txt','ferudun_v11_main.tex','ferudun14_v11_source.zip','ferudun14_v10.txt','zenodo23088516.json']),
 (B.parent.parent/'pr210_5100033/initial_review_20261015/private_reading',['invariants_final.pdf','invariants_final.txt','stachel_published.pdf']),
 (B.parent.parent/'pr210_5100033/initial_review_20261015/priority_classical_general_01/private_reading',['ks_pramana_final_ias.txt'])]:
 for name in names:primary.append(pin(folder/name))
# Exact actual source ZIP extraction remains unchanged and matches frozen member bytes.
with zipfile.ZipFile(B/'k303b-source-verification.zip') as z:
 assert all(z.read(i)==(R/i.filename).read_bytes() for i in z.infolist())
aggregate=R/'executed/REPRODUCTION.json';a=json.loads(aggregate.read_text());assert a['status']=='PASS' and a['scientific_programs']==8
cases=[('author','original_submission/verify.py','author/inputs/verify.py','author/inputs/verification.json','original_submission/verification.json',[]),('inherited','original_submission/independent_review/independent_check.py','inherited/inputs/independent_review/independent_check.py','inherited/stdout.txt','root_reproductions/root_reproduction_01/inherited_review/stdout.txt',[]),('root_geometry','scope_controls/root_exact_geometry.py','root_geometry/root_exact_geometry.py','root_geometry/root_reproduction_01/ROOT_EXACT_GEOMETRY.json','root_reproductions/root_reproduction_01/ROOT_EXACT_GEOMETRY.json',['utc']),('source','audits/source_domain_adversary_01/independent_controls.py','source/independent_controls.py','source/control_results.json','audits/source_domain_adversary_01/control_results.json',['created_utc']),('physical','audits/physical_geometry_adversary_01/cartesian_check.py','physical/cartesian_check.py','physical/RESULTS.json','audits/physical_geometry_adversary_01/RESULTS.json',[]),('meromorphic','audits/meromorphic_divisor_adversary_01/check_independent.py','meromorphic/check_independent.py','meromorphic/CHECK_RESULTS.json','audits/meromorphic_divisor_adversary_01/CHECK_RESULTS.json',['utc']),('contemporary_comparison','audits/priority_author_updates_01/check_comparison.py','contemporary_comparison/check_comparison.py','contemporary_comparison/COMPARISON_CHECK_RESULTS.json','audits/priority_author_updates_01/COMPARISON_CHECK_RESULTS.json',['created_utc']),('classical_bridge','audits/priority_classical_general_01/bridge_verify.py','classical_bridge/bridge_verify.py','classical_bridge/bridge_results.json','audits/priority_classical_general_01/bridge_results.json',[])]
rows=[]
for name,src,copied,out,expected,ignored in cases:
 p=R/'executed'/copied;assert p.read_bytes()==(V/src).read_bytes()==(X/'verification'/src).read_bytes()
 actual=json.loads((R/'executed'/out).read_text());want=json.loads((V/expected).read_text())
 for field in ignored:actual.pop(field,None);want.pop(field,None)
 assert actual==want,name
 receipt=R/'executed'/name/'REPLAY_RECEIPT.json';j=json.loads(receipt.read_text());assert j['status']=='PASS' and j['returncode']==0 and j['program_sha256']==pin(p)['sha256']
 rows.append(dict(name=name,program=pin(p),result=pin(R/'executed'/out),receipt=pin(receipt),ignored_only_declared_timestamps=ignored,all_scientific_fields_independently_identical=True))
# Private raw chronology stays in place; verify actual capture bytes without
# copying primary/provider bodies or displaying unrelated private transport data.
chron=V/'root_reproductions/priority_public_chronology_01/PUBLIC_CHRONOLOGY_OBSERVATIONS.json';cj=json.loads(chron.read_text());chron_rows=[]
for row in cj['raw_capture_pins']:
 p=D/'priority_public_chronology_01'/row['path'];r=pin(p);assert r['bytes']==row['bytes'] and r['sha256']==row['sha256'];chron_rows.append(r)
# All candidate bindings are unchanged since the initial review freeze.
f=json.loads((O/'FROZEN_BYTES.json').read_text());assert all(pin(B/r['path'])['sha256']==r['sha256'] and pin(B/r['path'])['bytes']==r['bytes'] for r in f['core']+f['source_manifest_actual_entries'])
result=dict(utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),status='PASS',primary_read_in_place=primary,root_actual_zip_aggregate=pin(aggregate),root_actual_eight_suite_artifacts=rows,root_extracted_zip_every_member_byte_identical=True,chronology_raw_capture_actual_byte_bindings=chron_rows,candidate_final_actual_core_and_all_source_entries_unchanged=True,own_read_only_zip_integrity_execution=dict(command='existing bundled Python -B actual-extracted-ZIP/verification/integrity.py',exit_code=0,stdout_verbatim='{"status": "PASS", "verified_files": 148}\n'),limits='Root performed genuine eight-suite execution; this reviewer read programs and independently recomputed byte/scientific-result comparisons, plus its own distinct controls. No claim this reviewer independently reran all eight suites. Raw third-party primary texts/private captures remain outside authored outputs.')
(O/'EVIDENCE_BINDINGS.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({k:v for k,v in result.items() if k not in ['primary_read_in_place','root_actual_eight_suite_artifacts','chronology_raw_capture_actual_byte_bindings']},indent=2))
