#!/usr/bin/env python3
"""Pure offline custody/report closure. No writes, network, subprocess or replay."""
from pathlib import Path,PurePosixPath
from copy import deepcopy
from fractions import Fraction as F
import hashlib,json,stat,sys,zipfile
P=Path(__file__).resolve().parent;S=P.parents[1]/'sources'
R_SHA='9ab3aa2364dbc078c0cae228e9a627b75586a6da5f9a1a4c2111391c5bd5ca20'
I_SHA='8a1ab282d865d18607417c6d2265a4925c00323f80efdb127db82b641f4f1962'
TERMINAL={'OWNED_MANIFEST.json','CLOSURE.json','SEAL.json'};COUNT=0
def ck(ok,msg):
 global COUNT
 COUNT+=1
 if not ok:raise ValueError(msg)
def h(p):return hashlib.sha256(Path(p).read_bytes()).hexdigest()
def j(p):return json.loads(Path(p).read_text())
def bound(p,e):
 p=Path(p);ck(p.is_file() and not p.is_symlink(),'regular file '+str(p));ck(p.stat().st_size==e['bytes'] and h(p)==e['SHA256'],'size/SHA256 '+str(p))
def valid(v):
 assert v['schema']=='row119_literal_scope_verdict_v1' and v['record_id']==22983513 and v['native_version']=='1.0.1'
 assert v['full_original_claim_supported'] is True and v['substantive_mathematical_gap'] is None and v['new_repair_or_narrowed_substitute'] is False
 c=v['exact_category'];assert c['dimension']=='every integer n>=1' and c['domain']=='every nonempty bounded open subset of Euclidean R^n'
 assert c['operator']=='form-defined Dirichlet Laplacian on H0^1(Omega)' and c['gap_index']=='every finite integer J>=1' and c['Yang_threshold']=='every real z>E1'
 for k in ('connectedness_required','boundary_regularity_required','H2_operator_domain_identification_assumed','threshold_endpoint_z_equals_E1_strict','positive_gap_or_simple_spectrum_required'):assert c[k] is False
 assert v['normalization']['corrected_second_moment']=='M2^2=(n+4)/n mean(E^2)'
 assert v['normalization']['literal_unsquared_OWR_display_promoted'] is False and v['normalization']['adjacent_quantitative_growth_or_EJ_le_Mp_claimed_solved'] is False
 assert all(v['independent_proof_checks'].values())
 for k in ('classical_trace_and_nonstrict_Yang_new','worldwide_firstness_verified','worldwide_2026_open_status_verified','uniform_scale_independent_positive_deficit_claimed','final_AMS1997_PDF_obtained','Ash2002_fresh_publisher_transport_authenticated'):assert v['credit_and_limits'][k] is False
 for k in ('current_sibling119_science_read','archived_review_bodies_read','human_peer_review','proof_assistant_certification','root119_initial_gate_open_at_finalization','scientific_release_authorized','publication_site_sheet_git_authority'):assert v['review_status'][k] is False
 assert v['review_status']['root_adoption'] is None and v['follow_up'] is None
 assert v['verification']['finite_checks_formalize_analytic_proof'] is False
 assert v['source_ready_SHA256']==R_SHA and v['initial_seal_SHA256']==I_SHA
