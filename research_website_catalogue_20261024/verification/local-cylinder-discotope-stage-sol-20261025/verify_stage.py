"""Read-only sealed-stage verification. Prints JSON; never writes or rerenders."""
from pathlib import Path
import hashlib,json,sys,xml.etree.ElementTree as ET
O=Path(__file__).resolve().parent;R=O.parents[1]
sys.path[:0]=[str(O),str(R/'scripts')]
from cylinder_discotope_source import cylinder_discotope_source_view

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def need(ok,tag):
    if not ok:raise ValueError('stage_verify:'+tag)

def validate(require_seal=True):
    baseline=json.loads((O/'protected-before.json').read_text());changed=[]
    for item in baseline['files']:
        p=Path(item['path'])
        if not p.is_file() or p.stat().st_size!=item['bytes'] or sha(p)!=item['sha256']:changed.append(str(p))
    need(not changed,'protected_existing_bytes_changed:'+repr(changed))
    live=Path(baseline['production_public_root']);old=[p for p in live.rglob('*') if p.is_file()]
    need(len(old)==baseline['public_file_count']==484,'production_public_inventory')
    target=json.loads((O/'target-checks.json').read_text());legacy=json.loads((O/'legacy-full-proposed.json').read_text());once=json.loads((O/'LEGACY_FULL_SUITE_ONCE.json').read_text())
    need(target['status']==legacy['status']=='PASS','positive_content_reports')
    need(set(target['papers'])=={'23387774','23074543'} and len(legacy['papers'])==59,'positive_report_exact_ID_sets')
    frozen=json.loads((O/'FROZEN_INPUT_SET.json').read_text())
    need(set(legacy['papers'])==set(frozen['old_configured_record_ids_in_order']) and once['state']=='COMPLETE_PASS_ONE_DISPATCH' and once['record_ids']==frozen['old_configured_record_ids_in_order'],'one_frozen_legacy_suite')
    equivalence=json.loads((O/'legacy-renderer-equivalence.json').read_text())
    need(equivalence['status']=='PASS' and equivalence['complete_renderer_executions']==118 and equivalence['record_ids']==frozen['old_configured_record_ids_in_order'],'59_complete_renderer_comparisons')
    old_input_bindings={}
    for record in equivalence['comparisons']:
        need(record['all_original_and_proposed_output_bytes_equal'] and record['filesystem_output_writes']==0,'memory_comparison_result')
        for name,item in record['original_read_bindings'].items():
            p=Path(name);need(p.is_file() and p.stat().st_size==item['bytes'] and sha(p)==item['sha256'],'old_renderer_source_input_changed:'+name);old_input_bindings[name]=item
    helper_controls=[]
    for name,opt in [('guard-controls.json',0),('guard-controls-optimized.json',1)]:
        data=json.loads((O/name).read_text());need(data['status']=='PASS' and data['python_optimization']==opt,'guard_control_report')
        need(sum(x.get('accepted',False) for x in data['checks'])==2 and sum(x.get('rejected',False) for x in data['checks'])==54,'actual_input_control_counts');helper_controls.append(len(data['checks']))
    faults=json.loads((O/'public-output-rejection-controls.json').read_text());need(faults['status']=='PASS' and len(faults['controls'])==4 and all(x['rejected'] for x in faults['controls']),'public_fault_controls')
    overlay=json.loads((O/'index-sitemap-overlay-checks.json').read_text());need(overlay['status']=='PASS' and overlay['merged_index_count']==62 and overlay['merged_sitemap_count']==63 and overlay['predicted_whole_public_files']==492,'overlay_summary')
    actual=sorted(str(p.relative_to(O/'public')) for p in (O/'public').rglob('*') if p.is_file())
    need(actual==overlay['actual_private_overlay_files'] and len(actual)==10,'exact_ten_overlay_files')
    pairs=[]
    for rid in frozen['authorized_new_record_ids']:
        p=R/'papers'/rid;c=json.loads((p/'publication.json').read_text());g=json.loads((p/'promotion.json').read_text())
        raw,view,asset_root=cylinder_discotope_source_view(p,c,g)
        for name in [c['pdf_filename'],c['supplement_filename']]:need((asset_root/name).read_bytes()==(O/'public/research'/c['slug']/name).read_bytes(),'whole_source_asset_copy')
        pairs.append({'record_id':rid,'source_receipt_original_shape':list(raw),'selected_pdf_pages':c['pdf_pages'],'canonical_configs_unchanged':True})
    manifest_files=0
    if require_seal:
        mf=O/'FINAL_MANIFEST.json';seal=json.loads((O/'FINAL_SEAL.json').read_text());need(seal['manifest_SHA256']==sha(mf),'manifest_seal')
        manifest=json.loads(mf.read_text());manifest_files=len(manifest['files'])
        expected=set()
        for item in manifest['files']:
            rel=Path(item['path']);need(not rel.is_absolute() and '..' not in rel.parts,'manifest_safe_path');p=O/rel
            need(not p.is_symlink() and p.is_file() and p.stat().st_size==item['bytes'] and sha(p)==item['SHA256'],'owned_binding:'+str(rel));expected.add(str(rel))
        present={str(p.relative_to(O)) for p in O.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name not in ['FINAL_MANIFEST.json','FINAL_SEAL.json']}
        need(present==expected,'complete_owned_inventory')
    return {'status':'PASS_READ_ONLY_PRIVATE_STAGE_VERIFICATION','owned_manifest_files_verified':manifest_files,'protected_existing_files_unchanged':len(baseline['files']),'production_public_files_unchanged':484,'actual_source_inputs_rechecked':len(old_input_bindings),'target_checks':sum(len(x['checks']) for x in target['papers'].values()),'legacy_checks_one_suite':sum(len(x['checks']) for x in legacy['papers'].values()),'normal_and_optimized_helper_cases':helper_controls,'public_rejection_cases':4,'overlay_files':10,'merged_index':62,'merged_sitemap':63,'predicted_integrated_public_files':492,'production_integrated':False,'HTTP_browser_native_verified':False,'canonical_gates_changed':False,'writes':0,'target_source_shapes':pairs}

if __name__=='__main__':print(json.dumps(validate(),indent=2))
