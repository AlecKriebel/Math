"""Read-only root authentication of four sealed PR124 source/priority reviews."""
from pathlib import Path
import datetime,hashlib,json,os
A=Path(__file__).resolve().parent
def req(ok,msg):
 if not ok:raise RuntimeError(msg)
def sha(b):return hashlib.sha256(b).hexdigest()
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def dump(p,obj):p.write_text(json.dumps(obj,indent=2,sort_keys=True)+'\n')
def pin(path,expected=None,size=None):
 req(path.is_file() and not path.is_symlink(),'Regular source/member '+str(path))
 b=path.read_bytes();h=sha(b)
 req(expected is None or h==expected,'Full body hash '+str(path))
 req(size is None or len(b)==size,'Full body size '+str(path))
 return {'path':str(path.relative_to(A)),'bytes':len(b),'sha256':h}
families=[
 ('historical_alexander_priority_adversary_20261006',6,'d3b376174f59a0f7e8c54fd699b9fab14e72845f60ed64b0fa1d7fb61c779b37','ae1b3c3c7ab1ccec0bffdd3fbf8884f2a9a03fd2a0edfec5d1f74a75d05951a7','13a7d3731e26168bc0815659ada761cebc7319f2acede9aa93dc7aa2da121031'),
 ('original_conjecture_priority_adversary_20261006',9,'88e80f1fe72d148ddd0719c09242f00bda20ae42f6f25d3fa5f55181b1cabd5c','2d5677e9cc627625aeff1356c2742abd52c9b9df2b3f583646440b6714722e30','81a3dc52fbf99ff6adbf7bba88ab6ff9b86b8e27a1e57c2b0885d8f406cd3857'),
 ('later_realization_priority_adversary_20261006',6,'815fbadb748c363e001b3246fdebbc32aee7f17d3bc8179c0304438941b39c7c','74e6497528b38be90fdf5c6b445f95b7aa8be105ba9950cbf8042664b2fdb621','4086b288cde43e82d9ec85127a87aa26cc82d9dcbb6ccb6283d92bc6da118859'),
 ('novel_contribution_adversary_20261006',6,'010d744b27c3d136b4f2665293b224204c9ef4fbed335a737d7e52bd55dc092a','b0fb2364fb35ea9327aa348bb2d0190770da80ed0998f8025201e5994c985832','a441e6f811e280a13ac20bccb6804b10ceec865607774eb227125bb14ad3379c')]
receipt_path=A/'ROOT_PRIORITY_FAMILY_AUTHENTICATION_20261006.json'
req(not receipt_path.exists(),'Completed receipt exists; inspect before rerun')
verified=[]
for directory,count,manifest_hash,report_hash,result_hash in families:
 F=A/directory;m=F/'SHA256SUMS.json';manifest=pin(m,manifest_hash)
 pin(F/'REPORT.md',report_hash);pin(F/'RESULT.json',result_hash)
 raw=json.loads(m.read_text());members=raw.get('members',raw.get('files'))
 req(isinstance(members,list) and len(members)==count,'Sealed member cardinality')
 paths=set();bodies=[]
 for item in members:
  r=Path(item['path']);req(not r.is_absolute() and '..' not in r.parts and not {'private_sources','__pycache__'}.intersection(r.parts),'Public member scope')
  req(str(r) not in paths and str(r)!='SHA256SUMS.json','Unique nonself member')
  paths.add(str(r));bodies.append(pin(F/r,item['sha256'],item['bytes']))
 actual={str(p.relative_to(F)) for p in F.rglob('*') if p.is_file() and 'private_sources' not in p.relative_to(F).parts and p.name!='SHA256SUMS.json'}
 req(actual==paths,'Exact public file coverage '+directory)
 verified.append({'directory':directory,'manifest':manifest,'report_sha256':report_hash,'result_sha256':result_hash,'members':bodies,'public_member_count':count,'result':json.loads((F/'RESULT.json').read_text())})
original=json.loads((A/'original_head_authentication_20261006/ORIGINAL_AUTHENTICATION.json').read_text())
req(original['original_file_count']==17 and original['original_budget']=='2/5','Preserved original ledger')
originals=[pin(A/'original_head_authentication_20261006/original_attempt'/x['path'],x['sha256'],x['bytes']) for x in original['original_files']]
math_gate_pin=pin(A/'MATHEMATICAL_SOURCE_GATE_20261006.json','4d820293c9c9fde1dad40c4a11fc81cb9f0a49f9b3715bdfadfb9418db160568')
math=json.loads((A/'MATHEMATICAL_SOURCE_GATE_20261006.json').read_text());req(math['status']=='PASS' and not math['publication_clearance'],'Original math gate')
math_receipt=json.loads((A/'ROOT_MATH_FAMILY_AUTHENTICATION_20261006.json').read_text())
req(math_receipt['actual_child_count']==58 and math_receipt['public_member_count']==47 and math_receipt['all_actual_expected_exits_passed'],'Earlier actual mathematical replays')
math_family_pins=[]
for family in json.loads((A/'MATH_FAMILY_SEAL_BINDINGS_20261006.json').read_text())['families']:
 F=A/family['directory'];pin(F/'SHA256SUMS.json',family['manifest_sha256']);raw=json.loads((F/'SHA256SUMS.json').read_text())['files']
 members=[{'path':k,'bytes':v.get('bytes',v.get('size_bytes')),'sha256':v['sha256']} for k,v in raw.items()] if isinstance(raw,dict) else raw
 math_family_pins.extend(pin(F/x['path'],x['sha256'],x['bytes']) for x in members)