def main():
 ck(h(S/'SOURCE_READY.json')==R_SHA,'source-ready exact original');ck(h(P/'INITIAL_SEAL.json')==I_SHA,'early independent seal unchanged')
 inp=j(P/'INPUT_MANIFEST.json');own=j(P/'OWNED_MANIFEST.json')
 for e in inp['inputs']:bound(e['path'],e)
 actual={str(q.relative_to(P)) for q in P.rglob('*') if q.is_file() and str(q.relative_to(P)) not in TERMINAL}
 ck(actual=={e['path'] for e in own['files']},'exact owned file set')
 for e in own['files']:
  q=P/e['path'];ck(q.resolve().is_relative_to(P),'owned confinement');bound(q,e)
 r=j(S/'SOURCE_READY.json');ck(r['version']=='1.0.1' and r['publication_date']=='2026-09-23','literal native version/declaration')
 ck(r['created']=='2026-09-26T22:07:10.253036+00:00' and r['updated']=='2026-10-10T21:31:59.357714+00:00','creation/update kept distinct')
 ck(r['selected_actual_PDF']['pages']==3 and r['controlling_TeX']['lines_mechanically_counted_not_displayed']==173,'actual PDF/TeX identity')
 ck(r['target_manuscript_scientifically_read'] is False and r['target_PDF_pages_rendered'] is False,'historical acquisition flags not overwritten')
 objs={e['role']:j(e['path']) for e in r['whole_native_API_objects']}
 ck(isinstance(objs['record']['files'],list) and isinstance(objs['files']['entries'],list) and objs['files']['order']==[] and objs['files']['default_preview'] is None,'whole native schemas/order/nulls')
 ck(objs['record']['files']==[a['original_api_file_object'] for a in r['all_assets_in_original_order']],'whole native file objects and order')
 ck([a['original_api_file_object']['key'] for a in r['all_assets_in_original_order']]==['source-and-verification.zip','paper.pdf','SHA256SUMS.txt'],'exact native three-asset order')
 for a in r['all_assets_in_original_order']:
  b=Path(a['path']).read_bytes();ck(hashlib.md5(b).hexdigest()==a['MD5']==a['original_api_file_object']['checksum'].removeprefix('md5:'),'original native MD5');ck(hashlib.sha256(b).hexdigest()==a['SHA256'] and len(b)==a['bytes'],'whole asset SHA/size')
 transports=j(r['actual_transport_receipt_path']);ck(isinstance(transports,list) and len(transports)==8,'literal list of eight native receipts')
 ck(sum(t['HTTP_status']==400 for t in transports)==1 and sum(t['HTTP_status']==200 for t in transports)==7,'failed version transport preserved alongside successes')
 for t in transports:bound(t['body_path'],t);ck(isinstance(t['response_headers_in_order'],list),'native header order retained')
 a=j(r['whole_archive_custody_path']);ck(isinstance(a['safe_regular_occurrences'],list) and len(a['archive_containers'])==1 and len(a['safe_regular_occurrences'])==30 and a['expanded_bytes_all_depths']==255407 and a['nested_archive_count']==0,'exact whole archive coverage, native occurrence list retained')
 container=a['archive_containers'][0]
 with zipfile.ZipFile(container['origin']) as z:
  infos=z.infolist();entries=container['entries_in_original_order'];ck(len(infos)==len(entries)==30 and z.testzip() is None,'whole ZIP directory/CRC')
  for inf,e in zip(infos,entries):
   path=PurePosixPath(inf.filename);ck(not path.is_absolute() and '..' not in path.parts and stat.S_ISREG(inf.external_attr>>16),'safe regular payload')
   ck(inf.filename==e['original_member_name'] and inf.CRC==int(e['CRC32'],16) and inf.file_size==e['bytes'] and inf.compress_size==e['compressed_bytes'] and inf.external_attr==e['native_external_attr'] and list(inf.date_time)==e['native_date_time'] and inf.flag_bits==e['native_flags'] and inf.compress_type==e['native_compression'],'native payload order/CRC/size/date/attrs/flags')
   ck(hashlib.sha256(z.read(inf)).hexdigest()==e['SHA256']==h(e['extracted_path']),'whole extracted body matches native original')
 ck(h(r['selected_actual_PDF']['path'])==h(r['all_embedded_PDF_members'][0]['extracted_path']),'standalone/embedded reader equality')
 for rp in sorted((P/'primary').glob('*.receipt.json')):
  t=j(rp);bound(t['path'],t);ck(Path(t['path']).read_bytes().startswith(b'%PDF-')==t['actual_PDF'],'primary body signature');ck(isinstance(t['headers_ordered'],list),'ordered whole primary transport')
 ash=j(P/'primary/ASH_HISTORICAL_CUSTODY.json');bound(ash['owned_copy'],ash);ck(ash['SHA256']=='453638f18bba69a103f65d724ae3a062adedff6a61cdc2be351f6a679b17eb69' and ash['fresh_publisher_transport_authenticated'] is False,'historical actual Ash body, no fresh transport substitution')
 ck(b'Proposition 6' in (P/'primary/HS1995.amstex').read_bytes(),'actual HS original source body retained')
 v=j(P/'VERDICT.json');valid(v);ck(True,'literal custom full-scope verdict')
 mutants=[(('exact_category','dimension'),'n>=2'),(('exact_category','boundary_regularity_required'),True),(('exact_category','connectedness_required'),True),(('exact_category','positive_gap_or_simple_spectrum_required'),True),(('exact_category','threshold_endpoint_z_equals_E1_strict'),True),(('exact_category','Yang_threshold'),'only eigenvalue thresholds'),(('normalization','literal_unsquared_OWR_display_promoted'),True),(('normalization','adjacent_quantitative_growth_or_EJ_le_Mp_claimed_solved'),True),(('credit_and_limits','worldwide_firstness_verified'),True),(('credit_and_limits','classical_trace_and_nonstrict_Yang_new'),True),(('credit_and_limits','Ash2002_fresh_publisher_transport_authenticated'),True),(('credit_and_limits','uniform_scale_independent_positive_deficit_claimed'),True),(('verification','finite_checks_formalize_analytic_proof'),True),(('review_status','human_peer_review'),True),(('review_status','proof_assistant_certification'),True),(('review_status','publication_site_sheet_git_authority'),True)]
 for route,value in mutants:
  m=deepcopy(v);m[route[0]][route[1]]=value
  try:valid(m)
  except AssertionError:ck(True,'synthetic semantic mutation rejected '+'.'.join(route))
  else:raise ValueError('accepted synthetic mutant '+str(route))
 ck(j(P/'SUPPLIED_NORMAL.json')==j(P/'SUPPLIED_OPTIMIZED.json')==j(S/'attempts/20261115T032014Z/published-source/owr_3389_016_strict_gap/verification/results.json'),'complete normal/optimized/original result equality')
 ck(h(P/'supplied_verify_copy.py')=='79d3698942534faf50418495300ca052634913a20aac2b90b8672b0e09e73ccf','exact inspected supplied checker copy')
 q=j(P/'INDEPENDENT_CHECKS.json');ck(q['status']=='PASS' and q['gap_cases']==960 and q['strict_real_threshold_cases']==1134 and q['repeated_ground_branch_cases']==2,'meaningful retained independent coverage')
 for t in q['infinite_support_fourier_witnesses']:
  z=F(t['z']);k=t['even_mode_above_threshold'];c=F(-8*k,(k*k-1)**2);ck(k%2==0 and k*k>z and F(t['pi_times_coordinate_coefficient'])==c and F(t['pi_squared_times_positive_remainder_summand'])==(z-1)*(k*k-1)*(k*k-z)*c*c>0,'exact infinite-support positive-tail witness')
 ledger=j(P/'READ_LEDGER.json');ck(ledger['personally_read_PDF_pages']==[1,2,3] and ledger['all_TeX_lines_personally_read']==173 and ledger['foreign_bodies_code_results_or_opinions119_read_before_initial'] is False,'whole personal target reading/initial independence ledger')
 sealed=False
 if (P/'SEAL.json').exists():
  seal=j(P/'SEAL.json')
  for name,key in [('REPORT.md','REPORT_SHA256'),('VERDICT.json','VERDICT_SHA256'),('INPUT_MANIFEST.json','INPUT_MANIFEST_SHA256'),('OWNED_MANIFEST.json','OWNED_MANIFEST_SHA256'),('CLOSURE.json','CLOSURE_SHA256')]:ck(h(P/name)==seal[key],'terminal seal '+name)
  sealed=True
 print(json.dumps({'status':'PASS','read_only':True,'network_subprocess_program_replay_or_writes':False,'checks':COUNT,'input_files':len(inp['inputs']),'owned_files':len(own['files']),'whole_native_payloads':30,'semantic_mutants_rejected':len(mutants),'final_seal_checked':sealed,'scope':'whole-byte custody, original schema and report consistency; not a formal analytic proof checker'},indent=2))
if __name__=='__main__':
 try:main()
 except Exception as e:print(json.dumps({'status':'FAIL','checks_completed':COUNT,'error':str(e)}));sys.exit(1)
