#!/usr/bin/env python3
"""SOURCE: run reviewed portable diagnostics and prepare support, ROOT only.
No imports or execution of this helper have been performed by its preparer.
Writes only new own-package capture/results/record/checksums; no network/Git.
SPDX-License-Identifier: MIT
"""
import argparse
import datetime
import hashlib
import json
import os
from pathlib import Path
import stat
import subprocess
import sys

BASE = Path(__file__).absolute().parent


def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def body_json(v): return (json.dumps(v, indent=2, sort_keys=True)+'\n').encode()
def sha(b): return hashlib.sha256(b).hexdigest()
def regular(name):
    q=BASE/name;s=q.lstat()
    if q.is_symlink() or not stat.S_ISREG(s.st_mode): raise ValueError('Regular own input required')
    b=q.read_bytes();t=q.lstat()
    if (s.st_ino,s.st_size,s.st_mode,s.st_mtime_ns,s.st_ctime_ns)!=(t.st_ino,t.st_size,t.st_mode,t.st_mtime_ns,t.st_ctime_ns): raise ValueError('Input changed while reading')
    return b, {'name':name,'bytes':len(b),'sha256':sha(b),'full_mode_07777':format(stat.S_IMODE(s.st_mode),'04o')}
def write_new(q,b):
    with q.open('xb') as f:f.write(b);f.flush();os.fsync(f.fileno())


def main():
    ap=argparse.ArgumentParser()
    ap.add_argument('--root-only-run-after-personally-reading-source',action='store_true',required=True)
    ap.parse_args()
    if not __debug__: raise ValueError('Guard execution required')
    for name in ['expected_results.json','VERIFICATION_RECORD.json','SHA256SUMS','diagnostic_run']:
        if (BASE/name).exists() or (BASE/name).is_symlink():raise ValueError('Refuse existing output: '+name)
    checker,checker_ref=regular('verify_integer_endpoint.py')
    manuscript,manuscript_ref=regular('integer_endpoint_discontinuity.tex')
    helper,helper_ref=regular('prepare_support_for_ROOT.py')
    run=BASE/'diagnostic_run';run.mkdir(exist_ok=False)
    write_new(run/'prelaunch_checker.py',checker)
    write_new(run/'prelaunch_operator.py',helper)
    write_new(run/'PRELAUNCH.json',body_json({'utc':now(),'actual_operator_pid':os.getpid(),'checker':checker_ref,'manuscript':manuscript_ref,'operator':helper_ref,'ROOT_approval_claimed':False}))
    argv=[sys.executable,'-B',str(BASE/'verify_integer_endpoint.py')]
    start=now();child=subprocess.Popen(argv,cwd=BASE,stdin=subprocess.DEVNULL,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
    out,err=child.communicate();end=now()
    write_new(run/'stdout.bin',out);write_new(run/'stderr.bin',err)
    cap={'schema':'pr57-portable-diagnostic-actual-capture/v1','actual_execution':True,'operator_pid':os.getpid(),'child_pid':child.pid,'argv':argv,'cwd':str(BASE),'start_utc':start,'end_utc':end,'exit_code':child.returncode,'completed':True,'checker':checker_ref,'manuscript':manuscript_ref,'operator':helper_ref,'stdout':{'name':'stdout.bin','bytes':len(out),'sha256':sha(out)},'stderr':{'name':'stderr.bin','bytes':len(err),'sha256':sha(err)},'ROOT_approval_claimed':False,'independent_review_credit':0}
    write_new(run/'CAPTURE.json',body_json(cap))
    if child.returncode!=0 or err:raise RuntimeError('Diagnostics failed; complete capture retained')
    result=json.loads(out)
    if result['status']!='PASS_FINITE_EXACT_DIAGNOSTICS':raise ValueError('Unexpected diagnostic status')
    if regular('verify_integer_endpoint.py')[1]!=checker_ref or regular('integer_endpoint_discontinuity.tex')[1]!=manuscript_ref or regular('prepare_support_for_ROOT.py')[1]!=helper_ref:raise ValueError('Exact source changed during run')
    write_new(BASE/'expected_results.json',out)
    record={'schema':'pr57-portable-verification-record/v1','actual_run':cap,'result_summary':{k:result[k] for k in ['status','geometric_control_count','logarithm_recurrence_control_count','Beltrami_degree_control_count','rational_metric_reconstruction_control_count']},'expected_results':regular('expected_results.json')[1],'finite_diagnostics_not_universal_proof':True,'new_independent_review_credit':0,'human_peer_review_claimed':False}
    write_new(BASE/'VERIFICATION_RECORD.json',body_json(record))
    # Explicit literal ZIP domain shared with the separately reviewed builder.
    names=['LICENSE-CODE.txt','LICENSE-TEXT.md','README.md','SOURCE_QUALIFICATIONS.md','VERIFICATION_PROVENANCE.json','VERIFICATION_RECORD.json','build_verification_zip.py','integer_endpoint_discontinuity.tex','expected_results.json','verify_integer_endpoint.py']
    rows=[]
    for name in sorted(names): b,_=regular(name);rows.append(sha(b)+'  '+name+'\n')
    write_new(BASE/'SHA256SUMS',''.join(rows).encode('ascii'))
    print(json.dumps({'status':'PASS_ACTUAL_DIAGNOSTICS_AND_SUPPORT_SOURCE_PREPARATION','actual_operator_pid':os.getpid(),'child_pid':child.pid,'record':regular('VERIFICATION_RECORD.json')[1],'archive_built':False,'ROOT_review_or_publication_approval_claimed':False},indent=2,sort_keys=True))


if __name__=='__main__':main()
