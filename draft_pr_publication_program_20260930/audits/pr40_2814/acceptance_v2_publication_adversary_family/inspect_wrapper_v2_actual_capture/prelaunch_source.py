#!/usr/bin/env python3
"""Independent wrapper source/data review and finite interface/publication controls."""
import argparse
import ast
import ctypes
import datetime as dt
import hashlib
import json
import os
from pathlib import Path
import sys

ROOT=Path('/Users/alec/Documents/Math')
HERE=Path(__file__).resolve().parent
AUDIT=HERE.parent
PACKAGE=AUDIT/'root_runner_preparation_family'
WRAPPER=AUDIT/'execute_root_acceptance_revised.py'
INPUTS={}
def sha(data): return hashlib.sha256(data).hexdigest()
def read(path):
    assert path.is_file() and not path.is_symlink()
    for parent in path.parents:
        assert not parent.is_symlink()
        if parent==ROOT: break
    raw=path.read_bytes()
    INPUTS[str(path.relative_to(ROOT))]={'path':str(path.relative_to(ROOT)),'bytes':len(raw),'sha256':sha(raw),'mode':path.stat().st_mode & 0o777}
    return raw
def strict(raw):
    def pairs(p):
        o={}
        for k,v in p:
            assert k not in o
            o[k]=v
        return o
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=lambda x: (_ for _ in ()).throw(ValueError(x)))
def bound(row):
    raw=read(ROOT/row['path'])
    assert len(raw)==row['bytes'] and sha(raw)==row['sha256']
    if 'mode' in row: assert (ROOT/row['path']).stat().st_mode & 0o777 == row['mode']
def closure(base,name,pin,count):
    raw=read(base/name)
    assert sha(raw)==pin
    obj=strict(raw)
    assert type(obj['files_count']) is int and obj['files_count']==count and len(obj['files'])==count
    names=set()
    for item in obj['files']:
        assert type(item['bytes']) is int and item['bytes']>=0 and item['path'] not in names and item['path']!=name
        names.add(item['path'])
        payload=read(base/item['path'])
        assert len(payload)==item['bytes'] and sha(payload)==item['sha256']
    actual={str(p.relative_to(base)) for p in base.rglob('*') if p.is_file()}
    expected_dirs={str(parent) for member in names for parent in Path(member).parents if str(parent) != '.'}
    actual_dirs={str(p.relative_to(base)) for p in base.rglob('*') if p.is_dir()}
    assert actual==names|{name} and actual_dirs==expected_dirs
    assert all((p.is_file() or p.is_dir()) and not p.is_symlink() for p in base.rglob('*'))
    return obj

manifest=closure(PACKAGE,'MANIFEST.json','aa58d2e3a9f470c6ce8d2781e47c72605de8338ee6766bb390a7f57ab7f42d50',11)
assert all((p.stat().st_mode & 0o777)==0o444 for p in PACKAGE.iterdir())
wrapper=read(WRAPPER)
assert len(wrapper)==27934 and sha(wrapper)=='f00d8be3926b02d10f46a351802688a87f107d406c842317f51a5674248d4215'
assert WRAPPER.stat().st_mode & 0o777 == 0o644
assert wrapper==read(PACKAGE/'WRAPPER_SOURCE.py.txt')
syntax=ast.parse(wrapper,filename=str(WRAPPER))
literal={node.targets[0].id:node.value for node in syntax.body if isinstance(node,ast.Assign) and len(node.targets)==1 and isinstance(node.targets[0],ast.Name)}
gate_names=ast.literal_eval(literal['GATE_NAMES'])
native=ast.literal_eval(literal['NATIVE13'])
allowed=ast.literal_eval(literal['ALLOWED'])
assert len(native)==len(set(native))==13
assert len(gate_names)==6
source_bindings=strict(read(PACKAGE/'SOURCE_BINDINGS.json'))
for item in source_bindings['whole_source_pins']: bound(item)
for item in source_bindings['immutable_exact_closures']:
    bound(item['manifest'])
    closure(ROOT/item['root'],Path(item['manifest']['path']).name,item['manifest']['sha256'],item['authored_members_excluding_self'])
assert tuple(source_bindings['native13_ordered_paths'])==native
assert source_bindings['helper_gate_string_count']==13 and source_bindings['allowed_native_mode_changes']==[]
for name in ['actual_pid','actual_exit_code','actual_current_head','actual_fresh_created_utc','actual_previous_pr39_mirror_sha256']:
    assert source_bindings[name] is None
