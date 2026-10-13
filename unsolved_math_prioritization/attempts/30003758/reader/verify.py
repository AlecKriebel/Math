#!/usr/bin/env python3
"""Check this source-scope reader's integrity and declared safeguards, not proofs."""
import ast
import hashlib
import json
from pathlib import Path
import re
import sys
from urllib.parse import urlparse

ROOT = Path(__file__).resolve().parent
FILES = {
    'README.md', 'RESEARCH_LOG.md', 'SCOPE_AUDIT.md',
    'SCOPE_RECORD.json', 'SOURCE_INSPECTION.json', 'verify.py', 'MANIFEST.json',
}
CHECKS = 0


def require(condition, message):
    global CHECKS
    CHECKS += 1
    if not condition:
        raise ValueError(message)


def read_json(name):
    return json.loads((ROOT / name).read_text(encoding='utf-8'))


def main():
    children = list(ROOT.iterdir())
    require({p.name for p in children} == FILES, 'Unexpected or missing package entry')
    require(all(p.is_file() and not p.is_symlink() for p in children),
            'Every package entry must be a regular, non-symlink file')
    require(sum(p.stat().st_size for p in children) < 40000, 'Package unexpectedly large')
    manifest = read_json('MANIFEST.json')
    require(manifest['schema_version'] == 1, 'Unexpected manifest schema')
    require(manifest['problem_id'] == 30003758, 'Manifest target mismatch')
    entries = manifest['files']
    names = [item['path'] for item in entries]
    require(len(names) == len(set(names)), 'Duplicate manifest entries')
    require(set(names) == FILES - {'MANIFEST.json'}, 'Manifest coverage mismatch')
    for item in entries:
        require('/' not in item['path'] and '\\' not in item['path'], 'Non-flat manifest path')
        data = (ROOT / item['path']).read_bytes()
        require(type(item['bytes']) is int and item['bytes'] == len(data),
                'Byte-count mismatch: ' + item['path'])
        require(item['sha256'] == hashlib.sha256(data).hexdigest(),
                'SHA-256 mismatch: ' + item['path'])

    record = read_json('SCOPE_RECORD.json')
    expected = {
        'schema_version': 1, 'problem_id': 30003758, 'source_code': 'OWR-15999-007',
        'queue_row': 1768, 'recommended_status': 'deferred',
        'readiness_cleared': False, 'original_question_preserved': True,
        'replacement_formalization_adopted': False,
        'new_substantive_proof_passes': 0, 'lifetime_proof_passes': 'unknown',
        'proof_search_performed': False, 'published_proofs_independently_audited': False,
        'published_paper_error_alleged': False,
        'acceptance_scope': 'source interpretation and readiness hold only',
        'global_openness_certified': False, 'exhaustive_literature_search_claimed': False,
        'source_sampling': 'uniform fixed-size subset',
        'later_theorem_sampling': 'independent Bernoulli', 'sampling_transfer_proved': False,
        'mathematical_resolution_completion_percent': None,
    }
    for key, value in expected.items():
        require(key in record and type(record[key]) is type(value) and record[key] == value,
                'Scope guard mismatch: ' + key)

    inspection = read_json('SOURCE_INSPECTION.json')
    require(inspection['problem_id'] == 30003758, 'Source record target mismatch')
    require(inspection['proof_audit_performed'] is False, 'Proof audit overclaim')
    sources = inspection['sources']
    expected_sources = {
        'owr2018': ('PDF', 3669431, 'bd4ea3dd8d02a9164097c3490fad5c59e47bad52eb3407d2b5434bfb2b5bfb48'),
        'mixon2017': ('PDF', 331910, '1b1a1bcc71818630b4e967089a3fc657a2d6daf0324473acca8b0457dc5faba2'),
        'zhuang2022': ('PDF', 750727, '684b2f1d75898d3acf4d47d5d8140a3de41ce7b127d3c03f917a6b908ba1133d'),
        'clum2024': ('HTML', 352802, 'ec7c932e690777559bbcbb98fe9695dad2b4d9ace7d1c3a1b7885d58d781f654'),
        'clum_arxiv2022': ('PDF', 735992, 'eba49c65e79e595c5e716c960cb0f00b0ac7f4b95c424fd6f85342fc1481177c'),
    }
    require(len(sources) == len(expected_sources), 'Source count mismatch')
    require({s['id'] for s in sources} == set(expected_sources), 'Source identities mismatch')
    hosts = {'ems.press', 'doi.org', 'arxiv.org', 'proceedings.mlr.press',
             'academic.oup.com', 'oup.silverchair-cdn.com'}
    for source in sources:
        fmt, size, digest = expected_sources[source['id']]
        data = source['retrieved_bytes']
        require((data['format'], data['bytes'], data['sha256']) == (fmt, size, digest),
                'Retrieved-source metadata mismatch: ' + source['id'])
        require(source['inspection_date_utc'] == '2026-10-13', 'Inspection date mismatch')
        require(bool(source['location_inspected']) and bool(source['inspection']),
                'Missing inspection limit or location')
        require(bool(source['public_urls']), 'Missing public source URL')
        for url in source['public_urls']:
            parsed = urlparse(url)
            require(parsed.scheme == 'https' and parsed.hostname in hosts
                    and not parsed.username and not parsed.password,
                    'Unexpected source URL')

    audit = (ROOT / 'SCOPE_AUDIT.md').read_text(encoding='utf-8')
    quotations = re.findall(r'^> (.+)$', audit, re.MULTILINE)
    require(len(quotations) == 1, 'Expected exactly one short historical-question quotation')
    require(len(quotations[0].split()) <= 25, 'Historical quotation exceeds 25 words')
    require(hashlib.sha256(quotations[0].encode('utf-8')).hexdigest() ==
            'e9b440a35b174a272667b4011abbee2322d4f66464c39f10be5fd7fc7c6cd6a4', 'Historical-question wording changed')
    require('independent Bernoulli' in audit and 'fixed-size' in audit,
            'Missing sampling-law distinction')
    require('No published-paper\nerror is alleged.' in audit, 'Missing non-allegation limit')
    require('proofs were not independently audited' in audit, 'Missing proof-audit limit')
    require('readiness remains uncleared' in audit, 'Readiness overclaim')

    text = '\n'.join(p.read_text(encoding='utf-8') for p in children if p.name != 'verify.py')
    forbidden = ('/workspace/', '/tmp/', 'private/', 'chatgpt.com/c/', 'codex://')
    for marker in forbidden:
        require(marker not in text, 'Nonpublic coordination marker found')
    tree = ast.parse((ROOT / 'verify.py').read_text(encoding='utf-8'))
    require(not any(isinstance(node, ast.Assert) for node in ast.walk(tree)),
            'Verifier must not use optimization-removable assertions')
    print(json.dumps({
        'ok': True, 'checks': CHECKS, 'optimization_level': sys.flags.optimize,
        'scope': 'Package integrity and declared scope safeguards only; not mathematical verification',
    }, sort_keys=True))


if __name__ == '__main__':
    try:
        main()
    except (OSError, ValueError, KeyError, TypeError, IndexError) as error:
        print(json.dumps({'ok': False, 'checks': CHECKS, 'error': str(error)}, sort_keys=True))
        sys.exit(1)
