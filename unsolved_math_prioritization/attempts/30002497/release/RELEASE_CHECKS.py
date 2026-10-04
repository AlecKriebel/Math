#!/usr/bin/env python3
"""Replay all controls and verify the corrected safe release. No network calls."""
import argparse
import ast
from fractions import Fraction
import hashlib
import json
from pathlib import Path
import subprocess
import sys
import tempfile

HERE = Path(__file__).resolve().parent


def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def check_sumfile(path):
    n = 0
    for line in path.read_text().splitlines():
        digest, name = line.split('  ', 1)
        candidate = path.parent / name
        assert candidate.is_file() and not candidate.is_symlink()
        assert sha(candidate) == digest, name
        n += 1
    return n


def function_ast(path, name):
    tree = ast.parse(path.read_text())
    return ast.dump(next(n for n in tree.body if isinstance(n, ast.FunctionDef) and n.name == name), include_attributes=False)


def parse_interval(s):
    return tuple(Fraction(x.strip()) for x in s.strip('[]').split(','))


def run_script(script, args, out):
    subprocess.run([sys.executable, str(script), *args, '--output', str(out)],
                   check=True, cwd=HERE)
    return json.loads(out.read_text())


def verify():
    original = HERE/'original-author'
    current = HERE/'current'
    audit = HERE/'audit'
    binding = json.loads((audit/'AUDITED_INPUTS.json').read_text())
    for f in binding['files']:
        assert sha(original/f['path']) == f['sha256'], f['path']
    result = {'problem_id': 30002497, 'status': 'unsolved', 'substantive_routes': 5,
              'original_author_files_bound': len(binding['files']),
              'preserved_audit_files_verified': check_sumfile(audit/'SHA256SUMS')}
    assert (original/'PROOF.md').read_bytes() == (current/'PROOF.md').read_bytes()
    assert (original/'SOURCES.md').read_bytes() == (current/'SOURCES.md').read_bytes()
    result['analytic_proof_and_sources_byte_identical'] = True
    assert (current/'verify_controls.py').read_bytes() == (audit/'verify_controls_outward.py').read_bytes()
    result['serializer_matches_supplied_audited_variant'] = True
    for f in ('finite_integral', 'A_bound'):
        assert function_ast(original/'verify_controls.py', f) == function_ast(current/'verify_controls.py', f)
    result['integration_engine_ast_unchanged'] = True
    replays = []
    with tempfile.TemporaryDirectory(prefix='fractional-autocorrelation-check-') as temp:
        temp = Path(temp)
        for cutoff, dps, filename, audit_filename in [
                (2048, 40, 'control_results.json', 'corrected_controls_2048_40.json'),
                (4096, 60, 'control_results_high_precision.json', 'corrected_controls_4096_60.json')]:
            args = ['--cutoff', str(cutoff), '--dps', str(dps)]
            for kind, folder in [('historical_original', original), ('corrected', current)]:
                out = temp/f'{kind}_{cutoff}_{dps}.json'
                run_script(folder/'verify_controls.py', args, out)
                assert out.read_bytes() == (folder/filename).read_bytes(), (kind, cutoff, dps)
                if kind == 'corrected':
                    assert out.read_bytes() == (audit/audit_filename).read_bytes()
                replays.append({'kind': kind, 'cutoff': cutoff, 'dps': dps,
                                'saved_output_exact_match': True, 'sha256': sha(out)})
        checked = run_script(audit/'verify_audit.py', ['--author', str(original), '--rerun'], temp/'audit.json')
        assert checked['all_checks_passed'] and checked['independent_rerun_exact_match']
        assert checked['outward_serializer_exact_tests'] == 24
    result['replays'] = replays
    low = json.loads((current/'control_results.json').read_text())
    high = json.loads((current/'control_results_high_precision.json').read_text())
    independent = json.loads((audit/'independent_results.json').read_text())
    assert len(low['metallic_reciprocals']) == len(high['metallic_reciprocals']) == len(independent['metallic_reciprocals']) == 11
    checks = []
    for a,b,c in zip(low['metallic_reciprocals'],high['metallic_reciprocals'],independent['metallic_reciprocals']):
        assert a['m'] == b['m'] == c['m']
        lo,hi = parse_interval(a['derivative_interval'])
        hl,hh = parse_interval(b['derivative_interval'])
        il,ih = Fraction(c['derivative']['lower']),Fraction(c['derivative']['upper'])
        assert il <= lo <= hl <= hh <= hi <= ih
        assert a['sign'] == b['sign'] == c['sign']
        assert (il > 0 if a['m'] <= 9 else ih < 0)
        checks.append({'m': a['m'], 'high_nested_in_low': True,
                       'low_nested_in_independent': True, 'sign': a['sign']})
    result['corrected_interval_relationships'] = checks
    result['audit_verification'] = checked
    result['all_checks_passed'] = True
    return result


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', type=Path)
    args = parser.parse_args()
    data = json.dumps(verify(), indent=2)+'\n'
    if args.output:
        args.output.write_text(data)
    else:
        print(data, end='')
