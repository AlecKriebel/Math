#!/usr/bin/env python3
"""Executable mathematical corruptions and fail-closed inventory controls."""
import copy, json, pathlib, shutil, subprocess, sys, tempfile
sys.dont_write_bytecode=True
from verify_package import require, verify_inventory, verify_equivalence
ROOT=pathlib.Path(__file__).resolve().parent

def failed_script(root, name, optimize):
    run=subprocess.run([sys.executable]+(['-O'] if optimize else [])+[str(root/name)],capture_output=True,timeout=120)
    require(run.returncode!=0,'mutation unexpectedly accepted: '+name)
    require(b'AssertionError' in run.stderr or b'FileNotFoundError' in run.stderr,'unrelated failure')

certificate=json.loads((ROOT/'certificate_N144.json').read_text())
triple=next(k for k,w in certificate['witnesses'].items() if w['kind']=='triple')
midpoint=next(k for k,w in certificate['witnesses'].items() if w['kind']=='midpoint')
def corrupt(c,kind):
    if kind=='ambient': c['N']=145
    elif kind=='duplicate_mark': c['A'][0]=c['A'][1]
    elif kind=='pair_sum': c['pair_sums'][0]+=1
    elif kind=='missing_blocker': del c['witnesses'][triple]
    elif kind=='triple_equation': c['witnesses'][triple]['c']=c['witnesses'][triple]['a']
    elif kind=='midpoint_equation': c['witnesses'][midpoint]['b']=c['witnesses'][midpoint]['a']
    elif kind=='unknown_kind': c['witnesses'][triple]['kind']='unsupported'

for optimize in (False,True):
    for kind in ('ambient','duplicate_mark','pair_sum','missing_blocker','triple_equation','midpoint_equation','unknown_kind','missing_certificate','missing_author_results','finite_value'):
        with tempfile.TemporaryDirectory() as td:
            p=pathlib.Path(td)/'packet';shutil.copytree(ROOT,p)
            c=copy.deepcopy(certificate)
            if kind=='missing_certificate': (p/'certificate_N144.json').unlink()
            elif kind=='missing_author_results': (p/'checks_results.json').unlink()
            elif kind=='finite_value':
                r=json.loads((p/'checks_results.json').read_text());r['exact_finite_values'][0]['g_N']=999
                (p/'checks_results.json').write_text(json.dumps(r))
            else:
                corrupt(c,kind);(p/'certificate_N144.json').write_text(json.dumps(c))
            failed_script(p,'independent_audit.py',optimize)
    # Mathematical algorithm corruption, not a mere metadata mutation.
    with tempfile.TemporaryDirectory() as td:
        p=pathlib.Path(td)/'packet';shutil.copytree(ROOT,p)
        script=p/'checks.py';s=script.read_text()
        require('a < b and (a + b) % 2 == 0' in s,'mutation anchor missing')
        script.write_text(s.replace('a < b and (a + b) % 2 == 0','False',1))
        failed_script(p,'checks.py',optimize)
print('PASS: 22 direct mathematical/missing-input rejection executions, normal and -O')

for kind in ('extra_root','extra_nested','nested_manifest','file_symlink','directory_symlink','missing','changed','empty_directory','unsafe_path','duplicate_key'):
    with tempfile.TemporaryDirectory() as td:
        p=pathlib.Path(td)/'packet';shutil.copytree(ROOT,p)
        if kind=='extra_root': (p/'extra.txt').write_text('x')
        elif kind=='extra_nested': (p/'original'/'extra.txt').write_text('x')
        elif kind=='nested_manifest': (p/'original'/'MANIFEST.json').write_text('{}')
        elif kind=='file_symlink': (p/'linked').symlink_to(p/'checks.py')
        elif kind=='directory_symlink': (p/'linked').symlink_to(p/'original',target_is_directory=True)
        elif kind=='missing': (p/'checks.py').unlink()
        elif kind=='changed': (p/'checks.py').write_text('bad')
        elif kind=='empty_directory': (p/'empty').mkdir()
        elif kind=='unsafe_path':
            m=json.loads((p/'MANIFEST.json').read_text());m['files']['../outside']={'sha256':'0'*64,'bytes':0};(p/'MANIFEST.json').write_text(json.dumps(m))
        elif kind=='duplicate_key':
            m=p/'MANIFEST.json';m.write_text(m.read_text().replace('"schema": 1','"schema": 1, "schema": 1'))
        try: verify_inventory(p)
        except (ValueError,FileNotFoundError): pass
        else: raise ValueError('inventory mutation accepted: '+kind)
print('PASS: 10 recursive inventory controls')
# AST equivalence is checked independently of manifest hashes.
with tempfile.TemporaryDirectory() as td:
    p=pathlib.Path(td)/'packet';shutil.copytree(ROOT,p)
    s=p/'checks.py';s.write_text(s.read_text().replace('range(1, 17)','range(1, 16)',1))
    try: verify_equivalence(p)
    except ValueError: pass
    else: raise ValueError('AST domain mutation accepted')
print('PASS: mathematical enumeration-domain AST mutation rejected')
