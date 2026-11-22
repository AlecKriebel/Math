"""Offline reproduction. All compilation/output artifacts use a disposable directory."""
import hashlib,json,os,subprocess,sys,tempfile
from pathlib import Path
sys.dont_write_bytecode=True
from validate import validate,require
ROOT=Path(__file__).resolve().parent
FLAGS=['-std=c++17','-O2','-Wall','-Wextra','-pedantic']
def run(args):
    p=subprocess.run(args,capture_output=True,text=True,env={**os.environ,'PYTHONDONTWRITEBYTECODE':'1'})
    require(p.returncode==0,'command failed: '+repr(args)+'\n'+p.stderr)
    return p.stdout,p.stderr
def main():
    validation=validate(ROOT)
    report={'validation':validation,'compiler_version':run(['g++','--version'])[0],'python_version':run([sys.executable,'--version'])[0].strip(),'runs':[],'network_required':False}
    with tempfile.TemporaryDirectory(prefix='theta-replay-') as tmp:
        for mode,extra in [('normal',[]),('ndebug',['-DNDEBUG'])]:
            binary=str(Path(tmp)/mode)
            stdout,stderr=run(['g++',*FLAGS,*extra,str(ROOT/'finite_test.cpp'),'-o',binary])
            out,err=run([binary]);require(out.encode()==(ROOT/'FINITE_TEST.json').read_bytes(),'finite byte mismatch')
            report['runs'].append({'program':'finite_test.cpp','mode':mode,'flags':FLAGS+extra,'compiler_stdout':stdout,'compiler_stderr':stderr,'stdout':out,'stderr':err,'byte_match':True})
        for mode,extra in [('normal',[]),('optimized',['-O'])]:
            for program,expected in [('profile_test.py','PROFILES.json'),('independent_check.py','INDEPENDENT_CHECK.json'),('exact_checks.py','EXACT_CHECKS.json'),('rank_checks.py','RANK_CHECKS.json')]:
                out,err=run([sys.executable,*extra,str(ROOT/program)])
                require(out.encode()==(ROOT/expected).read_bytes(),program+' byte mismatch')
                report['runs'].append({'program':program,'mode':mode,'stdout':out,'stderr':err,'byte_match':True})
    print(json.dumps(report,indent=2))
if __name__=='__main__':main()
