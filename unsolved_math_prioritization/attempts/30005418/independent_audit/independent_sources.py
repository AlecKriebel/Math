#!/usr/bin/env python3
"""Independently validate full external sources, emitting verification metadata only.

Usage: python independent_sources.py AUTHOR_SAFE PROBLEMS REPORTS CATALOG PDF_DIR
The five inputs remain external and are never copied into the audit package.
"""
import hashlib
import json
import pathlib
import sys

if not __debug__:
    raise SystemExit('Assertions must be enabled.')

def metadata(b):
    return {'bytes': len(b), 'sha256': hashlib.sha256(b).hexdigest()}

def main():
    if len(sys.argv) != 6:
        raise SystemExit(__doc__)
    author, problems, reports, catalog, pdf_dir = map(pathlib.Path, sys.argv[1:])
    source_metadata = json.loads((author/'SOURCES.json').read_text())
    inputs = {}
    documents = []
    for name, path in [('problems.json', problems), ('research_results.json', reports), ('catalog.json', catalog)]:
        data = path.read_bytes()
        actual = metadata(data)
        assert actual == source_metadata['dataset']['files'][name], name
        inputs[name] = dict(actual, match=True)
        documents.append(json.loads(data))
    P, R, C = documents
    assert len(P) == 15458 and len(R) == 6701 and len(C) == 15458
    selected = [r for r in P if str(r['id']) == '30005418']
    indexed = [r for r in C if str(r['id']) == '30005418']
    assert len(selected) == len(indexed) == 1
    p, c = selected[0], indexed[0]
    assert p['problem_number'] == c['problem_number'] == 'OWR-12697689-014'
    assert sum(r['problem_number'] == p['problem_number'] for r in P) == 1
    assert p['problem_number'] not in R
    assert c['rank'] == 797
    sh = hashlib.sha256(p['statement'].encode('utf-8')).hexdigest()
    rh = hashlib.sha256(json.dumps([p, {}], sort_keys=True).encode('utf-8')).hexdigest()
    assert sh == c['statement_hash'] == source_metadata['dataset']['statement_hash']
    assert rh == c['review_hash'] == source_metadata['dataset']['review_hash']
    b = catalog.read_bytes()
    git_sha = hashlib.sha1(b'blob '+str(len(b)).encode('ascii')+b'\0'+b).hexdigest()
    assert git_sha == source_metadata['dataset']['catalog_git_blob']
    pdfs = []
    for ref in source_metadata['sources']:
        b = (pdf_dir/ref['filename']).read_bytes()
        assert b.startswith(b'%PDF-')
        actual = metadata(b)
        assert actual == ref['pdf'], ref['filename']
        pdfs.append({'title': ref['title'], 'url': ref['url'], **actual, 'match': True})
    result = {'status': 'PASS', 'problem_id': 30005418, 'rank': 797,
              'record_count': len(P), 'prior_report_count': len(R), 'catalog_count': len(C),
              'selected_id_count': 1, 'selected_problem_number_count': 1,
              'selected_prior_report_present': False, 'statement_hash': sh, 'review_hash': rh,
              'catalog_git_blob': git_sha, 'full_corpus_inputs': inputs, 'scholarly_pdfs': pdfs,
              'limits': 'This program verifies bytes and joins. The audit report separately records source inspection.'}
    print(json.dumps(result, indent=2, sort_keys=True, ensure_ascii=False))

if __name__ == '__main__':
    main()
