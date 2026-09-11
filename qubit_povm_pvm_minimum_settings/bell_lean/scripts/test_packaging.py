#!/usr/bin/env python3
"""Real temporary-file tests of source packaging; no Lean process is run."""
from pathlib import Path
import json
import tempfile
import unittest
import zipfile
import package as pkg
from run_lean import write_json
from verify_files import verify

ROOT = Path(__file__).resolve().parents[1]

class PackageTests(unittest.TestCase):
    def setUp(self):
        self.t=tempfile.TemporaryDirectory(prefix='bell-package-test-')
        self.base=Path(self.t.name);self.root=self.base/'root';self.root.mkdir();self.dest=self.base/'source.zip'
        (self.root/'Bell.lean').write_bytes(b'import Mathlib\r\n')
    def tearDown(self):self.t.cleanup()
    def build(self):return pkg.make_package(self.root,self.dest)
    def test_roundtrip_bytes(self):
        self.build()
        with zipfile.ZipFile(self.dest) as z:self.assertEqual(z.read('bell_lean/Bell.lean'),b'import Mathlib\r\n')
    def test_historical_manifest_preserved(self):
        p=self.root/'preservation/SHA256SUMS.txt';p.parent.mkdir();p.write_text('historical bytes\n')
        self.build()
        with zipfile.ZipFile(self.dest) as z:self.assertEqual(z.read('bell_lean/preservation/SHA256SUMS.txt'),b'historical bytes\n')
    def test_font_excluded(self):
        (self.root/'never-share.ttf').write_bytes(b'not an actual font')
        self.build()
        with zipfile.ZipFile(self.dest) as z:self.assertFalse(any(n.endswith('.ttf') for n in z.namelist()))
    def test_cache_excluded(self):
        p=self.root/'.lake/something.olean';p.parent.mkdir();p.write_bytes(b'cache')
        (self.root/'something.olean').write_bytes(b'output')
        self.build()
        with zipfile.ZipFile(self.dest) as z:self.assertFalse(any('.lake' in n or n.endswith('.olean') for n in z.namelist()))
    def test_symlink_rejected(self):
        (self.root/'link').symlink_to(self.root/'Bell.lean')
        with self.assertRaises(ValueError):self.build()
    def test_credential_rejected(self):
        (self.root/'.env').write_text('FAKE_KEY=not-a-secret')
        with self.assertRaises(ValueError):self.build()
    def test_active_run_rejected(self):
        (self.root/'.lean-run.lock').write_text('test lock')
        with self.assertRaises(ValueError):self.build()
    def test_inside_output_rejected(self):
        with self.assertRaises(ValueError):pkg.make_package(self.root,self.root/'x.zip')
    def test_duplicate_manifest(self):
        line='0'*64+'  x\n'
        with self.assertRaises(ValueError):pkg.parse_manifest(line+line)
    def test_traversal_manifest(self):
        with self.assertRaises(ValueError):pkg.parse_manifest('0'*64+'  ../x\n')
    def test_newline_filename(self):
        (self.root/'bad\nname').write_text('bad name')
        with self.assertRaises(ValueError):self.build()
    def test_executable_mode(self):
        p=self.root/'run.sh';p.write_text('#!/bin/sh\n');p.chmod(0o755);self.build()
        with zipfile.ZipFile(self.dest) as z:self.assertEqual((z.getinfo('bell_lean/run.sh').external_attr>>16)&0o777,0o755)
    def test_reproducible(self):
        self.build();data=self.dest.read_bytes();self.build();self.assertEqual(self.dest.read_bytes(),data)
    def test_extracted_verifier(self):
        self.build();self.assertEqual(verify(self.root),1)
    def test_modified_file_fails(self):
        self.build();(self.root/'Bell.lean').write_text('changed')
        with self.assertRaises(ValueError):verify(self.root)
    def test_corrupted_member_fails(self):
        self.build();broken=self.base/'broken.zip'
        with zipfile.ZipFile(self.dest) as a,zipfile.ZipFile(broken,'w') as b:
            for n in a.namelist():b.writestr(n,b'changed' if n.endswith('Bell.lean') else a.read(n))
        with self.assertRaises(ValueError):pkg.verify_zip(broken)
    def test_extra_member_fails(self):
        self.build()
        with zipfile.ZipFile(self.dest,'a') as z:z.writestr('bell_lean/extra','x')
        with self.assertRaises(ValueError):pkg.verify_zip(self.dest)

if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(PackageTests))
    write_json(ROOT/'reports/preflight/package_tests.json',{'status':'passed' if result.wasSuccessful() else 'failed',
               'tests':result.testsRun,'lean_invoked':False,'kernel_checked':False,'scope':'Temporary-file byte integrity, archive safety, and preservation tests.'})
    raise SystemExit(0 if result.wasSuccessful() else 1)
