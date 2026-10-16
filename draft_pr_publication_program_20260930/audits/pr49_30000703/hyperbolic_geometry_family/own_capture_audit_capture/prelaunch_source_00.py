#!/usr/bin/python3
import datetime,hashlib,json,pathlib
own=pathlib.Path(__file__).parent
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
rows=[]
for p in sorted(own.glob('*_capture/CAPTURE.json')):
    cap=json.loads(p.read_text());folder=p.parent
    pre=json.loads((folder/'PRELAUNCH.json').read_text())
    assert cap['schema']=='actual_command_completed_v1' and pre['schema']=='actual_command_prelaunch_v1'
    assert cap['capture_completed'] is True and type(cap['child_pid']) is int and cap['child_pid']>0
    assert cap['operator_pid']==pre['operator_pid'] and cap['argv']==pre['argv'] and cap['cwd']==pre['cwd']
    assert pathlib.Path(cap['cwd']).is_dir()
    assert cap['prelaunch']['sha256']==sha(folder/'PRELAUNCH.json')
    for name in ['stdout','stderr']:
        q=folder/(name+'.bin')
        assert cap[name]['bytes']==q.stat().st_size and cap[name]['sha256']==sha(q)
    q=folder/'prelaunch_operator.py'
    assert pre['operator_copy']['sha256']==sha(q)==pre['operator']['sha256']
    assert pre['prelaunch_utc']<=cap['started_utc']<=cap['completed_utc']
    for src in pre['sources']:
        q=pathlib.Path(src['copied']['path'])
        assert src['byte_identical'] is True and src['original']['sha256']==src['copied']['sha256']==sha(q)
        assert src['original']['bytes']==src['copied']['bytes']==q.stat().st_size
    assert cap['returncode']==0
    rows.append({'capture':str(folder.relative_to(own)),'child_pid':cap['child_pid'],'returncode':cap['returncode'],'prelaunch_and_operator_source_copies_verified':True,'source_copies_verified':len(pre['sources']),'full_split_streams_verified':True,'stdout_bytes':cap['stdout']['bytes'],'stderr_bytes':cap['stderr']['bytes']})
result={'utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),'completed_existing_captures_checked':len(rows),'rows':rows,'scope':'Completed captures existing before this audit launched. This audit command has its own separate actual capture and is excluded from this earlier count; final closure verifies every payload identity.'}
(own/'OWN_CAPTURE_RESULT.json').write_text(json.dumps(result,indent=2)+'\n')
print(json.dumps({'completed_existing_captures_checked':len(rows),'all_verified':True}))
