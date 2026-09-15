#!/usr/bin/env python3
"""Tests of the reporting/scanning machinery; NOT Lean proof tests."""
import unittest
import tempfile
import shutil
from pathlib import Path
from source_inventory import inventory, check_delimiters, generate
from static_audit import ROOT
from check import parse_axioms, Runner, validate_negative_diagnostics
from unittest.mock import patch
import subprocess
from static_audit import strip_comments_strings, BANNED, audit, validation_registry

class MachineryTests(unittest.TestCase):
    def test_generated_queries_import_every_source_module(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            (root/'CyclicBell'/'Extra').mkdir(parents=True)
            (root/'reference').mkdir()
            (root/'CyclicBell.lean').write_text('import CyclicBell.Statements\n')
            (root/'CyclicBell'/'Statements.lean').write_text('namespace CyclicBell\ntheorem old : True := by trivial\nend CyclicBell\n')
            (root/'CyclicBell'/'Extra'/'New.lean').write_text('namespace CyclicBell\ntheorem added : True := by trivial\nend CyclicBell\n')
            generate(root)
            queries=(root/'CyclicBell'/'AxiomAudit.lean').read_text()
            self.assertIn('import CyclicBell.Extra.New\n',queries)
            self.assertIn('import CyclicBell.Statements\n',queries)
            self.assertNotIn('import CyclicBell\n',queries)
            self.assertNotIn('import CyclicBell.AxiomAudit\n',queries)
            self.assertIn('#print axioms CyclicBell.added\n',queries)

    def test_allowed_axioms(self):
        text="'Foo.a' depends on axioms: [propext,\n Classical.choice, Quot.sound]\n'Foo.b' does not depend on any axioms"
        self.assertEqual(parse_axioms(text,['Foo.a','Foo.b'])['Foo.b'], [])
    def test_custom_axiom_rejected(self):
        with self.assertRaises(ValueError):
            parse_axioms("'Foo.a' depends on axioms: [MadeUpAssumption]", ['Foo.a'])
    def test_sorry_rejected(self):
        with self.assertRaises(ValueError):
            parse_axioms("'Foo.a' depends on axioms: [sorryAx]", ['Foo.a'])
    def test_missing_report_rejected(self):
        with self.assertRaises(ValueError):
            parse_axioms('', ['Foo.a'])
    def test_duplicate_report_rejected(self):
        with self.assertRaises(ValueError):
            parse_axioms("'Foo.a' does not depend on any axioms\n'Foo.a' does not depend on any axioms", ['Foo.a'])
    def test_placeholder_hidden_in_comments_is_not_code(self):
        self.assertIsNone(BANNED.search(strip_comments_strings('/- outer /- sorry -/ admit -/\n-- native_decide\n"axiom"\ntheorem x : True := by trivial')))
    def test_real_placeholder_flagged(self):
        self.assertIsNotNone(BANNED.search(strip_comments_strings('theorem x : False := by sorry')))
    def test_real_native_flagged(self):
        self.assertIsNotNone(BANNED.search(strip_comments_strings('theorem x : True := by native_decide')))
    def test_unclosed_comment_rejected(self):
        with self.assertRaises(ValueError): strip_comments_strings('/-')
    def test_default_build_closure(self):
        result=audit()
        self.assertIn('CyclicBell.AxiomAudit',result['imported_modules'])
        self.assertFalse(result['kernel_checked'])

    def test_external_import_lookalike_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)/'project'
            shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('.lake','__pycache__','history','runs'))
            source=root/'CyclicBell/GeneralCoveragePolarAlgebra.lean'
            source.write_text(source.read_text().replace('import Mathlib\n','import MathlibUntrusted\n',1))
            with self.assertRaisesRegex(ValueError,'Unexpected external import: MathlibUntrusted'):
                audit(root)

    def test_unicode_axiom_name(self):
        name='CyclicBell.firstA₀_unitary'
        self.assertIn(name, parse_axioms(f"'{name}' depends on axioms: [propext]",[name]))
    def test_native_trust_axiom_rejected(self):
        with self.assertRaises(ValueError):
            parse_axioms("'Foo.a' depends on axioms: [Lean.ofReduceBool]", ['Foo.a'])
    def test_delimiters_reject_unclosed(self):
        with self.assertRaises(ValueError): check_delimiters('theorem x : (True := by trivial','x.lean')
    def test_delimiters_reject_extra_close(self):
        with self.assertRaises(ValueError): check_delimiters('theorem x : True) := by trivial','x.lean')
    def test_inventory_includes_unrestricted_upper_bounds(self):
        names={x['name'] for x in inventory()['declarations']}
        self.assertTrue({'CyclicBell.first_universal_upper','CyclicBell.second_universal_upper',
                         'CyclicBell.D4.first_counterexample','CyclicBell.D4.second_counterexample'} <= names)
    def test_added_unaudited_declaration_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)/'project'
            shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('.lake','__pycache__','history','runs'))
            with (root/'CyclicBell/Model.lean').open('a') as f:
                f.write('\nnamespace CyclicBell\ntheorem extra_unqueried : True := by trivial\nend CyclicBell\n')
            with self.assertRaises(ValueError):audit(root)
    def test_omitted_audit_import_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)/'project'
            shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('.lake','__pycache__','history','runs'))
            f=root/'CyclicBell.lean'
            f.write_text(f.read_text().replace('import CyclicBell.AxiomAudit','-- removed audit import'))
            with self.assertRaises(ValueError):audit(root)

    def test_general_upper_bound_separation(self):
        result=audit()
        closures=result['general_first_bound_import_closures']
        for modules in closures.values():
            self.assertNotIn('CyclicBell.GeneralWitness',modules)
            self.assertNotIn('CyclicBell.GeneralFirstWitness',modules)
            self.assertNotIn('CyclicBell.GeneralSwap',modules)
    def test_named_spectral_instances_are_queried(self):
        import json
        inv=inventory()
        instances=[x['name'] for x in inv['declarations'] if x['kind']=='instance']
        self.assertTrue({'CyclicBell.General.finiteMatrixSpectrum',
                         'CyclicBell.General.discreteMatrixSpectrum'} <= set(instances))
        names=json.loads((ROOT/'reference/expected_theorems.json').read_text())
        self.assertTrue(set(instances)<=set(names))
    def test_general_endpoints_present(self):
        names={x['name'] for x in inventory()['declarations']}
        expected={'first_all_dimension_counterexample','second_all_dimension_counterexample',
            'supported_multiplicity_rigidity','supported_dimension_divisible',
            'first_commuting_PVM_upper','second_commuting_PVM_upper',
            'binary_saturation_privacy','one_input_pure_projective_perfect_guess',
            'privateMUB_composition','first_behavior_nonuniqueness',
            'second_behavior_nonuniqueness','source_computational_MUB_exposure'}
        self.assertTrue({'CyclicBell.General.'+x for x in expected}<=names)
    def test_unimported_general_file_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)/'project'
            shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('.lake','__pycache__','history','runs'))
            (root/'CyclicBell/GeneralForgotten.lean').write_text('import CyclicBell.GeneralFourier\n')
            with self.assertRaises(ValueError):audit(root)
    def test_general_bound_witness_import_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)/'project'
            shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('.lake','__pycache__','history','runs'))
            p=root/'CyclicBell/GeneralFirstBound.lean'
            p.write_text('import CyclicBell.GeneralWitness\n'+p.read_text())
            with self.assertRaises(ValueError):audit(root)
    def test_deleting_spectral_instance_query_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)/'project'
            shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('.lake','__pycache__','history','runs'))
            instances=[x['name'] for x in inventory(root)['declarations'] if x['kind']=='instance']
            p=root/'CyclicBell/AxiomAudit.lean'
            p.write_text(p.read_text().replace('#print axioms '+instances[0]+'\n',''))
            with self.assertRaises(ValueError):audit(root)
    def test_general_false_controls_in_offline_runner(self):
        text=(ROOT/'scripts/check.py').read_text()
        for name in ['RejectGeneralNormalization','RejectGeneralCoefficients','RejectGeneralSwap']:
            self.assertIn('validation/'+name+'.lean',text)
            self.assertTrue((ROOT/'validation'/ (name+'.lean')).exists())

    def test_negative_control_unknown_identifier_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            runner=Runner(Path(d))
            bad=subprocess.CompletedProcess(['lean'],1,'error: unknown identifier Foo\nerror: unsolved goals\n')
            with patch('check.subprocess.run',return_value=bad):
                with self.assertRaises(RuntimeError):
                    runner.run(['lean','control.lean'],expect_failure=True)
    def test_negative_control_genuine_proof_failure_accepted(self):
        with tempfile.TemporaryDirectory() as d:
            runner=Runner(Path(d))
            (Path(d)/'validation').mkdir()
            (Path(d)/'validation/control.lean').write_text('example : (1 : Nat) = 2 := by\n  rfl\n')
            bad=subprocess.CompletedProcess(['lean'],1,'validation/control.lean:2:2: error: unsolved goals\n⊢ (1 : Nat) = 2\n')
            with patch('check.subprocess.run',return_value=bad):
                runner.run(['lean','validation/control.lean'],cwd=Path(d),expect_failure=True)


    def test_all_model_value_endpoints_are_queried(self):
        names = {x['name'] for x in inventory()['declarations']}
        wanted = {'first_reduced_values_q_qa_qc', 'first_augmented_values_q_qa_qc',
                  'second_reduced_values_q_qa_qc', 'second_augmented_values_q_qa_qc',
                  'binary_values_q_qa_qc', 'binary_componentwise_minimality',
                  'weighted_cycle_charpoly', 'finiteToCommuting_behavior'}
        self.assertTrue({'CyclicBell.General.'+n for n in wanted} <= names)

    def test_model_controls_registered_as_unexecuted(self):
        controls = validation_registry()
        self.assertFalse(controls['validation/AcceptModels.lean']['expect_failure'])
        for n in ('RejectModelValue', 'RejectClosureValue', 'RejectPurificationNorm', 'RejectCycleCharpoly'):
            self.assertTrue(controls['validation/'+n+'.lean']['expect_failure'])
        self.assertTrue(all(not c['lean_executed'] for c in controls.values()))

    def test_omitted_negative_control_command_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)/'project'
            shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('.lake','__pycache__','history','runs'))
            p = root/'scripts/check.py'
            s = p.read_text()
            s = '\n'.join(line for line in s.splitlines() if 'validation/RejectClosureValue.lean' not in line)+'\n'
            p.write_text(s)
            with self.assertRaisesRegex(ValueError,'registry'):
                validation_registry(root)

    def test_wrong_negative_control_expectation_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)/'project'
            shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('.lake','__pycache__','history','runs'))
            p = root/'scripts/check.py'
            s = p.read_text().replace("'validation/RejectClosureValue.lean'],expect_failure=True)",
                                      "'validation/RejectClosureValue.lean'],expect_failure=False)")
            p.write_text(s)
            with self.assertRaisesRegex(ValueError,'wrong outcome'):
                validation_registry(root)

    def test_unregistered_control_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)/'project'
            shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('.lake','__pycache__','history','runs'))
            (root/'validation/RejectUnregistered.lean').write_text('example : True := by trivial\n')
            with self.assertRaisesRegex(ValueError,'registry'):
                validation_registry(root)

    def test_control_placeholder_rejected(self):
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)/'project'
            shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('.lake','__pycache__','history','runs'))
            (root/'validation/RejectClosureValue.lean').write_text('example : False := by sorry\n')
            with self.assertRaisesRegex(ValueError,'Forbidden'):
                validation_registry(root)


    def test_claim_ledger_declarations_resolve_statically(self):
        self.assertGreaterEqual(audit()['claim_ledger_rows'],38)

    def test_unknown_claim_ledger_declaration_rejected(self):
        import json
        with tempfile.TemporaryDirectory() as d:
            root = Path(d)/'project'
            shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('.lake','__pycache__','history','runs'))
            p = root/'reference/paper_claim_ledger.json'
            ledger = json.loads(p.read_text())
            ledger['claims'][0]['theorems'] = ['CyclicBell.NonexistentProof']
            p.write_text(json.dumps(ledger))
            with self.assertRaisesRegex(ValueError,'Claim ledger'):
                audit(root)

    def test_adversarial_endpoints_are_in_query_inventory(self):
        import json
        names=set(json.loads((ROOT/'reference/expected_theorems.json').read_text()))
        wanted={'first_value_conditioned_guessing_bounds','second_value_conditioned_guessing_bounds',
                'first_four_value_entropy_upper','second_four_value_entropy_upper',
                'tripartiteToCommuting_behavior','fixed_realization_guessing_maximum',
                'first_GvalQ_nested','second_GvalQ_nested','source_qutrit_operator'}
        self.assertTrue({'CyclicBell.General.'+name for name in wanted}<=names)

    def test_adversarial_control_registry(self):
        controls=validation_registry()
        self.assertFalse(controls['validation/AcceptAdversarial.lean']['expect_failure'])
        for name in ['RejectAdversarialUniformBound','RejectEveProjectivity','RejectEveNormalization',
                     'RejectClosureSliceOrder','RejectSourceQutritSign']:
            self.assertTrue(controls['validation/'+name+'.lean']['expect_failure'])
        self.assertTrue(all(not row['lean_executed'] for row in controls.values()))

    def test_project_reference_audit_does_not_claim_lean_resolution(self):
        from project_reference_audit import audit as refs
        result=refs()
        self.assertFalse(result['kernel_checked'])
        self.assertFalse(result['is_lean_name_resolution'])
        self.assertEqual(result['issues'],[])
        self.assertGreater(result['known_reference_occurrences'],100)

    def test_old_dimension_dependency_error_is_detected(self):
        from project_reference_audit import audit as refs
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)/'project'
            shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('.lake','__pycache__','history','runs'))
            first=root/'CyclicBell/GeneralFourier.lean';later=root/'CyclicBell/GeneralWitness.lean'
            declaration='theorem dimension_pos : 0 < (d : ℝ) := by\n  exact_mod_cast Nat.pos_of_ne_zero (NeZero.ne d)\n'
            self.assertIn(declaration,first.read_text())
            first.write_text(first.read_text().replace(declaration,''))
            later.write_text(later.read_text().replace('theorem invSqrtDim_pos',declaration+'\ntheorem invSqrtDim_pos'))
            issues=refs(root)['issues']
            self.assertTrue(any(row['file']=='CyclicBell/GeneralScalar.lean' and
                                row['declaration']=='CyclicBell.General.dimension_pos' for row in issues))

    def test_missing_adversarial_import_is_detected(self):
        from project_reference_audit import audit as refs
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)/'project'
            shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('.lake','__pycache__','history','runs'))
            f=root/'CyclicBell/GeneralAdversarialEntropy.lean'
            f.write_text(f.read_text().replace('import CyclicBell.GeneralAdversarialValues',''))
            self.assertTrue(refs(root)['issues'])

    def test_same_file_forward_reference_is_detected(self):
        from project_reference_audit import audit as refs
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'CyclicBell').mkdir()
            (root/'CyclicBell/Test.lean').write_text(
                'namespace CyclicBell\n'
                'theorem uses_later_decl : True := distinctive_future_helper\n'
                'theorem distinctive_future_helper : True := by trivial\nend CyclicBell\n')
            result=refs(root)
            self.assertEqual(result['issues'][0]['kind'],'same_file_forward_reference')

    def test_fully_qualified_unimported_name_is_detected(self):
        from project_reference_audit import audit as refs
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'CyclicBell').mkdir()
            (root/'CyclicBell/A.lean').write_text('namespace CyclicBell\ntheorem small : True := by trivial\nend CyclicBell\n')
            (root/'CyclicBell/B.lean').write_text('namespace CyclicBell\ntheorem use_qualified : True := CyclicBell.small\nend CyclicBell\n')
            result=refs(root)
            self.assertEqual(result['issues'][0]['kind'],'not_in_import_closure')

    def test_comments_do_not_create_project_references(self):
        from project_reference_audit import audit as refs
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);(root/'CyclicBell').mkdir()
            (root/'CyclicBell/A.lean').write_text('namespace CyclicBell\ntheorem distinctive_other_helper : True := by trivial\nend CyclicBell\n')
            (root/'CyclicBell/B.lean').write_text('/- distinctive_other_helper -/\nnamespace CyclicBell\ntheorem safe : True := by trivial\nend CyclicBell\n')
            self.assertEqual(refs(root)['issues'],[])



    def _expect_invalid_run(self, code, text, *, negative=True):
        with tempfile.TemporaryDirectory() as d:
            runner = Runner(Path(d))
            fake = subprocess.CompletedProcess(['lean'], code, text)
            with patch('check.subprocess.run', return_value=fake):
                with self.assertRaises(RuntimeError):
                    runner.run(['lean', 'control.lean'], expect_failure=negative)
            self.assertEqual(runner.commands[0]['exit_code'], code)
            self.assertEqual((Path(d)/'001.log').read_text(), text)

    def test_negative_control_signal_with_proof_diagnostic_rejected(self):
        self._expect_invalid_run(-9, 'error: type mismatch\n')

    def test_negative_control_shell_kill_with_proof_diagnostic_rejected(self):
        self._expect_invalid_run(137, 'error: unsolved goals\n')

    def test_negative_control_heartbeat_exhaustion_rejected(self):
        self._expect_invalid_run(1, 'error: unsolved goals\nmaximum number of heartbeats has been reached\n')

    def test_negative_control_deterministic_timeout_rejected(self):
        self._expect_invalid_run(1, 'error: tactic failed\nerror: (deterministic) timeout\n')

    def test_negative_control_recursion_exhaustion_rejected(self):
        self._expect_invalid_run(1, 'error: type mismatch\nmaximum recursion depth has been reached\n')

    def test_negative_control_memory_exhaustion_rejected(self):
        self._expect_invalid_run(1, 'error: unsolved goals\nlibc++abi: terminating due to std::bad_alloc\n')

    def test_positive_run_resource_diagnostic_rejected_even_exit_zero(self):
        self._expect_invalid_run(0, 'error: maximum number of heartbeats has been reached\n', negative=False)

    def test_positive_run_signal_rejected(self):
        self._expect_invalid_run(-15, '', negative=False)

    def test_normal_type_mismatch_control_accepted(self):
        with tempfile.TemporaryDirectory() as d:
            runner=Runner(Path(d))
            (Path(d)/'validation').mkdir()
            (Path(d)/'validation/control.lean').write_text('example : (1 : Nat) = 2 := by\n  exact True.intro\n')
            bad=subprocess.CompletedProcess(['lean'],1,'validation/control.lean:2:2: error: type mismatch\n')
            with patch('check.subprocess.run',return_value=bad):
                runner.run(['lean','validation/control.lean'],cwd=Path(d),expect_failure=True)

    def test_apostrophe_axiom_name(self):
        name="CyclicBell.helper'"
        self.assertIn(name, parse_axioms(f"'{name}' depends on axioms: [propext]", [name]))

    def test_declaration_regex_does_not_swallow_neighbor_after_attribute(self):
        from source_inventory import DECL
        text='@[simp] theorem first : True := by simp [True]\n\ntheorem second : True := by trivial\n'
        self.assertEqual([m.group(2) for m in DECL.finditer(text)], ['first', 'second'])

    def test_negative_control_rejects_unrelated_or_header_errors(self):
        with tempfile.TemporaryDirectory() as d:
            control=Path(d)/'validation/control.lean'
            control.parent.mkdir()
            control.write_text('example : (1 : Nat) = 2 := by\n  rfl\n')
            for text in [
                'validation/control.lean:1:10: error: type mismatch\n',
                'validation/control.lean:2:2: error: type mismatch\nerror: other failure\n',
                'validation/other.lean:2:2: error: unsolved goals\n',
                'validation/control.lean:2:2: error: invalid syntax\n'
                'validation/control.lean:3:2: error: unsolved goals\n',
                'error: unsolved goals\n',
            ]:
                with self.subTest(text=text), self.assertRaises(RuntimeError):
                    validate_negative_diagnostics(text, control)

    def test_inventory_covers_indentation_apostrophe_sections_root_and_subfolders(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)
            (root/'CyclicBell/Nested').mkdir(parents=True)
            (root/'CyclicBell.lean').write_text(
                "namespace CyclicBell\n  theorem root' : True := by trivial\nend CyclicBell\n")
            (root/'CyclicBell/Nested/Helpers.lean').write_text(
                "namespace CyclicBell\nsection Local\n  theorem inner' : True := by trivial\n"
                "end Local\n theorem after_section : True := by trivial\nend CyclicBell\n")
            names={x['name'] for x in inventory(root)['declarations']}
            self.assertEqual(names, {"CyclicBell.root'", "CyclicBell.inner'", 'CyclicBell.after_section'})

    def test_inventory_refuses_unsupported_declarations(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d); (root/'CyclicBell').mkdir()
            for declaration in ['instance : Inhabited Nat := ⟨0⟩',
                                'opaque hidden : Nat := 0',
                                'private theorem hidden : True := by trivial']:
                (root/'CyclicBell/Test.lean').write_text('namespace CyclicBell\n'+declaration+'\nend CyclicBell\n')
                with self.subTest(declaration=declaration), self.assertRaisesRegex(ValueError, 'unsupported'):
                    inventory(root)

    def test_all_imports_on_same_line_scanned(self):
        from static_audit import lean_imports
        self.assertEqual(lean_imports('  import CyclicBell.Model Mathlib.Tactic\n'),
                         ['CyclicBell.Model', 'Mathlib.Tactic'])
        with self.assertRaises(ValueError): lean_imports('import\n')

    def test_settings_source_endpoints_present(self):
        names = {x['name'] for x in inventory()['declarations']}
        want = {'phasePair_sine_formula', 'standard_tables_nonuniform',
                'anchored_cross_nonuniform', 'anchored_qubit_cross_uniform',
                'standard_entropy_asymptotic'}
        self.assertTrue({'CyclicBell.General.'+n for n in want} <= names)


    def test_settings_controls_registered_as_unexecuted(self):
        controls=validation_registry()
        self.assertFalse(controls['validation/AcceptSettings.lean']['expect_failure'])
        for name in ['RejectSettingsUniform','RejectSettingsNormalization','RejectAnchorQubitGap']:
            self.assertTrue(controls['validation/'+name+'.lean']['expect_failure'])
        self.assertTrue(all(not c['lean_executed'] for c in controls.values()))

    def test_settings_audit_import_cannot_be_omitted(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)/'project'
            shutil.copytree(ROOT,root,ignore=shutil.ignore_patterns('.lake','__pycache__','history','runs'))
            # The generated axiom module now imports every source explicitly.
            # Remove every incoming edge to simulate omission from the build,
            # rather than merely removing one redundant import.
            for p in [root/'CyclicBell.lean',*(root/'CyclicBell').rglob('*.lean')]:
                p.write_text(p.read_text().replace('import CyclicBell.PhaseTableStatements','-- omitted settings audit'))
            with self.assertRaises(ValueError): audit(root)

    def test_settings_imports_do_not_depend_on_bell_bounds_or_scalar_extremum(self):
        import re
        modules={}
        for p in (ROOT/'CyclicBell').glob('*.lean'):
            modules['CyclicBell.'+p.stem]=re.findall(r'^import\s+(CyclicBell[.\w]*)',p.read_text(),re.M)
        seen=set()
        def walk(m):
            if m in seen: return
            seen.add(m)
            for dep in modules.get(m,[]): walk(dep)
        walk('CyclicBell.PhaseTableStatements')
        for bad in ['GeneralScalar','GeneralFirstBound','GeneralCommuting','GeneralRigidity',
                    'PhysicalBounds','Endpoints']:
            self.assertNotIn('CyclicBell.'+bad,seen)

if __name__ == '__main__': unittest.main(verbosity=2)
