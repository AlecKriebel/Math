#!/usr/bin/env python3
"""Parent integrity/schema/source-custody readback; never executes peer code."""
from pathlib import Path
from datetime import datetime, timezone
import hashlib
import json

BASE = Path(__file__).resolve().parent

def require(ok, why):
    if not ok:
        raise ValueError(why)

def pairs(items):
    result = {}
    for key, value in items:
        require(key not in result, 'Duplicate JSON key: ' + key)
        result[key] = value
    return result

def read_json(path):
    return json.loads(path.read_text(), object_pairs_hook=pairs)

def digest(path):
    require(path.is_file() and not path.is_symlink(), 'Missing/unsafe file: ' + str(path))
    data = path.read_bytes()
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

def safe(root, relative):
    p = Path(relative)
    require(not p.is_absolute() and '..' not in p.parts, 'Escaping path')
    path = root / p
    require(path.resolve().is_relative_to(root.resolve()), 'Escaping resolved path')
    require(not any((root / Path(*p.parts[:i])).is_symlink() for i in range(1, len(p.parts)+1)), 'Symlink component')
    return path

def main():
    out = BASE / 'PRIORITY_FAMILIES_READBACK.json'
    require(not out.exists(), 'Refuse to overwrite a readback')
    frozen = read_json(BASE / 'SOURCE_RECEIPT.json')
    expected_frozen = {
        x['path'].split('attempts/30002737/', 1)[1]:
        {'bytes': x['bytes'], 'sha256': x['sha256']}
        for x in frozen['files']
    }
    require(len(expected_frozen) == 12, 'Wrong frozen corpus')
    results = {}
    for name, seal_name, expected_seal in [
        ('priority_history', 'FINAL_SEAL.json', '97893927f43aab8f07db5330cc98e4e74f0fbcb2d9b3d0319ec18bd2d5bb65fe'),
        ('priority_constructions', 'SEAL.json', None),
    ]:
        root = BASE / 'reviews' / name
        seal_path = root / seal_name
        require(expected_seal is None or digest(seal_path)['sha256'] == expected_seal, 'Wrong communicated seal')
        seal = read_json(seal_path)
        public = read_json(root / 'PUBLIC_FILES.json')['files']
        require(len(public) == len(set(public)), 'Duplicate positive entry')
        require(len(public) == (25 if name == 'priority_history' else 27), 'Wrong positive count')
        payload = seal.get('public_payload')
        if payload is None:
            payload = {x['path']: {'bytes': x['bytes'], 'sha256': x['sha256']} for x in seal['public_file_hashes']}
            require(len(payload) == len(seal['public_file_hashes']), 'Duplicate seal entry')
        require(set(payload) == set(public) - {seal_name}, 'Incomplete positive seal')
        decoded = {}
        for relative in public:
            require('private_sources' not in Path(relative).parts and Path(relative).suffix not in {'.pdf', '.png', '.html'}, 'Foreign bytes in positive payload')
            path = safe(root, relative)
            actual = digest(path)
            if relative != seal_name:
                require(actual == payload[relative], 'Payload mismatch: ' + relative)
            text = path.read_text()
            if path.suffix == '.json':
                decoded[relative] = read_json(path)
            elif path.suffix == '.py':
                compile(text, str(path), 'exec')  # syntax check only; never execute
        source_count = 0
        if name == 'priority_history':
            inventory = decoded['receipts/PRIVATE_SOURCE_INVENTORY.json']['files']
            for relative, wanted in inventory.items():
                require(Path(relative).parts[0] == 'private_sources', 'Wrong private custody path')
                require(digest(safe(root, relative)) == wanted, 'Private-byte mismatch: ' + relative)
            source_count = len(inventory)
            for item in decoded['receipts/PRIMARY_SOURCE_LEDGER.json']:
                if 'file' in item:
                    require(digest(safe(root, item['file'])) == {'bytes': item['bytes'], 'sha256': item['sha256']}, 'Primary ledger mismatch')
            receipt = decoded['receipts/FROZEN_CORPUS_READ.json']
            binding = {x['path']: {'bytes': x['bytes'], 'sha256': x['sha256']} for x in receipt['artifacts']}
            require(binding == expected_frozen and all(x['read_in_full'] is True for x in receipt['artifacts']), 'History frozen binding mismatch')
            verdict = decoded['VERDICT.json']
            for k in ['blocking_findings', 'required_repairs', 'central_mathematical_gaps']:
                require(type(verdict[k]) is int and verdict[k] == len(verdict[k+'_details']), 'History finding schema mismatch')
            require([verdict[k] for k in ['blocking_findings', 'required_repairs', 'central_mathematical_gaps']] == [1, 1, 0], 'Wrong history interpretation')
            require(verdict['recommended_status'] == 'already_solved', 'Wrong recommendation')
            require(decoded['receipts/SPIN_FINITE_CHECKS.json']['source_error_bound_independently_reproduced'] is False, 'Unjustified certificate upgrade')
            report_path = root / 'REPORT.md'
        else:
            for relative, data in decoded.items():
                if not relative.endswith('SOURCE_RECEIPTS.json') and relative != 'PUBLISHED_SPIN_RETRY_RECEIPTS.json':
                    continue
                for item in data if isinstance(data, list) else [data]:
                    if 'error' in item:
                        require('sha256' not in item, 'Error mistaken for source')
                        continue
                    path = safe(root, item['private_path'])
                    require(Path(item['private_path']).parts[0] == 'private_sources', 'Wrong source custody')
                    require(digest(path) == {'bytes': item['bytes'], 'sha256': item['sha256']}, 'Source receipt mismatch')
                    source_count += 1
            receipt = decoded['FROZEN_READ_RECEIPT.json']
            binding = {x['path']: {'bytes': x['bytes'], 'sha256': x['sha256']} for x in receipt['files']}
            require(binding == expected_frozen and all(x['read_complete'] is True for x in receipt['files']), 'Construction frozen binding mismatch')
            verdict = decoded['RESULT.json']
            for k, details in [('priority_blocker_count', 'findings'), ('required_correction_count', 'required_corrections'), ('optional_improvement_count', 'optional_improvements')]:
                require(type(verdict[k]) is int and verdict[k] == len(verdict[details]), 'Construction finding schema mismatch')
            require(verdict['priority_blocker_count'] == 1 and verdict['required_correction_count'] == 1 and verdict['mathematical_correctness_reversal_count'] == 0, 'Wrong construction interpretation')
            require(verdict['independent_quadrature_certificate_count'] == 0 and verdict['source_numeric_evidence']['independently_certified'] is False, 'Unjustified numerical certificate')
            checks = decoded['AUDIT_VALIDATION.json']
            require(checks['check_count'] == len(checks['checks']) == 75 and all(x['pass'] is True for x in checks['checks']) and checks['failure_count'] == 0, 'Wrong artifact checks')
            report_path = root / 'PRIORITY_REPORT.md'
        results[name] = {
            'seal': digest(seal_path), 'report': digest(report_path),
            'positive_payload_count': len(public), 'frozen_binding_count': 12,
            'private_sources_byte_checked': source_count,
            'typed_priority_blockers': 1, 'typed_required_contextual_corrections': 1,
            'submitted_math_failure_found_by_family': False,
            'published_numerical_error_independently_certified_by_family': False,
            'all_positive_payloads_read_and_integrity_checked': True,
            'peer_code_executed': False,
        }
    result = {
        'read_at_utc': datetime.now(timezone.utc).isoformat(), 'families': results,
        'scope': 'Parent complete reports/code/logs and parsed structured-record readback, source byte custody and frozen binding. Not an approval for status mutation.',
        'foreign_content_read_limit': 'Parent inspected selected primary pages separately; byte inventory checks do not claim full reading of every downloaded foreign work.',
        'remaining': 'Fresh actual-hull classification adversary and rigorous historical-integral validation remain pending.',
        'reader_sha256': digest(Path(__file__))['sha256'],
    }
    out.write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
