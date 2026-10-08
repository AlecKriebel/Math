#!/usr/bin/env python3
"""Scoped replay after fixed external authentication; no claim to certify analysis."""
import argparse, ast, hashlib, json, os, subprocess, sys
from pathlib import Path

def need(ok,label):
    if not ok:raise ValueError(label)
def pairs(items):
    out={}
    for k,v in items:need(k not in out,'duplicate JSON key');out[k]=v
    return out
def load(b):return json.loads(b.decode('utf-8'),object_pairs_hook=pairs,parse_constant=lambda x:need(False,'nonfinite JSON'))
def sha(b):return hashlib.sha256(b).hexdigest()
def pin(b):return {'bytes':len(b),'sha256':sha(b),'git_blob':hashlib.sha1(b'blob '+str(len(b)).encode()+b'\0'+b).hexdigest()}
def stream(b):return {'type':'inline_utf8','bytes':len(b),'sha256':sha(b),'text':b.decode('utf-8')}
def unstream(s):
    need(type(s) is dict and set(s)=={'type','bytes','sha256','text'},'typed complete stream schema')
    need(s['type']=='inline_utf8' and type(s['text']) is str and type(s['bytes']) is int and s['bytes']>=0,'stream field types')
    b=s['text'].encode('utf-8');need(len(b)==s['bytes'] and sha(b)==s['sha256'],'stream bytes mismatch');return b
MUTATIONS={'flat_laplacian':'flat_harmonicity_by_exact_differences','flat_orientation':'flat_jacobian_polynomial_interpolation','area_normalization':'energy_area_exact_interpolation','curvature_sign':'negative_curvature_strict_rank_two_term','cusp_amplitude':'cusp_remote_folds_and_upper_derivative','cusp_harmonicity':'cusp_is_not_harmonic','collapsed_trace_injectivity':'collapsed_trace_tests_have_nontrivial_kernel','weak_lower_semicontinuity_direction':'lower_semicontinuity_is_only_one_sided','quotient_trace_equals_side_incidence':'quotient_trace_is_not_side_incidence'}
ORIGINAL_CHECKS=['flat_normal_harmonic','flat_tangential_harmonic','flat_normal_inward_derivative','flat_tangential_normal_derivative','flat_edge_flux_identically_zero','flat_jacobian_identity','flat_negative_interior_jacobian','flat_positive_interior_jacobian','chosen_points_inside_radius_two','energy_area_polynomial_identity','625_rational_matrix_regressions','cusp_bump_first_derivative','cusp_bump_second_derivative','cusp_trig_bound_identity','cusp_derivative_extremes','cusp_energy_bound_constant','cusp_nonharmonic_residual_numerator','identity_energy_density']
INDEPENDENT_CHECKS=['flat_harmonicity_by_exact_differences','flat_edge_flux_by_exact_differences','flat_jacobian_polynomial_interpolation','flat_opposite_orientation_inside_domain','energy_area_exact_interpolation','negative_curvature_strict_rank_two_term','cusp_remote_folds_and_upper_derivative','cusp_seam_exact_regularities','cusp_energy_majorant','cusp_is_not_harmonic','collapsed_trace_tests_have_nontrivial_kernel','quotient_trace_is_not_side_incidence','lower_semicontinuity_is_only_one_sided']
ABSENT={'original_full_reproduction':'NOT_RUN','full_original_patch_roundtrip':'NOT_RUN','source_pdf_rehash':'NOT_RUN','corpus_rehash':'NOT_RUN'}
def cases():return [('author_positive','verify.py',[],0,None),('author_negative','verify.py',['--negative-control'],1,'deliberately_false_jacobian_identity'),('independent_positive','independent_verify.py',[],0,None)]+[('mutation_'+n,'independent_verify.py',['--mutation',n],1,f) for n,f in MUTATIONS.items()]
def result_check(e,level):
    need(type(e) is dict and set(e)=={'label','script','arguments','optimization','exit_code','stdout','stderr'},'run exact schema')
    opts={c[0]:c for c in cases()};need(e['label'] in opts,'known run label');label,script,args,rc,fail=opts[e['label']]
    need(type(e['optimization']) is int and e['optimization']==level and type(e['exit_code']) is int and e['exit_code']==rc,'run mode and exit')
    need(e['script']==script and e['arguments']==args,'run command identity')
    need(unstream(e['stderr'])==b'','unexpected checker stderr');v=load(unstream(e['stdout']))
    need(type(v['optimization_level']) is int and v['optimization_level']==level and v['status']==('pass' if rc==0 else 'fail'),'checker result state')
    if script=='independent_verify.py':need(type(v['uid']) is int and v['uid']==1000,'checker UID')
    if fail:
        need(v.get('failed_check',v.get('error'))==fail,'wrong semantic failure')
    elif script=='verify.py':
        need(v['checks']==18 and type(v['checks']) is int and v['check_names']==ORIGINAL_CHECKS and v['rational_matrix_cases']==625,'author finite identities')
    else:
        need(v['check_count']==13 and type(v['check_count']) is int and [x['name'] for x in v['checks']]==INDEPENDENT_CHECKS,'independent check identities')
        evidence={x['name']:x['evidence'] for x in v['checks']}
        need(evidence['flat_opposite_orientation_inside_domain']=={'negative':'-19/16','positive':'29/16','largest_radius_squared':'17/16 < 4'},'flat exact evidence')
        need(evidence['negative_curvature_strict_rank_two_term']=={'nondegenerate_rational_cases':384},'curvature exact evidence')
        need(evidence['collapsed_trace_tests_have_nontrivial_kernel']=={'total_flux':'0','domain_pairing':'1/30'},'trace exact evidence')
        need(evidence['quotient_trace_is_not_side_incidence']=={'midpoint_x':'1/2','midpoint_y_squared':'5/4','bottom_boundary_y_squared_at_midpoint':'1/4','scope':'local geometric obstruction only'},'side-incidence evidence')
    return v

