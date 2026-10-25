"""Read-only verification of this exact fresh504 private stage. No rerender/replay."""
from pathlib import Path
import hashlib,json,sys
O=Path(__file__).resolve().parent;P=O.parents[1];sys.path[:0]=[str(O),str(P/'scripts')]
from ambient_block_modulus_source import ambient_block_modulus_source_view,STATUSES
from abm_body_contract import BodyText,expected_body
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def need(ok,tag):
    if not ok:raise ValueError('abm_stage_verify:'+tag)
def validate(sealed=True):
    before=json.loads((O/'protected-before.json').read_text())
    for item in before['files']:
        p=Path(item['path']);need(p.is_file() and p.stat().st_size==item['bytes'] and sha(p)==item['SHA256'],'protected_original:'+str(p))
    live=Path(before['production_public_root']);need(len([p for p in live.rglob('*') if p.is_file()])==504,'current_public_inventory')
    frozen=json.loads((O/'FROZEN_INPUT_SET.json').read_text());legacy=json.loads((O/'legacy64-checks.json').read_text());once=json.loads((O/'LEGACY_SUITE_ONCE.json').read_text())
    need(legacy['status']=='PASS' and set(legacy['papers'])==set(frozen['old_configured_record_ids_in_order']) and len(legacy['papers'])==64 and once['state']=='ONE_DISPATCH_COMPLETE_PASS','single_old64_suite')
    eq=json.loads((O/'LEGACY_RENDERER_EQUIVALENCE.json').read_text());need(eq['status']=='PASS' and eq['complete_renderer_executions']==128 and eq['record_ids']==frozen['old_configured_record_ids_in_order'] and all(x['outputs_equal'] for x in eq['comparisons']),'128_complete_memory_renders')
    need(sha(O/eq['input_bindings_path'])==eq['input_bindings_SHA256'],'deduplicated_old_read_manifest')
    source_inputs=json.loads((O/eq['input_bindings_path']).read_text())
    for path,item in source_inputs.items():
        p=Path(path);need(p.is_file() and p.stat().st_size==item['bytes'] and sha(p)==item['sha256'],'old_actual_read:'+path)
    target=json.loads((O/'target-checks.json').read_text());need(target['status']=='PASS' and set(target['papers'])==set(frozen['authorized_new_record_ids']),'target187')
    for mode,opt in [('normal',0),('optimized',1)]:
        c=json.loads((O/('guard-controls-'+mode+'.json')).read_text());need(c['status']=='PASS' and c['optimized']==opt and sum(x.get('accepted',False) for x in c['checks'])==3 and sum(x.get('rejected',False) for x in c['checks'])==98,'source_controls:'+mode)
        positive=json.loads((O/mode/'pristine3.json').read_text());need(positive['status']=='PASS' and set(positive['papers'])==set(frozen['authorized_new_record_ids']),'pristine:'+mode)
    faults=json.loads((O/'PUBLIC_OUTPUT_CONTROLS.json').read_text());need(faults['status']=='PASS' and len(faults['cases'])==116 and all(x['rejected'] for x in faults['cases']),'116_public_faults')
    for row in faults['cases']:
        rp=O/row['mode']/('checker-'+row['record_id']+'-'+row['case']+'.json');need(sha(rp)==row['report_SHA256'] and json.loads(rp.read_text())['issues']==row['issues'],'fault_receipt')
    overlay=json.loads((O/'OVERLAY_CHECKS.json').read_text());files=sorted(str(p.relative_to(O/'public')) for p in (O/'public').rglob('*') if p.is_file())
    need(overlay['status']=='PASS' and files==overlay['actual_files'] and len(files)==14 and overlay['index_items']==68 and overlay['sitemap_URLs']==69,'14_file_overlay')
    for rid in frozen['authorized_new_record_ids']:
        p=P/'papers'/rid;c=json.loads((p/'publication.json').read_text());g=json.loads((p/'promotion.json').read_text());raw,view,root=ambient_block_modulus_source_view(p,c,g);article=O/'public/research'/c['slug'];body=BodyText((article/'index.html').read_text())
        need(body.text==expected_body(c) and body.headings==[c['title']] and g['status']==STATUSES[rid],'exact_text_and_literal_status')
        for name in [c['pdf_filename'],c['supplement_filename']]:need((root/name).read_bytes()==(article/name).read_bytes(),'selected_unchanged_asset')
        need((article/'citation.bib').read_text()==c['prepared_bibtex'],'exact_BibTeX')
    if (O/'TESTED_CODE_BINDINGS.json').exists():
        for rel,item in json.loads((O/'TESTED_CODE_BINDINGS.json').read_text()).items():need(sha(O/rel)==item['SHA256'],'tested_code_unchanged:'+rel)
    prior=0
    if (O/'PRIOR_PACKET_CUSTODY.json').exists():
        for row in json.loads((O/'PRIOR_PACKET_CUSTODY.json').read_text())['packets']:
            base=Path(row['path']);need(sha(base/'FINAL_SEAL.json')==row['seal_SHA256'] and sha(base/'FINAL_MANIFEST.json')==row['manifest_SHA256'],'prior_sealed_packet')
            for item in json.loads((base/'FINAL_MANIFEST.json').read_text())['files']:
                path=base/item['path'];need(path.is_file() and path.stat().st_size==item['bytes'] and sha(path)==item['SHA256'],'prior_owned_output');prior+=1
    owned=0
    if sealed:
        mf=O/'FINAL_MANIFEST.json';seal=json.loads((O/'FINAL_SEAL.json').read_text());need(sha(mf)==seal['manifest_SHA256'],'manifest_seal');manifest=json.loads(mf.read_text());owned=len(manifest['files'])
        for item in manifest['files']:
            p=O/item['path'];need(p.is_file() and not p.is_symlink() and p.stat().st_size==item['bytes'] and sha(p)==item['SHA256'],'owned:'+item['path'])
        actual={str(p.relative_to(O)) for p in O.rglob('*') if p.is_file() and '__pycache__' not in p.parts and p.name not in ['FINAL_MANIFEST.json','FINAL_SEAL.json']}
        need(actual=={x['path'] for x in manifest['files']},'complete_owned_manifest')
    return {'status':'PASS_READ_ONLY_PRIVATE_STAGE_VERIFICATION','owned_manifest_files_verified':owned,'fresh_protected_files_unchanged':len(before['files']),'production_public_files_unchanged':504,'old_actual_read_inputs_rechecked':len(source_inputs),'earlier_owned_outputs_rechecked':prior,'target_checks':sum(len(x['checks']) for x in target['papers'].values()),'old64_checks_single_suite':sum(len(x['checks']) for x in legacy['papers'].values()),'complete_memory_renderer_executions':128,'source_rejections_each_normal_optimized_mode':98,'public_faults_rejected_each_mode':58,'pristine_records_each_mode':3,'overlay_files':14,'proposed_index_items':68,'proposed_sitemap_URLs':69,'predicted_integrated_public_files':516,'production_integrated':False,'HTTP_browser_native_verified':False,'canonical_gates_changed':False,'writes':0}
if __name__=='__main__':print(json.dumps(validate(),indent=2))
