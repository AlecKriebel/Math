#!/usr/bin/env python3
"""ROOT closes its completed actual reproduction; --verify is postexit readonly."""
import argparse,datetime as dt,hashlib,json,os,stat
from pathlib import Path,PurePosixPath
A=Path(__file__).absolute().parent;R=A.parents[2];D=A/'root_original_actual_reproduction'
MF='MANIFEST.json'
assert __debug__ and not os.environ.get('PYTHONOPTIMIZE')
def sha(b):return hashlib.sha256(b).hexdigest()
def read(p):
    assert not p.is_symlink() and not any(q.is_symlink() for q in p.parents) and stat.S_ISREG(p.stat().st_mode)
    return p.read_bytes()
def obj(p):return json.loads(read(p))
def row(p):
    b=read(p);return dict(path=p.relative_to(R).as_posix(),bytes=len(b),sha256=sha(b),full_mode=stat.S_IMODE(p.stat().st_mode))
def write(p,o):
    with p.open('xb') as f:f.write((json.dumps(o,indent=2,allow_nan=False)+'\n').encode());f.flush();os.fsync(f.fileno())
def inventory():
    files={};dirs=set()
    for p in D.rglob('*'):
        assert not p.is_symlink();n=p.relative_to(D).as_posix()
        if p.is_file():files[n]=read(p)
        else:assert stat.S_ISDIR(p.stat().st_mode);dirs.add(n)
    assert dirs=={q.as_posix() for n in files for q in PurePosixPath(n).parents if q.as_posix()!='.'}
    return files,dirs
def capture(p,pid,code):
    c=obj(p/'CAPTURE.json');assert c['actual_execution'] is True and c['completed'] is True and type(c['pid']) is int and c['pid']==pid and type(c['exit_code']) is int and c['exit_code']==code and c['operator_unchanged'] is True
    assert sha(read(p/'prelaunch_operator.py'))==c['operator_sha256']
    for ch in ['stdout','stderr']:
        b=read(p/c[ch]['path']);assert len(b)==c[ch]['bytes'] and sha(b)==c[ch]['sha256']
    start=dt.datetime.fromisoformat(c['started_utc']);end=dt.datetime.fromisoformat(c['finished_utc'])
    assert start.utcoffset()==end.utcoffset()==dt.timedelta(0) and start<end<dt.datetime.now(dt.timezone.utc)
    if code==0:assert not read(p/'stderr.bin')
    return {'entire_actual_capture':c,'members':[row(q) for q in sorted(p.iterdir())]}
parser=argparse.ArgumentParser();parser.add_argument('--verify',action='store_true');parser.add_argument('--expected-manifest-sha256');args=parser.parse_args()
if args.verify:
    assert sha(read(D/MF))==args.expected_manifest_sha256
    m=obj(D/MF);fs,ds=inventory()
    assert m['schema']=='pr49-root-original-complete-reproduction-self-only-closure/v1' and m['self_excluded']==[MF]
    assert set(fs)=={r['path'] for r in m['files']}|{MF} and ds==set(m['directories'])
    for r in m['files']:assert len(fs[r['path']])==r['bytes'] and sha(fs[r['path']])==r['sha256'] and stat.S_IMODE((D/r['path']).stat().st_mode)==r['full_mode']==0o444
    assert stat.S_IMODE((D/MF).stat().st_mode)==0o444 and len(m['files'])==m['files_count']
    for r in obj(D/'ROOT_CURRENT_REPRODUCTION_SUMMARY.json')['external_completed_first_party_bindings']:
        p=R/r['path'];b=read(p);assert len(b)==r['bytes'] and sha(b)==r['sha256'] and stat.S_IMODE(p.stat().st_mode)==r['full_mode']
    print(json.dumps({'status':'PASS_ROOT_POSTEXIT_COMPLETE_REPRODUCTION_READBACK','manifest_sha256':args.expected_manifest_sha256,'files_count':len(m['files']),'relative_directories':len(ds),'actual_pid':os.getpid(),'future_acceptance_approved':False}));raise SystemExit
assert not (D/MF).exists() and not (D/'ROOT_CURRENT_REPRODUCTION_SUMMARY.json').exists()
r=obj(D/'ROOT_REPRODUCTION_RESULT.json');assert r['status']=='PASS_ROOT_EXACT_ORIGINAL_AND_LITERAL_UNCHANGED_REPRODUCTION' and r['actual_operator_pid']==60012
assert len(r['complete_actual_Git_captures'])==33 and len(r['complete_actual_helper_captures'])==3 and r['identical_submitted_counted_independent'] is False
for c in r['complete_actual_Git_captures']+r['complete_actual_helper_captures']:
    assert c['actual_execution'] is True and c['completed'] is True and type(c['exit_code']) is int and c['exit_code']==0 and c['operator_pid']==60012 and c['operator_unchanged'] is True
    if c['schema']=='pr49-root-actual-readonly-git/v1':assert c['source'] is None and c['source_unchanged'] is None
    else:assert c['schema']=='pr49-root-actual-unchanged-helper/v1' and type(c['source']) is dict and c['source_unchanged'] is True
    for ch in ['stdout','stderr']:
        p=R/c[ch]['path'];b=read(p);assert len(b)==c[ch]['bytes'] and sha(b)==c[ch]['sha256']
