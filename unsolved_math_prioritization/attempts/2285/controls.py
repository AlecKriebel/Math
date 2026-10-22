"""Isolated negative controls. Does not alter the accepted package."""
from pathlib import Path
import subprocess,sys,tempfile,shutil,json,hashlib,ast,os
ROOT=Path(__file__).parent

def invoke(path,optimized):
 return subprocess.run([sys.executable]+(['-O'] if optimized else [])+[str(path)],capture_output=True,text=True)

def run():
 results=[]
 source=(ROOT/'checks.py').read_text()
 # Each mutation deliberately breaks a specific mathematical assertion.
 mutations=[('line size','len(L) == q + 1','len(L) == q + 2'),('pair uniqueness','== 1 for i, j in itertools.combinations','== 2 for i, j in itertools.combinations'),('mean identity','mean == k * p','mean == k * p + 1'),('variance identity','== q * p * (1 - p)','== q * p * (1 - p) + 1'),('covariance trace','trace == enumerated','trace == enumerated + 1'),('shared point covariance','joint - sum((x * x for x in b)) == rhs','joint - sum((x * x for x in b)) == rhs + 1'),('total variation bound','tv <= F(m, v)','tv <= -F(m, v)')]
 for optimized in (False,True):
  for label,old,new in mutations:
   if old not in source:raise RuntimeError('Mutation target missing: '+label)
   with tempfile.TemporaryDirectory() as t:
    path=Path(t)/'checks.py';path.write_text(source.replace(old,new))
    result=invoke(path,optimized)
    if result.returncode==0 or 'RuntimeError: Finite mathematical check failed:' not in result.stderr:raise RuntimeError('Mathematical control not rejected correctly: '+label)
    results.append(dict(kind='mathematical',control=label,optimized=optimized,result='REJECTED',exit_code=result.returncode))
  # Exercise actual n=9 threshold gate directly, not an edited output string.
  tree=ast.parse(source)
  last=next(x for x in tree.body if isinstance(x,ast.For) and isinstance(x.target,ast.Name) and x.target.id=='n' and isinstance(x.iter,ast.Call) and ast.unparse(x.iter)=='range(10, 100001)')
  last.iter=ast.parse('range(9, 10)',mode='eval').body
  module=ast.Module(body=[ast.ImportFrom(module='fractions',names=[ast.alias(name='Fraction',asname='F')],level=0),ast.Assign(targets=[ast.Name(id='summary',ctx=ast.Store())],value=ast.Dict(keys=[ast.Constant('order_cases')],values=[ast.Constant(0)])),last],type_ignores=[]);ast.fix_missing_locations(module)
  with tempfile.TemporaryDirectory() as t:
   path=Path(t)/'checks.py';path.write_text(ast.unparse(module));result=invoke(path,optimized)
   if result.returncode==0 or 'n > q + 1' not in result.stderr:raise RuntimeError('Threshold regression not rejected')
   results.append(dict(kind='mathematical',control='n=9 nontriviality regression',optimized=optimized,result='REJECTED',exit_code=result.returncode))
  for label in ['changed bytes','missing file','extra root file','extra nested file','nested symlink','unlisted FIFO','symlink root','duplicate manifest entry']:
   with tempfile.TemporaryDirectory() as t:
    root=Path(t)/'package';shutil.copytree(ROOT,root)
    if label=='changed bytes':(root/'RESEARCH.md').write_text('corrupted')
    elif label=='missing file':(root/'RESEARCH.md').unlink()
    elif label=='extra root file':(root/'unexpected.txt').write_text('unexpected')
    elif label=='extra nested file':(root/'nested').mkdir();(root/'nested'/'unexpected.txt').write_text('unexpected')
    elif label=='nested symlink':(root/'nested').mkdir();(root/'nested'/'link').symlink_to('../RESEARCH.md')
    elif label=='unlisted FIFO':os.mkfifo(root/'unexpected.fifo')
    elif label=='symlink root':
     link=Path(t)/'alias';link.symlink_to(root,target_is_directory=True)
    else:
     m=json.loads((root/'MANIFEST.json').read_text());m['files'].append(m['files'][0]);(root/'MANIFEST.json').write_text(json.dumps(m))
    if label=='symlink root':
     result=subprocess.run([sys.executable]+(['-O'] if optimized else [])+[str(root/'verify.py'),str(link)],capture_output=True,text=True)
    else:result=invoke(root/'verify.py',optimized)
    if result.returncode==0 or 'RuntimeError' not in result.stderr:raise RuntimeError('Inventory control not rejected: '+label)
    results.append(dict(kind='recursive inventory',control=label,optimized=optimized,result='REJECTED',exit_code=result.returncode))
 return results
if __name__=='__main__':print(json.dumps(run(),indent=2))
