#!/usr/bin/env python3
"""Initial V4 format controls using exact originals; no paper/current fixture.

The subject executes through its real CLI entry point. A Python profile hook
observes completed package authentication; an audit hook counts subprocesses.
No archival replay is authorized by this control program.
"""
from pathlib import Path, PurePosixPath
import argparse
import datetime
import hashlib
import json
import re
import stat
import subprocess
import sys

HERE = Path(__file__).resolve().parent.parent
AUDIT = HERE.parent
PRIVATE = HERE / 'private_v4'
TOOL_PIN = '8832a44a53f0df4867cb8196d725209dd7ac5944c82b4f296b7514155fe72e6c'
MANIFEST_PIN = '6b1d1281848190f616f6759f40454183c937b65e65219b893202254be6c3617d'
HEAD = '4b1ef9bbeb723a4171949a6c3934db98962ac615'
PROBE = r'''from pathlib import Path
import json,runpy,sys
tool=Path(sys.argv[1]); args=json.loads(sys.argv[2]); log=Path(sys.argv[3])
events={'package_authentication_completed':0,'subprocess_popen_events':0}
def audit(name,values):
    if name=='subprocess.Popen': events['subprocess_popen_events']+=1
def profile(frame,event,arg):
    if event=='return' and frame.f_code.co_filename==str(tool) and frame.f_code.co_name=='package_inputs' and isinstance(arg,dict) and 'package_index.json' in arg:
        events['package_authentication_completed']+=1
sys.addaudithook(audit)
sys.setprofile(profile)
sys.argv=[str(tool),*args]
try:
    runpy.run_path(str(tool),run_name='__main__')
finally:
    sys.setprofile(None)
    log.write_text(json.dumps(events,sort_keys=True))
'''


def check(ok, reason):
    if not ok:
        raise RuntimeError(reason)


def sha(raw):
    return hashlib.sha256(raw).hexdigest()


def encoded(value):
    return (json.dumps(value,indent=2,sort_keys=True)+'\n').encode()


def safe_name(name):
    check(type(name) is str and re.fullmatch(r'[A-Za-z0-9_./-]+',name), 'unsafe fixture path')
    check(not PurePosixPath(name).is_absolute() and all(p not in ('','.','..') for p in name.split('/')), 'unsafe fixture components')


def stage(run):
    manifest_raw=(AUDIT/'SOURCE_MANIFEST.json').read_bytes()
    check(sha(manifest_raw)==MANIFEST_PIN, 'external source manifest pin')
    manifest=json.loads(manifest_raw)
    check(manifest['head']==HEAD and manifest['pr']==885 and manifest['problem_id']=='9700042' and manifest['original_effort']=='5/5', 'assigned source identity')
    rows=manifest['files']
    check(len(rows)==30 and sum(r['bytes'] for r in rows)==214980, 'all30 source size/count')
    tool=(AUDIT/'publication_tools_03/portable.py').read_bytes()
    check(len(tool)==41629 and sha(tool)==TOOL_PIN, 'written V4 tool pin')
    payloads={'portable.py':tool,'root_evidence/SOURCE_MANIFEST.json':manifest_raw}
    receipts=[]
    for row in rows:
        name=row['path'];safe_name(name)
        source=AUDIT/'source'/name
        check(stat.S_ISREG(source.lstat().st_mode), 'original is nonregular')
        raw=source.read_bytes()
        blob=hashlib.sha1(b'blob '+str(len(raw)).encode()+b'\0'+raw).hexdigest()
        check(len(raw)==row['bytes'] and sha(raw)==row['sha256'] and blob==row['git_blob'], 'original immutable byte/Git-blob pin')
        payloads['source/'+name]=raw
        receipts.append({'path':name,'bytes':len(raw),'sha256':sha(raw),'git_blob':blob})
    fixture=run/'fixture';fixture.mkdir()
    pins=[]
    for name,raw in sorted(payloads.items()):
        safe_name(name)
        path=fixture/name;path.parent.mkdir(parents=True,exist_ok=True)
        with path.open('xb') as output: output.write(raw)
        pins.append({'path':name,'bytes':len(raw),'sha256':sha(raw)})
    index=encoded({'schema':'oriented-flow-9700042-verification-v1','problem_id':'9700042','files':pins})
    (fixture/'package_index.json').write_bytes(index)
    return fixture,sha(index),payloads,index,receipts


