#!/usr/bin/env python3
"""Offline read-only custody; standard library only, no project-code imports/replays."""
from pathlib import Path, PurePosixPath
import hashlib
import json
import sys

O=Path(__file__).resolve().parent
S=O.parents[1]/'sources'
EXCLUDED={'OWNED_MANIFEST.json','FINAL_SEAL.json'}
READY='c38e49d39bef6213a4703ee624be84eb110f1479a9c7b7e27b331bc39d417df4'
EARLY='ad8273125670270c9407db86159ff8ba303c603e3cf5d792ece240b830b87853'
N=0


def need(value,label):
    global N
    N+=1
    if not value:raise RuntimeError(label)


def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def load(p):return json.loads(p.read_text())


def check(root,rows):
    seen=set()
    for r in rows:
        name=r['path'];p=PurePosixPath(name)
        need(isinstance(name,str) and not p.is_absolute() and '..' not in p.parts and str(p)==name,'Unsafe relative path')
        f=root/name;need(f.resolve().is_relative_to(root) and not f.is_symlink(),'Path escapes/aliases root')
        need(name not in seen,'Duplicate manifest path');seen.add(name)
        need(f.is_file() and f.stat().st_size==r['bytes'],'Payload missing/size changed')
        need(sha(f)==r['SHA256'],'Payload SHA changed: '+str(f))
    return seen


