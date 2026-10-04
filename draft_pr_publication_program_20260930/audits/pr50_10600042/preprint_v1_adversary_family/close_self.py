#!/usr/bin/env python3
"""SOURCE for ROOT: closes only this review family after genuine readback.
No author-package chmod/write, native/Git action, approval or publication.
"""
from pathlib import Path
from datetime import datetime, timezone
import argparse, hashlib, json, os, stat

HERE=Path(__file__).resolve().parent
def pairs(items):
    out={}
    for k,v in items:
        if k in out: raise ValueError('duplicate JSON key '+k)
        out[k]=v
    return out
def obj(path): return json.loads(Path(path).read_bytes(),object_pairs_hook=pairs)
def ref(path,rel=False):
    path=Path(path); info=path.lstat()
    if not stat.S_ISREG(info.st_mode): raise ValueError('not regular '+str(path))
    body=path.read_bytes()
    return {'path':str(path.relative_to(HERE)) if rel else str(path),
            'mode':format(stat.S_IMODE(info.st_mode),'04o'), 'bytes':len(body),
            'sha256':hashlib.sha256(body).hexdigest()}
def require(ok,why):
    if not ok: raise ValueError(why)
def main():
    ap=argparse.ArgumentParser(); ap.add_argument('--expected-report-sha256',required=True)
    args=ap.parse_args(); mf=HERE/'SELF_MANIFEST.json'
    require(not mf.exists(),'already closed')
    require(ref(HERE/'REPORT.md')['sha256']==args.expected_report_sha256,'report pin')
    verdict=obj(HERE/'VERDICT.json')
    require(verdict['mandatory_issues']==[] and verdict['unresolved_proof_gaps_within_stated_scope']==[],'unclean review')
    inputs=obj(HERE/'REVIEWED_PACKAGE_BINDINGS.json')
    require(type(inputs['files_count']) is int and inputs['files_count']==19 and len(inputs['files'])==19,'input count')
    for row in inputs['files']: require(ref(row['path'])==row,'input changed '+row['path'])
    for name,pid in [('independent_invariant_run',13305),('author_checker_reproduction',13423)]:
        folder=HERE/name; cap=obj(folder/'CAPTURE.json'); pre=obj(folder/'PRELAUNCH.json')
        require(cap['actual_execution'] is True and cap['completed'] is True and type(cap['exit_code']) is int and cap['exit_code']==0,'capture failed')
        require(type(cap['child_pid']) is int and cap['child_pid']==pid and cap['operator_pid']==pre['operator_pid'],'actual PID')
        require(cap['argv']==pre['argv'] and cap['cwd']==pre['cwd'],'command/cwd')
        require(cap['source_unchanged'] is True and cap['operator_unchanged'] is True,'source changed')
        start=datetime.fromisoformat(cap['started_utc']); stop=datetime.fromisoformat(cap['finished_utc'])
        require(start.tzinfo is not None and stop.tzinfo is not None and start<=stop,'aware capture chronology')
        for member in ('stdout','stderr'): require(ref(folder/(member+'.bin'))==cap[member],'whole stream')
        require((folder/'prelaunch_source.py').read_bytes()==Path(pre['source']['path']).read_bytes(),'prelaunch source')
        require((folder/'prelaunch_operator.py').read_bytes()==Path(pre['operator']['path']).read_bytes(),'prelaunch operator')
    before=sorted(HERE.rglob('*'))
    require(all(not p.is_symlink() for p in before),'symlink scope')
    files=[p for p in before if p.is_file()]
    dirs=[HERE]+[p for p in before if p.is_dir()]
    require(all(p.is_file() or p.is_dir() for p in before),'special-file scope')
    # chmod is restricted to this family, after all external and actual capture checks.
    for p in files: os.chmod(p,0o444)
    rows=[ref(p,True) for p in files]
    result={'schema':'pr50-preprint-v1-adversary-self-only-closure/v1',
        'closed_utc':datetime.now(timezone.utc).isoformat(), 'self_excluded':'SELF_MANIFEST.json',
        'files_count':len(rows),'files':rows,
        'directories':[{'path':str(p.relative_to(HERE)),'mode':'0555'} for p in sorted(dirs)],
        'author_inputs_checked_at_close':19,'root_approval_claimed':False,'publication_claimed':False}
    with mf.open('x') as out: out.write(json.dumps(result,indent=2)+'\n')
    os.chmod(mf,0o444)
    for p in sorted(dirs,key=lambda p:len(p.parts),reverse=True): os.chmod(p,0o555)
    print(json.dumps({'status':'CLOSED_SELF_ONLY','manifest_sha256':ref(mf)['sha256'],'files_count':len(rows)},indent=2))
if __name__=='__main__': main()
