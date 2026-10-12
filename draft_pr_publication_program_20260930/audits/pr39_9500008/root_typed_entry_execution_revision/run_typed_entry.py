#!/usr/bin/env python3
"""Root-only typed gate and controls, then unchanged builder with literal argv.

Static preparation asserts no execution. Every actual attempt retains source,
full streams/clocks and failure; no private attempt is deleted automatically.
"""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import sys
import tempfile
import traceback

HERE = Path(__file__).resolve().parent
AUDIT = HERE.parent
SHA = lambda data: hashlib.sha256(data).hexdigest()
ENCODE = lambda value: (json.dumps(value, indent=2)+'\n').encode()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--capture-directory', type=Path, required=True)
    parser.add_argument('builder_argv', nargs=argparse.REMAINDER)
    args = parser.parse_args(); command = args.builder_argv
    if command and command[0] == '--': command = command[1:]
    capture = args.capture_directory.resolve()
    assert capture.parent == AUDIT and not capture.exists() and not capture.is_symlink()
    capture.mkdir(); runs = []; private = None
    receipt = {'status':'INCOMPLETE','actual_runs':runs,'builder_invoked':False,'new_substantive_attempts':0,'audit_turns':0}
    original_error = original_tb = None
    def write(name, data):
        path = capture/name; path.parent.mkdir(parents=True, exist_ok=True)
        try: path.write_bytes(data)
        except OSError:
            if private is not None:
                fallback = private/'retention_fallback'/name; fallback.parent.mkdir(parents=True, exist_ok=True); fallback.write_bytes(data)
            raise
        return {'path':path.relative_to(AUDIT).as_posix(),'size':len(data),'sha256':SHA(data)}
    def run(label, argv, source, expected):
        row = {'label':label,'argv':argv,'cwd':str(AUDIT),'started_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'launch_attempted':False,'actual_execution':False,'completed':False,'exit_code':None,'stdin_supplied':False,'timeout_seconds':600}
        runs.append(row); error = tb = result = None; launched = False
        try:
            row['source'] = write('sources/'+label+'.py',source.read_bytes())
            for channel in ['stdout','stderr']: row[channel] = write('streams/'+label+'.'+channel,b'')
            row['stdio_kind']='prelaunch_empty_placeholder'; write('RUNS.json',ENCODE(runs))
            row['launch_attempted']=True; write('RUNS.json',ENCODE(runs))
            try:
                launched=True;result=subprocess.run(argv,cwd=AUDIT,capture_output=True,timeout=600,env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',GIT_OPTIONAL_LOCKS='0'))
                row.update(actual_execution=True,completed=True,exit_code=result.returncode,stdio_kind='complete_child_streams'); values={'stdout':result.stdout,'stderr':result.stderr}
            except subprocess.TimeoutExpired as caught:
                error,tb=caught,caught.__traceback__;row.update(actual_execution=True,stdio_kind='partial_timeout');values={'stdout':caught.stdout,'stderr':caught.stderr}
            except OSError as caught:
                error,tb=caught,caught.__traceback__;row['stdio_kind']='no_child_launched';values={'stdout':None,'stderr':None}
            for channel,value in values.items():
                data=value.encode() if isinstance(value,str) else value or b''
                row[channel]=write('streams/'+label+'.'+channel,data);row[channel]['available']=value is not None
        except BaseException as caught:
            if not launched:row['launch_attempted']=False
            if error is None:error,tb=caught,caught.__traceback__
            else:row['secondary_retention_failure']=str(caught)
        finally:
            row['ended_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat()
            if error:row['failure']={'type':type(error).__name__,'message':str(error),'traceback':''.join(traceback.format_exception(type(error),error,tb))}
            try:write('RUNS.json',ENCODE(runs))
            except BaseException as caught:
                row['secondary_ledger_failure']=str(caught)
                if error is None:error,tb=caught,caught.__traceback__
        if error:raise error.with_traceback(tb)
        assert result.returncode==expected and not result.stderr, 'Wrong actual outcome; full streams retained'
        return json.loads(result.stdout)
    try:
        assert not sys.flags.optimize
        manifest=json.loads((HERE/'PREPARATION_MANIFEST.json').read_bytes())
        names={x['path'] for x in manifest['files']};assert manifest['excluded']==['PREPARATION_MANIFEST.json']
        assert {x.relative_to(HERE).as_posix() for x in HERE.rglob('*') if x.is_file()}==names|{'PREPARATION_MANIFEST.json'}
        assert not any(x.is_symlink() for x in HERE.rglob('*'))
        for row in manifest['files']:
            data=(HERE/row['path']).read_bytes();assert len(data)==row['size'] and SHA(data)==row['sha256'];write('prepared/'+row['path'],data)
        write('prepared/PREPARATION_MANIFEST.json',(HERE/'PREPARATION_MANIFEST.json').read_bytes())
        schema=json.loads((HERE/'frozen_type_schema.json').read_bytes());builder=AUDIT/schema['builder']['path']
        assert SHA(builder.read_bytes())==schema['builder']['sha256'] and command[:2]==['/usr/bin/python3',str(builder)]
        flags=command[2:];assert '--execute' in flags and flags.count('--execute')==1;flags=[x for x in flags if x!='--execute']
        assert len(flags)%2==0 and len(flags)//2==len(schema['builder']['literal_flags'])
        pairs=list(zip(flags[::2],flags[1::2]));assert len({k for k,v in pairs})==len(pairs) and dict(pairs)==schema['builder']['literal_flags']
        write('LITERAL_BUILDER_COMMAND.json',ENCODE(command));write('sources/unchanged_505_builder.py',builder.read_bytes())
        (AUDIT/'tmp').mkdir(exist_ok=True);private=Path(tempfile.mkdtemp(prefix='root_pr39_typed_',dir=AUDIT/'tmp'))
        guard=private/'typed_guard.py';guard.write_bytes((HERE/'typed_guard.py').read_bytes());guard.chmod(0o444)
        baseline=run('typed_baseline',['/usr/bin/python3',str(guard),'--schema',str(HERE/'frozen_type_schema.json'),'--audit-root',str(AUDIT)],guard,0)
        assert baseline['status']=='ACCEPTED_TYPED_METADATA' and baseline['entries']==len(schema['entries'])
        cases=json.loads((HERE/'control_cases.json').read_bytes());assert len(cases)>=11 and len({x['label'] for x in cases})==len(cases)
        for case in cases:
            value=json.loads((AUDIT/case['entry']).read_bytes());parent=value
            for key in case['path'][:-1]:parent=parent[key]
            key=case['path'][-1]
            if case['action']=='set':parent[key]=case['value']
            elif case['action']=='delete':del parent[key]
            elif case['action']=='duplicate_row':parent[key][1]=json.loads(json.dumps(parent[key][0]))
            else:assert case['action']=='duplicate_key'
            data=ENCODE(value)
            if case['action']=='duplicate_key':data=(json.dumps(value)[:-1]+', '+json.dumps(str(key))+': '+json.dumps(parent[key])+'}\n').encode()
            mutation=private/(case['label']+'.json');mutation.write_bytes(data);write('controls/'+case['label']+'.input.json',data)
            actual=run(case['label'],['/usr/bin/python3',str(guard),'--schema',str(HERE/'frozen_type_schema.json'),'--audit-root',str(AUDIT),'--single-entry',case['entry'],'--single-file',str(mutation)],guard,1)
            assert actual['status']=='REJECTED_TYPED_METADATA' and actual['kind']==case['expected_kind']
        # Recheck every approved byte/type after controls and immediately before
        # invoking root's literal command; controls never edit live inputs.
        run('typed_final_prebuild',['/usr/bin/python3',str(guard),'--schema',str(HERE/'frozen_type_schema.json'),'--audit-root',str(AUDIT)],guard,0)
        receipt['builder_invoked']=True;actual=run('unchanged_builder',command,builder,0)
        assert actual['status']=='CURRENT_PACKET_FROZEN_NEW_WHOLE_GATE_PENDING'
        receipt.update(status='TYPED_ADMINISTRATIVE_ENTRY_COMPLETED_NEW_WHOLE_GATE_PENDING',controls=len(cases),builder_result=actual)
    except BaseException as caught:
        original_error,original_tb=caught,caught.__traceback__;receipt.update(status='FAIL',failure={'type':type(caught).__name__,'message':str(caught),'traceback':''.join(traceback.format_exception(type(caught),caught,original_tb))})
    finally:
        receipt['finished_utc']=datetime.datetime.now(datetime.timezone.utc).isoformat();receipt['private_attempt_preserved']=private is not None
        receipt['private_attempt_path']=str(private) if private is not None else None
        try:
            write('TYPED_ENTRY_RECEIPT.json',ENCODE(receipt))
            rows=[]
            for path in sorted(capture.rglob('*')):
                assert not path.is_symlink()
                if path.is_file() and path.relative_to(capture).as_posix()!='TYPED_ENTRY_MANIFEST.json':
                    data=path.read_bytes();rows.append({'path':path.relative_to(capture).as_posix(),'size':len(data),'sha256':SHA(data)})
            write('TYPED_ENTRY_MANIFEST.json',ENCODE({'status':receipt['status'],'excluded':['TYPED_ENTRY_MANIFEST.json'],'files':rows,'schema_and_guard_retained':True,'foreign_or_private_clone_bodies_retained':False}))
        except BaseException as secondary:
            print('Typed-entry retention failed: '+str(secondary),file=sys.stderr)
            if original_error is None:original_error,original_tb=secondary,secondary.__traceback__
        if original_error:print(receipt.get('failure',str(original_error)),file=sys.stderr)
    if original_error:raise original_error.with_traceback(original_tb)
    print(json.dumps({'status':receipt['status'],'capture':str(capture),'controls':receipt['controls']},indent=2))


if __name__=='__main__':main()
