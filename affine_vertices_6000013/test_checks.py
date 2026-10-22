"""Executable guard, exact output, mathematical mutation and inventory tests."""
from pathlib import Path
import tempfile,subprocess,sys,json
sys.dont_write_bytecode=True
from inventory import inventory,verify,safe_name
root=Path(__file__).resolve().parent
source=(root/'verify.py').read_text()
expected=(root/'VERIFY_OUTPUT.txt').read_bytes()
def require(condition,message):
    if not condition:raise RuntimeError(message)
def run(path,opt):
    return subprocess.run([sys.executable]+opt+[str(path)],capture_output=True)
mutations=[
 ('cubic numerator','== 8640','== 8641'),
 ('power family','(2 * a - 1)','(2 * a + 1)'),
 ('sine factor','36 * s.sin','35 * s.sin'),
 ('conic Wronskian','-207360 * x','-207359 * x'),
 ('contact coefficient','4320 *','4321 *'),
 ('oval first variation','(n * n - 4)','(n * n - 5)'),
 ('spiral determinant','2 * s.exp(2 * t)','3 * s.exp(2 * t)'),
 ('spiral exponent collision','2 + 2 * s.I','2 - 2 * s.I'),
]
with tempfile.TemporaryDirectory() as td:
    temp=Path(td)
    for opt in ([],['-O']):
        baseline=run(root/'verify.py',opt)
        require(baseline.returncode==0 and baseline.stdout==expected and baseline.stderr==b'', 'Full baseline output mismatch')
        for label,old,new in mutations:
            require(source.count(old)>=1,'Mutation target absent: '+label)
            path=temp/'mutant.py';path.write_text(source.replace(old,new,1))
            result=run(path,opt)
            require(result.returncode!=0 and b'RuntimeError: Exact mathematical check failed' in result.stderr,'Mutation escaped: '+label)
        print('PASS: exact output and '+str(len(mutations))+' mathematical mutations in '+('optimized' if opt else 'normal')+' Python.')
    fixture=temp/'fixture';fixture.mkdir();(fixture/'proof.txt').write_text('proof')
    def freeze(): (fixture/'MANIFEST.json').write_text(json.dumps({'schema':1,'files':inventory(fixture)}))
    def rejected(label):
        try:verify(fixture)
        except ValueError:return
        raise RuntimeError('Inventory attack escaped: '+label)
    freeze();verify(fixture)
    nested=fixture/'nested';nested.mkdir();extra=nested/'MANIFEST.json';extra.write_text('{}')
    rejected('nested manifest addition')
    freeze();require('nested/MANIFEST.json' in verify(fixture),'Nested manifest excluded')
    extra.write_text('{"changed":true}');rejected('nested manifest alteration')
    extra.unlink();nested.rmdir();freeze()
    (fixture/'proof.txt').write_text('changed');rejected('content mutation')
    (fixture/'proof.txt').unlink();rejected('missing file')
    (fixture/'proof.txt').write_text('proof');freeze()
    link=fixture/'link';link.symlink_to(temp);rejected('directory symlink');link.unlink()
    link.symlink_to(fixture/'proof.txt');rejected('file symlink');link.unlink()
    for bad in ('../escape','/absolute','a/../b','a//b','./a','a\\b','C:/escape','a\x00b'):
        try:safe_name(bad)
        except ValueError:pass
        else:raise RuntimeError('Unsafe path accepted')
        (fixture/'MANIFEST.json').write_text(json.dumps({'schema':1,'files':{bad:{'bytes':0,'sha256':'0'*64}}}))
        rejected('unsafe manifest path')
    (fixture/'MANIFEST.json').unlink();(fixture/'MANIFEST.json').symlink_to(root/'VERIFY_OUTPUT.txt');rejected('root manifest symlink')
    print('PASS: recursive nested-manifest, tampering, missing-file, symlink and unsafe-path attacks.')
