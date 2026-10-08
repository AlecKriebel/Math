#!/usr/bin/env python3
"""Strict, offline arithmetic and frozen-byte audit. No theorem is proved here.

Default portable mode checks authored payload pins and arithmetic only; it explicitly
reports every source check as skipped. Source-backed mode requires every pinned
PDF, historical web capture, and corpus file. No dataset or source text is emitted.
Exit 0: requested checks passed; 1: mismatch/error; 2: required inputs missing.
"""
import argparse
from fractions import Fraction as F
import hashlib
import json
from pathlib import Path
import sys

PINS = {
    'REPORT.md': (7763, '441611b3a286a813d2684af06a09886c754e67a9d53f425205cbf31750bc8738'),
    'SCOPE_ADDENDUM.md': (4348, '9137ab45499acf2b1899c16aa824b6e952ff6ce2cf54cfe8a434b1b7e6af9fc8'),
    'SOURCE_MANIFEST.json': (2562, 'e8bb7b4db0621f0893957e25600a77efb9954dc6404638954f264df7beac6db2'),
    'PROVENANCE_ADDENDUM.json': (1345, 'a795b7f95a605a4a28249009091b0378d18bd3c710a496af382e4e1755b75dfc'),
    'verify.py': (1484, '364bd337f07ecb19fdb845166ce3e8521fa0373c735576f94e416cb50bddbb4d'),
    'CHECK_RESULTS.json': (395, 'bd0911ffcdbb97dd51d55b34e9b841dc112d2bf3131e9f0ccba28cf0b8614932'),
}
CAPTURE_FILES = ('hr_experimental.html', 'rowan_author_page.html')


def inspect_file(name, path, size, digest, skipped=False):
    out = {'name': name, 'expected_bytes': size, 'expected_sha256': digest}
    if skipped:
        out['status'] = 'SKIPPED_PORTABLE_MODE'
    elif path is None or not path.is_file():
        out['status'] = 'MISSING_REQUIRED_INPUT'
    else:
        data = path.read_bytes()
        out.update(actual_bytes=len(data), actual_sha256=hashlib.sha256(data).hexdigest())
        out['status'] = 'MATCH' if (len(data), out['actual_sha256']) == (size, digest) else 'MISMATCH'
    return out