def main(preseal):
    m=load(O/'OWNED_MANIFEST.json');need(m['excluded_terminal_files']==sorted(EXCLUDED),'Terminal boundary')
    owned=check(O,m['files']);need(owned=={p.relative_to(O).as_posix() for p in O.rglob('*') if p.is_file()}-EXCLUDED,'Owned completeness')
    sb=load(O/'SOURCE_BINDINGS.json');need(sb['record_id']==23578599 and Path(sb['source_root'])==S,'Source identity/root')
    original=check(S,sb['files']);need(len(original)==58 and original=={p.relative_to(S).as_posix() for p in S.rglob('*') if p.is_file()},'Whole original source boundary')
    need(sha(S/'SOURCE_READY.json')==READY,'Original readiness changed')
    ss=load(S/'SOURCE_READY_SEAL.json')
    for n,k in [('SOURCE_READY.json','SOURCE_READY_SHA256'),('SOURCE_READY_MANIFEST.json','MANIFEST_SHA256'),('SOURCE_READY_CLOSURE.json','CLOSURE_SHA256')]:need(sha(S/n)==ss[k],'Original terminal source seal')
    sm=load(S/'SOURCE_READY_MANIFEST.json');need(check(S,sm['files'])==original-{'SOURCE_READY_MANIFEST.json','SOURCE_READY_CLOSURE.json','SOURCE_READY_SEAL.json'},'Literal source manifest extent')
    r=load(S/'SOURCE_READY.json');need(r['HTTP_status_sequence']==[200,301,200,200,200,200,200],'Whole actual transport chronology')
    need(r['printed_date'] is None and r['printed_version'] is None,'Historical identity unread nulls altered')
    distinctions=r['native_schema_distinctions'];need(distinctions['record_swh']=={'present':True,'original_value':{}},'Original object distinction')
    need(distinctions['version_hit_swh_fields']==[{'present':True,'original_value':None}],'Original null distinction')
    need(distinctions['files_order']=={'present':True,'original_value':[]} and distinctions['files_default_preview']=={'present':True,'original_value':None},'Original array/null order')
    im=load(O/'INPUT_MANIFEST.json');need(im['whole_external_source_files']['files']==sb['files'],'Whole input/source bindings')
    check(O,im['owned_actual_primary_bodies'])
    need(sha(O/'EARLY_INDEPENDENCE_SEAL.json')==EARLY,'Early independent seal changed')
    es=load(O/'EARLY_INDEPENDENCE_SEAL.json');need(sha(O/'EARLY_MANIFEST.json')==es['manifest_SHA256'],'Early manifest binding')
    em=load(O/'EARLY_MANIFEST.json');need(Path(em['owned_root'])==O/'early','Early manifest root');check(O/'early',em['files'])
    need(es['actual_PDF_pages_read']==es['fresh_individual_rasters_read']==5 and es['controlling_TeX_lines_read']==380,'Full original reading ledger')
    need(es['foreign_primary_native_code_results_archived_current_opinions_read_before_seal'] is False and es['root123_gate_open_at_initial_seal'] is False,'Early independence history')
    freeze=load(O/'OWN_RESULT_FREEZE_BEFORE_NATIVE.json');need(freeze['own_code_SHA256']==sha(O/'own_diagnostics.py') and freeze['own_normal_output_SHA256']==sha(O/'computations/own-normal.stdout'),'Own code/output freeze')
    need(freeze['before_native_code_or_results_read'] is True and freeze['normal_optimized_output_bytes_equal'] is True,'Own/native chronology')
    ownbytes=[];nativebytes=[]
    v=S/'published-source/free_chain_nash_intersections_source/verification'
    expected=(v/'CHECK_RESULTS.json').read_bytes();code=(v/'exact_checks.py').read_bytes()
    need(expected==(O/'reproduction/CHECK_RESULTS.original.json').read_bytes(),'Complete original native expected object')
    for mode in ['normal','optimized']:
        receipt=load(O/f'computations/own-{mode}.receipt.json');need(receipt['exit_code']==0 and receipt['code_SHA256']==freeze['own_code_SHA256'],'Own actual exit/code')
        b=(O/f'computations/own-{mode}.stdout').read_bytes();x=json.loads(b);ownbytes.append(b)
        need(x['verdict']=='PASS' and x['network']==x['writes']==0 and x['native_code_or_results_read_for_implementation'] is False,'Own recorded disposition')
        need(x['counts']['coefficient_family_jet_cases']==24615 and x['counts']['Gaussian_polynomial_evaluation_comparisons']==24615,'Own bounded exact evidence')
        need(all(x['boundary_controls'].values()),'Own boundary falsifiers')
        nr=load(O/f'reproduction/native-{mode}.receipt.json');need(nr['exit_code']==0 and nr['native_code_bytes_identical'] is True,'Actual private native execution')
        need(nr['whole_output_bytes_equal_expected'] is True and nr['whole_output_JSON_equal_expected'] is True and nr['isolated_program_created_files']==[],'Native whole output/side effects')
        d=O/'reproduction'/mode;need((d/'exact_checks.py').read_bytes()==code and {p.name for p in d.iterdir()}=={'exact_checks.py'},'Unchanged isolated native code/no generated files')
        b=(O/f'reproduction/native-{mode}.stdout').read_bytes();need(b==expected,'Whole actual native output bytes');nativebytes.append(b)
    need(ownbytes[0]==ownbytes[1] and nativebytes[0]==nativebytes[1],'Normal/-O byte equivalence')
    nx=json.loads(expected);need(nx['status']=='PASS' and len(nx['negative_controls'])==12 and all(s=='rejected' for s in nx['negative_controls'].values()),'Native exact negative controls')
    gate=load(O/'ROOT_GATE_AUTHORITY.json');need(gate['initial_seal_gate_state']=='CLOSED' and gate['current_gate_state']=='OPEN' and gate['root_initial_mathematical_body_or_opinions_read'] is False,'Gate/independence ledger')
    verdict=load(O/'CUSTOM_VERDICT.json');need(verdict['record_id']==23578599 and verdict['full_original_claim_reviewed'] is True and verdict['substantive_defect_found'] is False and verdict['exact_remaining_in_scope_mathematical_gap'] is None,'Literal in-scope verdict')
    need(verdict['follow_up'] is None and verdict['public_install_authorized'] is False and verdict['source_changes']==[],'Task boundary')
    if not preseal:
        fs=load(O/'FINAL_SEAL.json');need(fs['OWNED_MANIFEST_SHA256']==sha(O/'OWNED_MANIFEST.json'),'Final owned seal')
        need(fs['REPORT_SHA256']==sha(O/'REPORT.md') and fs['CUSTOM_VERDICT_SHA256']==sha(O/'CUSTOM_VERDICT.json'),'Final scientific disposition seal')
        need(fs['owned_payloads']==len(owned) and fs['unchanged_source_files']==len(original),'Final extent')
    print(json.dumps({'record_id':23578599,'verdict':'PASS','mode':'preseal' if preseal else 'sealed','checks':N,'owned_payloads':len(owned),'unchanged_source_files':len(original),'scientific_programmes_rerun':0,'project_code_imports':0,'network_requests':0,'writes':0},sort_keys=True))


if __name__=='__main__':
    need(sys.argv[1:] in [[],['--preseal']],'Usage: verify_review.py [--preseal]')
    main(sys.argv[1:]==['--preseal'])
