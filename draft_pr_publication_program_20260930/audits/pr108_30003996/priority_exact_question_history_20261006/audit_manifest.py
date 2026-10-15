#!/usr/bin/env python3
"""Bind only this audit folder and explicitly named read-only inputs."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib, json, os, sys
D=Path(__file__).resolve().parent
A=D.parent
EMPTY=hashlib.sha256(b'').hexdigest()
def digest(p):
 b=p.read_bytes()
 return {"path":str(p),"bytes":len(b),"sha256":hashlib.sha256(b).hexdigest()}
def emit(name,obj):
 (D/name).write_text(json.dumps(obj,indent=2,ensure_ascii=False)+'\n')
def now(): return datetime.now(timezone.utc).isoformat()
def metadata():
 # Result headings produced by PDF search sometimes contain paragraphs. Publish URLs only.
 p=D/'SEARCH_RECEIPT.json'; s=json.loads(p.read_text())
 r=json.loads((D/'private/search17_metadata.json').read_text())
 if not any(x['id']=='search17' for x in s['rows']): s['rows'].append(r)
 for row in s['rows']:
  row['results']=[{'url':x['url']} for x in row.get('results',[])]
 s['search_query_count']=sum(len(r['queries']) for r in s['rows'])
 s['web_call_count']=len(s['rows'])
 s['result_metadata_policy']='URLs only. PDF-derived headings may be copyrighted prose and are deliberately omitted.'
 emit('SEARCH_RECEIPT.json',s)
 paths=[
 Path('/Users/alec/Documents/Math/AGENTS.md'),
 Path('/Users/alec/Documents/Math/unsolved_math_prioritization/AGENTS.md'),
 A/'primary_sources_20261006/owr.pdf',
 A/'ROOT_MATHEMATICAL_GATE_20261006.json',
 A/'repaired_diagnostics_v1/PROOF.md',
 A/'original_source_authentication_20261006/SELECTED_IMPORTED_PRIOR_REPORT.json',
 A/'original_source_authentication_20261006/QUEUE_STATUS_PROJECTION.json',
 A/'original_source_authentication_20261006/ORIGINAL_BLOB_MANIFEST.json',
 ]
 old=A/'original_source_authentication_20261006/original_attempt'
 paths += [old/x for x in ['source_record.json','source_manifest.json','README.md','RESEARCH_LOG.md','PROOF.md','independent_review/REVIEW.md']]
 emit('INPUT_BINDINGS.json',{'schema':'priority-audit-input-bindings/v1','utc':now(),'operator_pid':os.getpid(),'read_scope':'Instructions, source, original provenance, proof and mathematical gate only; no current peer priority report or root priority conclusion','original_head':'3526d46bf143b08e5055ffa7728c6278e9f958ea','files':[digest(p) for p in paths]})
 receipts=[]
 for p in sorted((D/'private').glob('*.json')):
  if 'receipt' in p.name:
   receipts.append({'custody':str(p.relative_to(D)),**digest(p),'data':json.loads(p.read_text())})
 gaps=[
 {'operation':'Initial pilot shell inventory','actual_pid':None,'argv':None,'exit_code':0,'stdout_sha256':None,'reason':'Not instrumented before receipts were introduced; exact argv and PID not retained in audit artifacts.'},
 {'operation':'Failed sparse-checkout README read after proof reading','actual_pid':None,'argv':None,'exit_code':1,'stdout_sha256':None,'reason':'FileNotFoundError in pilot wrapper. No complete process receipt was written. Successful full proof read is independently file-bound later.'},
 {'operation':'Corrected effective-proof/README/selected-QUEUE read','actual_pid':7219,'python_sys_argv':['-'],'exit_code':0,'stdout_sha256':None,'reason':'Read event/file hashes retained, full stdout not retained and UI output truncated. Entire effective proof was read.'},
 {'operation':'Later local inventory, original log and mathematical-gate read','actual_pid':13017,'python_sys_argv':['-'],'exit_code':0,'stdout_sha256':None,'reason':'Actual PID printed and tool exit observed; full stdout hash not retained. Gate and log are bound as inputs.'},
 {'operation':'search15 raw response','actual_pid':None,'argv':None,'exit_code':None,'stdout_sha256':None,'reason':'Web tool exposes no CLI PID; returned result was printed without retained raw store. Exact queries and selected primary URLs retained.'}
 ]
 emit('EXECUTION_LEDGER.json',{'schema':'priority-audit-execution-ledger/v1','utc':now(),'meaning':'Actual instrumented process and file-read receipts; missing values are gaps, not reconstructed measurements. Web-tool process metadata is not exposed. apply_patch is a tool mutation and not a claimed CLI run.','receipts':receipts,'instrumentation_gaps':gaps})
 sources=[
 {'id':'Kaibel2018','primary_url':'https://ems.press/content/serial-article-files/46772','metadata_urls':['https://ems.press/journals/owr/articles/16633','https://publications.mfo.de/handle/mfo/3672'],'read_scope':'Full Kaibel contribution, printed3014–3015/PDF46–47, FIRST, extraction at2026-10-06T04:59:45.988503+00:00. Adjacent contributions not attributed to Kaibel.','custody':str(A/'primary_sources_20261006/owr.pdf'),'extract':'private/kaibel_pdf46_47.txt','receipt':'private/receipt_initial_reads.json','status':'Exact question authenticated; historical wording not status proof','full_material_text_read':True},
 {'id':'ScaleFree2020','primary_url':'https://arxiv.org/abs/2005.13703','download_url':'https://arxiv.org/pdf/2005.13703v1','read_scope':'Entire27-page author preprint, pages1–8,9–18,19–27, including proofs/formulas/bibliography.','custody':'private/scale_free_2005.13703v1.pdf','extract':'private/scale_free_2005.13703v1.pdf.txt','receipt':'private/scale_free_2005.13703v1.pdf.receipt.json','read_receipts':['private/scale_free_read_1_8.receipt.json','private/scale_free_read_9_18.receipt.json','private/scale_free_read_19_27.receipt.json'],'status':'Material near match fully checked; added product variables / degree objectives, no exact transfer established','full_material_text_read':True},
 {'id':'RoutingModels2021','primary_url':'https://schmiste.github.io/tnsm21routing.pdf','alternative_primary_url':'https://eprints.cs.univie.ac.at/6946/1/6-tnsm21routing.pdf','read_scope':'Entire14-page author PDF, pages1–7,8–14 plus entirepage4 reread to fill UI truncation. Whitespace compacted for display; no semantic content intentionally removed.','custody':'private/routing_2021.pdf','extract':'private/routing_2021.pdf.txt','receipt':'private/routing_2021.pdf.receipt.json','read_receipts':['private/routing_read_1_7.receipt.json','private/routing_read_8_14.receipt.json','private/routing_read_page4.receipt.json'],'status':'Material near match fully checked; source–destination path multiplicity/other hardness, no exact transfer established','full_material_text_read':True},
 {'id':'OfficialAuthorBibliography','primary_url':'https://discopt.ovgu.de/people/kaibel.php','followed_url':'https://discopt.ovgu.de/publications/','read_scope':'Full returned author page208lines and publication-list post2018 entries in returned lines0–504; full1605line list not claimed read. Current exact-question search adds2025–2026 queries.','status':'Discovery chain, not exhaustive cited-by graph','full_material_text_read':False},
 {'id':'PublisherMFOmetadata','primary_url':'https://ems.press/journals/owr/articles/16633','second_primary_url':'https://publications.mfo.de/handle/mfo/3672','read_scope':'Returned metadata including dates/workshop/DOIs/license','status':'Primary bibliographic dates and custody restriction','full_material_text_read':True},
 {'id':'OriginalAuthorAndOldReview','primary_url':None,'read_scope':'Full authenticated source_record, source_manifest, originalPROOF/README/prose log, old independentREVIEW after initial freeze; effective repairedPROOF fully read. Original QUEUE projection/manifests read.','status':'Candidate/provenance comparison only; old negative search not proof of novelty','full_material_text_read':True},
 {'id':'Martin1991','primary_url':None,'read_scope':'Bibliographic identification through full scale-free reference list only; original paper not retrieved/read in this family','status':'Formulation citation lead, no concrete located hardness theorem; independent translation family adjudication pending','full_material_text_read':False},
 {'id':'OtherRetrievedLeads','primary_url':None,'read_scope':'Search metadata/snippets only unless individually named above','status':'Not relied on as full-theorem exclusions','full_material_text_read':False}
 ]
 historical=[
 {'search':'search03','scope':'Opened EMS article16633 and MFO handle3672; raw response retained. Exact nonquery arguments not retained in store.'},
 {'search':'search04/search05','scope':'Reopened publisher/MFO metadata at date/license sections; raw responses retained.'},
 {'search':'search06','scope':'Find requests for publication date2019, MFO date and publisher references; raw result retained.'},
 {'search':'search07','scope':'Old author URL and MFO occasion1845/www_view both returned internal errors; alternate official page found.'},
 {'search':'search08','scope':'Opened official author page and PMC full article initial lines1–218; later PMC request blocked by challenge.'},
 {'search':'search09','scope':'Followed official author all-publications link; opened arXiv abstract2005.13703; repeated PMC request returned challenge.'},
 {'search':'search10','scope':'Followed arXiv experimentalHTML; not treated as entire read. Author PDF read separately.'},
 {'search':'search12','scope':'Opened author-hosted routingPDF via web; complete full-text read performed separately by CLI.'}
 ]
 emit('SOURCE_LEDGER.json',{'schema':'priority-audit-source-read-scope/v1','utc':now(),'scope_policy':'Primary sources for substantive literature conclusions. Mirrors and secondary discovery results not relied on as theorems. Raw copyrighted extracts remain private.','sources':sources,'historical_nonsearch_requests':historical,'access_limitations':['PMC challenge after partial read; recovered primary arXivPDF','Old author URL and MFO eventview internal errors','No exhaustive cited-by graph accessed'],'concrete_unevaluated_plausible_exact_antecedents':[]})
 print(json.dumps({'operation':'metadata','utc':now(),'operator_pid':os.getpid(),'python_sys_argv':sys.argv,'inputs':len(paths),'search_queries':s['search_query_count'],'web_calls':s['web_call_count'],'read_receipts':len(receipts),'status':'complete'}))
def seal():
 r=json.loads((D/'METADATA_PROCESS_RECEIPT.json').read_text())
 wr=digest(D/'private/metadata_wrapper.stdout.txt')
 if wr['bytes']!=r['wrapper_tool_stdout_ascii_bytes']: raise SystemExit('captured wrapper stdout byte mismatch')
 r['wrapper_tool_stdout_bytes']=wr['bytes']; r['wrapper_tool_stdout_sha256']=wr['sha256']
 r['orchestration_note']='CLI metadata build succeeded. A subsequent TextEncoder reference in the orchestration isolate failed; exact retained result was recovered without rerunning the CLI.'
 emit('METADATA_PROCESS_RECEIPT.json',r)
 e=json.loads((D/'EXECUTION_LEDGER.json').read_text())
 e['post_build_process_witnesses']=[{'artifact':'METADATA_PROCESS_RECEIPT.json','actual_child_pid':r['actual_child_pid'],'actual_child_exit':r['actual_child_exit'],'wrapper_pid':r['wrapper_pid'],'wrapper_tool_exit':r['wrapper_tool_exit'],'stdout_sha256':r['stdout_sha256'],'wrapper_tool_stdout_sha256':wr['sha256']}]
 emit('EXECUTION_LEDGER.json',e)
 # Final process receipts are retrospective witnesses and excluded from this payload seal.
 exclusions={'PUBLIC_OUTPUT_MANIFEST.json','SHA256SUMS','SEAL_PROCESS_RECEIPT.json','VERIFY_PROCESS_RECEIPT.json','PAYLOAD_INTEGRITY_REPORT.json','SEAL_WRAPPER_STDOUT.jsonl','VERIFY_WRAPPER_STDOUT.jsonl','DELIVERY_SEAL.json'}
 private=[{**digest(p),'relative_path':str(p.relative_to(D))} for p in sorted((D/'private').rglob('*')) if p.is_file()]
 emit('PRIVATE_CUSTODY_MANIFEST.json',{'schema':'priority-audit-private-custody/v1','utc':now(),'public_contents':False,'exclude_from_publication':['private/**'],'private_files':private,'external_private_source':digest(A/'primary_sources_20261006/owr.pdf'),'policy':'Hashes/bytes/paths only; no third-party PDF/text or raw snippets in public payload.'})
 paths=[p for p in sorted(D.iterdir()) if p.is_file() and p.name not in exclusions]
 entries=[{**digest(p),'relative_path':p.name} for p in paths]
 manifest={'schema':'priority-audit-public-payload/v1','utc':now(),'operator_pid':os.getpid(),'files':entries,'excludes':['private/**',*sorted(exclusions)],'exclusion_reason':'Avoid self-reference; final process witnesses/verification are separately byte-hash bound by the final parent delivery seal.'}
 emit('PUBLIC_OUTPUT_MANIFEST.json',manifest)
 lines=['%s  %s'%(r['sha256'],r['relative_path']) for r in entries]
 lines += ['%s  PUBLIC_OUTPUT_MANIFEST.json'%digest(D/'PUBLIC_OUTPUT_MANIFEST.json')['sha256']]
 (D/'SHA256SUMS').write_text('\n'.join(lines)+'\n')
 print(json.dumps({'operation':'seal','utc':now(),'operator_pid':os.getpid(),'python_sys_argv':sys.argv,'public_payload_files':len(entries),'private_custody_files':len(private),'status':'complete'}))
def verify():
 m=json.loads((D/'PUBLIC_OUTPUT_MANIFEST.json').read_text()); errors=[]
 for r in m['files']:
  a=digest(D/r['relative_path'])
  if a['bytes']!=r['bytes'] or a['sha256']!=r['sha256']: errors.append({'file':r['relative_path'],'error':'public binding mismatch'})
 c=json.loads((D/'PRIVATE_CUSTODY_MANIFEST.json').read_text())
 for r in c['private_files']:
  a=digest(D/r['relative_path'])
  if a['bytes']!=r['bytes'] or a['sha256']!=r['sha256']: errors.append({'file':r['relative_path'],'error':'private binding mismatch'})
 for line in (D/'SHA256SUMS').read_text().splitlines():
  h,n=line.split('  ',1)
  if digest(D/n)['sha256']!=h: errors.append({'file':n,'error':'SHA256SUMS mismatch'})
 s=json.loads((D/'SEARCH_RECEIPT.json').read_text())
 if s['search_query_count']!=58 or s['web_call_count']!=17: errors.append({'error':'search count mismatch'})
 if any(set(r)!={'url'} for row in s['rows'] for r in row['results']): errors.append({'error':'public result prose survived sanitization'})
 if any('private/' in r['relative_path'] for r in m['files']): errors.append({'error':'private payload leak'})
 v=json.loads((D/'VERDICT.json').read_text())
 if v['audit_extra_central_proof_search_turns']!=0 or v['original_effort']!='2/5': errors.append({'error':'budget provenance mismatch'})
 report={'schema':'priority-audit-payload-integrity/v1','utc':now(),'operator_pid':os.getpid(),'python_sys_argv':sys.argv,'public_payload_bindings_checked':len(m['files']),'private_custody_bindings_checked':len(c['private_files']),'search_queries':s['search_query_count'],'web_calls':s['web_call_count'],'errors':errors,'status':'pass' if not errors else 'fail','audit_deliverable_completion_percent':100 if not errors else 95,'priority_clearance_percent':0,'not_a_priority_proof':True}
 emit('PAYLOAD_INTEGRITY_REPORT.json',report)
 print(json.dumps(report))
 return bool(errors)
if __name__=='__main__':
 if len(sys.argv)!=2 or sys.argv[1] not in ['metadata','seal','verify']: raise SystemExit('usage: audit_manifest.py metadata|seal|verify')
 if sys.argv[1]=='metadata': metadata()
 elif sys.argv[1]=='seal': seal()
 else: raise SystemExit(1 if verify() else 0)
