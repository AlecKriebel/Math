"""Read selected scientific/support records; write own bounded consistency result."""
from pathlib import Path
import json,hashlib
HERE=Path(__file__).resolve().parent;CASE=HERE.parent
def need(x,s):
    if not x:raise AssertionError(s)
def load(s):return json.loads((CASE/s).read_bytes())
def pin(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def main():
    exact=load('physical_geometric_audit_01/EXACT_ALGEBRA_RESULTS.json')
    need(exact['count']==len(exact['checks'])==20 and all(x['residual']=='0' for x in exact['checks']),'physical exact checks')
    num=load('physical_geometric_audit_01/NUMERICAL_GEOMETRY_RESULTS.json');r=num['records']
    need(len(r)==num['families']==109 and sum(x['phase_count'] for x in r)==num['genuine_closed_orbits']==763,'physical count')
    need(sum(x['N']*x['phase_count'] for x in r)==num['vertices_checked']==10374,'vertices count')
    reversed_axes=sum(x['outer_axis_order']=='y_longer' for x in r);need(reversed_axes==60,'reversed axis count')
    odd_variation=max(float(x['relative_product_variation']) for x in r if x['N']%2)
    need(odd_variation<2e-79 and num['not_interval_certified'] is True,'physical numerical scope')
    probe=load('physical_geometric_audit_01/PRECISION_PROBE_RESULTS.json')
    need(probe['families']==len(probe['records'])==4 and probe['decimal_precision']==130,'probe counts')
    mex=load('meromorphic_divisor_audit_01/SYMBOLIC_RESULTS.json')
    need(len(mex['checks'])==21 and all(x['zero_remainder'] is True and x['remainder']=='0' for x in mex['checks'].values()),'meromorphic exact')
    lat=load('meromorphic_divisor_audit_01/LATTICE_RESULTS.json')
    need(lat['case_count']==len(lat['cases'])==1053,'lattice count')
    mn=load('meromorphic_divisor_audit_01/NUMERIC_RESULTS.json')
    need(mn['ordinary_case_count']==len(mn['ordinary_cases'])==120 and len(mn['principal_parts'])==6 and len(mn['v_endpoint_approaches'])==4,'meromorphic diagnostic counts')
    suite=load('root_reproduction_preparation_01/ACTUAL_TEN_JOB_STDOUT.json')
    base=CASE/'root_reproduction_preparation_01/private_extracted/k904a_outer_focal_inverse_product/verification'
    # Parse a literal JOBS list without importing/executing the reviewed harness.
    import ast
    tree=ast.parse((base/'run_verification.py').read_bytes())
    jobs=next(ast.literal_eval(n.value) for n in tree.body if isinstance(n,ast.Assign) and any(isinstance(t,ast.Name) and t.id=='JOBS' for t in n.targets))
    need(len(jobs)==len(suite['replays'])==10,'suite coverage')
    for j,rp in zip(jobs,suite['replays']):
        need(j['id']==rp['id'] and rp['scientific_json_equal'] is True,'suite scientific result')
        need(pin((base/j['folder']/j['result']).read_bytes())['sha256']==rp['expected_result_sha256'],'suite expected full body pin')
        need(rp['ignored_environment_fields']==j.get('environment_fields',[]),'suite field ignore exact scope')
    need(sum(x['byte_identical'] for x in suite['replays'])==8,'eight raw-equal outputs')
    source_rows=[]
    for ledger_name,key in [('priority_classical_01/PRIMARY_SOURCES.json','sources'),('priority_author_updates_01/SOURCE_VERSION_SEARCH_LEDGER.json','records')]:
        ledger=load(ledger_name)
        for row in ledger[key]:
            pp=row if 'path' in row else row['pdf'];p=Path(pp['path']);b=p.read_bytes()
            need(pin(b)=={k:pp[k] for k in ('bytes','sha256')},'priority source body pin '+str(p))
            source_rows.append({'ledger':ledger_name,'id':row.get('id',row.get('source_id')),'pin':pin(b),'meaning':'Identity confirmed; exact personal reading limits are separate.'})
    time=load('root_priority_01/ROOT_ACTUAL_TIMELINE_CROSSCHECK_01.json')
    timeline_rows=[]
    mapping={'datacite_f22':'datacite_f22.json','datacite_kriebel':'datacite_kriebel.json','kriebel_23394004':'kriebel_23394004.json','zenodo_23404834':'zenodo_23404834.json'}
    for key,filename in mapping.items():
        b=(CASE/'priority_author_updates_01/private_reading'/filename).read_bytes();need(pin(b)=={k:time[key][k] for k in ('bytes','sha256')},'timeline raw source pin')
        j=json.loads(b)
        if key.startswith('datacite'):
            attr=j['data']['attributes'];need(attr['created']==time[key]['created'] and attr['registered']==time[key]['registered'],'DataCite timestamps')
        else:need(j['created']==time[key]['created'] and j['doi']==time[key]['doi'],'Zenodo timestamps')
        timeline_rows.append({'source':key,'pin':pin(b),'event':'registration' if key.startswith('datacite') else 'record creation','first_public_access_inferred':False})
    native=load('native_adoption_preparation_01/OFFLINE_SELFTEST_RESULT.json');peer=load('native_source_adversary_01/CONTROL_RESULT.json')
    need(native['check_count']==len(native['checks'])==106 and native['provider_calls']==0 and native['actual_acceptance_inferred'] is False,'preparation bounded scope')
    need(peer['check_count']==len(peer['checks'])==201 and peer['production_or_network_transport_calls']==0 and peer['actual_acceptance_or_case_readiness_inferred'] is False,'source peer bounded scope')
    return {'schema':'review02-support-consistency-v1','status':'PASS','physical':{'exact_checks':20,'families':109,'orbits':763,'vertices':10374,'reversed_axis_families':reversed_axes,'max_odd_relative_product_variation':odd_variation,'precision_probe_families':4},'meromorphic':{'exact_checks':21,'finite_lattice_cases':1053,'noninterval_cases':120,'principal_parts_cases':6,'endpoint_approaches':4},'ten_job_record':{'full_expected_result_pins_checked':10,'raw_equal_reported':8,'only_ignored_fields':'python in geometry_algebra and meromorphic_divisor','not_rerun_by_review02':True},'priority_primary_body_pins':source_rows,'timeline':timeline_rows,'conditional_native_records':{'preparer_finite_checks':106,'source_peer_finite_checks':201,'own_native_program_execution':False,'actual_effect_authority_granted':False},'limits':'Stored record consistency is not independent replay of all science or certification of omitted private material, foreign proofs, receipt authority or native effects.'}
if __name__=='__main__':
    result=main();(HERE/'SUPPORT_CONSISTENCY.json').write_text(json.dumps(result,indent=2)+'\n');print(json.dumps({'status':result['status'],'physical':result['physical'],'meromorphic':result['meromorphic'],'priority_source_body_pins':len(result['priority_primary_body_pins']),'timeline_raw_sources':len(result['timeline'])},indent=2))
