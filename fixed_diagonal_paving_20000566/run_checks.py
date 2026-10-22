"""Run optimization-safe checks in isolation and compare complete frozen stdout."""
import json,subprocess,sys,tempfile,shutil
from pathlib import Path
sys.dont_write_bytecode=True
from verify import verify
from check_provenance import check
ROOT=Path(__file__).parent

def main():
    verify(ROOT)
    check(ROOT)
    results=[]
    for name in ['checks.py','check_witness.py','exact_checks.py','strict_checks.py','theorem_checks.py']:
        with tempfile.TemporaryDirectory() as td:
            dest=Path(td)/name; shutil.copyfile(ROOT/name,dest)
            cmd=[sys.executable]+(['-O'] if sys.flags.optimize else [])+[str(dest)]
            p=subprocess.run(cmd,capture_output=True)
            if p.returncode or p.stderr:raise RuntimeError(name+' failed: '+p.stderr.decode())
            if p.stdout!=(ROOT/('outputs/'+name+'.stdout')).read_bytes():raise RuntimeError(name+' full stdout mismatch')
            for filename in ['CHECK_RESULTS.json','WITNESS_CHECK.json']:
                f=Path(td)/filename
                if f.exists() and f.read_bytes()!=(ROOT/('outputs/'+filename)).read_bytes():raise RuntimeError(filename+' output mismatch')
            results.append({'script':name,'status':'PASS','complete_stdout_equal':True})
    print(json.dumps({'status':'PASS','optimized':bool(sys.flags.optimize),'checks':results},indent=2))
if __name__=='__main__':main()
