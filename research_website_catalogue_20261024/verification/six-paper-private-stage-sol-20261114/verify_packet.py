"""Read-only sealed closure; in-memory reproduction, no disk builds/network/writes."""
import sys
sys.dont_write_bytecode=True
from six_common import *
from six_source import load_bundles
from verify_stage_read_only import verify
from semantic_controls import run as fault_replay
import argparse

def closure(*,preseal=False,current_base=False):
    if not preseal:
        seal=load(OWN/'FINAL_SEAL.json');manifest=load(OWN/'OWNED_MANIFEST.json')
        require(bind(OWN/'OWNED_MANIFEST.json')['sha256']==seal['manifest_sha256'],'owned_manifest_seal')
        actual={str(p.relative_to(OWN)) for p in OWN.rglob('*') if p.is_file()}
        require(actual=={x['path'] for x in manifest['files']}|{'OWNED_MANIFEST.json','FINAL_SEAL.json'},'closed_owned_inventory')
        for x in manifest['files']:require(bind(contained(OWN,x['path']))=={k:x[k] for k in ('bytes','sha256')},'owned_payload:'+x['path'])
    bundles=load_bundles();stage=OWN/'final-build-a/public';other=OWN/'final-build-b/public';build_date='2026-11-15'
    result=verify(stage,build_date,current_base=current_base,_bundles=bundles)
    require(result['status']=='PASS','complete_private_stage')
    pairs=load(OWN/'FINAL_PAIRED_BUILD_COMPARISON.json')
    files_a={str(p.relative_to(stage)):p.read_bytes() for p in stage.rglob('*') if p.is_file()};files_b={str(p.relative_to(other)):p.read_bytes() for p in other.rglob('*') if p.is_file()}
    require(files_a==files_b and len(files_a)==26 and pairs['all_complete_output_bytes_equal'] is True,'paired_final_code_fixed_date_output_bytes')
    from build_private import article_bytes,overlays
    reproduced=overlays(bundles,build_date)
    for b in bundles:
        c=b['c'];prefix='research/'+c['slug']+'/'
        reproduced[prefix+'index.html']=article_bytes(b,build_date);reproduced[prefix+'citation.bib']=b['prepared_bibtex']
        for a in b['asset_view']:reproduced[prefix+a['name']]=Path(a['path']).read_bytes()
    require(reproduced==files_a,'all26_final_code_bytes_reproduce_in_memory')
    for x in pairs['files']:require(bind(stage/x['path'])=={k:x[k] for k in ('bytes','sha256')},'final_overlay_binding')
    replay=fault_replay(stage,build_date,_bundles=bundles);normal=load(OWN/'faults/normal-recovery.stdout');optimized=load(OWN/'faults/optimized.stdout')
    require(json.dumps(replay,sort_keys=True)==json.dumps(normal,sort_keys=True)==json.dumps(optimized,sort_keys=True) and replay['rejected_faults']==457,'all457_new_only_faults_replayed')
    supplement=load(OWN/'SUPPLEMENTAL_AUTHORITY_BINDINGS.json')
    require(bind(supplement['path'])=={k:supplement[k] for k in ('bytes','sha256')} and same(load(supplement['path']),supplement['whole_original_root_audit_adoption']),'whole_additive_root_audit_authority')
    verdict=load(OWN/'VERDICT.json')
    require(verdict['literal_custom_verdict']=='PRIVATE_SIX_TARGET_STAGE_VERIFIED_PENDING_INDEPENDENT_CODE_AUDIT_AND_ROOT_ADOPTION','literal_private_custom_verdict')
    require(verdict['root_stage_adoption'] is False and verdict['independent_code_audit_adopted'] is False and verdict['production_install_authorized'] is False and verdict['canonical_url'] is None and verdict['AA'] is None,'unpassed_publication_gates')
    code=load(OWN/'CANDIDATE_CODE_MANIFEST.json')
    for x in code['files']:require(bind(OWN/x['path'])=={k:x[k] for k in ('bytes','sha256')},'frozen_candidate_code')
    return {'status':'PASS','records':list(IDS),'article_checks':sum(len(x) for x in result['records'].values()),'global_stage_checks':len(result['checks']),
       'target_faults_replayed':replay['rejected_faults'],'paired_complete_output_files':len(files_a),'whole_output_files_reproduced_in_memory':len(reproduced),'old_public_fence':result['old_nonoverlay_public_files_checked'],
       'installed_core_fence':result['installed_core_files_checked'],'current_base_checked':current_base,'source_inputs':len(load(OWN/'FROZEN_INPUT_SET.json')['files']),
       'private_only':True,'writes':0,'network':0,'old_campaigns':0}
if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('--preseal',action='store_true');p.add_argument('--current-base',action='store_true');a=p.parse_args()
    print(json.dumps(closure(preseal=a.preseal,current_base=a.current_base),sort_keys=True))
