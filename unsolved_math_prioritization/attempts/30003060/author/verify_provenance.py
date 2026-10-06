#!/usr/bin/env python3
"""Optional full-byte source verification. Never imports package code or prints source text."""
import argparse
import hashlib
import json
from pathlib import Path
import sys


def need(condition, message):
    if not condition:
        raise RuntimeError(message)


def checked(path, expected):
    p = Path(path)
    need(p.is_file() and not p.is_symlink(), 'input must be a regular non-symlink file')
    b = p.read_bytes()
    need(len(b) == expected['bytes'], 'source byte count mismatch')
    need(hashlib.sha256(b).hexdigest() == expected['sha256'], 'source digest mismatch')
    return b


def main():
    need(sys.flags.isolated == 1 and sys.flags.optimize == 0, 'use normal isolated Python')
    ap = argparse.ArgumentParser()
    ap.add_argument('--catalog', required=True)
    ap.add_argument('--problems', required=True)
    ap.add_argument('--reports', required=True)
    ap.add_argument('--pdf', action='append', default=[], metavar='SOURCE_ID=PATH')
    args = ap.parse_args()
    base = Path(__file__).resolve().parent
    selection = json.loads((base/'SELECTION_REVIEW.json').read_text())
    source = json.loads((base/'SOURCE_METADATA.json').read_text())
    loaded = {name: json.loads(checked(getattr(args, name), selection['complete_inputs'][name]))
              for name in ['catalog', 'problems', 'reports']}
    records = [r for r in loaded['problems'] if str(r['id']) == '30003060']
    need(len(records) == 1, 'target record must be unique')
    problem = records[0]
    report = loaded['reports'].get(problem['problem_number'], {})
    need(hashlib.sha256(problem['statement'].encode()).hexdigest() == selection['statement_sha256'],
         'statement digest mismatch')
    pair_sha = hashlib.sha256(json.dumps([problem, report], sort_keys=True).encode()).hexdigest()
    need(pair_sha == selection['complete_pair_review_sha256'], 'complete pair mismatch')
    need(report == {}, 'unexpected inherited report')
    cats = [r for r in loaded['catalog'] if str(r['id']) == '30003060']
    need(len(cats) == 1, 'catalog record must be unique')
    cat = cats[0]
    need(cat['rank'] == 865 and cat['turns_used'] == 0 and cat['local_status'] == 'queued',
         'unexpected original catalog status')
    need(cat['statement_hash'] == selection['statement_sha256'] and cat['review_hash'] == pair_sha,
         'catalog record is not bound to reviewed pair')
    by_id = {r['id']: r for r in source['sources']}
    verified = []
    for supplied in args.pdf:
        source_id, path = supplied.split('=', 1)
        need(source_id in by_id and 'pdf' in by_id[source_id], 'unknown PDF source identifier')
        checked(path, by_id[source_id]['pdf'])
        verified.append(source_id)
    print(json.dumps({'status': 'PASS', 'full_corpus_files': 3, 'target_records': 1,
                      'report_record_empty': True, 'statement_match': True,
                      'complete_pair_match': True, 'catalog_binding_match': True,
                      'pdf_ids_rehashed': sorted(verified),
                      'textual_inspection': 'NOT_PERFORMED_BY_THIS_HASH_CHECKER'},
                     sort_keys=True, indent=2))


if __name__ == '__main__':
    main()
