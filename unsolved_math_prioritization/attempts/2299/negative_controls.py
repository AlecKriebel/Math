"""Non-destructive offline integrity controls; all mutations occur in temporary copies."""
import ast
import os
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).absolute().parent

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def run_case(name, mutate):
    with tempfile.TemporaryDirectory(prefix='erdos776-negative-') as temporary:
        base = Path(temporary)
        target = base/'package'
        shutil.copytree(ROOT, target, symlinks=True)
        selected = mutate(target, base) or target
        result = subprocess.run([sys.executable, '-B', '-O', str(ROOT/'validate.py'), str(selected)], capture_output=True, text=True)
        print('CASE:', name)
        print('STDOUT:\n'+result.stdout, end='')
        print('STDERR:\n'+result.stderr, end='')
        print('EXIT:', result.returncode)
        require(result.returncode != 0 and 'FAIL:' in result.stderr, 'negative control was not rejected: '+name)
        print('PASS rejected '+name)

def mutate_file(p,b):
    with (p/'audit/INDEPENDENT_ARITHMETIC.json').open('ab') as stream:
        stream.write(b' ')

def root_link(p,b):
    link=b/'link'; link.symlink_to(p, target_is_directory=True); return link

if __name__ == '__main__':
    run_case('altered file', mutate_file)
    run_case('missing file', lambda p,b: (p/'audit/SYMBOLIC_REVIEW.md').unlink())
    def extra(p,b): (p/'unexpected.txt').write_text('unexpected')
    run_case('unexpected file', extra)
    run_case('empty unexpected directory', lambda p,b: (p/'unexpected').mkdir())
    run_case('nested directory symlink', lambda p,b: (p/'audit/link').symlink_to(p/'audit', target_is_directory=True))
    run_case('file symlink', lambda p,b: (p/'audit/link').symlink_to(p/'README.md'))
    run_case('FIFO', lambda p,b: os.mkfifo(p/'audit/pipe'))
    run_case('root symlink', root_link)
    source=(ROOT/'audit/independent_arithmetic.py').read_text()
    tree=ast.parse(source)
    require(not any(isinstance(n,ast.Assert) for n in ast.walk(tree)), 'assert remains in arithmetic')
    checks=[n for n in ast.walk(tree) if isinstance(n,ast.If) and any(isinstance(x,ast.Raise) for x in n.body)]
    require(len(checks)==8, 'unexpected number of hardened arithmetic checks')
    # Force a formerly asserted invariant false. Execute directly, outside receipt validation.
    first=next(n for n in ast.walk(tree) if isinstance(n,ast.If) and isinstance(n.test,ast.UnaryOp) and any(isinstance(x,ast.Raise) for x in n.body))
    first.test=ast.Constant(value=True)
    with tempfile.TemporaryDirectory(prefix='erdos776-check-') as temporary:
        script=Path(temporary)/'forced_failure.py'
        script.write_text(ast.unparse(ast.fix_missing_locations(tree))+'\n')
        result=subprocess.run([sys.executable,'-B','-O',str(script)],capture_output=True,text=True)
        print('CASE: forced arithmetic invariant under -O')
        print('STDOUT:\n'+result.stdout,end=''); print('STDERR:\n'+result.stderr,end=''); print('EXIT:',result.returncode)
        require(result.returncode != 0 and 'Arithmetic check failed:' in result.stderr,'optimized arithmetic invariant disappeared')
    print('PASS explicit arithmetic failures remain active under -O; no asserts in arithmetic')
    print('PASS all nine negative controls')
