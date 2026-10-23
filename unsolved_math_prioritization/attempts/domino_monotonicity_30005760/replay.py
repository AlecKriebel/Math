#!/usr/bin/env python3
"""Full unmodified module executions in temporary workspaces; no network."""
import concurrent.futures,hashlib,json,os,shutil,subprocess,sys,tempfile,time
from pathlib import Path
sys.dont_write_bytecode=True
from verify_package import verify,ROOT
HOOK="""import sys
sys.dont_write_bytecode=True
def deny(event,args):
 if event.startswith('socket.'): raise RuntimeError('network prohibited')
sys.addaudithook(deny)
"""
def run_mode(opt):
    with tempfile.TemporaryDirectory(prefix='domino-replay-') as td:
        w=Path(td)
        for name in ['domino_1890_analysis','domino_1890_audit']:shutil.copytree(ROOT/name,w/name)
        (w/'sitecustomize.py').write_text(HOOK)
        env=dict(os.environ,PYTHONPATH=td,PYTHONDONTWRITEBYTECODE='1')
        runs=[]
        cases=[('domino_1890_analysis/explore.py','domino_1890_analysis/counts.log'),('domino_1890_analysis/enumerate.py','domino_1890_analysis/counts_extended.log'),('domino_1890_analysis/verify.py','domino_1890_audit/verify_normal.log'),('domino_1890_analysis/basis.py','domino_1890_audit/basis_normal.log'),('domino_1890_analysis/independent_smallcase_check.py','domino_1890_audit/smallcase_normal.json'),('domino_1890_analysis/independent_f_test.py','domino_1890_audit/f_normal.log'),('domino_1890_analysis/transfer.py','domino_1890_audit/transfer_normal.log'),('domino_1890_analysis/transfer_extended.py','domino_1890_audit/transfer_extended_normal.log'),('domino_1890_analysis/find_half_obstruction.py','domino_1890_audit/half_obstruction_normal.log'),('domino_1890_audit/independent_check.py','domino_1890_audit/check_normal.json')]
        for script,expected in cases:
            start=time.monotonic();proc=subprocess.run([sys.executable]+(['-O'] if opt else [])+[script],cwd=w,env=env,capture_output=True)
            if proc.returncode or proc.stdout!=(ROOT/expected).read_bytes():raise RuntimeError((opt,script,proc.returncode,proc.stderr.decode(), 'output mismatch'))
            runs.append({'script':script,'exit_code':proc.returncode,'stdout_sha256':hashlib.sha256(proc.stdout).hexdigest(),'elapsed_seconds':round(time.monotonic()-start,3),'archive_byte_equal':True})
        for name in ['counts.json','counts_extended.json','basis_certificate.json','VALIDATION.json']:
            if (w/'domino_1890_analysis'/name).read_bytes()!=(ROOT/'domino_1890_analysis'/name).read_bytes():raise RuntimeError('generated artifact mismatch: '+name)
        return {'optimized':opt,'runs':runs,'regenerated_artifacts_byte_equal':True}
def main():
    integrity=verify()
    with concurrent.futures.ThreadPoolExecutor(max_workers=2) as pool:modes=list(pool.map(run_mode,[False,True]))
    with tempfile.TemporaryDirectory(prefix='domino-cpp-') as td:
        exe=Path(td)/'enumerate';cmd=['g++','-std=c++17','-O3','-Wall','-Wextra','-pedantic',str(ROOT/'domino_1890_audit/independent_enumerate.cpp'),'-o',str(exe)]
        subprocess.run(cmd,check=True,capture_output=True);proc=subprocess.run([str(exe)],check=True,capture_output=True)
        if proc.stdout!=(ROOT/'domino_1890_audit/independent_counts.json').read_bytes():raise RuntimeError('independent C++ output mismatch')
    result={'integrity':integrity,'modes':modes,'independent_cpp':{'byte_equal':True,'sha256':hashlib.sha256(proc.stdout).hexdigest()},'status':'PASS_PARTIAL_ONLY','full_conjecture':'UNRESOLVED'}
    text=json.dumps(result,indent=2)+'\n'
    if len(sys.argv)>1:Path(sys.argv[1]).write_text(text)
    else:print(text,end='')
if __name__=='__main__':main()
