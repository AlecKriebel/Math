"""Independent readonly post-custody audit with complete capture/source linkage."""
import datetime as dt,hashlib,json,math,stat
from pathlib import Path
F=Path(__file__).absolute().parent;R=F.parents[3];V=F.parent/'acceptance_preparation_family_v3'
def need(v,m):
    if not v:raise ValueError(m)
def sha(b):return hashlib.sha256(b).hexdigest()
def raw(p):need(p.is_file() and not p.is_symlink() and all(not d.is_symlink() for d in p.parents),'Regular nonsymlink');return p.read_bytes()
def parse(b):
    def pairs(rr):
        d={}
        for k,v in rr:need(k not in d,'Duplicate key');d[k]=v
        return d
    def fl(x):v=float(x);need(math.isfinite(v),'Finite number');return v
    return json.loads(b,object_pairs_hook=pairs,parse_float=fl,parse_constant=lambda x:(_ for _ in ()).throw(ValueError(x)))
def linked_capture(folder):
    c=parse(raw(folder/'CAPTURE.json'))
    need(c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid']>0 and type(c['exit_code']) is int and c['exit_code']==0 and c['stdin_supplied'] is False and c['operator_unchanged'] is True,'Actual successful untouched operator')
    if 'source_unchanged' in c:need(c['source_unchanged'] is True,'Actual source unchanged')
    op=folder/('PRELAUNCH_OPERATOR.py' if (folder/'PRELAUNCH_OPERATOR.py').exists() else 'prelaunch_operator.py')
    need(sha(raw(op))==c['operator_sha256'],'Whole prelaunch operator linkage')
    if 'source_sha256' in c:need(sha(raw(folder/'PRELAUNCH_SOURCE.py'))==c['source_sha256'],'Whole prelaunch source linkage')
    for name in ['stdout','stderr']:
        z=c[name];need(set(z)=={'path','bytes','sha256'} and z['path']==name+'.bin','Literal whole stream');b=raw(folder/z['path']);need(len(b)==z['bytes'] and sha(b)==z['sha256'],'Complete stream linkage')
    need(raw(folder/'stderr.bin')==b'','Actual full stderr empty')
    return c
def main():
    o=parse(raw(F/'INPUT_BINDINGS.json'));rr=o['normalized_complete_external_input_bindings']
    for z in rr:
        p=R/z['path'];b=raw(p);need(len(b)==z['bytes'] and sha(b)==z['sha256'] and stat.S_IMODE(p.stat().st_mode)==z['full_mode'],'Post-custody full input body/mode')
    ledger=parse(raw(F/'SOURCE_READ_LEDGER.json'))
    for z in ledger['files']:
        b=raw(R/z['path']);need(len(b)==z['bytes'] and sha(b)==z['sha256'] and z['entire_text_personally_read'] is True,'Entire personal SOURCE read pin')
    source=parse(raw(V/'ACTUAL47_PREDECESSOR_BINDINGS.json'));roles=[]
    for z in source['complete_six_actual_phase_captures']:
        c=linked_capture((R/z['capture']['path']).parent);roles.append(c['phase'])
        expected='integrate_reviewed_partial.py' if c['phase'] in ['preflight','overlay','prepush','finalize'] else 'state_mirror_reconciliation.py' if c['phase']=='mirror' else 'verify_post_acceptance.py'
        need(c['argv'][:2]==['/usr/bin/python3','-B'] and Path(c['argv'][2]).name==expected,'Actual role/argv connection')
        if c['phase'] in ['preflight','overlay','prepush','finalize']:need(c['argv'].count(c['phase'])==1,'One actual integration phase argument')
    need(roles==['preflight','overlay','prepush','finalize','mirror','post'],'Six distinct actual roles')
    linked_capture((R/source['complete_actual_ROOT_post_capture']['capture']['path']).parent)
    operations=parse(raw(F/'ROOT_SOURCE_OPERATIONS.json'))
    for z in operations:need(linked_capture((R/z['capture_path']).parent)['argv']==z['argv'],'Exact actual ROOT closure/readback')
    for name in ['private_controls_actual_capture','fixed_custody_v2_actual_capture']:linked_capture(F/name)
    for name in ['private_path_controls_v3_actual_capture','private_readback_v3_actual_capture']:linked_capture(V/name)
    result={'schema':'pr48-v3-fresh-source-postcustody-readback/v1','status':'PASS_ALL_CLOSED_INPUTS_AND_ACTUAL_CAPTURE_LINKAGES','utc':dt.datetime.now(dt.timezone.utc).isoformat(),'normalized_unique_fixed_inputs':len(rr),'source_text_read_ledger_members':len(ledger['files']),'actual47_phase_roles_and_argv_checked':roles,'production_imported_compiled_executed':False,'future_acceptance_approved':False}
    with (F/'POSTCUSTODY_READBACK_RESULT.json').open('x') as h:json.dump(result,h,indent=2,sort_keys=True);h.write('\n')
    print(json.dumps(result,sort_keys=True))
if __name__=='__main__':main()
