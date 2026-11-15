"""Read-only verification of the exact row111 source/scope review packet."""
from pathlib import Path
import hashlib,json,subprocess,sys,argparse
HERE=Path(__file__).resolve().parent
SOURCE=HERE.parent.parent/'sources'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 ap=argparse.ArgumentParser();ap.add_argument('--recompute',action='store_true');a=ap.parse_args();seal=json.loads((HERE/'FINAL_SEAL.json').read_text());assert sha(HERE/'FINAL_MANIFEST.json')==seal['FINAL_MANIFEST_SHA256'];manifest=json.loads((HERE/'FINAL_MANIFEST.json').read_text())
 for item in manifest['review_files']:
  p=HERE/item['path'];assert p.stat().st_size==item['bytes'] and sha(p)==item['SHA256'],str(p)
 assert sha(SOURCE/'SOURCE_READY.json')=='b9a6b2f5d848fd924682faf33ad39c74f80d6d849e1a0081abbc5d5bfdc0bf4d';assert sha(SOURCE/'SOURCE_READY_MANIFEST.json')=='6c0e7a2de9e057d850fc61addd2c493c6f2feacc6c5aa57bd0875df41fbd2924'
 for item in manifest['local_primary_cache_bindings']:
  p=HERE/item['path'];assert p.stat().st_size==item['bytes'] and sha(p)==item['SHA256']
 source_check=subprocess.run([sys.executable,'-B',str(SOURCE/'verify_sources.py')],capture_output=True,text=True,check=True,timeout=30);assert json.loads(source_check.stdout)['source_integrity']=='PASS'
 assert sha(HERE/'INITIAL_SEAL.json')=='ebcd02a2478cbc7cbbf2d9f7e842437b9ba39716c96c95ac6bc25f3c60f8cec1';initial=json.loads((HERE/'INITIAL_SEAL.json').read_text());assert sha(HERE/'INITIAL_RECONSTRUCTION.md')==initial['INITIAL_RECONSTRUCTION_SHA256']
 for name in ['native_exact','native_numeric','independent_final']:
  receipt=json.loads((HERE/(name+'.execution.json')).read_text());assert receipt['exit_code']==0
 exact=json.loads((HERE/'native_exact_results.json').read_text());numeric=json.loads((HERE/'native_numeric_results.json').read_text());independent=json.loads((HERE/'independent_final.stdout').read_text());assert exact['passed'] and len(exact['checks'])==10 and all(x['passed'] for x in exact['checks']);assert numeric['passed'] and numeric['check_count']==7679 and not numeric['failures'];assert independent['wrong_resolvent_order_rejected'] and independent['time_composition_law']
 recomputed=False
 if a.recompute:
  python=Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/tmp/shared-math-runtime/bin/python');run=subprocess.run([str(python),'-B',str(HERE/'verify_independent.py')],capture_output=True,text=True,check=True,timeout=30);new=json.loads(run.stdout);assert new['wrong_resolvent_order_rejected'] and new['time_composition_law'];recomputed=True
 verdict=json.loads((HERE/'VERDICT.json').read_text());print(json.dumps({'artifact_integrity':'PASS','source_integrity':'PASS','native_exact_checks':10,'optional_native_numeric_checks':7679,'independent_recomputed':recomputed,'scientific_disposition':verdict['scientific_disposition'],'finite_checks_are_not_the_universal_proof':True},indent=2))
if __name__=='__main__':main()
