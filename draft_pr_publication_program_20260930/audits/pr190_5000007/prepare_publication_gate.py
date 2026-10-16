"""Bind a finished, root-assessed fresh-review sequence to exact upload bytes."""
from pathlib import Path
import datetime,hashlib,json,stat
A=Path(__file__).resolve().parent
def require(ok,msg):
 if not ok:raise RuntimeError(msg)
def pin(p):
 b=p.read_bytes();return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def read(n):return json.loads((A/n).read_text())
require(not (A/'ROOT_PUBLICATION_GATE.json').exists(),'Gate already exists')
inp=read('ROOT_WHOLE_REVIEW_INPUT_02.json');require(pin(A/inp['package_manifest'])['sha256']==inp['package_manifest_SHA256'],'Input manifest changed')
for n,x in inp['other_exact_inputs'].items():require(pin(A/n)==x,'Whole-review-bound input changed '+n)
first=read('ROOT_WHOLE_REVIEW01_FINAL_AUTHENTICATION.json');last=read('ROOT_WHOLE_REVIEW02_FINAL_AUTHENTICATION.json')
require(first['reviewer']=='whole_package_review_01_final' and last['reviewer']=='whole_package_review_02','Not distinct completed whole reviewers')
for auth in [first,last]:
 d=auth['reviewer'];require(pin(A/d/'FINAL_REPORT.md')==auth['report'] and pin(A/d/'FINAL_SEAL.json')==auth['final_seal'],'Authenticated reviewer changed')
sealed=read('whole_package_review_02/FINAL_SEAL.json');require(sealed['disposition']=='PASS' and not sealed.get('required_issues',[]),'Final reviewer has required issues')
require('PASS' in (A/'whole_package_review_02/FINAL_REPORT.md').read_text(),'No final positive report')
repair=read('ROOT_GLOBAL_REPAIR_02.json');require(repair['current_science_unchanged'] and repair['required_issue'].startswith('Current DOI'),'Repair scope changed')
pack=read(inp['package_manifest']);P=A/pack['package_name'];payloads={}
for n,x in pack['payloads'].items():
 actual=pin(P/n);require(actual==x and stat.S_IMODE((P/n).stat().st_mode)==0o444,'Final packet identity/protection changed '+n);payloads[n]={'bytes':actual['bytes'],'SHA256':actual['sha256']}
meta=json.loads((P/'zenodo-deposit.json').read_text());require([x['path'] for x in meta['files']]==['dodecahedron_endpoint.pdf','dodecahedron_endpoint.tex','verification-package.zip'],'Upload membership changed')
require(meta['metadata']['publication_date']=='2026-10-15' and meta['metadata']['creators'][0]['orcid']=='0009-0001-9320-500X','Intended author/date changed')
pri=read('ROOT_PRIORITY_GATE_02.json');require(pri['qualified_note_route_authorized_by_human'] and not pri['historical_priority_clearance'] and pri['exact_current_primary_overlap_verified']['DOI_deposited_file_equals_current_website_file'] is True,'Qualified priority scope changed')
visual=read('ROOT_V2_VISUAL_ACCEPTANCE.json');require(visual['pages']==4 and visual['PDF']==pin(P/'dodecahedron_endpoint.pdf'),'Visual identity changed')
out={'UTC':datetime.datetime.now(datetime.UTC).isoformat(),'status':'READY_FOR_AUTHORIZED_PUBLICATION','PR':190,'original_head':'0c3346c8ebcb3b967a1d8bf9a283f027b44b738c','original_QUEUE_status':'claimed_solved','original_effort':'unknown/5 (interrupted)','package_name':P.name,'payloads':payloads,'upload_files':[x['path'] for x in meta['files']],'whole_package_reviews':[{'reviewer':first['reviewer'],'disposition':'REPAIR_REQUIRED','report':first['report'],'final_seal':first['final_seal'],'repair':'ROOT_GLOBAL_REPAIR_02.json'},{'reviewer':last['reviewer'],'disposition':'PASS','required_issues':[],'report':last['report'],'final_seal':last['final_seal']}],'exact_final_review_input':{'path':'ROOT_WHOLE_REVIEW_INPUT_02.json',**pin(A/'ROOT_WHOLE_REVIEW_INPUT_02.json')},'frozen_packet_manifest':{'path':inp['package_manifest'],**pin(A/inp['package_manifest'])},'mathematical_clearance':True,'result':'Imported bare-angle exclusion FALSE by exactly two proper face diagonals; adopted parity-selected endpoint exclusion PROVED without length bound.','source_author_authenticated_erratum':False,'source_unique_intent_certified':False,'bounded_priority_audit_complete':True,'historical_priority_clearance':False,'historical_firstness_or_guaranteed_novelty_certified':False,'current_open_status_certified':False,'awareness_or_independence_certified':False,'qualified_note_route_authorized':True,'current_Ferudun_DOI_version_identity_verified':True,'frozen_pre_review_workflow_flags':'Packet manifest and historical/provenance records retain their exact dated assembly states, including pending-review flags. This subsequent gate binds these immutable bytes to the actual completed review sequence; those dated pending flags are not present lifecycle authority. The reviewed pending-native manifest is also retained unchanged as integration_preparation/NATIVE_TEMPLATE_PENDING_02_MANIFEST.json before later factual updates.','unresolved_scientific_issues':[],'remaining_priority_limits':pri['material_gaps'],'extensive_AI':True,'unrefereed':True,'conventional_human_peer_review':False,'Zenodo_published_at_gate_creation':False,'tracker_or_merge_complete_at_gate_creation':False,'root_read_and_assessed_complete_review_reports':True}
p=A/'ROOT_PUBLICATION_GATE.json';p.write_text(json.dumps(out,indent=2)+'\n');p.chmod(0o444);print(json.dumps({'status':out['status'],'package_name':P.name,'payloads':payloads,'qualified_note_route':True,'historical_priority_clearance':False}))
