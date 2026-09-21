#!/usr/bin/env python3
"""Preflight tests. Runner tests use FAKE subprocesses in temporary directories.

No successful result generated here is evidence that Lean ran. The temporary
mock receipts are discarded, and only this explicitly labelled test summary is saved.
"""
from __future__ import annotations
import argparse
from contextlib import ExitStack, redirect_stdout, redirect_stderr
import hashlib
import io
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch

import preflight_checks as pc
import run_lean as runner
from check_axioms import inspect_reports
from source_audit import strip_comments

ROOT = Path(__file__).resolve().parents[1]
DECLS = [{'name': 'Bell.public', 'visibility': 'public'}]
STANDARD = "'Bell.public' depends on axioms: [propext, Classical.choice, Quot.sound]\n"

class TextTests(unittest.TestCase):
    def test_comments_and_strings(self):
        s = 'theorem x /- sorry /- axiom -/ -- hi\n-/ := "\\\"sorry"\n-- axiom\ntrue'
        clean = strip_comments(s)
        self.assertNotIn('sorry', clean); self.assertNotIn('axiom', clean)
        self.assertEqual(clean.count('\n'), s.count('\n'))
    def test_unterminated_comment(self):
        with self.assertRaises(ValueError): strip_comments('/- nested /- hi -/')
    def test_unterminated_string(self):
        with self.assertRaises(ValueError): strip_comments('"hello')
    def test_import_cycle(self):
        with self.assertRaises(AssertionError): pc.transitive_imports({'A':['B'],'B':['A']}, 'A')
    def test_import_closure(self):
        self.assertEqual(pc.transitive_imports({'A':['B'],'B':['C'],'C':[]},'A'), {'B','C'})
    def test_missing_identifier_import(self):
        texts={'A':'theorem long_project_reference : True := by trivial',
               'B':'theorem target : True := long_project_reference'}
        self.assertEqual(pc.dependency_candidates(texts, {'A':[],'B':[]})[0]['issue'], 'not_in_transitive_imports')
    def test_identifier_import_repaired(self):
        texts={'A':'theorem long_project_reference : True := by trivial',
               'B':'theorem target : True := long_project_reference'}
        self.assertEqual(pc.dependency_candidates(texts, {'A':[],'B':['A']}), [])
    def test_forward_reference(self):
        texts={'A':'def f := long_project_reference\ntheorem long_project_reference : True := by trivial'}
        self.assertEqual(pc.dependency_candidates(texts, {'A':[]})[0]['issue'], 'reference_before_declaration')
    def test_compiler_identity(self):
        runner.inspect_compiler('Lean (version 4.19.0, x86_64-unknown-linux-gnu, Release)',runner.PINNED_LEAN_COMMIT+'\n')
    def test_compiler_wrong_version(self):
        with self.assertRaises(runner.RunFailure): runner.inspect_compiler('Lean (version 4.19.01, Release)',runner.PINNED_LEAN_COMMIT)
    def test_compiler_wrong_commit(self):
        with self.assertRaises(runner.RunFailure): runner.inspect_compiler('Lean (version 4.19.0, Release)','f'*40)
    def test_invalid_proof_accepted(self):
        with self.assertRaises(runner.RunFailure): runner.require_negative_control_rejection(0,'')
    def test_invalid_proof_rejected(self):
        runner.require_negative_control_rejection(1,'x.lean:2:20: error: type mismatch\nTrue.intro has type True')
    def test_invalid_proof_crash_not_rejection(self):
        with self.assertRaises(runner.RunFailure): runner.require_negative_control_rejection(-11,'segmentation fault')
    def test_no_errors_rejects_sorry(self):
        with self.assertRaises(runner.RunFailure): runner.check_no_errors("warning: declaration uses 'sorry'",'test')
    def test_no_errors_rejects_recovered_compiler_panic(self):
        with self.assertRaises(runner.RunFailure):
            runner.check_no_errors('info: PANIC at Lean.Expr.appArg!', 'test')
    def test_config_pins_actual(self):
        self.assertEqual(len(runner.validate_pins(ROOT)),9)
    def test_baseline_receipt_records_proof_repairs(self):
        result=pc.evaluate(ROOT)
        modified=[v for v in result['module_preservation'] if not v['byte_identical']]
        # The historical compiler-free package changed only an import. Local
        # compiler repair legitimately changes proofs, and must report that.
        quantum = next(v for v in modified if v['file'] == 'Bell/Quantum.lean')
        self.assertFalse(quantum['nonimport_noncomment_text_unchanged'])
        for record in result['module_preservation']:
            current = hashlib.sha256((ROOT/record['file']).read_bytes()).hexdigest()
            self.assertEqual(record['after_sha256'], current)
            self.assertEqual(record['byte_identical'], record['before_sha256'] == current)
    def test_statement_contracts_not_executed(self):
        text=(ROOT/'validation/Statements.lean').read_text()
        self.assertIn('convexHull ℝ (Set.range',text)
        self.assertIn('ProjectiveStrategy',text)
        self.assertIn('example :',text)
        # These assertions are only source presence checks, never contract validation.

