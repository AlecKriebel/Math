"""Prepare a versioned repair after whole-review01; no remote actions."""
from pathlib import Path
import datetime,hashlib,json,shutil,stat
A=Path(__file__).resolve().parent
def require(ok,msg):
 if not ok:raise ValueError(msg)
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def replace_once(s,old,new):
 require(s.count(old)==1,'Expected unique repair text: '+old[:80]);return s.replace(old,new)
def write(p,s):
 require(not p.exists(),'Generation already exists: '+str(p));p.parent.mkdir(parents=True,exist_ok=True);p.write_text(s)
review=A/'whole_package_review_01_final'
seal=json.loads((review/'FINAL_SEAL.json').read_text())
entries=seal.get('files',seal.get('manifest',seal.get('key_files')))
require(isinstance(entries,list) and entries,'Review final seal schema')
for x in entries:
 p=review/x['path'];require(pin(p)['sha256']==x.get('sha256',x.get('SHA256')),'Review pin mismatch '+x['path']);require(stat.S_IMODE(p.stat().st_mode)==0o444,'Review file not protected '+x['path'])
require('REPAIR_REQUIRED' in (review/'FINAL_REPORT.md').read_text(),'Wrong review disposition')
identity=json.loads((A/'ROOT_DOI_FILE_IDENTITY_20261015_01.json').read_text());require(identity['all_three_files_authenticated'],'DOI check not complete')
for p in [A/'CURRENT_PROOF.md',A/'integration_preparation/CURRENT_TEMPLATE.json']:
 dst=p.with_name(p.stem+'_PRE_WHOLE_REVIEW01'+p.suffix);require(not dst.exists(),'Historical snapshot exists');shutil.copyfile(p,dst);dst.chmod(0o444)
