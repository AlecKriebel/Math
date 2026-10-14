#!/usr/bin/env python3
"""Read-only, relocatable verification of the KOU-21.6 draft package."""
from pathlib import Path
import hashlib
import json
import os
import subprocess
import sys
import tempfile
import zipfile

ROOT = Path(__file__).resolve().parent

def require(value, message):
    if not value:
        raise RuntimeError(message)

def digest(data):
    return hashlib.sha256(data).hexdigest()

def inventory():
    require(not any(p.is_symlink() for p in ROOT.rglob('*')), 'unexpected symbolic link')
    return {p.relative_to(ROOT).as_posix() for p in ROOT.rglob('*') if p.is_file()}

def check_package_manifest():
    manifest = json.loads((ROOT/'PUBLICATION_MANIFEST.json').read_text())
    expected = {r['path'] for r in manifest['files']}
    require(inventory() == expected | {'PUBLICATION_MANIFEST.json'}, 'recursive inventory differs from manifest')
    for row in manifest['files']:
        path = Path(row['path'])
        require(not path.is_absolute() and '..' not in path.parts, 'unsafe manifest path')
        data = (ROOT/path).read_bytes()
        require(len(data) == row['bytes'] and digest(data) == row['sha256'], 'file mismatch: '+row['path'])
    return len(expected) + 1

def check_archive(name, receipt_name, extracted, expected_count):
    archive = ROOT/'archives'/name
    receipt = json.loads((ROOT/'archives'/receipt_name).read_text())
    data = archive.read_bytes()
    require(len(data) == receipt['bytes'] and digest(data) == receipt['sha256'], 'original ZIP differs: '+name)
    folder = ROOT/extracted
    names = {p.name for p in folder.iterdir() if p.is_file()}
    with zipfile.ZipFile(archive) as z:
        require(z.testzip() is None, 'ZIP CRC failure: '+name)
        require(len(z.namelist()) == expected_count and set(z.namelist()) == names, 'ZIP inventory mismatch: '+name)
        for member in z.namelist():
            require(Path(member).name == member and member not in {'.','..'}, 'unsafe ZIP member')
            require(z.read(member) == (folder/member).read_bytes(), 'ZIP member differs: '+member)
    return expected_count

def main():
    files = check_package_manifest()
    author = check_archive('KOUROVKA_2515_AUTHOR_SAFE_FREEZE.zip','KOUROVKA_2515_AUTHOR_FREEZE_RECEIPT.json','author',10)
    audit = check_archive('KOUROVKA_2515_INDEPENDENT_AUDIT.zip','KOUROVKA_2515_INDEPENDENT_AUDIT_RECEIPT.json','audit',9)
    commands = [
      [str(ROOT/'author/verify_manifest.py')],
      [str(ROOT/'author/verify_math.py'),'--check'],
      [str(ROOT/'audit/verify_audit_manifest.py')],
      [str(ROOT/'audit/independent_verify.py'),'--check','--author-dir',str(ROOT/'author')],
    ]
    runs = []
    # Deliberately use an unrelated empty working directory, even when called
    # from this package. PYTHONDONTWRITEBYTECODE protects the immutable payload.
    with tempfile.TemporaryDirectory(prefix='kourovka-2515-cwd-') as tmp:
        env = dict(os.environ, PYTHONDONTWRITEBYTECODE='1')
        for args in commands:
            run = subprocess.run([sys.executable]+args,cwd=tmp,env=env,text=True,capture_output=True)
            require(run.returncode == 0, 'verification failed: '+args[0]+'\n'+run.stdout+'\n'+run.stderr)
            result = json.loads(run.stdout)
            require(result.get('status') == 'PASS', 'verifier did not report PASS')
            runs.append({'script':Path(args[0]).relative_to(ROOT).as_posix(),'status':'PASS'})
    require(check_package_manifest() == files, 'verification changed payload')
    print(json.dumps({'status':'PASS','publication_files':files,'frozen_author_members':author,
                     'frozen_audit_members':audit,'both_original_ZIPs_preserved':True,
                     'recursive_inventory_exact':True,'unrelated_cwd_replay':True,'checks':runs,
                     'infinite_proof':'Deductively audited; not certified by finite enumeration.'},indent=2,sort_keys=True))

if __name__ == '__main__':
    main()