def exact_json_equal(actual,expected,path='result'):
    need(type(actual) is type(expected),'exact JSON type mismatch '+path)
    if type(expected) is dict:
        need(set(actual)==set(expected),'exact JSON object keys '+path)
        for k in expected:exact_json_equal(actual[k],expected[k],path+'.'+k)
    elif type(expected) is list:
        need(len(actual)==len(expected),'exact JSON list length '+path)
        for i,(x,y) in enumerate(zip(actual,expected)):exact_json_equal(x,y,path+'['+str(i)+']')
    else:need(actual==expected,'exact JSON value mismatch '+path)

def compare_fresh_reference(fresh,reference):
    need(type(fresh) is dict and type(reference) is dict,'run comparison objects')
    need(set(fresh)==set(reference)=={'label','script','arguments','optimization','exit_code','stdout','stderr'},'run comparison exact keys')
    for k in ['label','script','arguments','optimization','exit_code']:exact_json_equal(fresh[k],reference[k],'run.'+k)
    newout,oldout=unstream(fresh['stdout']),unstream(reference['stdout'])
    newerr,olderr=unstream(fresh['stderr']),unstream(reference['stderr'])
    exact_json_equal(load(newout),load(oldout),'stdout_json')
    need(newout==oldout,'exact complete stdout bytes differ')
    need(newerr==olderr,'exact complete stderr bytes differ')
    exact_json_equal(fresh,reference,'complete_run')
    return {'complete_stdout_bytes_equal':True,'complete_stderr_bytes_equal':True,'recursive_json_types_and_values_equal':True}

def run_cases(root,level,references=None):
    rows=[];flags=[] if level==0 else ['-O' if level==1 else '-OO']
    for label,script,args,rc,fail in cases():
        c=[sys.executable,'-I','-S','-B',*flags,script,*args];p=subprocess.run(c,cwd=root,capture_output=True,timeout=60)
        e={'label':label,'script':script,'arguments':args,'optimization':level,'exit_code':p.returncode,'stdout':stream(p.stdout),'stderr':stream(p.stderr)}
        result_check(e,level)
        if references is not None:
            key=(level,label);need(key in references,'matching pinned reference required');compare_fresh_reference(e,references[key])
        rows.append(e)
    return rows

def check_scope(root):
    s=load((root/'SCOPE.json').read_bytes())
    scalars={'schema':'variational-maps-scoped-acceptance-v1','problem_id':30003946,'rank':1069,'source_problem_code':'OWR-16415-008','decision':'ACCEPT_CORRECTED_SCOPED_PARTIAL_RESULTS','outcome':'exhausted','approaches':5,'approach_limit':5}
    false=['full_target_resolved','complete_candidate','novelty_claim','sixth_approach_attempted','source_bodies_delivered','dataset_contents_delivered','private_coordination_delivered','original_full_packet_delivered','analytic_source_theorems_computer_certified','full_published_2024_followup_inspected']
    true=['interpolation_admissibility_required','self_glued_faces_remain_in_full_target','isometry_energy_equality_accepted','isometry_map_identification_conditional','D_and_weak_closure_distinct']
    need(set(s)==set(scalars)|set(false)|set(true)|{'default_checks','accepted_results','open_gaps'},'scope exact schema')
    for k,v in scalars.items():need(type(s[k]) is type(v) and s[k]==v,'scope scalar '+k)
    for k in false:need(s[k] is False,'unsupported scope promotion '+k)
    for k in true:need(s[k] is True,'missing mathematical qualification '+k)
    need(s['default_checks']==ABSENT,'absent input statuses')
    need(s['accepted_results']==['uniqueness conditional on finite energy, regularity, degree and admissible interpolation','target-flow balance conditional on edge regularity and invertibility','exact local flat harmonic folding and minimization with fixed outer data','compatible-facewise-isometry energy equality; map identification conditional','finite-energy proper degree-one cusp folds as nonharmonic method obstruction'],'accepted scope')
    need(s['open_gaps']==['general energy equality E(u)=E(v)','admissible interpolation for the source minimizers on all allowed self-gluings','edge orientation, trace invertibility and unrestricted stationarity without extra hypotheses'],'open gaps')
    p=load((root/'PROVENANCE.json').read_bytes())
    for n,expected in p['preserved_public_files'].items():need(pin((root/n).read_bytes())==expected,'preserved authored bytes '+n)
    for n,key,offset in [('AUDIT.md','historical_audit','publication_audit_preamble_bytes'),('CORRECTION.patch','historical_contextual_patch','publication_patch_preamble_bytes')]:
        b=(root/n).read_bytes();i=p[offset];need(type(i) is int and i>0 and pin(b[i:])==p[key],'authored audit and patch preservation')
    need('REJECTED OR SUPERSEDED' in (root/'CORRECTION.patch').read_text().split('--- frozen_v1/REPORT.md')[0],'rejected removed-hunk notice')
    for n in ['verify.py','independent_verify.py','verify_publication.py']:
        need(not any(isinstance(x,ast.Assert) for x in ast.walk(ast.parse((root/n).read_text()))),'assert-free guard code')
    return s

