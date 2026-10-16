#!/usr/bin/env python3
"""Own independent finite contract controls. Production is read only, never evaluated."""
import copy
import ctypes
import datetime as dt
import hashlib
import json
import math
import os
from pathlib import Path, PurePosixPath
import re
import stat
import subprocess
import sys

HERE=Path(__file__).absolute().parent
AUDIT=HERE.parent
REPO=AUDIT.parents[2]
counts={}
rejects=[]
def demand(value,label):
    assert value,label
    counts[label]=counts.get(label,0)+1
def digest(raw):return hashlib.sha256(raw).hexdigest()
def stamp():return dt.datetime.now(dt.timezone.utc).isoformat()
def decode(raw):
    def pairs(items):
        result={}
        for key,value in items:
            if key in result:raise ValueError('duplicate')
            result[key]=value
        return result
    def constant(x):raise ValueError('nonfinite')
    def number(x):
        value=float(x)
        if not math.isfinite(value):raise ValueError('overflow')
        return value
    return json.loads(raw,object_pairs_hook=pairs,parse_constant=constant,parse_float=number)
def path_ok(name):
    if type(name) is not str or not name or '\\' in name:raise ValueError('path')
    path=PurePosixPath(name)
    if path.is_absolute() or path.as_posix()!=name or {'.','..','.git','__pycache__'}.intersection(path.parts):raise ValueError('path')
    return name
def row_ok(row):
    if type(row) is not dict or set(row)!={'path','bytes','sha256'}:raise ValueError('fields')
    path_ok(row['path'])
    if type(row['bytes']) is not int or row['bytes']<0 or type(row['sha256']) is not str or not re.fullmatch('[0-9a-f]{64}',row['sha256']):raise ValueError('types')
def must_reject(fn,value,label):
    try:fn(value)
    except (ValueError,TypeError,KeyError):rejects.append(label);demand(True,'rejection')
    else:raise AssertionError('accepted mutant '+label)
def whole(path):
    demand(not path.is_symlink() and all(not parent.is_symlink() for parent in path.parents),'non_symlink')
    demand(stat.S_ISREG(path.stat().st_mode),'regular')
    body=path.read_bytes()
    if path.suffix=='.json':decode(body)
    if path.suffix=='.jsonl':
        for line in body.splitlines():decode(line)
    return body

production_names=['prepare_current_packet.py','capture_root_builder_operation.py']
production={name:whole(HERE/name) for name in production_names}
text=production['prepare_current_packet.py'].decode()
operator=production['capture_root_builder_operation.py'].decode()
for exact in ["BASE = '01358d66fc67d1c462bddf31c0d4ee5b120e6737'",'PR44_ROOT_CURRENT_REPRODUCTION_SUMMARY_v1',
              "rows(current['files']) == NATIVE", "stat.S_IMODE(path.stat().st_mode) == 0o444",
              "rename(os.fsencode(source), os.fsencode(destination), 4)",
              "equal(summary['entire_author_result'], saved)","equal(summary['entire_independent_result'], independent)",
              "[row['turn'] for row in ledger] == [1, 2]",'new_source_adversary_closed_clean_complete_report_personally_read',
              "args.root_evidence_bindings_sha256", "actual_manifest['self_excluded'] == ['MANIFEST.json']"]:
    demand(exact in text,'source_contract_text')
for name in production_names:
    source=production[name].decode()
    for banned in ['importlib','runpy','exec(', 'eval(', 'compile(', 'git push','git commit', 'shutil.rmtree']:
        demand(banned not in source,'no_forbidden_text_mechanism')
for exact in ['PR44_ROOT_OUTER_CAPTURE', 'PRELAUNCH_BUILDER_SOURCE.py', 'PRELAUNCH_OPERATOR.py',
              'root_evidence_bindings', "child.wait(timeout=600)", "record['completed'] is True"]:
    demand(exact in operator,'outer_actual_contract_text')
masked_false_positives=[]
for mode in range(0o10000):
    exact=mode==0o444
    masked=(mode & 0o777)==0o444
    if masked and not exact:masked_false_positives.append(mode)
    demand(exact==(mode in [0o444]),'all4096_full_modes')
