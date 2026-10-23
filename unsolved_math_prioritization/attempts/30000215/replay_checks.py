#!/usr/bin/env python3
"""Replay the byte-preserved checker with assertions enabled in every Python mode.

Python 3.10+; standard library only. Generated data stays in a temporary directory.
The --probe-assertion option is for negative tests, not mathematical verification.
"""
import sys
sys.dont_write_bytecode = True
import argparse
import ast
import contextlib
import dis
import hashlib
import io
import json
from pathlib import Path
import tempfile
import types
from validate_packet import validate, require

CHECKER_SHA256 = 'c86870f318768b0fe9cd89b6b2f83d62dec34640bf402a88aff6af9e2fcd7ca7'
RESULT_SHA256 = '5ea80af62ea2a954e12f49f91f626e8bb9a8749e65e2192edc7cbf01a5228e83'
ASSERTION_SITES = 16


def count_assertions(code):
    count = sum(i.opname == 'LOAD_ASSERTION_ERROR' for i in dis.get_instructions(code))
    return count + sum(count_assertions(c) for c in code.co_consts if isinstance(c, types.CodeType))


def assertion_sites(tree):
    sites = []
    for fn in tree.body:
        if isinstance(fn, (ast.FunctionDef, ast.AsyncFunctionDef)):
            sites.extend((node.lineno, fn.name, node) for node in ast.walk(fn) if isinstance(node, ast.Assert))
    return sorted(sites)


def compile_preserved(source, filename):
    code = compile(source, str(filename), 'exec', dont_inherit=True, optimize=0)
    require(len(assertion_sites(ast.parse(source))) == ASSERTION_SITES, 'source assertion count mismatch')
    # A chained comparison may compile more than one failure instruction.
    require(count_assertions(code) >= ASSERTION_SITES, 'compiled assertion failure paths missing')
    return code


def run_probe(source, root, index):
    """Force one original assertion site false, preserving all other source code.

The other assertion conditions are set true in this negative-test-only AST so
that the selected site's failure is isolated. No packaged source is rewritten.
"""
    tree = ast.parse(source)
    sites = assertion_sites(tree)
    require(len(sites) == ASSERTION_SITES and 0 <= index < len(sites), 'invalid assertion probe')
    line, fn, _ = sites[index]
    marker = 'FORCED_ORIGINAL_ASSERTION_%d_LINE_%d' % (index, line)
    for i, (_, _, node) in enumerate(sites):
        node.test = ast.Constant(value=(i != index))
        node.msg = ast.Constant(value=marker if i == index else 'isolated assertion probe')
    tree = ast.fix_missing_locations(tree)
    code = compile(tree, str(root / 'verify_exact.py'), 'exec', dont_inherit=True, optimize=0)
    ns = {'__name__': '__assertion_probe__', '__file__': str(root / 'verify_exact.py')}
    exec(code, ns)
    try:
        if fn == 'instance':
            ns['instance'](3, 3)
        elif fn == 'local_identity_checks':
            _, edges, pairs, bits = ns['instance'](3, 3)
            ns[fn](3, 3, edges, pairs, bits)
        elif fn in ('exhaustive_k33_image', 'main'):
            ns[fn]()
        else:
            raise ValueError('unrecognized assertion site function')
    except AssertionError as error:
        require(str(error) == marker, 'wrong assertion failed')
        print(json.dumps({'status': 'EXPECTED_ASSERTION_FAILURE', 'site': index, 'line': line,
                          'function': fn, 'outer_optimization': sys.flags.optimize,
                          'checker_compilation_optimization': 0}))
        return 3
    raise ValueError('forced original assertion was not enforced')


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--probe-assertion', type=int)
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    validate(root)
    source = (root / 'verify_exact.py').read_bytes()
    require(hashlib.sha256(source).hexdigest() == CHECKER_SHA256, 'checker pin mismatch')
    # This inspects the compiled unmodified source in every mode, even for probes.
    compile_preserved(source, root / 'verify_exact.py')
    with tempfile.TemporaryDirectory(prefix='crossing-reader-replay-') as tmp:
        temporary_root = Path(tmp)
        if args.probe_assertion is not None:
            return run_probe(source, temporary_root, args.probe_assertion)
        filename = temporary_root / 'verify_exact.py'
        filename.write_bytes(source)
        ns = {'__name__': '__main__', '__file__': str(filename)}
        output = io.StringIO()
        with contextlib.redirect_stdout(output):
            exec(compile_preserved(source, filename), ns)
        actual = (temporary_root / 'exact_checks.json').read_bytes()
        require(hashlib.sha256(actual).hexdigest() == RESULT_SHA256, 'replay result digest mismatch')
        require(actual == (root / 'exact_checks.json').read_bytes(), 'replay result bytes differ')
        summary = json.loads(output.getvalue())
        expected = {'status': 'PASS', 'geometry_cases': 60, 'local_k33_subgraphs': 1650,
                    'seeded_assignments': 1792, 'k33_image_rank': 17, 'k33_minimum_weight': 1}
        require(summary == expected, 'replay summary mismatch')
        print(json.dumps({'status': 'PASS', 'outer_optimization': sys.flags.optimize,
                          'checker_compilation_optimization': 0, 'compiled_assertion_sites': ASSERTION_SITES,
                          'compiled_assertion_failure_instructions': count_assertions(compile_preserved(source, filename)),
                          'checker_sha256': CHECKER_SHA256, 'result_sha256': RESULT_SHA256,
                          'result_bytes': len(actual), 'byte_identical_result': True, 'summary': summary}, sort_keys=True))
    return 0


if __name__ == '__main__':
    try:
        raise SystemExit(main())
    except (OSError, ValueError, TypeError, KeyError) as error:
        print('FAIL: ' + str(error), file=sys.stderr)
        raise SystemExit(1)