def main():
    parser=argparse.ArgumentParser(allow_abbrev=False)
    parser.add_argument('--run',default='run_01')
    args=parser.parse_args()
    check(re.fullmatch(r'run_[A-Za-z0-9_-]+',args.run), 'safe fresh run name')
    run=PRIVATE/args.run
    run.mkdir()  # Never overwrite an earlier run.
    fixture,pin,payloads,index,originals=stage(run)
    tool=fixture/'portable.py'
    output_alias=run/'output_alias';output_alias.symlink_to(fixture,target_is_directory=True)
    ancestor_alias=run/'ancestor_alias';ancestor_alias.symlink_to(run,target_is_directory=True)
    case_alias=run/'FIXTURE'
    data_alias=Path('/System/Volumes/Data')/str(fixture).lstrip('/')
    check(fixture.samefile(case_alias) and fixture.samefile(data_alias), 'actual case/APFS alias availability')
    cases=[]

    def execute(label,argv,flags,positive=False):
        log=run/(label+'.events.json')
        proc=subprocess.run([sys.executable,*flags,'-c',PROBE,str(tool),json.dumps(argv),str(log)],cwd=run,capture_output=True,timeout=60)
        (run/(label+'.stdout')).write_bytes(proc.stdout)
        (run/(label+'.stderr')).write_bytes(proc.stderr)
        events=json.loads(log.read_bytes())
        result=json.loads(proc.stdout)
        check(events=={'package_authentication_completed':1,'subprocess_popen_events':0}, label+' must authenticate once before rejection with zero subprocesses')
        check(not proc.stderr, label+' unexpected stderr')
        if positive:
            check(proc.returncode==0 and result['status']=='PASS' and result['replay']=='NOT_RUN', label+' authentication-only pass')
        else:
            check(proc.returncode!=0 and result['status']=='REJECTED' and result['reason'].startswith('output must be outside input tree'), label+' containment rejection')
        cases.append({'case':label,'interpreter_flags':flags,'returncode':proc.returncode,
                      'stdout_bytes':len(proc.stdout),'stdout_sha256':sha(proc.stdout),
                      'stderr_bytes':len(proc.stderr),'stderr_sha256':sha(proc.stderr),
                      **events,'result':result,'archival_execution':False})

    for optimized in (False,True):
        mode='optimized' if optimized else 'normal'
        flags=['-I','-S','-B']+(['-O'] if optimized else [])
        execute('authentication_only_'+mode,['verify',pin,'--root',str(fixture),'--verify-only'],flags,True)
        specifications=[
            ('direct',fixture,fixture),
            ('dotdot_root',fixture/'source'/'..',fixture),
            ('case_output',fixture,case_alias),
            ('case_root',case_alias,fixture),
            ('APFS_output',fixture,data_alias),
            ('APFS_root',data_alias,fixture),
            ('symlink_output_ancestor',fixture,output_alias),
            ('symlink_root_ancestor',ancestor_alias/'fixture',fixture),
            ('nested_input_directory',fixture,fixture/'source/audit_a'),
        ]
        for label,root,parent in specifications:
            output=parent/'oriented-flow-verification.zip'
            execute('containment_'+label+'_'+mode,['build',pin,str(output),'--root',str(root)],flags)
            check(not output.exists(), 'containment control created an archive')
    # Actual copied fixture and authoritative originals are rechecked; source
    # Git-blob identity is checked against the frozen manifest, with no Git call.
    for name,raw in payloads.items():
        check((fixture/name).read_bytes()==raw, 'fixture changed')
    check((fixture/'package_index.json').read_bytes()==index, 'fixture index changed')
    for row in originals:
        raw=(AUDIT/'source'/row['path']).read_bytes()
        check(len(raw)==row['bytes'] and sha(raw)==row['sha256'], 'authoritative original changed')
    receipt={'timestamp_utc':datetime.datetime.now(datetime.timezone.utc).isoformat(),
             'completion_estimate_percent':70,'tool_bytes':41629,'tool_sha256':TOOL_PIN,
             'source_manifest_sha256':MANIFEST_PIN,'assigned_head':HEAD,'fresh_Git_tree_comparison':'NOT_RUN: Git forbidden',
             'fixture_index_sha256':pin,'fixture_file_count':33,'original_files':originals,
             'cases':cases,'fixture_and_originals_unchanged_after':True,
             'scope':'Actual minimal portable fixture CLI authentication and containment controls; no paper/current fixture, archival replay or outside default build.',
             'wider_Data_root_case':'Helper-only evidence from earlier in-memory V3/V4 review; not a valid closed-tree package and not attempted as a CLI fixture.',
             'actual_current_validation':'PENDING external candidate and manifest pin',
             'final_whole_package_clear':False}
    destination=HERE/('V4_CLI_RECEIPTS_'+args.run+'.json')
    check(not destination.exists(), 'fresh safe receipt required')
    destination.write_bytes(encoded(receipt))
    print(json.dumps({'status':'PASS','cases':len(cases),'fixture_index_sha256':pin,'safe_receipt':destination.name,'subprocess_popen_events':0,'archival_execution':False},sort_keys=True))


if __name__=='__main__': main()