sources=[]
for s in json.loads((A/'root_primary_sources_20261006/SOURCES.json').read_text())['sources']:
 sources.append(pin(A/'root_primary_sources_20261006/private_sources'/(s['name']+'.pdf'),s['sha256'],s['bytes']))
for relative,h in [
 ('root_priority_sources_20261006/private_sources/turaev1986.pdf','9c9d358dd66197c7d86dbe98537229e73d6fb9f0f6e630d7aaae529cd6e41985'),
 ('root_priority_sources_20261006/private_sources/turaev2002_survey.pdf','ac7627fd50bb03ff1892555f5ad0261456103ced68daa1003029580924a08960'),
 ('root_priority_sources_20261006/private_sources/truman2006.pdf','1ba67777597b25eded6d113c7c448bdb038ac3c3354b21e38a1e6d2c185aba45'),
 ('root_priority_sources_20261006/private_sources/nicolaescu_book.pdf','a1be7c78b27a08c8643f4a68b8f7f85f1692168b413ac876ad39b43e8fe7a8b5'),
 ('root_priority_sources_20261006/private_sources/truman_thesis2006.pdf','3c77621dd7b99bae783e81bcc2202c2bb544ddb8579dc816e1bce679226465f3'),
 ('root_priority_sources_20261006/private_sources/ye2023.pdf','a0826ffde2756ece13fe0e111505892b0f40c57d9926147542fe614db654672c'),
 ('original_conjecture_priority_adversary_20261006/private_sources/turaev_frontmatter.pdf','e93ab1a4ccdafaf6975dff9810ff54c26c1f36ed0a7fc52fb063448c899b16a9'),
 ('original_conjecture_priority_adversary_20261006/private_sources/turaev_backmatter.pdf','bc3f64fe9570826942f058ea7bd78b86f64d5f3ff24912f45b9fee8beef31e5f')]:
 path=A/relative;req(path.read_bytes().startswith(b'%PDF-'),'Actual PDF source '+relative);sources.append(pin(path,h))
req(len(sources)==11 and len(math_family_pins)==47,'Primary/math counts')
receipt={'schema':'pr124-root-priority-family-full-body-authentication/v1','actual_operator_PID':os.getpid(),'UTC':now(),'families':verified,'priority_public_member_count':27,'priority_manifest_count':4,'original17_unchanged':originals,'mathematical47_members_unchanged':math_family_pins,'root_source_PDFs_authenticated':sources,'root_source_PDF_count':11,'mathematical_gate_pin':math_gate_pin,'root_full_reports_read':True,'earlier_actual_mathematical_child_replays':58,'this_operator_mathematical_child_replays':0,'source_audits_are_not_new_proof_search':True,'new_central_proof_search_turns':0,'original_attempts':'2/5','novelty_clearance':False,'priority_clearance':False,'publication_clearance':False,'shared_index_tracked_native_service_mutations':False}
dump(receipt_path,receipt)
gate={'schema':'pr124-priority-and-contribution-gate/v1','UTC':now(),'status':'WITHHELD_SOURCE_ACCESS_AND_APPLICATION_PRIORITY_UNRESOLVED','original_head':original['original_head'],'original_attempts':'2/5','native_literal_status':'claimed_solved','mathematical_and_source_status':'PASS','math_source_completion_estimate_percent':100,'bounded_priority_family_assignments_percent':100,'decisive_priority_completion_estimate_percent':70,'overall_PR_workflow_completion_estimate_percent':35,'publication_completion_percent':0,'counterexample_valid':True,'old_all_prime_formal_consequence_verified':True,'earlier_explicit_original_conjecture_refutation_located':False,'absence_of_earlier_refutation_established':False,'current_openness_established':False,'new_application_possible_but_unestablished':True,'blanket_already_solved_no_new_contribution_supported':False,'unread_material_book':'Vladimir Turaev, Torsions of 3-dimensional Manifolds (2002), DOI10.1007/978-3-0348-7999-6','exact_needed_book_locations':['II.3 pp22–23','II.4.4 pp23–26','II.5 pp27–30','III.4.3 pp45–51','VIII.5 pp114–118 for realization scope'],'book_access_question_pending':True,'other_source_gaps':['Explicit earlier Conjecture12.26/pair resolution remains unlocated','Alcaraz thesis; Turaev1976 and1989 fulltext not authenticated','Precise rank-one polynomial-part equivalence between Truman/Ye citations; characteristic2 torsion normalization route unverified'],'root_priority_authentication':'ROOT_PRIORITY_FAMILY_AUTHENTICATION_20261006.json','priority_clearance':False,'publication_clearance':False,'PR_disposition':'Remain open; no status change, close, merge, paper, DOI or tracker action authorized by this incomplete priority gate','no_global_qualified_note_exception':True,'program_completed':20,'eligible_dated_denominator':99,'program_completion_estimate_percent':20.2020202020202,'published_count':11,'goal_active':True,'ordered_cursor_may_advance':False,'new_central_proof_search_turns':0}
dump(A/'ROOT_PRIORITY_GATE_20261006.json',gate)
print(json.dumps({'actual_operator_PID':os.getpid(),'UTC':receipt['UTC'],'public_priority_members':27,'sealed_priority_families':4,'original_files_unchanged':17,'math_members_unchanged':47,'authenticated_PDFs':11,'priority_gate':gate['status'],'publication_clearance':False}))
