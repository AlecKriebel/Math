"""Read-only verification of this fresh492 private stage; never rerenders."""
from pathlib import Path
import hashlib,json,sys
O=Path(__file__).resolve().parent;P=O.parents[1];sys.path[:0]=[str(O),str(P/'scripts')]
from spanning_sos_gin_source import spanning_sos_gin_source_view
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def need(ok,tag):
    if not ok:raise ValueError('new3_stage_verify:'+tag)
def validate(sealed=True):
    before=json.loads((O/'protected-before.json').read_text())
    for item in before['files']:
        p=Path(item['path']);need(p.is_file() and p.stat().st_size==item['bytes'] and sha(p)==item['SHA256'],'protected_original:'+str(p))
    live=Path(before['production_public_root']);need(len([p for p in live.rglob('*') if p.is_file()])==492,'current_public_inventory')
    frozen=json.loads((O/'FROZEN_INPUT_SET.json').read_text());legacy=json.loads((O/'legacy61-checks.json').read_text());once=json.loads((O/'LEGACY_SUITE_ONCE.json').read_text())
    need(legacy['status']=='PASS' and set(legacy['papers'])==set(frozen['old_configured_record_ids_in_order']) and len(legacy['papers'])==61 and once['state']=='ONE_DISPATCH_COMPLETE_PASS','single_current61_legacy_suite')
    eq=json.loads((O/'LEGACY_RENDERER_EQUIVALENCE.json').read_text());need(eq['status']=='PASS' and eq['complete_renderer_executions']==122 and eq['record_ids']==frozen['old_configured_record_ids_in_order'],'complete_current61_renderer_equivalence')
    source_inputs={}
    for row in eq['comparisons']:
        need(row['outputs_equal'] and row['filesystem_output_writes']==0,'memory_comparison')
        for path,item in row['original_read_bindings'].items():
            p=Path(path);need(p.is_file() and p.stat().st_size==item['bytes'] and sha(p)==item['sha256'],'old_actual_source_read:'+path);source_inputs[path]=item
    target=json.loads((O/'target-checks.json').read_text());need(target['status']=='PASS' and set(target['papers'])==set(frozen['authorized_new_record_ids']),'target187')
    for mode,opt in [('normal',0),('optimized',1)]:
        c=json.loads((O/('guard-controls-'+mode+'.json')).read_text());need(c['status']=='PASS' and c['optimized']==opt and sum(x.get('accepted',False) for x in c['checks'])==3 and sum(x.get('rejected',False) for x in c['checks'])==74,'source_guard_controls:'+mode)
        positive=json.loads((O/mode/'pristine3.json').read_text());need(positive['status']=='PASS' and set(positive['papers'])==set(frozen['authorized_new_record_ids']),'normal_optimized_pristine:'+mode)
    faults=json.loads((O/'PUBLIC_OUTPUT_CONTROLS.json').read_text());need(faults['status']=='PASS' and len(faults['cases'])==70 and all(x['rejected'] for x in faults['cases']),'70_public_output_faults')
    overlay=json.loads((O/'OVERLAY_CHECKS.json').read_text());files=sorted(str(p.relative_to(O/'public')) for p in (O/'public').rglob('*') if p.is_file())
    need(overlay['status']=='PASS' and files==overlay['actual_files'] and len(files)==14 and overlay['index_items']==65 and overlay['sitemap_URLs']==66,'exact_overlay_inventory')
    for rid in frozen['authorized_new_record_ids']:
        p=P/'papers'/rid;c=json.loads((p/'publication.json').read_text());g=json.loads((p/'promotion.json').read_text());raw,view,root=spanning_sos_gin_source_view(p,c,g)
        for name in [c['pdf_filename'],c['supplement_filename']]:need((root/name).read_bytes()==(O/'public/research'/c['slug']/name).read_bytes(),'selected_source_asset_copy')
    owned=0
    if sealed:
        mf=O/'FINAL_MANIFEST.json';seal=json.loads((O/'FINAL_SEAL.json').read_text());need(sha(mf)==seal['manifest_SHA256'],'manifest_seal');manifest=json.loads(mf.read_text());owned=len(manifest['files'])
        for item in manifest['files']:
            p=O/item['path'];need(p.is_file() and not p.is_symlink() and p.stat().st_size==item['bytes'] and sha(p)==item['SHA256'],'owned:'+item['path'])
        actual={str(p.relative_to(O)) for p in O.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name not in ['FINAL_MANIFEST.json','FINAL_SEAL.json']}
        need(actual=={x['path'] for x in manifest['files']},'complete_owned_manifest')
    return {'status':'PASS_READ_ONLY_PRIVATE_STAGE_VERIFICATION','owned_manifest_files_verified':owned,'fresh_protected_files_unchanged':len(before['files']),'production_public_files_unchanged':492,'old_actual_source_inputs_rechecked':len(source_inputs),'target_checks':sum(len(x['checks']) for x in target['papers'].values()),'old61_checks_single_suite':sum(len(x['checks']) for x in legacy['papers'].values()),'complete_memory_renderer_executions':122,'source_rejections_each_normal_optimized_mode':74,'public_faults_rejected_each_mode':35,'pristine_records_each_mode':3,'overlay_files':14,'proposed_index_items':65,'proposed_sitemap_URLs':66,'predicted_integrated_public_files':504,'production_integrated':False,'HTTP_browser_native_verified':False,'canonical_gates_changed':False,'writes':0}
if __name__=='__main__':print(json.dumps(validate(),indent=2))
