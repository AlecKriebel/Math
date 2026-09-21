#!/usr/bin/env python3
"""Compiler-free regressions for the fail-closed production source inventory."""
from pathlib import Path
import tempfile
import unittest

from source_audit import production_modules, strip_comments, theorem_declarations


class ProductionRootTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='bell-source-roots-')
        self.root = Path(self.temp.name)
        (self.root / 'Bell').mkdir()

    def tearDown(self):
        self.temp.cleanup()

    def test_flat_sources_discovered_and_generated_audit_excluded(self):
        for name in ('Z.lean', 'A.lean', 'Audit.lean'):
            (self.root / 'Bell' / name).write_text('import Mathlib\n')
        self.assertEqual([p.name for p in production_modules(self.root)], ['A.lean', 'Z.lean'])

    def test_nested_proof_is_rejected(self):
        directory = self.root / 'Bell' / 'Nested'
        directory.mkdir()
        (directory / 'Missed.lean').write_text('example : True := True.intro\n')
        with self.assertRaisesRegex(AssertionError, 'Bell/Nested/Missed.lean'):
            production_modules(self.root)

    def test_nested_audit_is_not_silently_exempted(self):
        directory = self.root / 'Bell' / 'Nested'
        directory.mkdir()
        (directory / 'Audit.lean').write_text('example : True := True.intro\n')
        with self.assertRaisesRegex(AssertionError, 'Nested production Lean modules'):
            production_modules(self.root)

    def test_non_lean_support_files_are_not_production_modules(self):
        directory = self.root / 'Bell' / 'notes'
        directory.mkdir()
        (directory / 'review.md').write_text('No Lean module here.\n')
        self.assertEqual(production_modules(self.root), [])


class DeclarationInventoryTests(unittest.TestCase):
    def test_same_line_attribute_theorem_and_lemma(self):
        source = '@[simp] theorem first : True := True.intro\n@[simp] lemma second : True := True.intro\n'
        self.assertEqual(theorem_declarations(source), {
            1: ('public', 'theorem', 'first'), 2: ('public', 'lemma', 'second')})

    def test_multiple_multiline_attributes_and_modifiers(self):
        source = '@[simp,\n ext] @[aesop safe]\nprotected theorem first : True := True.intro\n@[simp] private lemma second : True := True.intro\n'
        self.assertEqual(theorem_declarations(source), {
            3: ('protected', 'theorem', 'first'), 4: ('private', 'lemma', 'second')})

    def test_separate_attribute_preserves_declaration_line(self):
        self.assertEqual(theorem_declarations('@[simp]\ntheorem first : True := True.intro'),
                         {2: ('public', 'theorem', 'first')})

    def test_comments_and_strings_do_not_declare_theorems(self):
        source = '-- theorem fake\n/- @[simp] lemma falseName -/\ndef text := "theorem imaginary"\n@[simp] theorem real : True := True.intro'
        self.assertEqual(theorem_declarations(strip_comments(source)),
                         {4: ('public', 'theorem', 'real')})

    def test_unsupported_prefix_fails_closed(self):
        with self.assertRaisesRegex(AssertionError, 'Unsupported theorem declaration syntax'):
            theorem_declarations('unsupported theorem silentlyMissed : True := True.intro')

    def test_same_line_second_declaration_fails_closed(self):
        with self.assertRaisesRegex(AssertionError, 'Unsupported theorem declaration syntax'):
            theorem_declarations('theorem first : True := True.intro; theorem missed : True := True.intro')


if __name__ == '__main__':
    unittest.main(verbosity=2)
