"""Run positive checks and actual corrupted-input negative controls in temporary copies."""
from pathlib import Path
import json, shutil, subprocess, sys, tempfile
ROOT=Path(__file__).resolve().parent

def require(ok, text):
    if not ok: raise RuntimeError(text)

def run(path, optimized=False, manifest=False):
    cmd=[sys.executable]+(['-O'] if optimized else [])+[str(path/'verify_arithmetic_gap.py')]+(['--manifest'] if manifest else [])
    return subprocess.run(cmd,capture_output=True,text=True)

def main():
    mutations=[
      ('graph coefficient', '(e[0]+e[3],e[1]+2*e[2])', '(e[0]+e[3],e[1]+3*e[2])'),
      ('real witness', 's.sqrt(2)*e[0]+e[1]', 's.sqrt(3)*e[0]+e[1]'),
      ('arrow matrix', 'T=s.Matrix([[0,2],[1,0]])', 'T=s.Matrix([[0,3],[1,0]])'),
      ('H cone generator', '4*w+e[j]', '3*w+e[j]'),
    ]
    for optimized in [False,True]:
      mode='optimized' if optimized else 'normal'
      good=run(ROOT,optimized,True)
      require(good.returncode==0,good.stdout+good.stderr)
      print('PASS:',mode,'baseline exact checks and manifest')
      for label,old,new in mutations:
        with tempfile.TemporaryDirectory() as td:
          copy=Path(td); code=(ROOT/'verify_arithmetic_gap.py').read_text()
          require(code.count(old)==1,'Mutation target is not unique: '+label)
          (copy/'verify_arithmetic_gap.py').write_text(code.replace(old,new))
          result=run(copy,optimized)
          require(result.returncode!=0 and 'RuntimeError: FAIL:' in result.stderr,'Mutation escaped explicit guards: '+label)
          print('PASS:',mode,'rejected matrix mutation:',label)
      for label in ['changed bytes','missing file','unexpected file','false digest','false size']:
        with tempfile.TemporaryDirectory() as td:
          copy=Path(td)/'package'; shutil.copytree(ROOT,copy,ignore=shutil.ignore_patterns('__pycache__'))
          target=copy/'README.md'
          if label=='changed bytes': target.write_bytes(target.read_bytes()+b'\nTAMPER\n')
          elif label=='missing file': target.unlink()
          elif label=='unexpected file': (copy/'unexpected.txt').write_text('unexpected')
          else:
            path=copy/'MANIFEST.json'; data=json.loads(path.read_text())
            if label=='false digest': data['files'][0]['sha256']='0'*64
            else: data['files'][0]['bytes']+=1
            path.write_text(json.dumps(data))
          result=run(copy,optimized,True)
          require(result.returncode!=0 and 'RuntimeError: FAIL: manifest' in result.stderr,'Manifest corruption escaped: '+label)
          print('PASS:',mode,'rejected manifest control:',label)
    print('PASS: 2 positive executions, 8 matrix mutations, 10 manifest corruptions; no assert-dependent guards.')
if __name__=='__main__': main()
