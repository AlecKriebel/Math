#!/usr/bin/env python3
"""Test transfer integrity/safety and workflow embedding; NEVER mock a Lean proof pass."""
from __future__ import annotations
from contextlib import redirect_stdout
import copy
import hashlib
import importlib.util
import io
import json
import os
from pathlib import Path
import py_compile
import subprocess
import sys
import tarfile
import tempfile
import unittest
import zipfile

HERE=Path(__file__).resolve().parent
spec=importlib.util.spec_from_file_location('restore', HERE/'restore_environment.py')
restore=importlib.util.module_from_spec(spec)
spec.loader.exec_module(restore)


def fixture(directory: Path, special=None):
    archive=directory/'fixture.tar.gz'
    content=b'integrity test only; not a compiler or a proof\n'
    with tarfile.open(archive, 'w:gz') as t:
        root=tarfile.TarInfo(restore.BUNDLE_NAME)
        root.type=tarfile.DIRTYPE; root.mode=0o755; t.addfile(root)
        f=tarfile.TarInfo(restore.BUNDLE_NAME+'/README.txt')
        f.size=len(content); f.mode=0o640; t.addfile(f,io.BytesIO(content))
        if special is not None:
            t.addfile(special)
    data=archive.read_bytes()
    parts=[]
    size=max(1,(len(data)+2)//3)
    for i,start in enumerate(range(0,len(data),size)):
        value=data[start:start+size]
        name=f'{restore.PART_PREFIX}{i:02d}'
        (directory/name).write_bytes(value)
        parts.append({'index':i,'name':name,'bytes':len(value),
                      'sha256':hashlib.sha256(value).hexdigest()})
    m={'schema':'bell-lean-offline/v1','toolchain':restore.TOOLCHAIN,
       'lean_git_hash':restore.LEAN_HASH,'platform':'linux-x86_64',
       'payload_root':restore.BUNDLE_NAME,'parts':parts,
       'archive_bytes':len(data),'archive_sha256':hashlib.sha256(data).hexdigest(),
       'unpacked_regular_bytes':len(content),
       'paper_kernel_checked':False,'full_paper_proved':False}
    (directory/'environment-manifest.json').write_text(json.dumps(m))
    archive.unlink()
    return m,content


class HandoffTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.d=Path(self.tmp.name)
    def tearDown(self): self.tmp.cleanup()
    def test_raw_roundtrip_and_modes(self):
        m,c=fixture(self.d)
        restore.validate_manifest(m)
        combined=self.d/'combined.tar.gz'
        restore.combine(self.d,m,combined)
        root=restore.extract(combined,self.d/'extracted',m['unpacked_regular_bytes'])
        self.assertEqual((root/'README.txt').read_bytes(),c)
        self.assertEqual((root/'README.txt').stat().st_mode & 0o777,0o640)
    def test_artifact_zip_roundtrip(self):
        m,c=fixture(self.d)
        for i,name in enumerate(['environment-manifest.json']+[p['name'] for p in m['parts']]):
            p=self.d/name
            with zipfile.ZipFile(self.d/f'artifact_{i}.zip','w') as z: z.write(p,'nested/'+name)
            p.unlink()
        actual=restore.load_manifest(self.d,None)
        self.assertEqual(actual,m)
        combined=self.d/'combined.tar.gz'
        restore.combine(self.d,m,combined)
        root=restore.extract(combined,self.d/'extracted',m['unpacked_regular_bytes'])
        self.assertEqual((root/'README.txt').read_bytes(),c)
    def test_corrupt_part_rejected(self):
        m,_=fixture(self.d); p=self.d/m['parts'][0]['name']
        b=p.read_bytes(); p.write_bytes(bytes([b[0]^1])+b[1:])
        with self.assertRaises(ValueError): restore.combine(self.d,m,self.d/'combined.tar.gz')
    def test_missing_part_rejected(self):
        m,_=fixture(self.d); (self.d/m['parts'][-1]['name']).unlink()
        with self.assertRaises(ValueError): restore.combine(self.d,m,self.d/'combined.tar.gz')
    def test_duplicate_part_rejected(self):
        m,_=fixture(self.d); p=self.d/m['parts'][0]['name']
        with zipfile.ZipFile(self.d/'duplicate.zip','w') as z:z.write(p,p.name)
        with self.assertRaises(ValueError): restore.combine(self.d,m,self.d/'combined.tar.gz')
    def test_part_order_rejected(self):
        m,_=fixture(self.d); m['parts'].reverse()
        with self.assertRaises(ValueError): restore.validate_manifest(m)
    def test_oversized_part_rejected(self):
        m,_=fixture(self.d); m['parts'][0]['bytes']=restore.MAX_PART_BYTES+1
        with self.assertRaises(ValueError): restore.validate_manifest(m)
    def test_false_proof_label_rejected(self):
        m,_=fixture(self.d); m['paper_kernel_checked']=True
        with self.assertRaises(ValueError): restore.validate_manifest(m)
    def test_wrong_toolchain_rejected(self):
        m,_=fixture(self.d); m['lean_git_hash']='0'*40
        with self.assertRaises(ValueError): restore.validate_manifest(m)
    def test_wrong_whole_hash_rejected(self):
        m,_=fixture(self.d); m['archive_sha256']='0'*64
        with self.assertRaises(ValueError): restore.combine(self.d,m,self.d/'combined.tar.gz')
    def test_conflicting_manifests_rejected(self):
        m,_=fixture(self.d); other=copy.deepcopy(m); other['archive_sha256']='0'*64
        with zipfile.ZipFile(self.d/'conflict.zip','w') as z:z.writestr('environment-manifest.json',json.dumps(other))
        with self.assertRaises(ValueError): restore.load_manifest(self.d,None)
    def test_traversal_rejected(self):
        bad=tarfile.TarInfo(restore.BUNDLE_NAME+'/../../outside')
        bad.size=0
        m,_=fixture(self.d,bad); combined=self.d/'combined.tar.gz'; restore.combine(self.d,m,combined)
        with self.assertRaises(ValueError):restore.extract(combined,self.d/'extracted',m['unpacked_regular_bytes'])
        self.assertFalse((self.d/'outside').exists())
    def test_external_symlink_rejected(self):
        bad=tarfile.TarInfo(restore.BUNDLE_NAME+'/escape')
        bad.type=tarfile.SYMTYPE;bad.linkname='../../outside'
        m,_=fixture(self.d,bad); combined=self.d/'combined.tar.gz'; restore.combine(self.d,m,combined)
        with self.assertRaises(ValueError):restore.extract(combined,self.d/'extracted',m['unpacked_regular_bytes'])
    def test_internal_symlink_preserved(self):
        link=tarfile.TarInfo(restore.BUNDLE_NAME+'/readme-link')
        link.type=tarfile.SYMTYPE;link.linkname='README.txt'
        m,c=fixture(self.d,link); combined=self.d/'combined.tar.gz'; restore.combine(self.d,m,combined)
        root=restore.extract(combined,self.d/'extracted',m['unpacked_regular_bytes'])
        self.assertTrue((root/'readme-link').is_symlink())
        self.assertEqual((root/'readme-link').read_bytes(),c)
    def test_internal_hardlink_preserved(self):
        link=tarfile.TarInfo(restore.BUNDLE_NAME+'/readme-hardlink')
        link.type=tarfile.LNKTYPE;link.linkname=restore.BUNDLE_NAME+'/README.txt'
        m,c=fixture(self.d,link); combined=self.d/'combined.tar.gz'; restore.combine(self.d,m,combined)
        root=restore.extract(combined,self.d/'extracted',m['unpacked_regular_bytes'])
        self.assertEqual((root/'readme-hardlink').read_bytes(),c)
        self.assertEqual((root/'readme-hardlink').stat().st_ino,(root/'README.txt').stat().st_ino)
    def test_special_device_rejected(self):
        bad=tarfile.TarInfo(restore.BUNDLE_NAME+'/fifo');bad.type=tarfile.FIFOTYPE
        m,_=fixture(self.d,bad); combined=self.d/'combined.tar.gz'; restore.combine(self.d,m,combined)
        with self.assertRaises(ValueError):restore.extract(combined,self.d/'extracted',m['unpacked_regular_bytes'])
    def test_extracted_size_mismatch_rejected(self):
        m,_=fixture(self.d); combined=self.d/'combined.tar.gz'; restore.combine(self.d,m,combined)
        with self.assertRaises(ValueError):restore.extract(combined,self.d/'extracted',m['unpacked_regular_bytes']-1)
    def test_cli_extract_only_no_proof_claim(self):
        fixture(self.d)
        result=subprocess.run([sys.executable,str(HERE/'restore_environment.py'),
            '--parts',str(self.d),'--output',str(self.d/'out'),'--extract-only'],capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)
        r=json.loads((self.d/'out/restore-status.json').read_text())
        self.assertEqual(r['status'],'bytes_restored_not_compiler_checked')
        self.assertFalse(r['paper_kernel_checked'])
    def test_existing_output_untouched(self):
        fixture(self.d); out=self.d/'out';out.mkdir();(out/'keep').write_text('untouched')
        result=subprocess.run([sys.executable,str(HERE/'restore_environment.py'),
            '--parts',str(self.d),'--output',str(out),'--extract-only'],capture_output=True,text=True)
        self.assertNotEqual(result.returncode,0)
        self.assertEqual((out/'keep').read_text(),'untouched')
    def test_scripts_compile(self):
        for p in HERE.glob('*.py'):py_compile.compile(str(p),doraise=True)
    def test_workflow_embeds_exact_scripts_and_pins(self):
        import yaml
        value=yaml.load((HERE/'bell-lean-offline.yml').read_text(),Loader=yaml.BaseLoader)
        self.assertEqual(value['permissions'],{'contents':'read'})
        self.assertIn('workflow_dispatch',value['on'])
        self.assertEqual(value['jobs']['export']['runs-on'],'ubuntu-22.04')
        steps=value['jobs']['export']['steps']; code=steps[0]['run']
        syntax=subprocess.run(['bash','-n'],input=code,text=True,capture_output=True)
        self.assertEqual(syntax.returncode,0,syntax.stderr)
        result=subprocess.run(['bash','-c',code],cwd=self.d,capture_output=True,text=True)
        self.assertEqual(result.returncode,0,result.stderr)
        for name in ('export_environment.py','restore_environment.py','pins.json'):
            self.assertEqual((self.d/name).read_bytes(),(HERE/name).read_bytes())
        uploads=[s for s in steps if 'uses' in s]
        self.assertEqual(len(uploads),14)
        part_names=[s['with']['name'] for s in uploads if s['with']['name'].startswith('bell-lean419-part')]
        self.assertEqual(part_names,[f'bell-lean419-part{i:02d}' for i in range(12)])
        for s in steps:
            if 'run' in s:
                cmd=s['run'].replace('${{ github.run_id }}','123').replace('${{ github.run_attempt }}','1')
                syntax=subprocess.run(['bash','-n'],input=cmd,text=True,capture_output=True)
                self.assertEqual(syntax.returncode,0,syntax.stderr)

if __name__=='__main__':
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(HandoffTests)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    report={'tests_run':result.testsRun,'failures':len(result.failures),'errors':len(result.errors),
            'passed':result.wasSuccessful(),
            'scope':'Transport integrity/safety, script syntax, exact workflow embedding only.',
            'lean_compiler_executed':False,'workflow_executed_on_github':False,
            'full_paper_proved':False}
    (HERE/'handoff_tests.json').write_text(json.dumps(report,indent=2)+'\n')
    raise SystemExit(0 if result.wasSuccessful() else 1)
