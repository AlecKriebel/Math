#!/usr/bin/env python3
"""Run UID-1000 read-only and mutation tests against the frozen public packet.
Usage: python run_readonly_audit.py /path/to/original/public
No source PDFs, network, third-party modules, or optimized-away assertions are used.
Creates temporary test copies only; writes the result to stdout.
"""
import ast
import hashlib
import json
import os
from pathlib import Path
import shutil
import stat
import subprocess
import sys
import tempfile


def check(condition, message):
    if not condition:
        raise RuntimeError(message)


def sha(data):
    return hashlib.sha256(data).hexdigest()


def snapshot(root):
    return {str(p.relative_to(root)):sha(p.read_bytes()) for p in sorted(root.rglob('*')) if p.is_file()}


WRAPPER = r'''
import errno,json,os,runpy,sys
from pathlib import Path
if os.getuid()!=1000 or os.geteuid()!=1000:
    raise RuntimeError('Audit requires genuine UID and EUID 1000')
if sys.flags.optimize!=int(sys.argv[2]):
    raise RuntimeError('Wrong optimization level')
p=Path(sys.argv[1]); cwd=Path.cwd()
if (cwd.stat().st_mode & 0o777)!=0o555 or (p.stat().st_mode & 0o777)!=0o444:
    raise RuntimeError('Readonly modes not established')
proof={'uid':os.getuid(),'euid':os.geteuid(),'gid':os.getgid(),'optimization':sys.flags.optimize,'cwd_mode':'0555','script_mode':'0444'}
for label, operation in [('create',lambda:(cwd/'write_probe').open('xb')),('append',lambda:p.open('ab'))]:
    try:
        handle=operation()
    except OSError as exc:
        if exc.errno not in (errno.EACCES,errno.EROFS,errno.EPERM):
            raise
        proof[label+'_denied']=True
        proof[label+'_errno']=exc.errno
    else:
        handle.close()
        raise RuntimeError('Readonly write probe unexpectedly succeeded')
print(json.dumps(proof,sort_keys=True),file=sys.stderr)
sys.argv=[str(p)]
runpy.run_path(str(p),run_name='__main__')
'''


def execute(case, code, expected, root):
    d=root/case
    d.mkdir()
    p=d/'check.py'
    p.write_bytes(code)
    p.chmod(0o444)
    d.chmod(0o555)
    before=snapshot(d)
    runs=[]
    try:
        for optimization,flag in ((0,[]),(1,['-O']),(2,['-OO'])):
            result=subprocess.run([sys.executable,'-I','-B']+flag+['-c',WRAPPER,str(p),str(optimization)],cwd=d,capture_output=True,timeout=60)
            stderr=result.stderr.decode()
            first=stderr.splitlines()[0] if stderr else ''
            proof=json.loads(first)
            check(proof['uid']==1000 and proof['euid']==1000,'Wrong tested UID')
            check(proof['create_denied'] and proof['append_denied'],'Write denial missing')
            check(snapshot(d)==before,'Test directory changed')
            if isinstance(expected,bytes):
                check(result.returncode==0,'Unexpected baseline failure: '+stderr)
                check(result.stdout==expected,'Baseline stdout changed')
                check(len(stderr.splitlines())==1,'Unexpected baseline stderr')
                detected='PASS'
            else:
                check(result.returncode!=0,'Mutation escaped: '+case)
                check(expected in stderr,'Wrong mutation detection: '+case+' '+stderr)
                check(not result.stdout,'Mutation printed successful payload')
                detected=expected
            runs.append({'flags':flag,'exit_code':result.returncode,'stdout_bytes':len(result.stdout),'stdout_sha256':sha(result.stdout),'detected':detected,'environment':proof,'directory_unchanged':True})
    finally:
        d.chmod(0o755)
        p.chmod(0o644)
    return {'case':case,'code_sha256':sha(code),'runs':runs}


def mutate(source,old,new):
    check(source.count(old)==1,'Mutation target not unique: '+old)
    return source.replace(old,new).encode()


def main():
    check(len(sys.argv)==2,'Pass the original public packet directory')
    check(os.getuid()==os.geteuid()==1000,'Run as UID 1000; root is not accepted')
    original=Path(sys.argv[1]).resolve()
    before=snapshot(original)
    code=(original/'verify_exact.py').read_bytes()
    check(sha(code)=='208b1f8a05fbfc03c5efb5fc8aa64ab626eb1f1911bf7737e0bfe160371efc1b','Wrong frozen checker')
    expected=(original/'EXACT_CHECKS.json').read_bytes()
    check(sha(expected)=='9ed8e2898b651ea06f20a3e7c4eb2742bda3ba8d955ae7f7b23fa22e546054ca','Wrong expected frozen output')
    own=Path(__file__).resolve().parent
    independent=(own/'independent_exact.py').read_bytes()
    independent_output=(own/'INDEPENDENT_EXACT.json').read_bytes()
    original_text=code.decode()
    independent_text=independent.decode()
    for name,source in [('frozen',original_text),('independent',independent_text),('harness',Path(__file__).read_text())]:
        check(not any(isinstance(n,ast.Assert) for n in ast.walk(ast.parse(source))),name+' contains optimization-disabled assert')
    cases=[('frozen_baseline',code,expected),('independent_baseline',independent,independent_output)]
    specifications=[
        ('frozen_bad_inverse','result[i] = (-(i + 1), i, i + 1)','result[i] = (i,)','Artin generator inverse failed'),
        ('frozen_bad_second_product','q = (conjugate((1, 1), b), b)','q = (conjugate((1, 1, 1), b), b)','Second product differs from beta'),
        ('frozen_identity_conjugator','g = (1, -2, -1)','g = ()','Simultaneous conjugation failed'),
        ('frozen_shifted_homology','[0, -n, 1]','[0, -(n + 1), 1]','Determinantal-divisor mismatch'),
        ('frozen_changed_form','omega1 = (1, 2, 0, 0, -2, -3)','omega1 = (1, 2, 0, 0, -2, -2)','Pfaffian identity failed'),
        ('frozen_added_genus','genus = (d - 1) * (d - 2) // 2','genus = (d - 1) * (d - 2) // 2 + 1','Capping Euler characteristic failed')]
    for name,old,new,message in specifications:
        cases.append((name,mutate(original_text,old,new),message))
    independent_specifications=[
        ('independent_identity_conjugator','g=[1,-2,-1]','g=[]','global conjugacy'),
        ('independent_wrong_row_move','rowadd(m,0,1,-1)','rowadd(m,0,1,-2)','universal Smith reduction'),
        ('independent_changed_form','(1,3):(0,-2)','(1,3):(0,-1)','universal exterior-square identity'),
        ('independent_wrong_chern','chi_closed=(0,3,-1)','chi_closed=(0,4,-1)','universal Euler identity')]
    for name,old,new,message in independent_specifications:
        cases.append((name,mutate(independent_text,old,new),message))
    with tempfile.TemporaryDirectory(prefix='curve-isotopy-readonly-') as scratch:
        results=[execute(name,source,expect,Path(scratch)) for name,source,expect in cases]
    check(snapshot(original)==before,'Original packet changed')
    out={'status':'PASS','uid':os.getuid(),'euid':os.geteuid(),'python_version':sys.version.split()[0],
         'baseline_runs':6,'mutation_runs':30,'mutation_families':10,'source_free':True,'no_assert_statements':True,
         'original_packet_unchanged':True,'original_checker_sha256':sha(code),'independent_checker_sha256':sha(independent),
         'tests':results}
    print(json.dumps(out,sort_keys=True,indent=2))


if __name__=='__main__':
    main()
