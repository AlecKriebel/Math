#!/usr/bin/env python3
"""Read-only verifier for the pre-candidate PR329 source baseline.

Uses only the frozen own-namespace files and the single authorized original PDF.
Never creates receipts, changes files, reads candidate material, or uses network.
"""
from pathlib import Path
import hashlib
import json
import stat
import sys

N = Path(__file__).resolve().parent
M = N / 'SOURCE_ONLY_FREEZE.json'

def digest(b):
    return hashlib.sha256(b).hexdigest()

def check_row(row, external=False):
    if external:
        p = Path(row['path'])
    else:
        relative = Path(row['path'])
        assert not relative.is_absolute() and '..' not in relative.parts, row
        p = N / relative
    assert not p.is_symlink(), str(p)
    s = p.stat()
    assert stat.S_ISREG(s.st_mode), str(p)
    b = p.read_bytes()
    assert len(b) == row['bytes'], ('length', str(p))
    assert digest(b) == row['sha256'], ('sha256', str(p))
    assert stat.S_IMODE(s.st_mode) == row['mode_decimal'], ('mode', str(p))

def main():
    m = json.loads(M.read_text())
    assert m['schema'] == 'pr329-source-only-freeze-v1'
    assert m['candidate_exposure_gate'] == 'CLOSED'
    assert m['final_seal'] is False and m['publication_authorization'] is False
    rows = m['payloads']
    assert len({r['path'] for r in rows}) == len(rows)
    for row in rows:
        check_row(row)
    assert len(m['authorized_external_source_pins']) == 1
    for row in m['authorized_external_source_pins']:
        check_row(row, external=True)
    pins = json.loads((N / 'SOURCE_PINS.json').read_text())
    orig = Path(pins['provided_original']['path']).read_bytes()
    current = (N / pins['current_official']['path']).read_bytes()
    assert orig == current
    assert digest(orig) == '8b64d2f6b91f791c35afae10b2ef79c15a927a94c2142a56386f80c8b8a596e6'
    assert len(orig) == 502057
    http = json.loads((N / 'private_source_evidence/official_current.http_stdout').read_text())
    assert http['http_code'] == 200 and http['exitcode'] == 0
    assert http['url_effective'] == pins['current_official']['url']
    for receipt_path in pins['native_receipt_paths']:
        receipt = json.loads((N / receipt_path).read_text())
        assert receipt['exit_code'] == 0, receipt_path
        assert receipt['started_utc'] <= receipt['finished_utc'], receipt_path
    text = (N / 'private_source_evidence/question17_physical51.layout.txt').read_text()
    assert 'Problem/Question 17.' in text and 'Compute the 5-torsion of E.' in text
    assert all(mark in text for mark in ['(i)', '(ii)', '(iii)', '(iv)'])
    assert 'Problem/Question 16.' in text and 'Problem/Question 18.' in text
    reading = json.loads((N / 'READING_RECORD.json').read_text())
    assert reading['candidate_mathematics_read'] is False
    assert reading['post_source_literature_read'] is False
    assert reading['whole_pdf_read_claimed'] is False
    print(json.dumps({'result':'PASS','own_payloads_verified':len(rows),
      'authorized_external_source_pins_verified':1,'official_original_byte_equality':True,
      'candidate_exposure_gate':'CLOSED','final_seal':False,
      'scope':'integrity and source-operation facts; not correctness, novelty, priority or reading certification'},indent=2))

if __name__ == '__main__':
    try:
        main()
    except Exception as e:
        print('FAIL: ' + repr(e), file=sys.stderr)
        raise