demand(len(masked_false_positives)==7 and set(masked_false_positives)=={0o444|bit for bit in range(0o1000,0o10000,0o1000)},'mask_only_seven_false_positives')
fixture=HERE/'private_controls'
fixture.mkdir(exist_ok=False)
observations=[]
for mode in [0o444,0o1444,0o2444,0o4444]:
    member=fixture/('mode_'+format(mode,'05o'))
    member.write_bytes(b'exact full-mode observation\n')
    member.chmod(mode)
    observed=stat.S_IMODE(member.stat().st_mode)
    demand(observed==mode,'actual_special_mode_set')
    demand((observed==0o444)==(mode==0o444),'actual_special_mode_rejection_predicate')
    observations.append({'path':member.name,'observed_at_test_full_mode':format(observed,'04o'),
                         'accepted_by_exact_full444_predicate':observed==0o444,
                         'later_frozen_source_fixture_mode':'0444'})
    member.chmod(0o444)
base={'path':'folder/member.json','bytes':0,'sha256':digest(b'')}
row_ok(base);demand(True,'valid_row')
for key,value,label in [('bytes',True,'bool_bytes'),('bytes',-1,'negative_bytes'),('bytes',1.0,'float_bytes'),
                        ('sha256','0'*63,'short_hash'),('sha256','A'*64,'uppercase_hash'),('path','../x','escape'),
                        ('path','/absolute','absolute'),('path','a//b','noncanonical'),('path','a\\b','backslash'),
                        ('path','a/./b','dot'),('path','a/.git/b','git_path'),('path','a/__pycache__/b','pycache')]:
    value_row=dict(base);value_row[key]=value
    must_reject(row_ok,value_row,label)
extra=dict(base,unknown=True);must_reject(row_ok,extra,'extra_row_key')
for raw,label in [(b'{"a":1,"a":2}','duplicate_JSON_key'),(b'{"x":NaN}','NaN'),
                  (b'{"x":Infinity}','Infinity'),(b'{"x":1e999}','float_overflow')]:must_reject(decode,raw,label)
for left,right in [(True,1),(0,False),(None,False),(1,1.0)]:
    demand(json.dumps(left,separators=(',',':'))!=json.dumps(right,separators=(',',':')),'typed_scalar_tokens')
draft=decode(whole(HERE/'DRAFT_ROOT_READ_LEDGER.json'))
demand(draft['reading_completed'] is False and all(value is False for value in draft['root_flags'].values()),'draft_false_flags')
for name in ['DRAFT_ROOT_EVIDENCE_BINDINGS.json','DRAFT_ROOT_CURRENT_INPUT_PREIMAGES.json']:
    obj=decode(whole(HERE/name));demand(obj['approved_by_root'] is False and obj['created_utc'] is None,'draft_pending')
native={ 'unsolved_math_prioritization/'+name for name in ['QUEUE.md','state.json','history.jsonl','catalog.json','assessments.json',
         'queue.py','policy.json','manifest.json','cache/problems.json','cache/research_results.json','cache/catalog.sqlite',
         'review_v2/related_target_groups.json']}
native.add('draft_pr_publication_program_20260930/inventory.json')
demand(len(native)==13,'native_set13')
bindings=decode(whole(HERE/'STATIC_INPUT_BINDINGS.json'))
full_reads=0
for row in bindings['auxiliary']:
    row_ok(row);body=whole(AUDIT/row['path']);full_reads+=1
    demand(len(body)==row['bytes'] and digest(body)==row['sha256'],'aux_full_pin')
for name,obj in bindings['families'].items():
    own={r['path'] for r in obj['copied_members']}; foreign={r['path'] for r in obj['foreign_members']}
    demand(not own.intersection(foreign),'disjoint_ownership')
    actual={p.relative_to(AUDIT/name).as_posix() for p in (AUDIT/name).rglob('*') if p.is_file()}
    demand(actual==own|foreign|{obj['manifest']['path']},'family_exact_topology')
    for row in obj['copied_members']+obj['foreign_members']+[obj['manifest']]:
        row_ok(row);body=whole(AUDIT/name/row['path']);full_reads+=1
        demand(len(body)==row['bytes'] and digest(body)==row['sha256'],'family_full_pin')
        demand(stat.S_IMODE((AUDIT/name/row['path']).stat().st_mode)==0o444,'family_full_modes')
    for row in obj['external_inputs']:
        row_ok(row);body=whole(AUDIT/row['path']);full_reads+=1
        demand(len(body)==row['bytes'] and digest(body)==row['sha256'],'family_external_full_pin')
