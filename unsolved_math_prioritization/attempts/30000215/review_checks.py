#!/usr/bin/env python3
"""Independent integration checks. Standard library; no network or packet writes.

Temporary AST probes test assertion enforcement only. They add no mathematical
pass. Full unchanged-checker replays remain supplemental to the accepted proof.
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
import re
import shutil
import subprocess
import tempfile
import types
from validate_packet import validate, require

MODES = [('normal', []), ('-O', ['-O']), ('-OO', ['-OO'])]
CHECKER_PIN = 'c86870f318768b0fe9cd89b6b2f83d62dec34640bf402a88aff6af9e2fcd7ca7'
REGRESSIONS = ['tamper_unknown_modes', 'assertion_wrong_outer_mode',
               'positive_duplicate_modes', 'preservation_wrong_source',
               'replay_boolean_optimizer', 'tamper_unknown_case',
               'assertion_wrong_line', 'assertion_wrong_function',
               'positive_wrong_file_count', 'preservation_wrong_role',
               'replay_extra_key', 'test_report_extra_key']


def instructions(code):
    return sum(item.opname == 'LOAD_ASSERTION_ERROR' for item in dis.get_instructions(code)) + sum(
        instructions(item) for item in code.co_consts if isinstance(item, types.CodeType))


def sites(tree):
    return sorted((node.lineno, function.name, node) for function in tree.body
                  if isinstance(function, ast.FunctionDef)
                  for node in ast.walk(function) if isinstance(node, ast.Assert))


def independent_probes(root):
    source = (root/'verify_exact.py').read_bytes()
    require(hashlib.sha256(source).hexdigest() == CHECKER_PIN, 'independent source pin failed')
    original_sites = sites(ast.parse(source))
    require(len(original_sites) == 16, 'independent site inventory mismatch')
    unmodified = [instructions(compile(source, 'verify_exact.py', 'exec',
                                      dont_inherit=True, optimize=level)) for level in (0, 1, 2)]
    require(unmodified[0] >= 16 and unmodified[1:] == [0, 0], 'optimization control mismatch')
    rows = []
    for selected in range(16):
        tree = ast.parse(source)
        listing = sites(tree)
        line, function, _ = listing[selected]
        marker = 'INDEPENDENT_SITE_%d_LINE_%d' % (selected, line)
        for index, (_, _, node) in enumerate(listing):
            node.test = ast.Constant(value=index != selected)
            node.msg = ast.Constant(value=marker)
        ast.fix_missing_locations(tree)
        code = compile(tree, 'verify_exact.py', 'exec', dont_inherit=True, optimize=0)
        require(instructions(code) >= 1, 'negative probe assertion removed')
        with tempfile.TemporaryDirectory(prefix='crossing-independent-probe-') as tmp:
            ns = {'__name__': '__independent_probe__', '__file__': str(Path(tmp)/'verify_exact.py')}
            exec(code, ns)
            caught = False
            with contextlib.redirect_stdout(io.StringIO()):
                try:
                    if function == 'instance':
                        ns[function](3, 3)
                    elif function == 'local_identity_checks':
                        _, edges, pairs, bits = ns['instance'](3, 3)
                        ns[function](3, 3, edges, pairs, bits)
                    elif function in ('main', 'exhaustive_k33_image'):
                        ns[function]()
                    else:
                        raise ValueError('unknown assertion function')
                except AssertionError as error:
                    require(str(error) == marker, 'wrong independent assertion failed')
                    caught = True
            require(caught, 'independent assertion did not fail')
        rows.append({'site': selected, 'line': line, 'function': function,
                     'status': 'EXPECTED_ASSERTION_FAILURE'})
    return {'status': 'PASS', 'outer_optimization': sys.flags.optimize,
            'checker_compilation_optimization': 0, 'assertion_sites': 16,
            'unmodified_assertion_failure_instructions': unmodified[0],
            'direct_optimized_negative_controls': [
                {'compile_optimization': level, 'assertion_failure_instructions': unmodified[level],
                 'assertions_enforced': False, 'mathematical_run_performed': False} for level in (1, 2)],
            'probes': rows, 'assertion_failures_confirmed': len(rows)}


def execute(script, flags=(), args=()):
    result = subprocess.run([sys.executable, '-B', *flags, str(script), *map(str, args)],
                            capture_output=True, text=True, timeout=180)
    require(result.returncode == 0, 'command failed: '+script.name+' '+result.stderr)
    return json.loads(result.stdout)


def regression_mutation(root, case):
    name = 'TEST_REPORT.json'
    if case.startswith('preservation_'): name = 'PRESERVATION_MAP.json'
    if case.startswith('replay_'): name = 'REPLAY_REPORT.json'
    data = json.loads((root/name).read_text())
    if case == 'tamper_unknown_modes':
        for row in data['tamper_tests']: row['mode'] = 'unknown_'+row['mode']
    elif case == 'assertion_wrong_outer_mode':
        for row in data['assertion_probes']: row['outer_optimization'] = 99
    elif case == 'positive_duplicate_modes':
        data['positive_validations'] = [data['positive_validations'][0]]*3
    elif case == 'preservation_wrong_source': data['artifacts'][0]['source_artifact'] = 'WRONG.md'
    elif case == 'replay_boolean_optimizer': data['complete_replays'][0]['checker_compilation_optimization'] = False
    elif case == 'tamper_unknown_case': data['tamper_tests'][0]['case'] = 'nonexistent_test'
    elif case == 'assertion_wrong_line': data['assertion_probes'][0]['line'] = 999
    elif case == 'assertion_wrong_function': data['assertion_probes'][0]['function'] = 'nonexistent_function'
    elif case == 'positive_wrong_file_count': data['positive_validations'][0]['result']['files'] = 999
    elif case == 'preservation_wrong_role': data['artifacts'][0]['source_role'] = 'incorrect source role'
    elif case in ('replay_extra_key', 'test_report_extra_key'): data['unrecognized'] = 'untrusted metadata'
    else: raise ValueError('unknown regression case')
    raw = (json.dumps(data, indent=2)+'\n').encode()
    (root/name).write_bytes(raw)
    manifest = json.loads((root/'MANIFEST.json').read_text())
    for row in manifest['files']:
        if row['path'] == name:
            row.update(bytes=len(raw), sha256=hashlib.sha256(raw).hexdigest())
    (root/'MANIFEST.json').write_text(json.dumps(manifest, indent=2)+'\n')


def local_links(root):
    links = []
    for path in sorted(root.glob('*.md')):
        for match in re.finditer(r'\[[^\]\n]+\]\(([^)\n]+)\)', path.read_text()):
            target = match.group(1)
            if re.match(r'https?://', target): continue
            require('#' not in target and '/' not in target and '\\' not in target,
                    'unsupported local link target: '+target)
            require((root/target).is_file(), 'broken local link: '+path.name+' -> '+target)
            links.append({'source': path.name, 'target': target, 'status': 'PASS'})
    return links


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--probe-child', action='store_true')
    parser.add_argument('--inventory-only', action='store_true',
                        help='Explicitly skip replay and assertion checks; use only for restore inventory.')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    validate(root)
    if args.probe_child:
        print(json.dumps(independent_probes(root), indent=2)); return
    positives, replays, independent, regressions = [], [], [], []
    for mode, flags in MODES:
        positives.append({'mode': mode, **execute(root/'validate_packet.py', flags)})
        if not args.inventory_only:
            replays.append({'mode': mode, **execute(root/'replay_checks.py', flags)})
            independent.append({'mode': mode, **execute(Path(__file__), flags, ['--probe-child'])})
        for case in REGRESSIONS:
            with tempfile.TemporaryDirectory(prefix='crossing-review-regression-') as tmp:
                target = Path(tmp)/'public'; shutil.copytree(root, target)
                regression_mutation(target, case)
                result = subprocess.run([sys.executable, '-B', *flags, str(root/'validate_packet.py'), str(target)],
                                        capture_output=True, text=True, timeout=180)
                require(result.returncode == 1 and 'frozen historical evidence mismatch' in result.stderr,
                        'resealed metadata not rejected: '+mode+'/'+case)
                regressions.append({'mode': mode, 'case': case, 'status': 'REJECTED',
                                    'diagnostic': result.stderr.strip()})
    original_suite = execute(root/'test_packet.py', args=['--skip-assertion-probes'] if args.inventory_only else [])
    require(original_suite['tamper_rejections'] == 54, 'original tamper suite mismatch')
    require(original_suite['assertion_probes_skipped'] is args.inventory_only, 'incorrect skipped-probe reporting')
    for path in root.glob('*.py'):
        tree = ast.parse(path.read_bytes(), filename=path.name)
        if path.name != 'verify_exact.py':
            require(not any(isinstance(node, ast.Assert) for node in ast.walk(tree)),
                    'review gate must not use assertions: '+path.name)
    report = {'schema_version': 1, 'status': 'PASS', 'mathematical_passes_added': 0,
              'remote_mutations': 0, 'inventory_only': args.inventory_only,
              'positive_validations': positives, 'complete_replays': replays,
              'independent_assertion_checks': independent,
              'independent_assertion_failures_confirmed': sum(r['assertion_failures_confirmed'] for r in independent),
              'original_suite': original_suite,
              'metadata_regressions': regressions, 'metadata_tamper_rejections': len(regressions),
              'local_links': local_links(root), 'python_syntax': 'PASS',
              'review_gates_use_explicit_exceptions': True,
              'limits': 'Finite replays are supplemental. AST probes test enforcement only. Historical reports remain immutable; hashes require trusted validator and external seal bytes.'}
    print(json.dumps(report, indent=2))


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError, subprocess.TimeoutExpired) as error:
        print('FAIL: '+str(error), file=sys.stderr)
        raise SystemExit(1)