def check_sources(root):
    m=load((root/'SOURCE_MANIFEST.json').read_bytes());a=load((root/'SOURCE_AUDIT_MANIFEST.json').read_bytes())
    need(m['included_source_contents'] is False and len(m['sources'])==5 and len(a['sources'])==5,'source metadata scope')
    for x,y in zip(m['sources'],a['sources']):
        need(x['name']==y['name'] and x['sha256']==y['sha256'] and x['bytes']==y['bytes'],'source metadata agreement')
        need(type(x['bytes']) is int and x['bytes']>0 and y['source_content_included'] is False,'source field types')
    need(m['sources'][-1]['resource_type']=='HTML, not PDF','published response type preserved')
    return {'historical_metadata_records':5,'fresh_source_pdf_rehash':'NOT_RUN','fresh_corpus_rehash':'NOT_RUN','full_published_2024_followup_inspected':False}

def check_receipts(root):
    r=load((root/'verification/REPRODUCTION.json').read_bytes())
    need(r['schema']=='variational-maps-fresh-runs-v1' and type(r['uid']) is int and r['uid']==1000,'fresh receipt identity')
    need(r['historical_runs_reused'] is False and r['tested_inputs_before']==r['tested_inputs_after'],'fresh unchanged inputs')
    need(r['default_absent_inputs']==ABSENT,'fresh absent input scope')
    need(r['readonly']['actual_create_denied'] is True and r['readonly']['actual_existing_write_open_denials']==3,'actual read-only snapshot probes')
    need(len(r['runs'])==36,'fresh run inventory');seen=set()
    for e in r['runs']:
        key=(e['optimization'],e['label']);need(key not in seen and key[0] in (0,1,2),'unique fresh run');seen.add(key);result_check(e,key[0])
    need(seen=={(m,c[0]) for m in (0,1,2) for c in cases()},'complete fresh run identities')
    p=load((root/'verification/PREPUBLICATION.json').read_bytes())
    need(p['schema']=='variational-maps-separate-input-checks-v1' and p['uid']==1000,'prepublication identity')
    need(p['original_inventory_before']==p['original_inventory_after'] and p['original_manifest_match'] is True,'original unchanged manifest audit')
    need(p['source_rehash']['matched_records']==5 and p['source_rehash']['new_source_content_inspection'] is False,'separate source-byte scope')
    for name in ['patch_forward','patch_reverse']:
        e=p[name];need(type(e['exit_code']) is int and e['exit_code']==0 and unstream(e['stderr'])==b'','patch run');unstream(e['stdout']);need(e['exact_expected_bytes'] is True,'patch exact output')
    need(p['public_default_checks']==ABSENT,'separate inputs not available by default')
    return {'fresh_preserved_runs':len(seen),'full_stdout_stderr_verified':True,'separate_original_and_patch_preparation':'PASS_RECORDED_SEPARATE_INPUTS','public_default_checks':ABSENT}

def verify(root,queue):
    need(os.getuid()==os.geteuid()==1000,'UID=EUID=1000 required');scope=check_scope(root);sources=check_sources(root);receipts=check_receipts(root)
    proof=load((root/'QUEUE_PROOF.json').read_bytes());need(pin(queue.read_bytes())==proof['after'],'actual queue bytes')
    references={(e['optimization'],e['label']):e for e in load((root/'verification/REPRODUCTION.json').read_bytes())['runs']}
    return {'schema':'variational-maps-mathematical-replay-v1','status':'PASS_SCOPED_PARTIAL_RESULTS','problem_id':30003946,'outcome':'exhausted','approaches':5,'full_target_resolved':False,'novelty_claim':False,'uid':os.geteuid(),'optimization':sys.flags.optimize,'default_absent_inputs':scope['default_checks'],'sources':sources,'receipts':receipts,'fresh_outputs_equal_recorded_reference':True,'fresh_replays':run_cases(root,sys.flags.optimize,references)}
if __name__=='__main__':
    try:
        p=argparse.ArgumentParser(description=__doc__);p.add_argument('root',type=Path);p.add_argument('--queue',required=True,type=Path);a=p.parse_args()
        print(json.dumps(verify(a.root.absolute(),a.queue.absolute()),indent=2,sort_keys=True))
    except Exception as e:print('REJECT: '+type(e).__name__+': '+str(e),file=sys.stderr);sys.exit(1)
