#!/usr/bin/env python3
"""Strict closed review-custody/observed-outcome verifier; no project imports or service calls."""
from pathlib import Path
import hashlib,json,re,sys
H=Path(__file__).resolve().parent
sha=lambda b:hashlib.sha256(b).hexdigest()
def need(v,m):
    if not v:raise RuntimeError(m)
def verify():
    manifest_path=H/'MANIFEST.json';m=json.loads(manifest_path.read_bytes())
    need((H/'MANIFEST.sha256').read_text()==sha(manifest_path.read_bytes())+'  MANIFEST.json\n','Manifest seal changed')
    expected={e['path'] for e in m['files']}
    visible={p.name for p in H.iterdir() if p.is_file() and p.name not in {'MANIFEST.json','MANIFEST.sha256'} and not re.fullmatch('PROGRESS_MODE_[012]\\.jsonl',p.name)}
    need(visible==expected,'Closed top-level inventory changed')
    for e in m['files']:
        p=H/e['path'];need(not p.is_symlink() and p.is_file(),'Nonregular review artifact')
        b=p.read_bytes();need(len(b)==e['bytes'] and sha(b)==e['sha256'],'Review artifact changed: '+e['path'])
    pins=json.loads((H/'SOURCE_PINS.json').read_bytes())['files'];private_expected=set()
    for e in pins:
        p=H/e['snapshot'];b=p.read_bytes();original=Path(e['original'])
        need(not p.is_symlink() and original.is_file(),'Source snapshot/actual missing')
        need(len(b)==e['bytes'] and sha(b)==e['sha256'] and original.read_bytes()==b,'Protected input changed')
        need(p.stat().st_ino!=original.stat().st_ino or p.stat().st_dev!=original.stat().st_dev,'Original hardlink')
        private_expected.add(e['snapshot'])
    private_actual={str(p.relative_to(H)) for p in (H/'private').rglob('*') if p.is_file()}
    need(private_actual==private_expected,'Private snapshot inventory changed or case tree remains')
    need(not any(p.is_dir() for p in (H/'private').iterdir()),'Retained case fixture directory')
    numerical={'new02_response_bad_updatedCells_4.0','new02_response_bad_updatedRows_True','new02_response_bad_updatedRows_1.0','new02_response_bad_updatedColumns_4.0'}
    oversize={'new02_account_page_size_196','new02_account_page_size_197'}
    reference=None;execution_count=0
    for mode,name in enumerate(['RESULTS_NORMAL.json','RESULTS_OPTIMIZED.json','RESULTS_DOCSTRINGS_REMOVED.json']):
        r=json.loads((H/name).read_bytes());need(r['mode']==mode and r['cases']==1066 and r['full_main_executions']==1066,'Wrong execution mode/count')
        need(r['helper_sha256']=='d0fe59f4967facfd64db7332aad0f9663b4771f7a116c463c89bf4c30b88eacb' and r['plan_sha256']=='83df78463704c63ea3969a87325f18ab21c21893d6e1b8b49c5b16a6b4e3b2e1','Wrong immutable target')
        need(r['original_inputs_unchanged'] and r['private_fixtures_only'] and not r['offline_denied_attempts'],'Input/boundary safety failed')
        rows=r['results'];need(len(rows)==1066 and len({v['case'] for v in rows})==1066,'Duplicate/missing case')
        need({v['case'] for v in rows if not v['passed']}==numerical|oversize,'Unexpected diagnostic or hidden failure')
        need(all(v['passed'] for v in rows[:371]),'Inherited control failed')
        for v in rows:
            need(not v['unexpected_service_paths'] and v['state']['network']==0 and v['state']['subprocess']==0,'Unexpected boundary path')
            if v['case'] in numerical:
                need(v['error'] is None and v['state']['append']==1 and v['receipt_saved'] and v['receipt_row']==182 and v['simulated_ledger_rows']==182,'Numeric diagnostic no longer reproduced')
            elif v['case'] in oversize:
                need(v['error'].startswith('DepositError: Unexpected or incomplete Zenodo JSON response;') and v['state']['append']==0 and not v['receipt_saved'],'Oversized positive fixture disposition changed')
            elif v['case'].startswith(('new02_shape_','new02_idempotent_postread_','new02_account_late_alias_')):
                need(v['error'] is not None and v['state']['append']==0 and not v['receipt_saved'],'Finite corpus mutation escaped')
            need(v['error'] is None or '[Errno 28]' not in v['error'],'ENOSPC interpreted as rejection')
        normalized=json.loads(json.dumps(rows))
        for v in normalized:
            if v['error']:v['error']=re.sub(r'/private/case-[^/]+/',r'/private/CASE/',v['error'])
        if reference is None:reference=normalized
        else:need(normalized==reference,'Optimization changed an observed outcome')
        execution_count+=len(rows)
    verdict=json.loads((H/'VERDICT.json').read_bytes())
    need(verdict['primary_full_main_executions']==execution_count==3198 and verdict['material_objections_within_finite_profile']==[],'Verdict/count mismatch')
    need(verdict['generic_alias_parser_approved'] is False and verdict['mutation_authorized'] is False and verdict['operational_acceptance_created'] is False,'Review wrongly claims authority')
    context=json.loads((H/'CONTEXT_AND_PIN_INSPECTION.json').read_bytes())
    need(context['account_records']==197 and context['ledger_rows']==181 and context['raw_string_keys_and_values']==43495 and context['fresh_changed_leaves']==152 and context['compared_leaf_values']==22526 and not context['independent_semantic_leads'],'Context evidence changed')
    return {'verified':True,'review_manifest_sha256':sha(manifest_path.read_bytes()),'primary_full_main_executions':execution_count,'modes':[0,1,2],'material_finite_profile_objections':0,'disclosed_numeric_response_accepts':12,'oversized_positive_hypotheses_rejected':6,'protected_input_files':len(pins),'all_inputs_unchanged':True,'private_case_trees_retained':0,'mutations_authorized':False}
if __name__=='__main__':print(json.dumps(verify(),indent=2))