for name,row in bindings['original18'].items():
    row_ok(row);body=whole(AUDIT/row['path']);full_reads+=1
    demand(len(body)==row['bytes'] and digest(body)==row['sha256'],'original18_full_pin')

demand(sys.platform=='darwin','macOS_exclusive_rename_control')
libc=ctypes.CDLL(None,use_errno=True)
rename=libc.renamex_np
rename.argtypes=[ctypes.c_char_p,ctypes.c_char_p,ctypes.c_uint];rename.restype=ctypes.c_int
src=fixture/'rename_source'; dst=fixture/'rename_existing'
src.mkdir();dst.mkdir()
(src/'member').write_bytes(b'new\n');(dst/'sentinel').write_bytes(b'keep\n')
code=rename(os.fsencode(src),os.fsencode(dst),4);error=ctypes.get_errno()
demand(code==-1 and error==17,'exclusive_existing_rejection')
demand((src/'member').read_bytes()==b'new\n' and (dst/'sentinel').read_bytes()==b'keep\n','existing_tree_preserved')
absent=fixture/'rename_absent'
demand(rename(os.fsencode(src),os.fsencode(absent),4)==0 and not src.exists() and (absent/'member').read_bytes()==b'new\n','exclusive_absent_success')

git_directory=HERE/'private_readonly_git'
git_directory.mkdir()
commands=[]
for args in [['branch','--show-current'],['rev-parse','HEAD']]:
    index=len(commands);argv=['git',*args];rec={'argv':argv,'cwd':str(REPO),'started_utc':stamp()}
    with (git_directory/(str(index)+'.stdout')).open('xb') as out,(git_directory/(str(index)+'.stderr')).open('xb') as err:
        child=subprocess.Popen(argv,cwd=REPO,stdin=subprocess.DEVNULL,stdout=out,stderr=err,env=dict(os.environ,GIT_OPTIONAL_LOCKS='0'))
        rec.update(pid=child.pid,actual_execution=True,exit_code=child.wait(timeout=60),completed=True,stdin_supplied=False)
    rec['finished_utc']=stamp()
    for channel in ['stdout','stderr']:
        body=(git_directory/(str(index)+'.'+channel)).read_bytes()
        rec[channel]={'path':'private_readonly_git/'+str(index)+'.'+channel,'bytes':len(body),'sha256':digest(body)}
    demand(rec['exit_code']==0 and rec['stderr']['bytes']==0,'readonly_Git_success')
    commands.append(rec)
demand((git_directory/'0.stdout').read_bytes().strip()==b'main','main_branch')
for name,body in production.items():demand(whole(HERE/name)==body,'production_sources_unchanged')
result={'schema':'PR44_OWN_INDEPENDENT_SOURCE_CONTRACT_CONTROLS_v1','utc':stamp(),'status':'PASS',
        'assertions':sum(counts.values()),'categories':counts,'rejected_mutants':rejects,
        'bound_full_input_reads':full_reads,'actual_mode_observations':observations,
        'mask_only_false_positive_full_modes':[format(mode,'04o') for mode in masked_false_positives],
        'fixtures_frozen_after_observations':True,'production_import_compile_exec':False,
        'production_source_sha256':{k:digest(v) for k,v in production.items()},'actual_readonly_git_commands':commands,
        'native_Git_or_remote_mutations':False,'scientific_assertions':0,'new_substantive_attempts':0,'audit_turns':0}
(HERE/'PRIVATE_CONTRACT_CONTROL_RESULTS.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({k:result[k] for k in ['status','assertions','bound_full_input_reads','rejected_mutants','production_import_compile_exec']},indent=2))
