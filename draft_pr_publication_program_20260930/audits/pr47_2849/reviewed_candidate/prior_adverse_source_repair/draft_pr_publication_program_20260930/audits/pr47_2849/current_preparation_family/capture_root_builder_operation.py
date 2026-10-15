#!/usr/bin/env python3
"""TEXT ONLY: ROOT's future capture, never run/import/compile during source preparation."""
import argparse, datetime as dt, hashlib, json, os, re, stat, subprocess, sys, traceback
from pathlib import Path
def need(v,m):
    if not v: raise ValueError(m)
def sha(b): return hashlib.sha256(b).hexdigest()
def stamp(): return dt.datetime.now(dt.timezone.utc).isoformat()
def raw(p):
    need(not p.is_symlink() and all(not q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode),'Regular nonsymlink source'); return p.read_bytes()
def write(p,o):
    with p.open('xb') as h: h.write((json.dumps(o,indent=2,allow_nan=False)+'\n').encode()); h.flush(); os.fsync(h.fileno())
def main():
    parser=argparse.ArgumentParser(description=__doc__); parser.add_argument('--execute',action='store_true'); parser.add_argument('--expected-builder-sha256',required=True)
    names=['root-scope-certificate','root-read-ledger','root-science-card','root-current-input-manifest','root-evidence-bindings']
    for n in names: parser.add_argument('--'+n+'-sha256',required=True)
    args=parser.parse_args(); need(args.execute and all(type(v) is str and re.fullmatch('[0-9a-f]{64}',v) for k,v in vars(args).items() if k.endswith('sha256')),'Explicit ROOT execute and reviewed exact pins'); need(not sys.flags.optimize and os.environ.get('PYTHONOPTIMIZE','') in ('','0'),'No optimized guards')
    script=Path(__file__).absolute(); F=script.parent; A=F.parent; R=A.parents[2]; need(F.name=='current_preparation_family' and A.name=='pr47_2849' and R==Path('/Users/alec/Documents/Math'),'Exact ROOT PR47 anchor')
    builder=F/'prepare_current_packet.py'; source=raw(builder); operator=raw(script); need(sha(source)==args.expected_builder_sha256,'Reviewed builder bytes changed'); need(not (A/'reviewed_candidate').exists() and not (A/'reviewed_candidate').is_symlink(),'Candidate absent before launch')
    (A/'tmp').mkdir(exist_ok=True); need(not (A/'tmp').is_symlink(),'Regular audit tmp'); capture=A/'tmp'/('root_pr47_current_outer_'+dt.datetime.now(dt.timezone.utc).strftime('%Y%m%dT%H%M%S.%fZ')); capture.mkdir(exist_ok=False)
    (capture/'PRELAUNCH_BUILDER_SOURCE.py').write_bytes(source); (capture/'PRELAUNCH_OPERATOR.py').write_bytes(operator)
    argv=['/usr/bin/python3','-B',str(builder),'--execute']
    for n in names: argv.extend(['--'+n+'-sha256',getattr(args,n.replace('-','_')+'_sha256')])
    pre={'schema':'PR47_ROOT_BUILDER_PRELAUNCH_v1','operator_pid':os.getpid(),'started_utc':stamp(),'argv':argv,'cwd':str(R),'builder_sha256':sha(source),'operator_sha256':sha(operator),'administrative_only':True,'scientific_helpers_run':False}; write(capture/'OPERATION_PRELAUNCH.json',pre)
    rec=dict(pre,schema='PR47_ROOT_ACTUAL_BUILDER_OPERATION_v1',actual_execution=False,completed=False,pid=None,exit_code=None,stdin_supplied=False)
    try:
        with (capture/'stdout.bin').open('xb') as out,(capture/'stderr.bin').open('xb') as err:
            child=subprocess.Popen(argv,cwd=R,stdin=subprocess.DEVNULL,stdout=out,stderr=err,env=dict(os.environ,PR47_ROOT_OUTER_CAPTURE=capture.relative_to(A).as_posix(),GIT_OPTIONAL_LOCKS='0')); rec.update(actual_execution=True,pid=child.pid)
            try: rec['exit_code']=child.wait(timeout=600); rec['completed']=True
            except BaseException: child.kill(); rec['exit_code']=child.wait(); raise
    except BaseException: rec['operator_failure']=traceback.format_exc()
    finally:
        rec['finished_utc']=stamp()
        for channel in ['stdout','stderr']:
            p=capture/(channel+'.bin')
            if p.exists(): b=raw(p); rec[channel]={'path':p.name,'bytes':len(b),'sha256':sha(b)}
        for k,p,b in [('builder_unchanged_after_child',builder,source),('operator_unchanged_after_child',script,operator)]:
            try: rec[k]=raw(p)==b
            except BaseException: rec[k]=False; rec[k+'_failure']=traceback.format_exc()
        rec.update(new_whole_current_gate='PENDING',current_whole_verdict=None,ROOT_full_final_outer_capture_and_original_inner_full_records_streams_read_AFTER_child_exit_required=True,inner_GIT_COMMANDS_written_incrementally_by_live_builder=True,outer_operator_does_not_write_inner_GIT_COMMANDS=True)
        ok=rec['actual_execution'] is True and rec['completed'] is True and type(rec['exit_code']) is int and rec['exit_code']==0 and rec['builder_unchanged_after_child'] is True and rec['operator_unchanged_after_child'] is True and 'operator_failure' not in rec
        rec['status']='ACTUAL_ADMINISTRATIVE_CAPTURE_COMPLETE_WHOLE_REVIEW_PENDING' if ok else 'FAILED_ACTUAL_OPERATION_PRESERVED'
        # CAPTURE exists only after actual child exit (or no-launch failure).
        write(capture/'CAPTURE.json',rec)
    print(json.dumps({'status':rec['status'],'audit_relative_capture':capture.relative_to(A).as_posix(),'pid':rec['pid'],'exit_code':rec['exit_code'],'capture_sha256':sha(raw(capture/'CAPTURE.json')),'new_whole_current_gate':'PENDING'},indent=2)); return 0 if ok else 1
if __name__=='__main__': sys.exit(main())
