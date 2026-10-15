#!/usr/bin/env python3
"""Independent finite contract models and private publication experiments."""
import ast
import copy
import datetime as dt
import hashlib
import json
import os
from pathlib import Path, PurePosixPath
import re

HERE=Path(__file__).resolve().parent
REV=HERE.parent/'acceptance_execution_preparation_family/integration_source_revision_v2'
RESULTS=[]
def test(name, wanted, thunk):
    try: actual=bool(thunk())
    except (AssertionError,ValueError,TypeError,KeyError): actual=False
    assert actual is wanted, (name,wanted,actual)
    RESULTS.append({'name':name,'expected':wanted,'observed':actual})

def canonical(name):
    path=PurePosixPath(name)
    return type(name) is str and bool(name) and not path.is_absolute() and '..' not in path.parts and path.as_posix()==name and '\\' not in name and '\0' not in name
def clock(s):
    assert type(s) is str and s==s.strip()
    value=dt.datetime.fromisoformat(s[:-1]+'+00:00' if s.endswith('Z') else s)
    assert value.tzinfo is not None and value.utcoffset()==dt.timedelta(0)
    return value
def interval(start, finish, receipt):
    values=[clock(x) for x in [start,finish,receipt]]
    return values[0]<=values[2]<=values[1]
def capture(names):
    assert len(names)==2
    return len(set(names))==2 and all(canonical(n) and len(PurePosixPath(n).parts)==1 and n not in {'CAPTURE.json','prelaunch_source.py'} for n in names)

t0='2026-10-02T22:00:00Z'; t1='2026-10-02T22:01:00+00:00'; tm='2026-10-02T22:00:30+00:00'
test('UTC interior',True,lambda:interval(t0,t1,tm))
test('UTC exact boundary',True,lambda:interval(t0,t0,t0))
for name,s in [('invalid','yes'),('naive','2026-10-02T22:00:00'),('nonUTC','2026-10-02T22:00:00+02:00'),('bool',True),('padded',' '+tm)]: test('UTC '+name,False,lambda s=s:interval(s,t1,tm))
test('UTC reversed',False,lambda:interval(t1,t0,tm))
test('UTC receipt outside',False,lambda:interval(t0,tm,t1))
test('capture standard',True,lambda:capture(['stdout.bin','stderr.bin']))
test('capture other root names',True,lambda:capture(['out.data','err.data']))
for names in [['stdout.bin','stdout.bin'],['stdout.bin','prelaunch_source.py'],['CAPTURE.json','stderr.bin'],['nested/out','stderr.bin'],['./out','stderr.bin'],['../out','stderr.bin']]: test('capture '+str(names),False,lambda names=names:capture(names))

CACHE={'unsolved_math_prioritization/cache/'+name for name in ['problems.json','research_results.json','catalog.sqlite']}
TRACKED={'draft_pr_publication_program_20260930/inventory.json'}|{'unsolved_math_prioritization/'+n for n in ['QUEUE.md','state.json','history.jsonl','catalog.json','assessments.json','queue.py','policy.json','manifest.json','review_v2/related_target_groups.json']}
NATIVE=CACHE|TRACKED
payload={n:('whole '+n+'\n').encode() for n in NATIVE}
pins={n:{'bytes':len(v),'sha256':hashlib.sha256(v).hexdigest()} for n,v in payload.items()}
git_entries={n:('100644','blob',v) for n,v in payload.items() if n in TRACKED}

def split_check(entries,live,pinned,skip=set()):
    assert set(pinned)==NATIVE and len(pinned)==13
    assert skip<={'unsolved_math_prioritization/QUEUE.md'}
    for n,p in pinned.items():
        assert type(p['bytes']) is int and p['bytes']>=0
        if n in skip: continue
        if n in CACHE:
            assert n not in entries
            body=live[n]
        else:
            assert n in entries and entries[n][0] in {'100644','100755'} and entries[n][1]=='blob'
            body=entries[n][2]
        assert len(body)==p['bytes'] and hashlib.sha256(body).hexdigest()==p['sha256']
    return True
test('S7 preflight cache3 absent tracked10 exact',True,lambda:split_check(git_entries,payload,pins))
test('S7 merge cache3 absent tracked9 exact queue skipped',True,lambda:split_check(git_entries,payload,pins,{'unsolved_math_prioritization/QUEUE.md'}))
for n in sorted(CACHE):
    bad=dict(git_entries); bad[n]=('100644','blob',payload[n])
    test('S7 present ignored '+n,False,lambda bad=bad:split_check(bad,payload,pins))
    badlive=dict(payload); badlive[n]=payload[n]+b'changed'
    test('S7 changed live cache '+n,False,lambda badlive=badlive:split_check(git_entries,badlive,pins))
for n in sorted(TRACKED):
    bad=dict(git_entries); del bad[n]
    test('S7 missing tracked '+n,False,lambda bad=bad:split_check(bad,payload,pins))
    bad=dict(git_entries); bad[n]=('100644','blob',payload[n]+b'changed')
    test('S7 changed tracked full bytes '+n,False,lambda bad=bad:split_check(bad,payload,pins))
