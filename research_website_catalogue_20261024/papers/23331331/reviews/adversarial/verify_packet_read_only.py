#!/usr/bin/env python3
"""Strict pure offline custody. No project imports, subprocesses, science or writes."""
from pathlib import Path, PurePosixPath
import binascii, hashlib, json, stat, sys, zipfile
O=Path(__file__).resolve().parent
EXCLUDED={'OWNED_MANIFEST.json','FINAL_SEAL.json'}
N=0
def need(v,m):
 global N
 N+=1
 if not v:raise RuntimeError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def load(p):return json.loads(p.read_text())
def typed(a,b):
 if type(a) is not type(b):return False
 if isinstance(a,dict):return list(a)==list(b) and all(typed(a[k],b[k]) for k in a)
 if isinstance(a,list):return len(a)==len(b) and all(typed(x,y) for x,y in zip(a,b))
 return a==b
def bound(row,base=None):
 if base:
  s=row['path'];q=PurePosixPath(s);need(not q.is_absolute() and '..' not in q.parts and str(q)==s,'Unsafe owned path');p=base/s;need(p.resolve().is_relative_to(base),'Owned path escape')
 else:p=Path(row['path']);need(p.is_absolute(),'External path must be absolute')
 need(p.is_file() and not p.is_symlink(),'Missing or symlink byte input '+str(p));b=p.read_bytes();need(len(b)==row['bytes'] and sha(b)==row.get('SHA256',row.get('sha256')),'Changed bytes '+str(p));return b
