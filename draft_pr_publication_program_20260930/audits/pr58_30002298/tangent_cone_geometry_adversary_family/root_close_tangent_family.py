"""UNEXECUTED ROOT helper. python root_close_tangent_family.py /absolute/receipt.json
Read lean fixed bytes/modes and in-place sources only; ROOT owns/captures execution.
No scientific operator, cache, network, Git/native or publication action is run.
"""
import hashlib,json,os,stat,sys
from datetime import datetime,timezone
from pathlib import Path
FAMILY=Path(__file__).resolve().parent
def sha(b):return hashlib.sha256(b).hexdigest()
def mode(p):return format(stat.S_IMODE(p.stat().st_mode),'04o')
def load(p):return json.loads(p.read_bytes())
def validate():
    p=FAMILY/'SOURCE.json';b=p.read_bytes();idx=json.loads(b)
    assert mode(p)=='0444' and not p.is_symlink()
    listed={e['relative_path'] for e in idx['files']}
    assert len(listed)==len(idx['files']) and 'SOURCE.json' not in listed
    assert {str(p.relative_to(FAMILY)) for p in FAMILY.rglob('*') if p.is_file()}==listed|{'SOURCE.json'}
    assert {'.'}|{str(p.relative_to(FAMILY)) for p in FAMILY.rglob('*') if p.is_dir()}==set(idx['directories'])
    for name in idx['directories']:
        p=FAMILY if name=='.' else FAMILY/name
        assert mode(p)=='0755' and not p.is_symlink()
    for e in idx['files']:
        p=FAMILY/e['relative_path'];data=p.read_bytes()
        assert mode(p)==e['full_mode_07777']=='0444' and not p.is_symlink()
        assert len(data)==e['bytes'] and sha(data)==e['sha256']
    external=[]
    for e in load(FAMILY/'INPLACE_SOURCE_BINDINGS.json')['bindings']:
        p=Path(e['absolute_path']);data=p.read_bytes();actual=mode(p)
        assert not p.is_symlink() and len(data)==e['bytes'] and sha(data)==e['sha256']
        observed=e['observed_full_mode_07777']
        assert actual==observed or (observed=='0644' and actual=='0444')
        external.append({'path':str(p),'full_mode_07777_current':actual,
                         'observed_mode_at_family_pin':observed,'subsequent_readonly_freeze':actual!=observed})
    for tag in ('primary_read','geometric_controls','handoff'):
        folder=FAMILY/'captures'/tag;cap=load(folder/'CAPTURE.json');pre=load(folder/'PRELAUNCH.json')
        assert all(cap[k]==v for k,v in pre.items()) and cap['exit_code']==0
        assert cap['owned_child_pid']>0 and cap['collector_pid']>0 and not cap['ROOT_helpers_executed']
        for role in ('operator','collector'):
            assert sha((folder/(role+'_prelaunch.py')).read_bytes())==cap[role+'_prelaunch_sha256']
            assert cap[role+'_prelaunch_sha256']==cap[role+'_after_sha256']
        assert sha(Path(cap['argv'][1]).read_bytes())==cap['operator_prelaunch_sha256']
        for stream in ('stdout','stderr'):
            data=(folder/(stream+'.bin')).read_bytes()
            assert len(data)==cap[stream+'_bytes'] and sha(data)==cap[stream+'_sha256']
    children=load(FAMILY/'primary_child_captures/OWNED_RUNS.json');assert len(children)==11
    for cap in children:
        assert cap['owner_pid']==22956 and cap['owned_child_pid']>0 and cap['exit_code']==0
        stem=cap['stdout_file'].removesuffix('.stdout.bin')
        assert all(cap[k]==v for k,v in load(FAMILY/'primary_child_captures'/(stem+'.PRELAUNCH.json')).items())
        for stream in ('stdout','stderr'):
            data=(FAMILY/'primary_child_captures'/cap[stream+'_file']).read_bytes()
            assert len(data)==cap[stream+'_bytes'] and sha(data)==cap[stream+'_sha256']
    primary=load(FAMILY/'PRIMARY_SOURCE_RECEIPTS.json')
    assert all(s['acquired'] for s in primary['sources'][:3])
    assert not primary['publisher_full_PDF_available'] and not primary['ROOT_cache_required']
    failure=primary['sources'][3]
    assert not failure['acquired'] and failure['error_type']=='HTTPError'
    assert failure['HTTP_failure_body_bytes']==832806 and failure['HTTP_failure_body_private_retained']
    assert primary['published_metadata']['DOI']=='10.1016/j.aim.2016.12.026'
    controls=load(FAMILY/'GEOMETRIC_CONTROL_RESULTS.json')
    assert controls['control_families']==8 and len(controls['controls'])==8
    assert controls['all_exact'] and controls['finite_controls_are_not_universal_proof']
    ready=load(FAMILY/'READY.json');assert not ready['ROOT_helpers_executed'] and not ready['ROOT_closure_readback_claimed']
    assert ready['mathematical_verdict']=='PASS_COMPLETE_PRIOR_GEOMETRIC_CHARACTERIZATION'
    assert not any(n.endswith(('.pdf','.png','.layout.txt')) for n in listed)
    return {'SOURCE_sha256':sha(b),'SOURCE_bytes':len(b),'indexed_file_count':len(listed),
        'total_including_SOURCE':len(listed)+1,'full_modes_checked':True,'external_source_mode_chronology':external,
        'owned_operator_captures':3,'owned_primary_children':11,'exact_control_families':8,
        'private_primary_cache_read':False,'scientific_operators_imported_or_executed':False,
        'acceptance_publication_authority_inferred':False}
def main():
    assert len(sys.argv)==2;output=Path(sys.argv[1]).resolve()
    assert FAMILY not in output.parents and not output.exists()
    result=validate();result.update(schema='pr58-tangent-ROOT-close/v1',executing_pid=os.getpid(),
        utc=datetime.now(timezone.utc).isoformat(),validation_complete=True,
        receipt_actual_only_if_ROOT_owns_and_captures_this_run=True)
    output.parent.mkdir(parents=True,exist_ok=True)
    with output.open('x') as f:f.write(json.dumps(result,indent=2,sort_keys=True)+'\n')
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':main()