for name in ['actual_root_execution','approved_by_root','root_full_runner_and_helper_review_completed','new_independent_runner_review_completed','wrapper_import_compile_execution','candidate_helper_import_compile_execution']:
    assert source_bindings[name] is False
for item in manifest['files']:
    if item['path'].endswith('.json'): strict(read(PACKAGE/item['path']))

# Authoring capture is retained provenance, not helper/wrapper execution.
capture_dir=AUDIT/'acceptance_execution_preparation_family/prepare_root_runner_package_actual_capture'
author=strict(read(capture_dir/'CAPTURE.json'))
assert author['actual_execution'] is True and author['completed'] is True and type(author['pid']) is int and author['pid']==74744 and type(author['exit_code']) is int and author['exit_code']==0
assert author['candidate_helper_or_ROOT_wrapper_import_compile_execution'] is False
assert dt.datetime.fromisoformat(author['started_utc'])<=dt.datetime.fromisoformat(author['finished_utc'])
assert {p.name for p in capture_dir.iterdir()}=={'CAPTURE.json','prelaunch_source.py','stdout.bin','stderr.bin'}
for name in ['prelaunch_source','stdout','stderr']:
    item=author[name]; raw=read(capture_dir/item['path']); assert len(raw)==item['bytes'] and sha(raw)==item['sha256']
assert sha(read(capture_dir/'prelaunch_source.py'))==author['source_sha256']
author_stdout=strict(read(capture_dir/'stdout.bin'))
assert author_stdout['actual_root_execution'] is False and author_stdout['wrapper_import_compile_execution'] is False

# Independent contract parser: this models flag shapes, never a candidate invocation.
tests=[]
def interface(phase,args):
    class Rejected(Exception): pass
    class Quiet(argparse.ArgumentParser):
        def error(self,message): raise Rejected(message)
    p=Quiet(add_help=False)
    if phase=='final':
        p.add_argument('--execute',action='store_true');
        for n in ['plan','plan-sha256','preparation-manifest-sha256','output']: p.add_argument('--'+n,required=True)
    else:
        if phase not in {'mirror','post'}: p.add_argument('phase',choices=['preflight','overlay','prepush','finalize'])
        p.add_argument('--execute',action='store_true')
        p.add_argument('--preparation-manifest-sha256',required=True)
        for n in gate_names:
            p.add_argument('--'+n,required=True); p.add_argument('--'+n+'-sha256',required=True)
        p.add_argument('--merge-queue-preimage-sha256')
    try: value=p.parse_args(args)
    except Rejected: return False
    return value.execute is True
keys={'preparation-manifest-sha256'}|set(gate_names)|{n+'-sha256' for n in gate_names}
assert len(keys)==13
for phase in ['preflight','overlay','prepush','finalize','mirror','post']:
    args=([phase] if phase not in {'mirror','post'} else [])+['--execute']
    for name in sorted(keys): args+=['--'+name,'SYNTHETIC_LOCAL_CONTRACT_VALUE']
    if phase=='overlay': args+=['--merge-queue-preimage-sha256','SYNTHETIC_QUEUE_PIN']
    assert interface(phase,args)
    tests.append({'case':'valid local '+phase+' flag shape','accepted':True})
    assert not interface(phase,args+['--fresh-queue-preimage-sha256','PR39_ONLY_INVALID_FLAG'])
    tests.append({'case':'reject PR39-only flag '+phase,'accepted':False})
fargs=['--execute','--plan','SYNTHETIC_PLAN','--plan-sha256','SYNTHETIC_PIN','--preparation-manifest-sha256','SYNTHETIC_PREP','--output','SYNTHETIC_OUTPUT']
assert interface('final',fargs) and not interface('final',fargs[:-2])
tests += [{'case':'valid local final output shape','accepted':True},{'case':'reject missing mandatory final output','accepted':False}]

def result_status(actual,completed,pid,exit_code,timed_out,native_ok,checks_ok,errors):
    return actual is True and completed is True and type(pid) is int and pid>0 and type(exit_code) is int and exit_code==0 and not timed_out and native_ok and checks_ok and not errors
good=[True,True,1234,0,False,True,True,[]]
assert result_status(*good)
for i,bad in [(0,False),(1,False),(2,True),(2,None),(3,False),(3,1),(4,True),(5,False),(6,False),(7,['outer error'])]:
    mutant=list(good); mutant[i]=bad
    assert not result_status(*mutant)
    tests.append({'case':'reject incomplete/error capture field '+str(i)+' '+repr(bad),'accepted':False})
