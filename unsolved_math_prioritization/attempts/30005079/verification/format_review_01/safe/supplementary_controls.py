"""Additional independent checks; keeps raw data in this review's private folder."""
from pathlib import Path
import datetime
import hashlib
import importlib.util
import json
import os
import shutil
import struct
import sys

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('own_controls',HERE/'independent_controls.py')
c=importlib.util.module_from_spec(spec); spec.loader.exec_module(c)
c.CURRENT=c.PRIVATE/'current'
c.RECEIPTS=json.loads((HERE/'ACTUAL_CLI_RECEIPTS.json').read_bytes())
index=c.pin((c.FIXTURE/'package_index.json').read_bytes())['sha256']

if __name__=='__main__':
    # A default replay request must reject changed archival code before importing wheels.
    r=c.PRIVATE/'default_corrupt_source'
    if not r.exists():
        r=c.clone('default_corrupt_source')
    p=r/'source/checks/verify_construction.py'
    marker=c.PRIVATE/'MUST_NOT_EXIST_CORRUPT_SOURCE'
    p.write_bytes((c.FIXTURE/'source/checks/verify_construction.py').read_bytes()+('\nfrom pathlib import Path\nPath(%r).write_bytes(b"BAD")\n'%str(marker)).encode())
    digest=c.repin(r)
    c.run('default_corrupt_source_before_execution',['verify',digest,'--root',r,'--dependency-dir',c.WHEELS],r,wanted=False,reason='pin mismatch: source/')
    assert not marker.exists()
    # The two wheel files have a closed tree and exact byte hashes, independent of suffix.
    wheels=c.PRIVATE/'bad_wheels'; wheels.mkdir()
    os.link(c.WHEELS/'sympy-1.14.0-py3-none-any.whl',wheels/'sympy-1.14.0-py3-none-any.whl')
    shutil.copyfile(c.WHEELS/'mpmath-1.3.0-py3-none-any.whl',wheels/'mpmath-1.3.0-py3-none-any.whl')
    p=wheels/'mpmath-1.3.0-py3-none-any.whl'; raw=bytearray(p.read_bytes()); raw[-1]^=1; p.write_bytes(raw)
    c.run('corrupted_wheel_before_replay',['verify',index,'--root',c.FIXTURE,'--dependency-dir',wheels],wanted=False,reason='pin mismatch: mpmath')
    c.run('default_verify_missing_wheels',['verify',index,'--root',c.FIXTURE],wanted=False,reason='default replay requires')
    output=c.PRIVATE/'output/another/rank-two-fano-verification.zip'; output.parent.mkdir()
    c.run('build_missing_wheels_no_auth_only_fallback',['build',index,output,'--root',c.FIXTURE],wanted=False,reason='default replay requires')
    assert not output.exists() and not list(output.parent.iterdir())
    c.run('build_rejects_verify_only_flag',['build',index,output,'--root',c.FIXTURE,'--verify-only'],wanted=False)
    # Explicit hostile paths and startup hooks are ignored under real -I -S -B.
    hostile=c.PRIVATE/'hostile_environment'; hostile.mkdir()
    environment_marker=hostile/'MUST_NOT_EXIST_ENVIRONMENT'
    hostile_body=('from pathlib import Path\nPath(%r).write_bytes(b"HOSTILE")\nraise RuntimeError("hostile import")\n'%str(environment_marker)).encode()
    for name in ['sitecustomize.py','usercustomize.py','sympy.py','mpmath.py','argparse.py']:
        (hostile/name).write_bytes(hostile_body)
    old={k:os.environ.get(k) for k in ['PYTHONPATH','PYTHONUSERBASE','PYTHONOPTIMIZE']}
    os.environ.update(PYTHONPATH=str(hostile),PYTHONUSERBASE=str(hostile),PYTHONOPTIMIZE='2')
    try:
        c.run('hostile_environment_ignored_real_replay',['verify',index,'--root',c.FIXTURE,'--dependency-dir',c.WHEELS],wanted=True,optimize=True)
    finally:
        for key,value in old.items():
            if value is None: os.environ.pop(key,None)
            else: os.environ[key]=value
    assert not environment_marker.exists()
    c.run('wrong_external_index_pin',['verify','0'*64,'--root',c.FIXTURE,'--dependency-dir',c.WHEELS],wanted=False,reason='external index pin mismatch')
    alias=c.PRIVATE/'output_parent_symlink'; alias.symlink_to(c.PRIVATE/'output',target_is_directory=True)
    c.run('symlink_output_parent',['build',index,alias/'another/rank-two-fano-verification.zip','--root',c.FIXTURE],wanted=False,reason='output parent/ancestor must be nonsymlink directory')
    assert not (c.PRIVATE/'output/another/rank-two-fano-verification.zip').exists()
    # Additional coherent-index raw ZIP metadata and copied-object controls.
    for label,mutate,reason in [
        ('zip_unix_symlink_mode',lambda raw,central:struct.pack_into('<I',raw,central+38,(0o120777<<16)), 'ZIP unsafe central metadata'),
        ('zip_timestamp_mismatch',lambda raw,central:struct.pack_into('<H',raw,central+12,1), 'ZIP unsafe central metadata'),
    ]:
        r=c.clone(label,True); p=r/'rank-two-fano-verification.zip'; raw=bytearray(p.read_bytes()); central=struct.unpack_from('<I',raw,len(raw)-22+16)[0]; mutate(raw,central); p.write_bytes(raw); c.repin(r,True); c.current(label,r,reason=reason)
    r=c.clone('outer_metadata_differs',True)
    c.change_json(r,'metadata.json',lambda x:x.update(description='Different valid text'))
    c.repin(r,True); c.current('outer_metadata_copy_mismatch',r,reason='outer/portable exact copy mismatch')
    # Instrumentation is a separate in-process observation, not an actual CLI count.
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
    c.write_json(HERE/'INDEPENDENT_TEST_SUMMARY.json',{'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'completion_percent':90,'tool_sha256':c.EXPECTED_TOOL,'actual_cli_cases':len(c.RECEIPTS),'all_expectations_met':all(r['expectation_met'] for r in c.RECEIPTS),'engineering_controls_read':False,'whole_package_clearance':False,'separate_in_process_observations':1})
