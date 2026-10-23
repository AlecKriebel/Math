"""Full replay in isolated temporary directories; published evidence is not overwritten."""
import ast,hashlib,json,os,shutil,subprocess,sys,tempfile
from pathlib import Path
ROOT=Path(__file__).parent
SCRIPTS=['check_tricycles.py','check_lengths.py','audit_independent.py']
OUTPUTS=['TRICYCLE_CHECKS.json','LENGTH_CHECKS.json','AUDIT_CHECKS.json']
def main():
    result=[]
    for flags in [[],['-O']]:
        with tempfile.TemporaryDirectory() as td:
            td=Path(td)
            for n in SCRIPTS:shutil.copyfile(ROOT/n,td/n)
            logs=[]
            for n in SCRIPTS:
                c=subprocess.run([sys.executable,*flags,'-B',str(td/n)],cwd=td,text=True,capture_output=True)
                logs.append({'script':n,'exit':c.returncode,'stdout':c.stdout,'stderr':c.stderr})
                if c.returncode:raise RuntimeError(logs)
            matches={n:json.loads((td/n).read_text())==json.loads((ROOT/n).read_text()) for n in OUTPUTS}
            if not all(matches.values()):raise RuntimeError(matches)
            result.append({'mode':'optimized' if flags else 'normal','logs':logs,'full_output_matches':matches})
    print(json.dumps(result,separators=(',',':')))
if __name__=='__main__':main()