class ParserExtraTests(unittest.TestCase):
    def test_error_overrides_dependency_text(self):
        with self.assertRaises(AssertionError): inspect_reports(STANDARD+'Audit.lean:1:1: error: failed',DECLS)
    def test_prefix_spoof(self):
        with self.assertRaises(AssertionError): inspect_reports('source says '+STANDARD,DECLS)
    def test_ansi(self):
        self.assertEqual(len(inspect_reports('\x1b[32m'+STANDARD+'\x1b[0m',DECLS)),1)
    def test_duplicate_inventory(self):
        with self.assertRaises(AssertionError): inspect_reports(STANDARD,DECLS+DECLS)
    def test_kernel_bypass_dependency(self):
        with self.assertRaises(AssertionError): inspect_reports("Bell.public depends on axioms: [Lean.trustCompiler]",DECLS)
    def test_truncated_list(self):
        with self.assertRaises(AssertionError): inspect_reports("Bell.public depends on axioms: [propext",DECLS)
    def test_other_name_does_not_suffice(self):
        with self.assertRaises(AssertionError): inspect_reports("Bell.public_extra depends on axioms: []",DECLS)

class FakeProcess:
    def __init__(self,code=0,text=''):
        self.code=code; self.stdout=io.StringIO(text)
    def wait(self,timeout=None): return self.code
    def terminate(self): pass
    def kill(self): pass

