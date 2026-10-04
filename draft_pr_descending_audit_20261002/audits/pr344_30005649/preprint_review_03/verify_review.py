"""Read-only review replay, using owned snapshots and standard-library Python.

Default replays both public default verifiers. --full additionally replays
both public full verifiers, every control, independent arithmetic, and direct
mathematical negatives. --preflight is explicitly unfinished custody and
must never be interpreted as final clearance. No external source is read.
"""
import datetime, hashlib, json, os, pathlib, stat, subprocess, sys
from audit_relations import R,P,check,load,require,pin
RUNTIMES={'py314':'/opt/homebrew/bin/python3','py312':'/Users/alec/.cache/codex-runtimes/codex-primary-runtime/dependencies/python/bin/python3'}
MANIFEST='FINAL_NAMESPACE_MANIFEST.json'
def namespace():
    result={'.':dict(type='directory',mode=oct(stat.S_IMODE(R.stat().st_mode)))}
    for q in sorted(R.rglob('*')):
        require(not q.is_symlink(),f'symlink prohibited {q}')
        n=str(q.relative_to(R));m=oct(stat.S_IMODE(q.stat().st_mode))
        if q.is_dir():result[n]=dict(type='directory',mode=m)
        else:
            require(q.is_file(),f'nonregular {q}')
            result[n]=dict(type='file',**pin(q))
    return result
def frozen_namespace(current):
    frozen=load(R/MANIFEST)
    require(frozen['scope']=='Every file and directory; only own manifest bytes excluded','manifest scope')
    expected=frozen['entries'];actual=dict(current)
    require(MANIFEST in actual and actual[MANIFEST]['mode']=='0o644','own manifest regular mode')
    actual[MANIFEST]=dict(type='file',mode=actual[MANIFEST]['mode'],own_bytes_excluded=True)
    require(actual==expected,'complete final namespace inventory/bytes/modes')
    return frozen
def replay(full):
    env=dict(os.environ,PYTHONDONTWRITEBYTECODE='1',PYTHONHASHSEED='0');env.pop('PYTHONOPTIMIZE',None)
    cmds={'version':['--version'],'default':['-B',str(P/'verify_supplement.py')]}
    if full:
        cmds.update({'full':['-B',str(P/'verify_supplement.py'),'--full'],'priority':['-B',str(P/'priority/verify_public.py')],'honda':['-B',str(P/'controls/check_realization.py')],'semilinear':['-B',str(P/'controls/verify_semilinear.py')],'intrinsic':['-B',str(P/'controls/verify_intrinsic.py')],'integral_flag':['-B',str(P/'controls/check_integral_flag.py')]})
    streams={};events=[]
    def execute(runtime,args,cwd):
        command=[RUNTIMES[runtime],*args];start=datetime.datetime.now(datetime.timezone.utc).isoformat()
        cp=subprocess.run(command,cwd=cwd,env=env,capture_output=True)
        end=datetime.datetime.now(datetime.timezone.utc).isoformat()
        events.append(dict(runtime=runtime,command=command,cwd=str(cwd),started_utc=start,ended_utc=end,exit_code=cp.returncode,stdout_bytes=len(cp.stdout),stdout_sha256=hashlib.sha256(cp.stdout).hexdigest(),stderr_bytes=len(cp.stderr),stderr_sha256=hashlib.sha256(cp.stderr).hexdigest()))
        return cp
    for runtime in RUNTIMES:
        for label,args in cmds.items():
            cp=execute(runtime,args,P)
            require(cp.returncode==0 and cp.stderr==b'',f'fresh positive {runtime}-{label}')
            require(cp.stdout==(R/'receipts'/(runtime+'-'+label+'.stdout')).read_bytes(),f'fresh complete stream {runtime}-{label}')
            streams[(runtime,label)]=cp.stdout
        if full:
            cp=execute(runtime,['-B',str(R/'independent_controls.py')],R)
            require(cp.returncode==0 and cp.stderr==b'' and cp.stdout==(R/'receipts'/('independent-'+runtime+'.stdout')).read_bytes(),'fresh independent complete stream')
            streams[(runtime,'independent')]=cp.stdout
            for row in load(R/'mutation_summary.json')['mutations']:
                if not row['receipt'].startswith(runtime+'-negative-'):continue
                d=load(R/'receipts'/(row['receipt']+'.json'));label=row['receipt'].split('-negative-')[1]
                script=R/'mutants'/label/pathlib.Path(d['command'][-1]).name
                cp=execute(runtime,['-B',str(script)],script.parent)
                require(cp.returncode==d['exit_code']!=0 and cp.stdout==b'','fresh direct mathematical negative')
                error={'old_generic_formula':b'AssertionError','inverse_integral_F_twist':b'integral flag unstable','unsaturated_integral_first_generator':b'integral basis inverse failed','bad_Honda_input':b'AssertionError'}[label]
                require(error in cp.stderr and b'Traceback' in cp.stderr and b'manifest' not in cp.stderr.lower(),'fresh mathematical rejection reason')
    for label in cmds:
        if label!='version':require(streams[('py314',label)]==streams[('py312',label)],'fresh complete cross-runtime equality')
    if full:require(streams[('py314','independent')]==streams[('py312','independent')],'fresh independent cross-runtime equality')
    return events
def main():
    require(__debug__,'optimization disables mathematical assertions')
    require(set(sys.argv[1:])<={'--full','--preflight'},'usage: verify_review.py [--full] [--preflight]')
    start=datetime.datetime.now(datetime.timezone.utc).isoformat();before=namespace()
    preflight='--preflight' in sys.argv;full='--full' in sys.argv
    if not preflight:frozen_namespace(before)
    relations=check();events=replay(full)
    after=namespace();require(before==after,'review replay changed namespace bytes/inventory/modes')
    if not preflight:frozen_namespace(after)
    verdict=load(R/'VERDICT.json') if (R/'VERDICT.json').is_file() else None
    if not preflight:require(verdict is not None,'missing scientific verdict')
    if verdict and verdict['scientific_verdict']=='CLEAN_NO_MANDATORY_CHANGES':require(verdict['mandatory_findings']==[],'clean verdict contradicts mandatory findings')
    result=dict(integrity='UNFINALIZED_PREFLIGHT_PASS' if preflight else 'PASS',mode='full' if full else 'public',scientific_verdict=verdict['scientific_verdict'] if verdict else 'NOT_YET_FROZEN',mandatory_findings=verdict['mandatory_findings'] if verdict else None,scientific_clearance=bool(verdict and verdict['scientific_verdict']=='CLEAN_NO_MANDATORY_CHANGES' and not verdict['mandatory_findings']),integrity_does_not_override_scientific_verdict=True,namespace_unchanged=True,external_source_paths_read=False,relations=relations,actual_fresh_replays=events,started_utc=start,ended_utc=datetime.datetime.now(datetime.timezone.utc).isoformat())
    print(json.dumps(result,indent=2,sort_keys=True))
if __name__=='__main__':
    try:main()
    except Exception as e:
        print(json.dumps(dict(integrity='FAIL',reason=str(e),scientific_clearance=False)),file=sys.stderr)
        raise SystemExit(1)