for phase in ['final','preflight','overlay','prepush','finalize','mirror','post']:
    permitted=allowed.get(phase,set())
    assert permitted <= set(native)
    for changed in native:
        answer={changed}<=permitted
        tests.append({'case':'native byte scope '+phase+' '+changed,'accepted':answer})
    tests.append({'case':'native mode change always rejected '+phase,'accepted':False})

code=wrapper.decode()
facts={
    'final_output_flag':"'--output', final_output.name" in code,
    'exact13_complete_strings':'len(keys) == 13' in code and 'all(type(value) is str for value in gates.values())' in code,
    'source_and_review_before_after':'check_preparation()' in code and 'Complete ROOT review bytes/mode changed during child' in code,
    'four_final_five_nonfinal_capture':"if phase != 'final':\n        names.add('prelaunch_guards.py')" in code,
    'real_Popen_and_full_stdio':'child = subprocess.Popen(argv' in code and 'out, err = child.communicate(timeout=180)' in code,
    'failure_cannot_PASS':'not record[\'timed_out\'] and native_ok and checks_ok and not errors' in code,
    'exclusive_directory_publication': 'rename(os.fsencode(stage), os.fsencode(destination), 0x00000004)' in code,
    'final_output_reserved_names_rejected': 'final_output.name not in reserved_captures' in code,
    'present_null_current_metadata': all("'"+n+"': None" in code for n in ['current_model','current_reasoning_effort','current_deadline_utc']),
    'post_inventory41': "{'current_pr': CURRENT_PR_AFTER_ACCEPTANCE" in code,
}
assert all(facts.values())
assert sys.platform=='darwin'
lib=ctypes.CDLL(None,use_errno=True)
rename=lib.renamex_np
rename.argtypes=[ctypes.c_char_p,ctypes.c_char_p,ctypes.c_uint]; rename.restype=ctypes.c_int
fixtures=HERE/'directory_publication_fixtures'; fixtures.mkdir()
publication=[]
for name,kind in [('absent','absent'),('empty_intervening','empty'),('populated_intervening','populated')]:
    base=fixtures/name; base.mkdir()
    stage=base/'complete_stage'; stage.mkdir()
    (stage/'payload.bin').write_bytes(b'Full proposed independent capture\n')
    target=base/'capture'
    if kind!='absent':
        target.mkdir()
        if kind=='populated': (target/'authoritative.bin').write_bytes(b'Full existing capture\n')
    rc=rename(os.fsencode(stage),os.fsencode(target),4)
    if kind=='absent':
        assert rc==0 and not stage.exists() and (target/'payload.bin').read_bytes()==b'Full proposed independent capture\n'
        publication.append({'case':name,'published_complete_directory':True})
    else:
        errno=ctypes.get_errno()
        assert rc==-1 and errno==17 and stage.is_dir() and (stage/'payload.bin').read_bytes()==b'Full proposed independent capture\n'
        assert target.is_dir() and (not list(target.iterdir()) if kind=='empty' else (target/'authoritative.bin').read_bytes()==b'Full existing capture\n')
        (base/'ERROR.txt').write_text(str(OSError(errno,os.strerror(errno)))+'\n')
        publication.append({'case':name,'actual_errno':errno,'existing_target_preserved':True,'complete_stage_retained':True})
    fd=os.open(base,os.O_RDONLY)
    try: os.fsync(fd)
    finally: os.close(fd)

print(json.dumps({'status':'PASS_WRAPPER_SOURCE_AND_OWN_CONTROLS','pid':os.getpid(),'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'wrapper_lines':len(wrapper.splitlines()),'wrapper_sha256':sha(wrapper),'wrapper_package_manifest_sha256':sha(read(PACKAGE/'MANIFEST.json')),'input_members':[INPUTS[k] for k in sorted(INPUTS)],'AST_source_facts':facts,'local_contract_cases':tests,'local_contract_case_count':len(tests),'actual_private_directory_publication_controls':publication,'reviewed_wrapper_helper_import_compile_execution':False,'actual_future_final_gate_merge_mirror_post_claimed':False,'authoring_capture_is_runtime_certificate':False,'new_substantive_attempts':0,'audit_turns':0},indent=2,sort_keys=True))
