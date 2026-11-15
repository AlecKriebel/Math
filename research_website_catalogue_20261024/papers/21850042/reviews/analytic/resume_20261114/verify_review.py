"""Read-only integrity and exact-evidence verifier for analytic review 21850042.
No source writes, build/replay shell scripts, site/Sheet/Git changes or networking.
"""
from pathlib import Path
from fractions import Fraction as F
import hashlib,json,sys,subprocess,argparse
if hasattr(sys,'set_int_max_str_digits'):sys.set_int_max_str_digits(0)
HERE=Path(__file__).resolve().parent
LANE=HERE.parent
PAPER=LANE.parent.parent

def digest(p):
 h=hashlib.sha256()
 with p.open('rb') as f:
  for block in iter(lambda:f.read(1024*1024),b''):h.update(block)
 return h.hexdigest()

def main():
 ap=argparse.ArgumentParser();ap.add_argument('--recompute',action='store_true');ap.add_argument('--whole-archive',action='store_true');args=ap.parse_args()
 seal=json.loads((LANE/'FINAL_SEAL.json').read_text());manifest_path=LANE/'FINAL_MANIFEST.json';assert digest(manifest_path)==seal['FINAL_MANIFEST_SHA256'];manifest=json.loads(manifest_path.read_text())
 for item in manifest['review_artifacts']:
  p=LANE/item['path'];assert p.stat().st_size==item['bytes'] and digest(p)==item['SHA256'],str(p)
 source=PAPER/'sources';assert digest(source/'SOURCE_READY.json')=='b0fbd1e6e0b06518f837b4d59e1c5bc28e40a4aed044d9d46b3408856b3a45ce';assert digest(source/'SOURCE_READY_MANIFEST.json')=='6730040cb9b0f47cd51b524c929cdbabeb90f0ae113704b08767462fab3c9f9e'
 native=json.loads((source/'SOURCE_READY_MANIFEST.json').read_text());native_count=0;skipped=[]
 for item in native['files']:
  if item['path']=='cache/original-release.zip' and not args.whole_archive:skipped.append(item['path']);continue
  p=source/item['path'];assert p.stat().st_size==item['bytes'] and digest(p)==item['sha256'],str(p);native_count+=1
 assert digest(LANE/'INITIAL_SEAL.json')=='5b7d0b5d6eb383a02da84db9ee130ac4a3774df1d124c65be1181699f2412896'
 verdict=json.loads((LANE/'VERDICT.json').read_text())
 expected_pass=['triangle-shared-runtime','fixed_rank','diffuse_algebra','triangle_all_weights','native_flint36','independent_flint36','seven_verified','growing_pendant','weighted_pendant','affine_algebra']
 for name in expected_pass:
  receipt=json.loads((HERE/(name+'.execution.json')).read_text());assert receipt['exit_code']==0 and not receipt.get('timeout',False),name
 q2=json.loads((HERE/'q2_bounded_final.execution.json').read_text());assert (q2['exit_code']==0 and not q2['timeout'])==verdict['checks']['direct_two_portal_native_replay_completed']
 src=source/'published-source/AlecKriebel-Math-dec8693/universal_simultaneous_amplification/phase4_landmark_closure';cert=json.loads((src/'threshold/clique_pendant_product_counterexample/certificate.json').read_text());x=F(cert['rules']['Bd']['ratio']);y=F(cert['rules']['dB']['ratio']);assert x>F(5609,5000)>1 and F(223,250)<y<1;assert x*y>F(1250807,1250000)>1 and (x+y)/2>F(10069,10000)>1
 triangle=json.loads((HERE/'triangle-shared-runtime.stdout').read_text());assert triangle['endpoint']['first_stage_constants']==['1/4','27/16'];assert triangle['endpoint']['dB_difference']=='-16/81';assert triangle['endpoint']['dB_graph_coefficient']=='-25/81';assert triangle['endpoint']['dB_complete_coefficient']=='-1/9'
 seven=json.loads((HERE/'seven_verified.stdout').read_text());assert seven['all_harmonic_residuals_zero'] and seven['theta_greater_than_177_over_2000'];assert seven['theta_rational_SHA256']=='dc13fb68473a2b0a20d8086a59e49674f30eab5145d0805bf4ab7a4b2bd6c606'
 recomputed=[]
 if args.recompute:
  python=HERE/'.exact-runtime/bin/python';assert python.is_file(),'Private exact runtime is absent; install sympy 1.14.0 and python-flint 0.9.0 in a separate local environment and select it explicitly.'
  for name in ['exact_triangle_continuation.py','verify_seven_vertex.py','verify_scope_probe.py']:
   r=subprocess.run([str(python),'-B',str(HERE/name)],capture_output=True,text=True,timeout=30,check=True);assert r.returncode==0;recomputed.append(name)
 print(json.dumps({'artifact_integrity':'PASS','native_manifest_bindings_verified':native_count,'already_authenticated_archive_not_rehashed':skipped,'exact_finite_witness_inequalities':'PASS','independent_recomputations':recomputed,'scientific_disposition':verdict['scientific_disposition'],'universal_in_N_proof_location':'DERIVATIONS.md and REPORT.md; finite computations alone are not that proof'},indent=2))
if __name__=='__main__':main()