proof=(A/'CURRENT_PROOF.md').read_text()
proof=replace_once(proof,'Current audit revision, 2026-10-14.','Current audit revision, 2026-10-15.')
proof=replace_once(proof,'Competing current-site files were not compared to inaccessible DOI-deposited files.','On 15 October 2026, the DOI-version PDF, source ZIP and verification report were retrieved successfully; their record sizes/checksums and SHA256 hashes matched the previously pinned website files/metadata. In particular, the inspected website PDF and source ZIP equal the DOI-version files byte for byte. Earlier 403 acquisition failures remain historical records and are superseded on this specific identity point.')
p=A/'CURRENT_PROOF.md';p.chmod(0o644);p.write_text(proof);p.chmod(0o444)
g=json.loads((A/'ROOT_PRIORITY_GATE_01.json').read_text());g['UTC']=datetime.datetime.now(datetime.UTC).isoformat();g['case_percent']=68;g['supersedes_on_DOI_file_identity_only']='ROOT_PRIORITY_GATE_01.json';g['exact_current_primary_overlap_verified']['DOI_deposited_file_equals_current_website_file']=True;g['exact_current_primary_overlap_verified']['DOI_identity_evidence']='ROOT_DOI_FILE_IDENTITY_20261015_01.json';g['material_gaps']=[x for x in g['material_gaps'] if 'Ferudun DOI files' not in x];g['material_gaps'].append('Historical exact-byte public visibility, author awareness/independence and exhaustive priority remain unestablished; current DOI-file identity is verified.');write(A/'ROOT_PRIORITY_GATE_02.json',json.dumps(g,indent=2)+'\n')
tex=(A/'publication_package_v1/dodecahedron_endpoint.tex').read_text()
tex=replace_once(tex,'\\date{14 October 2026}','\\date{15 October 2026}')
tex=replace_once(tex,'DataCite records DOI registration on that date; our audit distinguishes the current website files from the inaccessible Zenodo file bodies.','DataCite records DOI registration on that date. On 15~October~2026, we retrieved the DOI-version files and verified the record checksums and matching SHA256 hashes: the inspected website PDF and source archive equal their DOI-version counterparts byte for byte. Earlier access failures are retained as historical acquisition records, not a present file-identity gap.')
tex=replace_once(tex,'including unavailable journal-version comparisons','including uncompleted journal-version comparisons')
tex=replace_once(tex,'current body at \\url{https://eulersolve.org/papers/amr-049/}.','DOI-version PDF and source archive matched the inspected copies at \\url{https://eulersolve.org/papers/amr-049/}.')
write(A/'publication_package_v2/dodecahedron_endpoint.tex',tex)
s=(A/'assemble_publication_package_v1.py').read_text().replace('publication_package_v1','publication_package_v2').replace('ROOT_PRIORITY_GATE_01.json','ROOT_PRIORITY_GATE_02.json').replace('PACKAGE_V1_ASSEMBLY_01.json','PACKAGE_V2_ASSEMBLY_01.json')
s=replace_once(s,"'publication_date':'2026-10-14'","'publication_date':'2026-10-15'")
s=replace_once(s,'Current website files could not be compared to its DOI-deposited files, and journal/body-version gaps remain disclosed.','On 15 October 2026, the DOI-version files were retrieved successfully and authenticated against record checksums and the previously pinned website hashes; the inspected PDF and source ZIP are byte-identical to the DOI-version files. Uncompleted journal/body-version comparisons remain disclosed.')
s=replace_once(s,'DOI-deposited files could not be compared with the current site bytes; journal-version/body gaps remain.','The 15 October 2026 successful retrieval authenticates DOI-version PDF/source ZIP equality with the inspected website copies, and all three files match their prior website metadata hashes. Earlier failed-acquisition records are historical and superseded on this identity point. Journal-version/body comparisons remain incomplete.')
needle="copy(A/'CURRENT_PROOF.md','CURRENT_PROOF.md')"
extra="""
copy(A/'ROOT_DOI_FILE_IDENTITY_20261015_01.json','provenance/ROOT_DOI_FILE_IDENTITY_20261015_01.json')
copy(A/'ROOT_GLOBAL_REPAIR_02.json','provenance/ROOT_GLOBAL_REPAIR_02.json')
copy(A/'ROOT_PRIORITY_GATE_01.json','provenance/historical_ROOT_PRIORITY_GATE_01.json')
names=json.loads((A/'whole_package_review_01_final/SAFE_AUTHORED_ALLOWLIST.json').read_text())['key_files']
for n in names:copy(A/'whole_package_review_01_final'/n,'whole_review_history/review01/'+n)
"""
s=replace_once(s,needle,needle+'\n'+extra)
s=replace_once(s,'priority/ contains two completed independent bounded primary-body/version/current-literature audits.','priority/ contains two completed independent bounded primary-body/version/current-literature audits. Their sealed reports preserve the original acquisition observations and are not rewritten. The current DOI-file identity correction is in provenance/ROOT_DOI_FILE_IDENTITY_20261015_01.json and ROOT_GLOBAL_REPAIR_02.json; it supersedes their earlier DOI access/identity gap without changing the remaining priority caveats. whole_review_history/review01 preserves the completed independent REPAIR_REQUIRED review that found this evidence change; the current packet incorporates its required repair and still awaits a fresh whole-package review.')
s=replace_once(s,'The independent programs use distinct exact constructions:','The secondary independent_face_word.py and independent_double_pentagon.py retain assertion-based checks: run their documented ordinary-Python commands above. Their historical optimized-Python output equality is an execution observation, not evidence that their assertions were enforced. Optimization-safe verification is provided by the canonical current runner and explicit-guard independent checks.\n\nThe independent programs use distinct exact constructions:')
write(A/'assemble_publication_package_v2.py',s)
s=(A/'prepare_native_template_pending_01.py').read_text().replace('publication_package_v1','publication_package_v2').replace('native_template_pending_01','native_template_pending_02').replace('PR_METADATA_PROPOSAL_01.json','PR_METADATA_PROPOSAL_02.json').replace('TRACKER_ROW_PROPOSAL_01.json','TRACKER_ROW_PROPOSAL_02.json')
s=replace_once(s,'Current website and DOI-deposited file equality remains unverified403.','On15October2026 the DOI-version PDF, source ZIP and verification report were retrieved and authenticated against record checksums and prior website hashes; the inspected PDF/source ZIP equal their DOI-version counterparts byte for byte. Earlier403 observations are retained as historical acquisition records, superseded on this identity point. Historical visibility/awareness/independence remain uncertified.')
s=s.replace('source-version identity and author independence remain uncertified','uncompleted older journal-version comparisons and author independence remain uncertified; current Ferudun DOI-file identity is verified')
s=s.replace('Publication workflow62%','Publication workflow68%').replace('Four-page exact packet protected for successive NEW whole-package reviews','Whole review01 required a current DOI-identity evidence correction, now propagated globally; four-page v2 packet protected for the next NEW whole-package review')
s=replace_once(s,"(A/'integration_preparation/CURRENT_TEMPLATE.json').write_text(json.dumps(pointer,indent=2)+'\\n')","pointer_path=A/'integration_preparation/CURRENT_TEMPLATE.json'\nif pointer_path.exists():pointer_path.chmod(0o644)\npointer_path.write_text(json.dumps(pointer,indent=2)+'\\n')\npointer_path.chmod(0o444)\narchive=A/'integration_preparation/NATIVE_TEMPLATE_PENDING_02_MANIFEST.json'\nif archive.exists():raise RuntimeError('Template manifest already exists')\narchive.write_bytes(pointer_path.read_bytes());archive.chmod(0o444)")
write(A/'prepare_native_template_pending_02.py',s)
rec={'UTC':datetime.datetime.now(datetime.UTC).isoformat(),'status':'REPAIR01_PROPAGATED_NEW_PACKET_ASSEMBLY_AND_FRESH_REVIEW_PENDING','case_percent':68,'previous_packet':'publication_package_v1','new_packet':'publication_package_v2','review_report':str(review.relative_to(A)/'FINAL_REPORT.md'),'review_report_pin':pin(review/'FINAL_REPORT.md'),'review_seal_pin':pin(review/'FINAL_SEAL.json'),'required_issue':'Current DOI inaccessibility/noncomparison wording superseded by actual successful DOI-file downloads and byte identity.','identity_evidence':pin(A/'ROOT_DOI_FILE_IDENTITY_20261015_01.json'),'current_science_unchanged':True,'historical_artifacts_preserved':True,'firstness_or_independence_certified':False,'source_author_erratum_certified':False,'fresh_whole_review_required':True,'published':False,'root_pre_repair_proof_pin':pin(A/'CURRENT_PROOF_PRE_WHOLE_REVIEW01.md'),'current_proof_pin':pin(A/'CURRENT_PROOF.md')}
write(A/'ROOT_GLOBAL_REPAIR_02.json',json.dumps(rec,indent=2)+'\n')
for n in ['ROOT_PRIORITY_GATE_02.json','ROOT_GLOBAL_REPAIR_02.json']:(A/n).chmod(0o444)
print(json.dumps(rec))