bad=dict(git_entries); bad['unsolved_math_prioritization/state.json']=('120000','blob',payload['unsolved_math_prioritization/state.json'])
test('S7 symlink Git mode',False,lambda:split_check(bad,payload,pins))
test('S7 broad skip prohibited',False,lambda:split_check(git_entries,payload,pins,{'unsolved_math_prioritization/state.json'}))
badpins=copy.deepcopy(pins); badpins[next(iter(CACHE))]['bytes']=False
test('S7 bool size rejected',False,lambda:split_check(git_entries,payload,badpins))
badpins=copy.deepcopy(pins); key=next(iter(CACHE)); del badpins[key]; badpins['unsolved_math_prioritization/cache/other.json']=pins[key]
test('S7 generic cache exception prohibited',False,lambda:split_check(git_entries,payload,badpins))

def rebase(o,now):
    created=clock(o['created_utc'])
    return o['approved_by_root'] is True and created<=clock(now) and type(o['reason_date_utc']) is str and o['reason_date_utc']==created.date().isoformat() and type(o['reason']) is str and o['reason']==o['reason'].strip() and len(o['reason'])>=40 and len(o['reason'].split())>=6 and type(o['current_head']) is str and re.fullmatch('[0-9a-f]{40}',o['current_head']) is not None
good={'approved_by_root':True,'created_utc':t0,'reason_date_utc':'2026-10-02','reason':'The completed prior acceptance changed the native state and current main checkpoint.','current_head':'a'*40}
test('rebase complete UTC record',True,lambda:rebase(good,t1))
for key,value in [('approved_by_root',1),('created_utc',t1),('reason_date_utc','2026-10-01'),('reason','yes'),('reason',' '+good['reason']),('current_head','g'*40)]:
    o={**good,key:value}
    test('rebase reject '+key+repr(value),False,lambda o=o:rebase(o,tm))

# Inspect structure as data; never execute candidate functions.
source=(REV/'pr40_guards.py').read_text()
syntax=ast.parse(source)
funcs={n.name:n for n in syntax.body if isinstance(n,ast.FunctionDef)}
native=funcs['native_git_snapshot']
assert any(isinstance(n,ast.If) and ast.unparse(n.test)=='n in IGNORED_CACHE3' for n in ast.walk(native))
assert "native_git_snapshot(merge,load(R/pre['fresh_preimage'])['files'],{'unsolved_math_prioritization/QUEUE.md'})" in source
assert "g.native_git_snapshot(head,fresh['files'])" in (REV/'integrate_reviewed_partial.py').read_text()
assert "os.link(tmp,p,follow_symlinks=False)" in source and source.index('os.link(tmp,p,follow_symlinks=False)')<source.index('tmp.unlink()')
assert 'current_pr=41' in (REV/'integrate_reviewed_partial.py').read_text()
assert "{'current_pr':41,'completed_count':30}" in (REV/'state_mirror_reconciliation.py').read_text()
ast_fact={'source_sha256':hashlib.sha256(source.encode()).hexdigest(),'cache_conditional_present':True,'merge_queue_only_skip_present':True,'preflight_calls_split':True,'hardlink_before_unlink':True,'inventory_write_guard_41':True,'candidate_execution':False}

fixtures=HERE/'publication_fixtures'; fixtures.mkdir()
publications=[]
for name,collision in [('absent',False),('intervening',True)]:
    folder=fixtures/name; folder.mkdir()
    temp=folder/'complete_temp.bin'; target=folder/'target.bin'
    new=b'Complete independent proposed receipt bytes\n'; old=b'Complete intervening authoritative bytes\n'
    with temp.open('xb') as f: f.write(new); f.flush(); os.fsync(f.fileno())
    if collision: target.write_bytes(old)
    try: os.link(temp,target,follow_symlinks=False)
    except FileExistsError as error:
        assert collision and target.read_bytes()==old and temp.read_bytes()==new
        (folder/'ERROR.txt').write_text(repr(error)+'\n')
        publications.append({'case':name,'target_preserved':True,'complete_temp_retained':True,'actual_errno':error.errno})
    else:
        assert not collision and target.read_bytes()==new
        temp.unlink()
        fd=os.open(folder,os.O_RDONLY)
        try: os.fsync(fd)
        finally: os.close(fd)
        publications.append({'case':name,'complete_target_published':True,'temp_removed_after_success':True,'directory_fsync':True})

print(json.dumps({'status':'PASS_OWN_FINITE_CONTROLS','pid':os.getpid(),'utc':dt.datetime.now(dt.timezone.utc).isoformat(),'predicate_controls':RESULTS,'predicate_control_count':len(RESULTS),'AST_source_facts':ast_fact,'private_publication_controls':publications,'candidate_import_compile_execution':False,'actual_future_gate_merge_mirror_post_claimed':False,'new_substantive_attempts':0,'audit_turns':0},indent=2,sort_keys=True))
