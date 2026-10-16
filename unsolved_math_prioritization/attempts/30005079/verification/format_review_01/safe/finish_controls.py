"""Small remaining controls after the documented supplementary ENOSPC failure."""
from pathlib import Path
import datetime
import importlib.util
import json
import os
import struct

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('own_controls',HERE/'independent_controls.py')
c=importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
c.CURRENT=c.PRIVATE/'current'
c.RECEIPTS=json.loads((HERE/'ACTUAL_CLI_RECEIPTS.json').read_bytes())
index=c.pin((c.FIXTURE/'package_index.json').read_bytes())['sha256']

if __name__=='__main__':
    hostile=c.PRIVATE/'hostile_environment'
    marker=hostile/'MUST_NOT_EXIST_ENVIRONMENT'
    old={k:os.environ.get(k) for k in ['PYTHONPATH','PYTHONUSERBASE','PYTHONOPTIMIZE']}
    os.environ.update(PYTHONPATH=str(hostile),PYTHONUSERBASE=str(hostile),PYTHONOPTIMIZE='2')
    try:
        c.run('hostile_environment_ignored_outer_authentication',['verify',index,'--root',c.FIXTURE,'--verify-only'],wanted=True,optimize=True)
    finally:
        for key,value in old.items():
            if value is None: os.environ.pop(key,None)
            else: os.environ[key]=value
    assert not marker.exists()
    c.run('wrong_external_index_pin',['verify','0'*64,'--root',c.FIXTURE,'--dependency-dir',c.WHEELS],wanted=False,reason='external index pin mismatch')
    alias=c.PRIVATE/'output_parent_symlink'; alias.symlink_to(c.PRIVATE/'output',target_is_directory=True)
    c.run('symlink_output_parent',['build',index,alias/'another/rank-two-fano-verification.zip','--root',c.FIXTURE],wanted=False,reason='output parent/ancestor must be nonsymlink directory')
    assert not (c.PRIVATE/'output/another/rank-two-fano-verification.zip').exists()
    for label,mutate,reason in [
        ('zip_unix_symlink_mode',lambda raw,central:struct.pack_into('<I',raw,central+38,(0o120777<<16)), 'ZIP unsafe central metadata'),
        ('zip_timestamp_mismatch',lambda raw,central:struct.pack_into('<H',raw,central+12,1), 'ZIP unsafe central metadata'),
    ]:
        r=c.clone(label,True); p=r/'rank-two-fano-verification.zip'; raw=bytearray(p.read_bytes()); central=struct.unpack_from('<I',raw,len(raw)-22+16)[0]; mutate(raw,central); p.write_bytes(raw); c.repin(r,True); c.current(label,r,reason=reason)
    r=c.clone('outer_metadata_differs',True)
    c.change_json(r,'metadata.json',lambda x:x.update(description='Different valid text'))
    c.repin(r,True); c.current('outer_metadata_copy_mismatch',r,reason='outer/portable exact copy mismatch')
    corpus=HERE.parents[3]/'unsolved_math_prioritization'
    paths=[corpus/'catalog.json',corpus/'cache/problems.json',corpus/'cache/research_results.json']
    events=[]
    original_stream=c.tool.stream_pin; original_read=c.tool.read_regular; original_parse=c.tool.strict_json
    def stream(path,size,pin):
        original_stream(path,size,pin); events.append({'kind':'full_stream_authenticated','name':path.name})
    def read(path,*args,**kwargs):
        assert path in paths
        assert len([e for e in events if e['kind']=='full_stream_authenticated'])==3
        events.append({'kind':'read_for_parsing','name':path.name})
        return original_read(path,*args,**kwargs)
    def parse(raw):
        assert len([e for e in events if e['kind']=='full_stream_authenticated'])==3
        events.append({'kind':'parse'})
        return original_parse(raw)
    def forbidden(*args,**kwargs):
        raise AssertionError('archival entry point or child execution reached in source-only')
    c.tool.stream_pin=stream; c.tool.read_regular=read; c.tool.strict_json=parse
    c.tool.original_inputs=forbidden; c.tool.package_inputs=forbidden; c.tool.current_inputs=forbidden; c.tool.replay=forbidden
    prior_subprocess=c.tool.subprocess.run; c.tool.subprocess.run=forbidden
    try:
        observed=c.tool.source_only(paths)
    finally:
        c.tool.subprocess.run=prior_subprocess
    c.write_json(HERE/'SOURCE_ONLY_IN_PROCESS_OBSERVATION.json',{'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'actual_cli':False,'instrumented_in_process_only':True,'events':events,'result':observed,'archival_entrypoints_and_subprocess_forbidden':True,'all_three_full_authentications_precede_first_read_or_parse':True})
    failures=[{'label':r['label'],'reason':r['output'].get('reason')} for r in c.RECEIPTS if not r['expectation_met']]
    c.write_json(HERE/'INDEPENDENT_TEST_SUMMARY.json',{'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'completion_percent':92,'tool_sha256':c.EXPECTED_TOOL,'actual_cli_invocations':len(c.RECEIPTS),'distinct_actual_cli_cases':len(set(r['label'] for r in c.RECEIPTS)),'expectations_met':sum(r['expectation_met'] for r in c.RECEIPTS),'unmet_expectations':failures,'engineering_controls_read':False,'whole_package_clearance':False,'separate_in_process_observations':1})
