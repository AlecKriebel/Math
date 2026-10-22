#!/usr/bin/env python3
"""Convert only Assert AST nodes to explicit, optimization-safe failure gates.

Assert(test, msg) becomes If(Not(test), Raise(AssertionError(msg))), while a bare
assert raises AssertionError() with no arguments. Failure message expressions
remain evaluated only on failure. AST unparse changes formatting and locations.
No mathematical statement, report object, path, or data input is added or edited.
"""
import argparse
import ast
import copy
from datetime import datetime, timezone
import hashlib
import json
from pathlib import Path


def sha(data):
    return hashlib.sha256(data).hexdigest()


class ExplicitAssertions(ast.NodeTransformer):
    def __init__(self):
        self.predicates = []

    def visit_Assert(self, node):
        self.predicates.append({'original_line': node.lineno,
                                'predicate_ast': ast.dump(node.test, include_attributes=False),
                                'message_ast': ast.dump(node.msg, include_attributes=False)
                                if node.msg is not None else None})
        args = [] if node.msg is None else [node.msg]
        return ast.copy_location(ast.If(
            test=ast.UnaryOp(op=ast.Not(), operand=node.test),
            body=[ast.Raise(exc=ast.Call(func=ast.Name(id='AssertionError', ctx=ast.Load()),
                                      args=args, keywords=[]), cause=None)], orelse=[]), node)


class RestoreAssertions(ast.NodeTransformer):
    def visit_If(self, node):
        if (isinstance(node.test, ast.UnaryOp) and isinstance(node.test.op, ast.Not)
                and len(node.body) == 1 and not node.orelse
                and isinstance(node.body[0], ast.Raise)
                and node.body[0].cause is None):
            exc = node.body[0].exc
            if (isinstance(exc, ast.Call) and isinstance(exc.func, ast.Name)
                    and exc.func.id == 'AssertionError' and not exc.keywords
                    and len(exc.args) <= 1):
                return ast.copy_location(ast.Assert(test=node.test.operand,
                    msg=exc.args[0] if exc.args else None), node)
        return self.generic_visit(node)


def transform(source):
    original = ast.parse(source)
    expected_count = sum(isinstance(n, ast.Assert) for n in ast.walk(original))
    # These frozen files do not shadow the builtin AssertionError.
    names = [n.id for n in ast.walk(original) if isinstance(n, ast.Name)
             and n.id == 'AssertionError']
    if names:
        raise RuntimeError('Input references AssertionError; shadowing requires review')
    conversion = ExplicitAssertions()
    changed = ast.fix_missing_locations(conversion.visit(copy.deepcopy(original)))
    text = ast.unparse(changed) + '\n'
    reparsed = ast.parse(text)
    if ast.dump(reparsed, include_attributes=False) != ast.dump(changed, include_attributes=False):
        raise RuntimeError('Generated source differs from the intended transformed AST')
    restored = RestoreAssertions().visit(copy.deepcopy(reparsed))
    if ast.dump(restored, include_attributes=False) != ast.dump(original, include_attributes=False):
        raise RuntimeError('Inverse transformation did not recover the exact original AST')
    remaining = sum(isinstance(n, ast.Assert) for n in ast.walk(reparsed))
    if len(conversion.predicates) != expected_count or remaining != 0:
        raise RuntimeError('Assertion correspondence mismatch')
    certificate = {'original_assert_count': expected_count,
                   'transformed_explicit_gate_count': len(conversion.predicates),
                   'remaining_assert_count': remaining,
                   'transformed_ast_matches_generated_source': True,
                   'inverse_transform_restores_original_ast': True,
                   'exception_type': 'builtins.AssertionError',
                   'bare_assert_args': [],
                   'message_evaluation': 'only on failure; original expression preserved',
                   'predicates': conversion.predicates}
    return text, certificate


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--case', type=Path, required=True)
    args = parser.parse_args()
    case = args.case.resolve()
    review = case / 'reviews' / 'reproduction_adversary'
    source = case / 'source_snapshot' / 'unsolved_math_prioritization' / 'attempts' / '20001515'
    records = []
    for name in ('verify.py', 'audit/independent_audit.py', 'audit/independent_algebra.py'):
        src = source / name
        dst = review / 'overlay' / name
        dst.parent.mkdir(parents=True, exist_ok=True)
        result, certificate = transform(src.read_text())
        dst.write_text(result)
        records.append({'program': name, 'frozen_input_sha256': sha(src.read_bytes()),
                        'overlay_sha256': sha(dst.read_bytes()), **certificate})
    metadata = {'recorded_at_utc': datetime.now(timezone.utc).isoformat(),
                'type': 'validation-only optimization-safe explicit checks',
                'author_proof_attempts_added': 0,
                'diagnostic_differences': 'AST unparse changes formatting, line numbers, and tracebacks; no literal traceback identity is claimed.',
                'exception_binding_precondition': 'No original program references or shadows AssertionError; runs use an unmodified builtin environment.',
                'programs': records}
    (review / 'OVERLAY_PROVENANCE.json').write_text(json.dumps(metadata, indent=2) + '\n')
    print(json.dumps({'programs': len(records),
                      'predicates': sum(r['original_assert_count'] for r in records),
                      'all_inverse_ast_checks_pass': all(r['inverse_transform_restores_original_ast']
                                                        for r in records)}, indent=2))


if __name__ == '__main__':
    main()