def main(preseal):
 m=load(O/'OWNED_MANIFEST.json');need(m['excluded_terminal_files']==sorted(EXCLUDED),'Owned terminal exclusion set');owned=set()
 for r in m['files']:bound(r,O);need(r['path'] not in owned,'Duplicate owned path');owned.add(r['path'])
 need(owned=={p.relative_to(O).as_posix() for p in O.rglob('*') if p.is_file()}-EXCLUDED,'Complete own inventory')
 sm=load(O/'SOURCE_INPUT_MANIFEST.json');S=Path(sm['source_root']);source_paths=set()
 for r in sm['files']:bound(r);need(r['path'] not in source_paths,'Duplicate source input');source_paths.add(r['path'])
 need(len(source_paths)==87 and source_paths=={str(p) for p in S.rglob('*') if p.is_file()},'Complete unchanged87source namespace')
 readyb=(S/'SOURCE_READY.json').read_bytes();ready=json.loads(readyb);seal=load(S/'SOURCE_READY_SEAL.json')
 need(sha(readyb)=='28a9736d92beaadb1faa37c9146d56191be83fb217116f24b33162bea922e469','Assigned whole sourceREADY identity')
 need(sha((S/'SOURCE_READY_SEAL.json').read_bytes())=='c523e830e06555037254c26d9d85c82f4324c841cdd268f99d95664bf02e2150','Assigned source seal identity')
 need(seal['SOURCE_READY_SHA256']==sha(readyb) and seal['MANIFEST_SHA256']==sha((S/'SOURCE_READY_MANIFEST.json').read_bytes()),'Native source seal/manifest')
 old=load(S/'SOURCE_READY_MANIFEST.json')
 for r in old['files']:bound(r,S)
 need(len(old['files'])==84 and {r['path'] for r in old['files']}=={p.relative_to(S).as_posix() for p in S.rglob('*') if p.is_file()}-set(old['excluded_terminal_files']),'Original source owned completeness')
 need(seal['CLOSURE_SHA256']==sha((S/'SOURCE_READY_CLOSURE.json').read_bytes()),'Original source closure bytes')
 protocol=load(O/'NATIVE_PROTOCOL_IDENTITY.json');verdict=load(O/'CUSTOM_VERDICT.json')
 need(typed(protocol['whole_original_SOURCE_READY'],ready) and typed(verdict['whole_original_SOURCE_READY'],ready),'Whole typed/order/null original READY retained twice')
 for item in protocol['whole_API_objects']:
  b=bound(item['original_binding']);need(typed(item['actual_parsed_whole_object'],json.loads(b)),'Whole original native API types/key/list order')
 need(typed(protocol['whole_original_transport_aggregate'],load(S/'ALL_TRANSPORT_RECEIPTS.json')),'Whole original native transport aggregate order')
 native_record=next(x['actual_parsed_whole_object'] for x in protocol['whole_API_objects'] if x['original_binding']['role']=='record')
 need(str(native_record['id'])=='23331331' and native_record['doi']=='10.5281/zenodo.23331331','Actual native target')
 need(native_record['metadata']['version']==ready['version']==verdict['native_version']=='1.0','Original native version')
 need(native_record['metadata']['publication_date']==ready['publication_date']==verdict['native_publication_date']=='2026-10-13','Original native declared publication')
 for row in ready['all_native_assets_in_original_order']:
  b=bound(row);api=row['original_api_file_object'];need(len(b)==api['size'] and hashlib.md5(b).hexdigest()==api['checksum'].split(':')[1],'Whole native asset original MD5/size')
  need(Path(row['transport_body_path']).read_bytes()==b,'Actual native transport body/asset equality')
 pdf=ready['selected_actual_PDF'];bound(pdf);need(pdf['pages']==5,'Five actual PDF pages')
 tex=ready['controlling_TeX'];tb=Path(tex['extracted_path']).read_bytes();need(len(tb)==tex['bytes'] and sha(tb)==tex['SHA256'] and len(tb.splitlines())==342,'Whole342-line controlling TeX')
 prep=load(O/'MANUSCRIPT_PREPARATION.json');need(typed(prep['source_PDF'],pdf) and typed(prep['controlling_TeX'],tex),'Actual manuscript intake pins')
 need(len(prep['fresh_individual_rasters'])==5 and all(Path(x).is_file() for x in prep['fresh_individual_rasters']),'Five own fresh individual rasters')
 initial=load(O/'INITIAL_SEAL.json');need(initial['INITIAL_MANIFEST_SHA256']==sha((O/'INITIAL_MANIFEST.json').read_bytes()) and initial['INITIAL_RECONSTRUCTION_SHA256']==sha((O/'INITIAL_RECONSTRUCTION.md').read_bytes()),'Immutable initial reconstruction seal')
 im=load(O/'INITIAL_MANIFEST.json')
 for r in im['files']:bound(r)
 need(im['actual_complete_PDF_pages_personally_read']==5 and im['controlling_TeX_lines_personally_read']==342 and im['own_fresh_individual_rasters_personally_viewed']==5 and im['distinct_attack_families']==11,'Initial reading scope ledger')
 proof=load(O/'OWN_PROOF_RESULTS_SEAL.json');need(proof['OWN_PROOF_RESULTS_MANIFEST_SHA256']==sha((O/'OWN_PROOF_RESULTS_MANIFEST.json').read_bytes()) and proof['DERIVATIONS_SHA256']==sha((O/'DERIVATIONS.md').read_bytes()),'Immutable pre-native own-proof/result seal')
 pm=load(O/'OWN_PROOF_RESULTS_MANIFEST.json')
 for r in pm['files']:bound(r,O)
 need(pm['supplied_code_results_foreign_scientific_bodies_or_opinions_read'] is False and proof['pre_native_and_pre_foreign_freeze'] is True,'Own result independence boundary')
 ownrun=load(O/'OWN_EXACT_EXECUTION.json')['actual_tool_result'];need(ownrun['exit_code']==0 and json.loads(ownrun['output'])['predicate_count_including_ring_and_denominator_guards']==811,'Actual frozen own exact result receipt')
 isolated=load(O/'ISOLATED_PAYLOAD_MANIFEST.json');rows=isolated['unchanged_regular_payloads'];need(len(rows)==isolated['copied_payload_count']==38,'Whole original isolated payload count')
 Z=Path(isolated['whole_original_ZIP']['path']);bound(isolated['whole_original_ZIP']);names=[]
 with zipfile.ZipFile(Z) as z:
  actual=[i for i in z.infolist() if not i.is_dir()];need(len(actual)==38,'Original ZIP regular member count')
  for i,r in zip(actual,rows):
   q=PurePosixPath(i.filename);need(not q.is_absolute() and '..' not in q.parts and i.filename.casefold() not in names,'Safe unique ZIP member');names.append(i.filename.casefold())
   mode=i.external_attr>>16;need(not mode or stat.S_ISREG(mode),'Only regular payloads')
   b=z.read(i);need(i.filename==r['original_member_name'] and len(b)==i.file_size==r['bytes'] and sha(b)==r['SHA256'] and format(binascii.crc32(b)&0xffffffff,'08x')==r['CRC32']==format(i.CRC,'08x'),'Whole original ZIP CRC/size/SHA')
   need((i.compress_type,i.external_attr,i.flag_bits,list(i.date_time))==(r['compression_method'],r['external_attr'],r['flags'],r['native_date_time']),'Original archive metadata retained')
   need(Path(r['source_path']).read_bytes()==Path(r['isolated_path']).read_bytes()==b,'Unchanged original/source/isolated whole payload')
 need({str(p) for p in (O/'native-isolated').rglob('*') if p.is_file()}=={r['isolated_path'] for r in rows},'No isolated payload additions or overwrites')
 runtime=load(O/'RUNTIME_METADATA.json');need(runtime['exit_code']==0 and runtime['actual_stderr']=='' and runtime['parsed']['versions']=={'sympy':'1.14.0','mpmath':'1.3.0','numpy':'2.3.4','scipy':'1.16.3'},'Actual pinned native runtime dependencies')
 replay=load(O/'NATIVE_REPLAY_RECEIPTS.json');comparison=load(O/'NATIVE_BASELINE_COMPARISON.json');need(replay['sole_native_selected_checker']=='author/verify.py' and len(replay['runs'])==2,'Sole selected native route')
 actual_outputs=[]
 for run in replay['runs']:
  need(run['exit_code']==0 and run['timeout'] is False,'Actual selected checker exit')
  for role in ['stdout','stderr']:
   b=Path(run[role+'_path']).read_bytes();need(len(b)==run[role+'_bytes'] and sha(b)==run[role+'_SHA256'],'Whole actual native output receipt')
  need(run['stderr_bytes']==0 and run['source_SHA256_after']=='dca748ae931ba5276a16dedd00c502d474a5ac78957b30f87b4846e64c884bbb','Native unchanged source/empty error output')
  actual_outputs.append(Path(run['stdout_path']).read_bytes())
 need(actual_outputs[0]==actual_outputs[1] and len(actual_outputs[0])==2369 and sha(actual_outputs[0])=='21b99f1d150f011d89610ca29afe467138af2894a05fb8226135e9a1533fbf50','Both actual complete outputs and archived hash')
 output=json.loads(actual_outputs[0]);need(typed(output,comparison['whole_actual_ordinary_output']),'Every actual output field typed/order equality')
 baseline=load(Path(comparison['baseline_path']));need(typed(baseline,comparison['whole_original_native_baseline_object']),'Whole actual original baseline interface')
 expected=next(r for r in baseline['replays'] if r['replay']=='AUTHOR_REPLAY');need(typed(expected,comparison['selected_whole_baseline_entry']) and expected['output_sha256']==sha(actual_outputs[0]),'Literal archived expected whole hash')
 need(output['exact_assertions']==expected['exact_controls']==63 and sum(output['exact_families'].values())==63,'All exact native output counts')
 nd=output['numerical_diagnostics'];need(nd['defined_centroid_cases']==expected['numeric_controls']==1984 and nd['simple_positive_area_cases']==704 and nd['undefined_circle_cases']==224,'Actual numerical output categories')
 need(replay['runs'][0]['assertions_enabled'] is True and replay['runs'][1]['assertions_enabled'] is False and comparison['optimized_assertions_disabled_not_counted_as_science_verification'] is True,'Optimized mode qualification')
 primary=load(O/'PRIMARY_READ_LEDGER.json');need(len(primary['sources'])==5 and len(primary['primary_rasters_personally_viewed'])==8,'Bounded actual primary reading')
 for row in primary['sources']:bound(row['complete_downloaded_body']);need(row['whole_paper_proof_audit_claimed'] is False,'Primary full-proof limits')
 transport=load(Path(primary['actual_transport_receipts']));need(len(transport)==5 and all(r['status']==200 for r in transport),'Five complete ordinary primary GETs')
 for row in transport:
  b=Path(row['body_path']).read_bytes();need(len(b)==row['bytes'] and sha(b)==row['SHA256'] and sha(Path(row['complete_text_path']).read_bytes())==row['text_SHA256'],'Actual whole primary bodies/text')
  need(all(type(p) is list and len(p)==2 and all(type(s) is str for s in p) for p in row['headers_in_received_order']),'Actual primary header pair order')
 need(verdict['central_mathematical_gap'] is None and verdict['substantive_defect_found'] is False and verdict['source_repair'] is False and verdict['narrowed_replacement'] is False,'Literal scientific disposition')
 need(verdict['root_gate_at_sealing']=='CLOSED' and verdict['current_root_or_scope_scientific_findings_read'] is False and verdict['scientific_findings_sent_before_explicit_root_OPEN'] is False,'Closed gate exposure boundary')
 need(verdict['follow_up'] is None and verdict['canonical_url'] is None and verdict['AA'] is None and verdict['publication_authority'] is False and verdict['source_old_packets_site_core_Sheet_Git_deploy_redirect_contact_mutations'] is False,'No publication/mutation authority')
 if not preseal:
  final=load(O/'FINAL_SEAL.json');need(final['OWNED_MANIFEST_SHA256']==sha((O/'OWNED_MANIFEST.json').read_bytes()),'Final owned manifest seal')
  for n,v in final['selected_payload_SHA256'].items():need(v==sha((O/n).read_bytes()),'Final selected payload seal '+n)
 print(json.dumps({'verdict':'PASS_CUSTODY_ONLY','mode':'preseal' if preseal else 'sealed','checks':N,'owned_payloads':len(owned),'source_files_unchanged':87,'whole_regular_ZIP_payloads':38,'actual_PDF_pages':5,'controlling_TeX_lines':342,'primary_bodies':5,'selected_native_runs_in_receipts':2,'scientific_or_prior_code_executions_by_this_helper':0,'network_requests':0,'writes':0,'subprocesses':0},sort_keys=True))
if __name__=='__main__':
 need(sys.argv[1:] in [[],['--preseal']],'Usage: verify_packet_read_only.py [--preseal]')
 main(sys.argv[1:]==['--preseal'])