raw=obj(A/'ROOT_COMPLETE_RAW_SQL_AUDIT.json');assert raw['status']=='PASS_FULL_RAW_PRIOR_SQL_AND_ORIGINAL_PLAIN_SOURCE' and raw['actual_pid']==62744 and raw['all_SQL_rows']==len(raw['complete_row_bindings'])==15458 and raw['full_raw_and_prior_bytes']==149266659
assert raw['selected_prior_key_present'] is False and raw['SQLite_literal_fallback']=='{}' and raw['literal_original_prior_file_value'] is None and raw['literal_original_prior_differs_from_upstream_absent_fallback'] is True
outer=[]
for name,pid,code in [('root_pr49_original_ROOT_reproduction_actual_capture',60012,0),('root_pr49_full_raw_SQL_actual_capture',60964,1),('root_pr49_full_raw_SQL_v2_actual_capture',61299,1),('root_pr49_full_raw_SQL_v3_actual_capture',62744,0)]:outer.append(capture(A.parent/'pr45_9900007'/name,pid,code))
bindings=[row(A/n) for n in ['ROOT_MATHEMATICAL_REVIEW.md','ROOT_COMPLETE_RAW_SQL_AUDIT.json','ROOT_REPRODUCTION_PRELAUNCH_SOURCE.py','reproduce_original_ROOT.py','ROOT_RAW_AUDIT_PRELAUNCH_SOURCE.py','audit_raw_provenance_ROOT.py','ROOT_RAW_AUDIT_V2_PRELAUNCH_SOURCE.py','audit_raw_provenance_ROOT_v2.py','ROOT_RAW_AUDIT_V3_PRELAUNCH_SOURCE.py','audit_raw_provenance_ROOT_v3.py']]
for o in outer:bindings+=o['members']
summary={'schema':'pr49-root-current-complete-reproduction-summary/v1','status':'PASS_ROOT_COMPLETED_FIRST_PARTY_REPRODUCTION','created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_closing_pid':os.getpid(),'entire_reproduction_result':r,'raw_result_pending_field_in_original_receipt_is_dated_history':True,'actual_completed_raw_PID':62744,'complete_raw_audit':row(A/'ROOT_COMPLETE_RAW_SQL_AUDIT.json'),'ROOT_mathematical_notes':row(A/'ROOT_MATHEMATICAL_REVIEW.md'),'external_completed_first_party_bindings':bindings,'entire_completed_outer_captures':outer,'retained_ROOT_raw_failures':[60964,61299],'original_substantive_attempts':0,'turn_limit':5,'new_substantive_attempts':0,'audit_turns':0,'known_credited_full_target_only':True,'project_solved':False,'novelty_claimed':False,'future_acceptance_approved':False,'new_current_package_and_whole_review':'PENDING','foreign_native_raw_SQL_PDF_OCR_pixel_bodies_copied':False,'closing_child_outer_completion':'PENDING_CHILD_EXIT_REQUIRES_SEPARATE_ROOT_CAPTURE_AND_READBACK'}
write(D/'ROOT_CURRENT_REPRODUCTION_SUMMARY.json',summary)
files,dirs=inventory()
for n in files:(D/n).chmod(0o444)
rows=[{'path':n,'bytes':len(b),'sha256':sha(b),'full_mode':0o444} for n,b in sorted(files.items())]
m={'schema':'pr49-root-original-complete-reproduction-self-only-closure/v1','created_utc':dt.datetime.now(dt.timezone.utc).isoformat(),'actual_closing_pid':os.getpid(),'self_excluded':[MF],'files_count':len(rows),'files':rows,'directories':sorted(dirs),'all_payload_full_mode':0o444,'future_acceptance_approved':False,'external_postexit_capture_and_separate_readback_required':True}
write(D/MF,m);(D/MF).chmod(0o444)
after,ads=inventory();assert set(after)==set(files)|{MF} and ads==dirs
for n,b in files.items():assert after[n]==b and stat.S_IMODE((D/n).stat().st_mode)==0o444
print(json.dumps({'status':'CLOSED_ROOT_COMPLETED_REPRODUCTION_ONLY','manifest_sha256':sha(read(D/MF)),'files_count':len(rows),'relative_directories':len(dirs),'actual_pid':os.getpid(),'future_acceptance_approved':False}))
