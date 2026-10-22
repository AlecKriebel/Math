"""Mutations execute certificate validators directly, independent of manifest rejection."""
import hashlib
import json
import pathlib
import shutil
import subprocess
import sys
import tempfile

def require(condition,reason):
    if not condition: raise RuntimeError(reason)

def run(script,root,optimized):
    return subprocess.run([sys.executable,'-I','-B']+(['-O'] if optimized else [])+[script],cwd=root,capture_output=True,timeout=120)

def main():
    root=pathlib.Path(__file__).resolve().parent
    results=[]
    mutations=[('verify_exact.py','H=s.diag(-1,s.Rational(3,4))','H=s.diag(-1,s.Rational(1,2))'),
               ('verify_low_rank.py','cs = [F(3, 4), F(1, 8), F(1, 8)]','cs = [F(2, 4), F(1, 8), F(1, 8)]'),
               ('replay.py','[[3247,-881,-2481,-561]','[[3248,-881,-2481,-561]'),
               ('replay.py','p=(n+1)//2; q=n//2','p=(n+1)//2; q=0')]
    for optimized in (False,True):
        baseline=run('verify_manifest.py',root,optimized)
        require(baseline.returncode==0 and not baseline.stderr,'Pristine manifest baseline failed')
        for index,(name,old,new) in enumerate(mutations):
            with tempfile.TemporaryDirectory() as td:
                tmp=pathlib.Path(td); code=(root/name).read_text()
                require(code.count(old)==1,'Ambiguous mutation target')
                (tmp/name).write_text(code.replace(old,new))
                result=run(name,tmp,optimized)
                require(result.returncode!=0 and b'RuntimeError: Certificate validation failed' in result.stderr,'Mutation did not reach certificate validator')
                results.append({'kind':'certificate','case':index,'optimized':optimized,'rejected_by':'certificate validator'})
        for mutation in ['changed_byte','missing_file','extra_file','manifest_hash','manifest_total','manifest_duplicate','manifest_traversal']:
            with tempfile.TemporaryDirectory() as td:
                tmp=pathlib.Path(td)/'package'; shutil.copytree(root,tmp)
                m=json.loads((tmp/'MANIFEST.json').read_text())
                if mutation=='changed_byte': (tmp/'README.md').write_bytes((tmp/'README.md').read_bytes()+b'!')
                elif mutation=='missing_file': (tmp/'README.md').unlink()
                elif mutation=='extra_file': (tmp/'unexpected.txt').write_text('unexpected')
                elif mutation=='manifest_hash': m['files'][0]['sha256']='0'*64
                elif mutation=='manifest_total': m['total_bytes_excluding_manifest']+=1
                elif mutation=='manifest_duplicate': m['files'].append(m['files'][0])
                elif mutation=='manifest_traversal': m['files'][0]['path']='../outside.txt'
                (tmp/'MANIFEST.json').write_text(json.dumps(m))
                result=run('verify_manifest.py',tmp,optimized)
                require(result.returncode!=0 and b'RuntimeError:' in result.stderr,'Manifest mutation was not rejected')
                results.append({'kind':'manifest','case':mutation,'optimized':optimized,'rejected':True})
    print(json.dumps({'status':'PASS','controls':results},indent=2))
if __name__=='__main__': main()
