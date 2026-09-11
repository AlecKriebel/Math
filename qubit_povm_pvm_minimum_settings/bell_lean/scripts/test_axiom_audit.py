#!/usr/bin/env python3
"""Unit tests of dependency-log parsing using MOCK TEXT, not Lean output."""
from pathlib import Path
import hashlib
import json
import unittest
from check_axioms import inspect_reports

ROOT=Path(__file__).resolve().parents[1]
D=[{'name':'Bell.public','visibility':'public'},
   {'name':'Bell.helper','visibility':'private'}]

class AuditParserTests(unittest.TestCase):
    def test_standard(self):
        r=inspect_reports("'Bell.public' depends on axioms: [propext, Classical.choice, Quot.sound]",D)
        self.assertEqual(len(r),1)
    def test_no_axioms(self):
        self.assertEqual(inspect_reports("Bell.public does not depend on any axioms",D)[0]['axioms'],[])
    def test_missing(self):
        with self.assertRaises(AssertionError):inspect_reports('',D)
    def test_private_not_queried(self):
        r=inspect_reports("Bell.public does not depend on any axioms",D)
        self.assertEqual(r[0]['name'],'Bell.public')
    def test_sorry_dependency(self):
        with self.assertRaises(AssertionError):inspect_reports("Bell.public depends on axioms: [sorryAx]",D)
    def test_custom_axiom(self):
        with self.assertRaises(AssertionError):inspect_reports("Bell.public depends on axioms: [Bell.assumed_main]",D)
    def test_duplicate(self):
        with self.assertRaises(AssertionError):inspect_reports("Bell.public depends on axioms: []\nBell.public depends on axioms: []",D)
    def test_suffix_name(self):
        with self.assertRaises(AssertionError):inspect_reports("Other.Bell.public depends on axioms: []",D)
    def test_empty_inventory(self):
        with self.assertRaises(AssertionError):inspect_reports('',[])
    def test_multiline(self):
        r=inspect_reports("'Bell.public' depends on axioms:\n [propext,\n Quot.sound]",D)
        self.assertEqual(set(r[0]['axioms']),{'propext','Quot.sound'})

if __name__=='__main__':
    result=unittest.TextTestRunner(verbosity=2).run(unittest.defaultTestLoader.loadTestsFromTestCase(AuditParserTests))
    report={'status':'passed' if result.wasSuccessful() else 'failed',
      'test_count':result.testsRun,'input_kind':'mock dependency-report strings',
      'lean_ran':False,'kernel_checked':False,
      'scope':'Python parser behavior only; not an axiom audit of any real theorem',
      'parser_sha256':hashlib.sha256((ROOT/'scripts/check_axioms.py').read_bytes()).hexdigest()}
    (ROOT/'reports/source_completion/axiom_parser_tests.json').write_text(json.dumps(report,indent=2)+'\n')
    raise SystemExit(0 if result.wasSuccessful() else 1)
