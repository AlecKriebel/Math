"""Adversarial checks use disposable copies; no sockets are created."""
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import sys
import tempfile

ROOT = Path(__file__).resolve().parent

def rehash(root, name):
    m = json.loads((root / 'MANIFEST.json').read_text())
    b = (root / name).read_bytes()
    m['files'][name] = {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}
    (root / 'MANIFEST.json').write_text(json.dumps(m, indent=2, sort_keys=True) + '\n')

def run(root, optimized, script='validate.py'):
    return subprocess.run([sys.executable, '-I', '-B'] + (['-O'] if optimized else []) + [str(root / script)], cwd=root, capture_output=True, timeout=60)

def main():
    records=[]
    for optimized in [False, True]:
        for kind in ['baseline','missing','extra_file','extra_directory','symlink','manifest_symlink','proof_tamper','manifest_wrong_size','manifest_wrong_hash','checker_rehashed','result_rehashed','stdout_rehashed','deletion_predicate','merge_operator','finite_exception']:
            with tempfile.TemporaryDirectory() as t:
                p=Path(t)/'bundle'; shutil.copytree(ROOT,p)
                script='validate.py'
                if kind=='missing': (p/'ACCEPTANCE_REPORT.md').unlink()
                if kind=='extra_file': (p/'unexpected.txt').write_text('unexpected')
                if kind=='extra_directory': (p/'unexpected').mkdir()
                if kind=='symlink': (p/'unexpected_link').symlink_to('README.md')
                if kind=='proof_tamper': (p/'MATHEMATICAL_AUDIT.md').write_text('tampered proof')
                if kind.startswith('manifest_wrong_'):
                    m=json.loads((p/'MANIFEST.json').read_text()); key='bytes' if kind.endswith('size') else 'sha256'
                    m['files']['README.md'][key]=0 if key=='bytes' else '0'*64
                    (p/'MANIFEST.json').write_text(json.dumps(m))
                if kind=='checker_rehashed':
                    q=p/'regression.py'; q.write_text(q.read_text().replace('u = a | b','u = a & b')); rehash(p,q.name)
                if kind in ['result_rehashed','stdout_rehashed']:
                    name='REGRESSION_RESULTS.json' if kind=='result_rehashed' else 'REPLAY_NORMAL.stdout'
                    q=p/name; q.write_bytes(q.read_bytes().replace(b'64594',b'64593')); rehash(p,name)
                if kind in ['deletion_predicate','merge_operator','finite_exception']:
                    changes={'deletion_predicate':('len(c - d) == 1','len(c - d) == 2'),'merge_operator':('u = a | b','u = a & b'),'finite_exception':('c == {full}','c == set()')}
                    old,new=changes[kind]; q=p/'regression.py'; data=q.read_text()
                    if old not in data: raise RuntimeError('Mutation target missing')
                    q.write_text(data.replace(old,new)); script='regression.py'
                if kind == 'manifest_symlink':
                    (p/'MANIFEST.json').unlink()
                    target = Path(t)/'harmless_manifest_target.json'
                    target.write_text('{"harmless": true}\n')
                    (p/'MANIFEST.json').symlink_to(target)
                    r=subprocess.run([sys.executable, '-I', '-B'] + (['-O'] if optimized else []) + [str(ROOT/'manifest_symlink_probe.py'), str(p)], capture_output=True, timeout=60)
                    if r.returncode or r.stderr or json.loads(r.stdout) != {'manifest_reads': 0, 'rejected_before_read': True}:
                        raise RuntimeError('Manifest symlink probe failed: '+r.stderr.decode())
                    records.append({'case':kind,'optimized':optimized,'returncode':r.returncode,'expected':'reject before content read','matched':True,'manifest_reads':0})
                    continue
                r=run(p,optimized,script)
                rejected = r.returncode != 0
                if rejected != (kind!='baseline'):
                    raise RuntimeError('Unexpected mutation outcome: '+kind)
                if script=='regression.py' and b'AssertionError: regression check' not in r.stderr:
                    raise RuntimeError('Semantic mutation did not hit explicit check')
                records.append({'case':kind,'optimized':optimized,'returncode':r.returncode,'expected':'accept' if kind=='baseline' else 'reject','matched':True,'explicit_runtime_check':script=='regression.py'})
    print(json.dumps({'tests':records,'passed':len(records),'failed':0,'actual_sockets_created':0},indent=2,sort_keys=True))

if __name__=='__main__': main()
