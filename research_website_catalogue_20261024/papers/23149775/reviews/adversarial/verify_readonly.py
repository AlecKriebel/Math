"""Read-only custody/evidence verifier. No imports or replay of mathematical checkers."""
from pathlib import Path
import hashlib,json,zipfile,zlib,argparse
E=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23149775/reviews/adversarial');S=E.parents[1]/'sources';N=S/'cache/extracted/container-001'
def load(p):return json.loads(p.read_text())
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def need(ok,label):
 if not ok:raise ValueError(label)
def binding(p,n,h):need(p.stat().st_size==n and sha(p)==h,'binding '+str(p))
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--preseal',action='store_true');args=ap.parse_args()
 need(sha(S/'SOURCE_READY.json')=='4cd6366eabab646cbb7837b7b3854cf931b3fa57fc7de0152d0ff210ab35c16a','native source-ready pin')
 source=load(E/'NATIVE_SOURCE_BINDINGS.json')
 for x in source['all_original_bindings']:binding(Path(x['path']),x['bytes'],x['SHA256'])
 native=load(S/'SOURCE_READY_MANIFEST.json');need(source['whole_original_native_source_manifest']==native,'whole native manifest unchanged')
 ready=load(S/'SOURCE_READY.json')
 for x in ready['all_native_assets_in_original_order']:
  p=Path(x['path']);binding(p,x['bytes'],x['SHA256']);need(hashlib.md5(p.read_bytes()).hexdigest()==x['MD5'],'native MD5')
  need(x['original_api_file_object']['checksum']=='md5:'+x['MD5'],'actual native checksum field')
 zpath=Path(ready['all_native_assets_in_original_order'][1]['path'])
 with zipfile.ZipFile(zpath) as z:
  items=[x for x in z.infolist() if not x.is_dir()];need(len(items)==24,'all 24 ZIP payloads')
  for x in items:
   d=z.read(x);need(zlib.crc32(d)&0xffffffff==x.CRC and d==(N/x.filename).read_bytes(),'ZIP CRC/extraction identity '+x.filename)
 for x in load(N/'MANIFEST.json')['files']:binding(N/x['path'],x['bytes'],x['sha256'])
 initial=load(E/'INITIAL_SEAL.json');need(sha(E/'INITIAL_MANIFEST.json')==initial['manifest_sha256'],'initial manifest/seal')
 for x in load(E/'INITIAL_MANIFEST.json')['files']:binding(Path(x['path']),x['bytes'],x['sha256'])
 exposure=load(E/'INITIAL_READ_EXPOSURE.json');need(exposure['personally_read_actual_PDF_pages']==6 and exposure['personally_read_full_controlling_TeX_lines']==387,'full initial reading')
 for k in ['foreign_primary_bodies_read','source_programs_read_or_executed','supplement_notes_data_results_read','triage_archived_current_peer_opinions_read']:need(exposure[k] is False,'initial independence '+k)
 for x in exposure['personally_inspected_fresh_PDF_renders']:need(sha(Path(x['path']))==x['sha256'],'actual PDF render')
 runs=load(E/'NATIVE_EXECUTION.json');need(runs['normal_execution_assertions_enabled'] is True and len(runs['runs'])==6,'six ordinary native runs')
 published=load(N/'VERIFICATION_RESULTS.json')['runs']
 for run,old in zip(runs['runs'],published):
  p=N/'verification'/run['program'];need(sha(p)==run['original_program_sha256']==run['executed_copy_sha256']==old['program_sha256'],'executed native program identity')
  need(run['exit_code']==0 and run['stderr_bytes']==0 and Path(run['stderr_path']).read_bytes()==b'','successful native run')
  need(sha(Path(run['stdout_path']))==run['stdout_sha256']==old['stdout_sha256'] and Path(run['stdout_path']).read_bytes()==(N/old['stdout_path']).read_bytes(),'published/fresh stdout identity')
 result=load(E/'INDEPENDENT_CHECKS.stdout.json');need(result['status']=='PASS' and result['exact_assertions_and_finite_diagnostic_predicates']==9414,'independent bounded result')
 need(result['real_families']==21 and result['real_phase_geometries']==63 and result['focal_pairs']==126 and len(result['complex_families'])==4 and len(result['negative_controls'])==3,'meaningful adversarial coverage')
 need((E/'INDEPENDENT_CHECKS.stderr.txt').read_bytes()==b'','independent stderr')
 need(sha(E/'INDEPENDENT_CHECKS.stdout.json')==load(E/'CHECK_EXECUTION.json')['stdout_sha256'],'independent execution binding')
 primary=load(E/'PRIMARY_TRANSPORT.json')[0];binding(Path(primary['path']),primary['bytes'],primary['sha256']);need(primary['status']==200,'actual Stachel PDF')
 for x in load(E/'FINAL_READ_LEDGER.json')['Stachel_critical_renders']:need(sha(Path(x['path']))==x['sha256'],'Stachel critical pixels')
 for x in load(E/'PRIOR_IMMUTABLE_BINDINGS.json'):binding(Path(x['path']),x['bytes'],x['SHA256'])
 v=load(E/'VERDICT.json');need(v['assessment']=='PASS_FULL_ORIGINAL_SIGNED_FOCAL_PROPORTIONALITY_WITH_EXPLICIT_ELLIPTICAL_CAUSTIC_AND_PRIORITY_LIMITS','literal custom verdict')
 need(v['substantive_defect'] is None and v['remaining_mathematical_gap_in_main_theorem'] is None and v['source_repair'] is False and v['narrowed_replacement'] is False,'original theorem disposition')
 need(v['publication_clearance'] is False and v['canonical_url'] is None and v['AA'] is None and v['follow_up'] is None,'no public promotion')
 if not args.preseal:
  need(sha(E/'FINAL_MANIFEST.json')==load(E/'FINAL_SEAL.json')['manifest_sha256'],'final manifest/seal')
  for x in load(E/'FINAL_MANIFEST.json')['files']:binding(Path(x['path']),x['bytes'],x['sha256'])
 print(json.dumps({'status':'PASS_READ_ONLY_ADVERSARIAL_CUSTODY_AND_EVIDENCE','original_source_bindings':len(source['all_original_bindings']),'native_ZIP_payloads':24,'native_manifest_payload_bindings':len(load(N/'MANIFEST.json')['files']),'initial_manifest_and_exposure_verified':True,'six_native_outputs_byte_identical_to_published':True,'independent_finite_predicates':9414,'independent_negative_controls':3,'prior_immutable_bindings':4,'mathematical_programs_replayed':False,'network_or_source_writes':False,'final_envelope_verified':not args.preseal,'publication_clearance':False},indent=2))
if __name__=='__main__':main()