class RunnerControlFlowTests(unittest.TestCase):
    """Only mocks; temporary source/log roots never enter the delivered archive."""
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory(prefix='bell-mock-run-')
        self.root=Path(self.temp.name)
        (self.root/'reports/source_completion').mkdir(parents=True)
        (self.root/'Bell').mkdir(); (self.root/'scripts').mkdir()
        (self.root/'validation').mkdir()
        for filename in runner.REQUIRED_CONTRACTS:
            (self.root/'validation'/filename).write_text('example : True := True.intro\n')
        (self.root/'reports/declarations.json').write_text(json.dumps(DECLS))
        (self.root/'reports/source_completion/source_inventory.json').write_text(json.dumps({'topological_module_order':['Bell.First','Bell.Second']}))
        for filename in ('kernel_report.json','axiom_audit.json','statement_audit.json'):
            (self.root/'reports'/filename).write_text(json.dumps({'status':'passed','run_id':'OLD_MOCK','dependency_audit_passed':True}))
        self.overrides={}; self.calls=[]; self.has_lake=True; self.pin_error=None
        self.snapshots=[{'Bell/A.lean':'mock-source-sha'}, {'Bell/A.lean':'mock-source-sha'}]
    def tearDown(self): self.temp.cleanup()
    def fake_process(self, argv, **kwargs):
        self.calls.append(argv)
        key=' '.join(argv)
        for needle,value in self.overrides.items():
            if needle in key:
                if isinstance(value,BaseException): raise value
                return FakeProcess(*value)
        if '--version' in argv: return FakeProcess(0,'Lean (version 4.19.0, Release)\n')
        if '--githash' in argv: return FakeProcess(0,runner.PINNED_LEAN_COMMIT+'\n')
        if any('SmokeInvalid.lean' in x for x in argv): return FakeProcess(1,'error: type mismatch\nTrue.intro has type True\n')
        if 'Bell/Audit.lean' in argv: return FakeProcess(0,STANDARD)
        return FakeProcess()
    def invoke(self,serial=False):
        with ExitStack() as stack:
            stack.enter_context(patch.object(runner,'validate_pins',side_effect=self.pin_error,return_value=[]))
            stack.enter_context(patch.object(runner,'source_snapshot',side_effect=self.snapshots))
            stack.enter_context(patch.object(runner.shutil,'which',return_value='/mock/lake' if self.has_lake else None))
            stack.enter_context(patch.object(runner.subprocess,'Popen',side_effect=self.fake_process))
            stack.enter_context(patch('check_axioms.REQUIRED_MAIN',{'Bell.public'}))
            stack.enter_context(redirect_stdout(io.StringIO()));stack.enter_context(redirect_stderr(io.StringIO()))
            return runner.run(argparse.Namespace(bootstrap=False,serial=serial),self.root)
    def assert_failed(self):
        kernel=json.loads((self.root/'reports/kernel_report.json').read_text())
        self.assertFalse(kernel['main_declarations_kernel_checked'])
        for n in ('axiom_audit.json','statement_audit.json'):
            report=json.loads((self.root/'reports'/n).read_text())
            self.assertNotEqual(report['status'],'passed')
            self.assertEqual(report['run_id'],kernel['run_id'])
        self.assertFalse((self.root/'reports/.lean-run.lock').exists())
        return kernel
    def test_mock_full_success(self):
        self.assertEqual(self.invoke(),0)
        report=json.loads((self.root/'reports/kernel_report.json').read_text())
        self.assertTrue(report['main_declarations_kernel_checked'])
        self.assertEqual(report['last_stage'],'complete')
        self.assertTrue(any('validation/Statements.lean' in c for c in self.calls))
        # This temporary MOCK report is deleted in tearDown; not verification evidence.
    def test_stale_success_cleared_before_pin_check(self):
        self.pin_error=runner.RunFailure('mock wrong pins')
        self.assertNotEqual(self.invoke(),0)
        report=self.assert_failed()
        self.assertEqual(report['commands'],[])
        self.assertTrue((self.root/report['logs_directory']/'previous/axiom_audit.json').is_file())
    def test_missing_lake(self):
        self.has_lake=False
        self.assertEqual(self.invoke(),127)
        self.assertFalse(self.assert_failed()['lean_build_invoked'])
    def test_wrong_lean_version(self):
        self.overrides['--version']=(0,'Lean (version 4.20.0, Release)')
        self.assertNotEqual(self.invoke(),0); self.assert_failed()
    def test_wrong_lean_commit(self):
        self.overrides['--githash']=(0,'0'*40)
        self.assertNotEqual(self.invoke(),0); self.assert_failed()
    def test_build_failure(self):
        self.overrides['lake build Bell']=(1,'mock build failed')
        self.assertNotEqual(self.invoke(),0); self.assert_failed()
    def test_serial_partial_not_full(self):
        self.overrides['lake build Bell.Second']=(1,'mock second module failed')
        self.assertNotEqual(self.invoke(serial=True),0)
        self.assertEqual(self.assert_failed()['last_stage'],'lean_build')
        self.assertFalse(any('validation/Statements.lean' in c for c in self.calls))
    def test_contract_failure(self):
        self.overrides['validation/Statements.lean']=(1,'mock type mismatch')
        self.assertNotEqual(self.invoke(),0); self.assert_failed()
    def test_expanded_contract_failure(self):
        self.overrides['validation/HilbertContracts.lean']=(1,'error: missing normalization')
        self.assertNotEqual(self.invoke(),0); self.assert_failed()
    def test_missing_bridge_contract(self):
        (self.root/'validation/StochasticContracts.lean').unlink()
        self.assertNotEqual(self.invoke(),0); self.assert_failed()
    def test_all_added_contracts_are_executed(self):
        (self.root/'validation/Additional.lean').write_text('example : True := True.intro\n')
        (self.root/'validation/nested').mkdir()
        (self.root/'validation/nested/Additional.lean').write_text('example : True := True.intro\n')
        self.assertEqual(self.invoke(),0)
        for name in runner.REQUIRED_CONTRACTS | {'Additional.lean', 'nested/Additional.lean'}:
            self.assertTrue(any('validation/'+name in c for c in self.calls))
    def test_nested_contract_failure(self):
        (self.root/'validation/nested').mkdir()
        (self.root/'validation/nested/Extra.lean').write_text('example : True := True.intro\n')
        self.overrides['validation/nested/Extra.lean']=(1,'error: nested contract failure')
        self.assertNotEqual(self.invoke(),0); self.assert_failed()
    def test_contract_error_with_zero_exit(self):
        self.overrides['validation/Statements.lean']=(0,'error: unresolved goals')
        self.assertNotEqual(self.invoke(),0); self.assert_failed()
    def test_negative_accepted(self):
        self.overrides['SmokeInvalid.lean']=(0,'')
        self.assertNotEqual(self.invoke(),0); self.assert_failed()
    def test_negative_crash(self):
        self.overrides['SmokeInvalid.lean']=(-11,'crash')
        self.assertNotEqual(self.invoke(),0); self.assert_failed()
    def test_missing_axiom_report(self):
        self.overrides['Bell/Audit.lean']=(0,'')
        self.assertNotEqual(self.invoke(),0); self.assert_failed()
    def test_unapproved_axiom(self):
        self.overrides['Bell/Audit.lean']=(0,"Bell.public depends on axioms: [sorryAx]\n")
        self.assertNotEqual(self.invoke(),0); self.assert_failed()
    def test_compiler_error_in_axiom_log(self):
        self.overrides['Bell/Audit.lean']=(0,STANDARD+'error: unresolved constant')
        self.assertNotEqual(self.invoke(),0); self.assert_failed()
    def test_sources_changed(self):
        self.snapshots[1]={'Bell/A.lean':'different'}
        self.assertNotEqual(self.invoke(),0); self.assert_failed()
    def test_interrupted(self):
        self.overrides['lake build Bell']=KeyboardInterrupt()
        self.assertEqual(self.invoke(),130); self.assert_failed()
    def test_previous_local_build_moved(self):
        old=self.root/'.lake/build/old.txt';old.parent.mkdir(parents=True);old.write_text('old local output')
        self.assertEqual(self.invoke(),0)
        self.assertFalse(old.exists())
        backups=list((self.root/'.lake/preflight-builds').rglob('old.txt'))
        self.assertEqual(len(backups),1); self.assertEqual(backups[0].read_text(),'old local output')
    def test_symlinked_build_refused(self):
        target=self.root/'external';target.mkdir()
        (self.root/'.lake').mkdir();(self.root/'.lake/build').symlink_to(target,target_is_directory=True)
        self.assertNotEqual(self.invoke(),0); self.assert_failed()
        self.assertTrue(target.is_dir())
    def test_concurrent_lock_refuses_without_overwriting_other_run(self):
        (self.root/'reports/.lean-run.lock').write_text('{"run_id":"OTHER_ACTIVE_RUN"}')
        before=(self.root/'reports/kernel_report.json').read_bytes()
        self.assertEqual(self.invoke(),2)
        self.assertEqual((self.root/'reports/kernel_report.json').read_bytes(),before)

if __name__ == '__main__':
    suite=unittest.TestSuite(unittest.defaultTestLoader.loadTestsFromTestCase(c)
                             for c in (TextTests,ParserExtraTests,RunnerControlFlowTests))
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    report={'status':'passed' if result.wasSuccessful() else 'failed','tests':result.testsRun,
            'scope':'Python static/preflight/runner tests; runner subprocess outputs are explicitly MOCKED in temporary roots.',
            'lean_invoked':False,'kernel_checked':False,
            'runner_sha256':hashlib.sha256((ROOT/'scripts/run_lean.py').read_bytes()).hexdigest(),
            'test_sha256':hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    runner.write_json(ROOT/'reports/preflight/harness_tests.json',report)
    raise SystemExit(0 if result.wasSuccessful() else 1)
