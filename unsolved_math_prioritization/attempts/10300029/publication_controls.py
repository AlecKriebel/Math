"""Adversarial publication-integrity tests. Authenticate this file before execution."""
import sys
if not (sys.flags.isolated and sys.flags.no_site and sys.dont_write_bytecode):
    raise SystemExit('REFUSED: Python -I -S -B required')
import hashlib
import json
import os
from pathlib import Path
import shutil
import subprocess
import tempfile


def need(ok, why):
    if not ok:
        raise ValueError(why)


def sha(b):
    return hashlib.sha256(b).hexdigest()


need(len(sys.argv) == 4, 'usage: publication_controls.py ROOT MANIFEST_SHA256 BOOTSTRAP_SHA256')
ROOT = Path(sys.argv[1]); PIN = sys.argv[2]; BOOTPIN = sys.argv[3]
RAW = (ROOT/'publication_bootstrap.py').read_bytes()
need(sha(RAW) == BOOTPIN, 'external bootstrap authentication failed')


def api(root):
    d = {'__name__': 'authenticated_publication_test', '__file__': str(root/'publication_bootstrap.py')}
    exec(compile(RAW, d['__file__'], 'exec'), d)
    return d


original = api(ROOT)
original['verify'](ROOT, PIN)
checks = []
with tempfile.TemporaryDirectory(prefix='finite-radius-publication-controls-') as td:
    td = Path(td)
    clean = td/'clean'; shutil.copytree(ROOT, clean)
    for flags, mode in [([], 'normal'), (['-O'], 'optimized')]:
        for location, root in [('original', ROOT), ('relocated', clean)]:
            code = 'import sys;sys.argv=sys.argv[1:];__file__=sys.argv[0];exec(compile('+repr(RAW)+',__file__,"exec"))'
            p = subprocess.run([sys.executable,'-I','-S','-B',*flags,'-c',code,str(root/'publication_bootstrap.py'),str(root),PIN],capture_output=True,cwd=td)
            need(p.returncode == 0 and json.loads(p.stdout)['verdict'] == 'PASS', 'positive '+location)
            checks.append({'case': location, 'mode': mode, 'result': 'pass'})
    for flags, label in [(['-I','-B'],'missing_no_site'),(['-S','-B'],'missing_isolation'),(['-I','-S'],'missing_no_bytecode')]:
        p = subprocess.run([sys.executable,*flags,str(clean/'publication_bootstrap.py'),str(clean),PIN],capture_output=True,cwd=td)
        need(p.returncode != 0 and b'REFUSED' in p.stderr, 'isolation guard')
        checks.append({'case': label, 'result': 'rejected'})
    cases = ['extra_file','extra_directory','missing_file','changed_proof_same_size','changed_bootstrap',
             'changed_author_zip_same_size','changed_audit_zip_same_size','changed_author_receipt',
             'changed_audit_receipt','changed_external_manifest','changed_audit_code','rehashed_manifest',
             'symlink_file','symlink_directory','symlink_root','symlink_ancestor','oversized_file',
             'wrong_manifest_pin','relative_root','wrong_entrypoint']
    targets = {'changed_proof_same_size':'author/RESULT.md','changed_bootstrap':'publication_bootstrap.py',
               'changed_author_zip_same_size':'leaf_space_10300029_frozen_v1.zip',
               'changed_audit_zip_same_size':'LEAF_SPACE_10300029_INDEPENDENT_AUDIT_SAFE.zip',
               'changed_author_receipt':'FREEZE_RECEIPT.json',
               'changed_audit_receipt':'LEAF_SPACE_10300029_INDEPENDENT_AUDIT_RECEIPT.json',
               'changed_external_manifest':'LEAF_SPACE_10300029_INDEPENDENT_AUDIT_EXTERNAL_MANIFEST.json',
               'changed_audit_code':'audit/VERIFY_AUTHOR.py'}
    for label in cases:
        root = td/label; shutil.copytree(ROOT, root); pin = PIN
        if label in targets:
            p = root/targets[label]; b = p.read_bytes(); p.write_bytes(b'!'+b[1:])
        elif label == 'extra_file': (root/'unexpected.py').write_text('raise RuntimeError("DO_NOT_EXECUTE")')
        elif label == 'extra_directory': (root/'unexpected').mkdir()
        elif label == 'missing_file': (root/'author/RESULT.md').unlink()
        elif label == 'rehashed_manifest':
            p = root/'author/RESULT.md'; p.write_bytes(p.read_bytes()+b'\n')
            m = json.loads((root/'PUBLICATION_MANIFEST.json').read_bytes())
            m['files']['author/RESULT.md'] = {'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())}
            (root/'PUBLICATION_MANIFEST.json').write_text(json.dumps(m))
        elif label == 'symlink_file':
            p = root/'author/RESULT.md'; p.unlink(); p.symlink_to(ROOT/'author/RESULT.md')
        elif label == 'symlink_directory':
            shutil.rmtree(root/'author'); (root/'author').symlink_to(ROOT/'author',target_is_directory=True)
        elif label == 'symlink_root':
            link = td/'root-link'; link.symlink_to(root,target_is_directory=True); root = link
        elif label == 'symlink_ancestor':
            link = td/'ancestor-link'; link.symlink_to(td,target_is_directory=True); root = link/label
        elif label == 'oversized_file': (root/'author/RESULT.md').write_bytes(b'x'*2000001)
        elif label == 'wrong_manifest_pin': pin = '0'*64
        elif label == 'relative_root': root = Path('.')
        d = api(root)
        if label == 'wrong_entrypoint': d['__file__'] = str(root/'other.py')
        try:
            d['verify'](root, pin)
        except Exception:
            checks.append({'case':label,'result':'rejected'})
        else:
            raise ValueError('accepted mutation '+label)
    for label, raw in [('duplicate_json_key',b'{"a":1,"a":2}'),('nonfinite_json',b'{"a":NaN}')]:
        try: original['parse'](raw)
        except Exception: checks.append({'case':label,'result':'rejected'})
        else: raise ValueError('accepted '+label)
    # Treat a forged manifest with a new external pin as untrusted: immutable archive pins still reject it.
    root = td/'forged'; shutil.copytree(ROOT,root)
    p = root/'leaf_space_10300029_frozen_v1.zip';p.write_bytes(b'!'+p.read_bytes()[1:])
    m = json.loads((root/'PUBLICATION_MANIFEST.json').read_bytes())
    m['files'][p.name]={'bytes':p.stat().st_size,'sha256':sha(p.read_bytes())}
    (root/'PUBLICATION_MANIFEST.json').write_text(json.dumps(m))
    try: api(root)['verify'](root,sha((root/'PUBLICATION_MANIFEST.json').read_bytes()))
    except Exception: checks.append({'case':'forged_manifest_and_external_pin','result':'rejected'})
    else: raise ValueError('immutable archive pin missing')
need(original['verify'](ROOT,PIN)[2]['verdict']=='PASS','source changed')
print(json.dumps({'verdict':'PASS','harness_optimized':not __debug__,
                  'positive_runs':sum(c['result']=='pass' for c in checks),
                  'negative_runs':sum(c['result']=='rejected' for c in checks),
                  'checks':checks,'scope':'Integrity only; no mathematical execution'},indent=2,sort_keys=True))
