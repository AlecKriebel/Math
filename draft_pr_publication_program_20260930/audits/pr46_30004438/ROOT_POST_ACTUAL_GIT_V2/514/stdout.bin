#!/usr/bin/env python3
"""ROOT's read-only postclosing-child verifier; capture it separately outside this family."""
from pathlib import Path, PurePosixPath
import argparse, datetime as dt, hashlib, json, os, re, stat
F=Path(__file__).absolute().parent
def req(v,n):
    if not v: raise ValueError(n)
def sha(b): return hashlib.sha256(b).hexdigest()
def read(p):
    req(not p.is_symlink() and not any(q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode),'Regular nonsymlink member required'); return p.read_bytes()
def clock(s):
    q=dt.datetime.fromisoformat(s); req(q.tzinfo is not None and q.utcoffset()==dt.timedelta(0),'AwareUTC required'); return q
def main():
    p=argparse.ArgumentParser(description=__doc__); p.add_argument('--expected-manifest-sha256',required=True); a=p.parse_args()
    req(re.fullmatch('[a-f0-9]{64}',a.expected_manifest_sha256) is not None,'Actual externally supplied closure pin required')
    req(F.name=='current_source_adversary_family_v2' and F.parent.name=='pr46_30004438','Exact family required')
    raw=read(F/'MANIFEST.json'); req(sha(raw)==a.expected_manifest_sha256,'Closure SHA changed'); m=json.loads(raw)
    req(m['schema']=='PR46_INDEPENDENT_V2_SOURCE_ADVERSARY_SELF_ONLY_CLOSURE_v1' and m['self_excluded']==['MANIFEST.json'],'Self-only closure required')
    req(type(m['files_count']) is int and m['files_count']==len(m['files']),'Complete typed member count')
    names=set(); actual=set(); dirs=set()
    for row in m['files']:
        req(type(row) is dict and set(row)=={'path','bytes','sha256'},'Exact row required'); n=row['path']; q=PurePosixPath(n)
        req(type(n) is str and n and not q.is_absolute() and str(q)==n and not set(q.parts).intersection({'.','..','.git','__pycache__'}) and '\\' not in n and '\0' not in n,'Canonical row required')
        req(n not in names and type(row['bytes']) is int and row['bytes']>=0 and re.fullmatch('[a-f0-9]{64}',row['sha256']) is not None,'Typed unique row')
        names.add(n); body=read(F/n); req(len(body)==row['bytes'] and sha(body)==row['sha256'] and stat.S_IMODE((F/n).stat().st_mode)==0o444,'Full bytes/SHA/full0444 required')
    for member in F.rglob('*'):
        req(not member.is_symlink(),'Symlink rejected'); n=member.relative_to(F).as_posix()
        if stat.S_ISREG(member.stat().st_mode): actual.add(n)
        else: req(stat.S_ISDIR(member.stat().st_mode),'Special member rejected'); dirs.add(n)
    req(actual==names|{'MANIFEST.json'} and stat.S_IMODE((F/'MANIFEST.json').stat().st_mode)==0o444,'Exact topology/full0444 self manifest')
    req(dirs=={str(p) for n in names|{'MANIFEST.json'} for p in PurePosixPath(n).parents if str(p)!='.'}==set(m['directories']),'No extra/empty directory')
    req(set(m['directory_modes'])==dirs and all(stat.S_IMODE((F/n).stat().st_mode)==v for n,v in m['directory_modes'].items()),'Exact directory modes')
    req(clock(m['closed_utc'])<=dt.datetime.now(dt.timezone.utc),'No future closure')
    req(type(m['closing_child_pid']) is int and m['closing_child_pid']>0 and m['private_final_suite_assertions']==29095,'Honest closing PID/count')
    req(m['production_import_compile_execute'] is False and m['future_acceptance_approved'] is False and m['ROOT_runtime_or_future_merge_certified'] is False,'Source-only scope')
    for capdir in sorted(F.glob('actual_private_capture_*')):
        cap=json.loads(read(capdir/'CAPTURE.json')); pre=json.loads(read(capdir/'PRELAUNCH.json'))
        req(cap['actual_execution'] is True and cap['completed'] is True and type(cap['pid']) is int and cap['pid']>0 and type(cap['exit_code']) is int,'Actual private capture types')
        req(cap['source_unchanged'] is True and cap['operator_unchanged'] is True and cap['native13_unchanged'] is True and cap['native13_before']==cap['native13_after'],'Source/operator/native beforeafter anchors')
        req(sha(read(capdir/'PRELAUNCH_SOURCE.py'))==cap['source_sha256'] and sha(read(capdir/'PRELAUNCH_OPERATOR.py'))==cap['operator_sha256'],'Complete prelaunch sources')
        req(pre['actual_execution'] is False and pre['pid'] is None and pre['completed'] is False and pre['exit_code'] is None,'Honest prelaunch state')
        req(clock(cap['started_utc'])<=clock(cap['finished_utc'])<=clock(m['closed_utc']),'Capture before closure')
        for k in ['stdout','stderr']:
            rr=cap[k]; b=read(capdir/rr['path']); req(len(b)==rr['bytes'] and sha(b)==rr['sha256'],'Full retained streams')
    b=json.loads(read(F/'PRIVATE_CONTROL_RESULTS.json')); e=json.loads(read(F/'EXTENDED_CONTROL_RESULTS.json'))
    req(b['assertions_passed']==13179 and e['assertions_passed']==15916 and len(b['assertion_labels'])==13179 and len(e['assertion_labels'])==15916,'Exact final private assertion accounting')
    req(b['fixed_full_body_reads_unique']==len(b['complete_fixed_member_reads'])==627,'Complete fixed-read receipt')
    print(json.dumps({'status':'PASS_ROOT_POSTCLOSE_READ_ONLY_FAMILY_MEMBERSHIP_VERIFICATION','manifest_sha256':sha(raw),'files_count':m['files_count'],'closing_child_pid':m['closing_child_pid'],'verification_child_pid':os.getpid(),'verification_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'private_final_suite_assertions':29095,'complete_report_personally_read_by_ROOT':None,'ROOT_runtime_or_future_merge_certified':False,'future_acceptance_approved':False,'production_executed':False},sort_keys=True))
if __name__=='__main__': main()