def arithmetic():
    count = 0
    for den in range(3, 61):
        for num in range(den // 2 + 1, den):
            H = F(num, den)
            for q in (F(201, 100), F(21, 10), F(5, 2), F(3), F(4), F(10), F(1000), None):
                iq = F(0) if q is None else 1 / q
                A = 1 - 1 / (2 * H)
                S = 1 - 1 / H + iq / H
                alpha = (max(F(0), S) + A) / 2
                if not (A - S == (F(1, 2) - iq) / H and 0 < alpha < A < F(1, 2)
                        and alpha > S and 1 - H - iq + H * alpha > 0):
                    raise ValueError('General rational parameter check failed')
                count += 1
    H, q, alpha = F(3, 4), F(4), F(1, 6)
    witness = (1 - 1 / H + 1 / (H * q), 1 - 1 / (2 * H), 1 - H - 1 / q + H * alpha)
    if witness != (0, F(1, 3), F(1, 8)):
        raise ValueError('Explicit witness failed')
    H, alpha = F(1, 4), F(-11, 10)
    product = (1 + alpha * H) * (alpha + 1 / (2 * H))
    if not (1 - 1 / (2 * H) == -1 and F(1, 2) - 1 / (2 * H) == F(-3, 2)
            and F(-3, 2) < alpha < -1 and product == F(261, 400) > F(1, 2)):
        raise ValueError('Restricted one-dimensional positive example failed')
    return {'status': 'PASS', 'rational_parameter_tests': count,
            'explicit_witness': {'H': '3/4', 'q': '4', 'alpha': '1/6', 'S': '0', 'A': '1/3', 'scaling_exponent': '1/8'},
            'BM_restricted_example': {'H': '1/4', 'alpha': '-11/10', 'product': '261/400'}}


def corpus_gate(directory, manifest):
    problems = json.loads((directory / 'problems.json').read_text())
    reports = json.loads((directory / 'research_results.json').read_text())
    target = json.loads((directory / '30005030.json').read_text())
    gate = manifest['prior_gate']
    terms = gate['search_terms']
    pc = sum(any(t in json.dumps(p, ensure_ascii=False).lower() for t in terms) for p in problems)
    rc = sum(any(t in json.dumps(r, ensure_ascii=False).lower() for t in terms) for r in reports.values())
    exact = 'OWR-9790360-001' in reports
    valid = (len(problems) == gate['problem_records'] and len(reports) == gate['research_reports']
             and pc == gate['screened_candidate_problem_count'] and rc == gate['screened_candidate_report_count']
             and exact == gate['exact_prior_report'] == False
             and target['problem']['id'] == 30005030 and target.get('research') is None)
    return {'status': 'PASS' if valid else 'MISMATCH', 'problem_records': len(problems),
            'research_reports': len(reports), 'term_matched_problem_count': pc,
            'term_matched_report_count': rc, 'exact_prior_report_present': exact,
            'limitation': 'Term-search counts and exact-record absence only; no exhaustive semantic novelty guarantee.'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--mode', choices=('portable', 'source-backed'), default='portable')
    parser.add_argument('--source-dir', type=Path, help='Directory containing the five pinned PDF/web files')
    parser.add_argument('--corpus-dir', type=Path, help='Directory containing the three pinned corpus files')
    args = parser.parse_args()
    root = Path(__file__).resolve().parent
    out = {'audit_schema': 1, 'mode': args.mode,
           'scope': 'Exact arithmetic, frozen payload identity, and (only if requested) supplied source bytes and corpus term counts. No theorem proof, peer review, historical retrieval attestation, or exhaustive literature search.',
           'checker_sha256': hashlib.sha256(Path(__file__).read_bytes()).hexdigest()}
    out['payload_checks'] = [inspect_file(n, root / n, size, sha) for n, (size, sha) in PINS.items()]
    out['arithmetic'] = arithmetic()
    if any(x['status'] != 'MATCH' for x in out['payload_checks']):
        out['status'] = 'FAIL_PAYLOAD_IDENTITY'
        print(json.dumps(out, indent=2))
        return 1
    manifest = json.loads((root / 'SOURCE_MANIFEST.json').read_text())
    provenance = json.loads((root / 'PROVENANCE_ADDENDUM.json').read_text())
    source_dir = args.source_dir or root.parent / 'private_sources'
    skip = args.mode == 'portable'
    checks = []
    for src in manifest['downloaded_sources']:
        checks.append(inspect_file(src['local_basename'], source_dir / src['local_basename'], src['bytes'], src['sha256'], skip))
    for name, src in zip(CAPTURE_FILES, provenance['additional_web_captures']):
        checks.append(inspect_file(name, source_dir / name, src['bytes'], src['sha256'], skip))
    for name, src in manifest['corpus_checks'].items():
        p = None if args.corpus_dir is None else args.corpus_dir / name
        checks.append(inspect_file(name, p, src['bytes'], src['sha256'], skip))
    out['source_checks'] = checks
    out['source_checks_complete'] = all(x['status'] == 'MATCH' for x in checks)
    out['corpus_gate'] = {'status': 'SKIPPED_PORTABLE_MODE' if skip else 'NOT_RUN_REQUIRED_INPUTS_MISSING_OR_MISMATCHED'}
    if skip:
        out['status'] = 'PASS_ARITHMETIC_AND_PAYLOAD_ONLY'
        code = 0
    elif any(x['status'] == 'MISMATCH' for x in checks):
        out['status'] = 'FAIL_SOURCE_MISMATCH'
        code = 1
    elif not out['source_checks_complete']:
        out['status'] = 'INCOMPLETE_REQUIRED_SOURCES'
        code = 2
    else:
        out['corpus_gate'] = corpus_gate(args.corpus_dir, manifest)
        code = 0 if out['corpus_gate']['status'] == 'PASS' else 1
        out['status'] = 'PASS_ARITHMETIC_PAYLOAD_AND_SUPPLIED_SOURCE_HASHES' if code == 0 else 'FAIL_CORPUS_GATE'
    print(json.dumps(out, indent=2))
    return code


if __name__ == '__main__':
    try:
        sys.exit(main())
    except (OSError, ValueError, KeyError, TypeError) as error:
        print(json.dumps({'status': 'FAIL_INPUT_OR_CHECK_ERROR', 'error_type': type(error).__name__,
                          'scope': 'No successful verification is asserted.'}))
        sys.exit(1)
