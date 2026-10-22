#!/usr/bin/env python3
"""Exact author normalization specification; inputs are not distributed.

Usage: python3 normalize_statement.py primary-pdftotext-layout.txt selected.json
The selected JSON can be the one-record array or the selected record object.
Only digests and comparison metadata are printed, never source text.
"""
import hashlib
import json
import re
import sys
from pathlib import Path


def normalize(s):
    s = re.sub(r'-\s*\n\s*', '', s)
    s = s.replace('X 0', 'X PRIME').replace('X ′', 'X PRIME')
    s = re.sub(r'\s+', ' ', s).strip()
    s = re.sub(r'\s+([,.])', r'\1', s)
    return s


def check(primary_text, selected):
    start = primary_text.index('Problem 96 (')
    end = primary_text.index('Remark 32.', start)
    source_statement = primary_text[start:end].split('). ', 1)[1]
    if isinstance(selected, list):
        assert len(selected) == 1
        selected = selected[0]
    assert selected['id'] == 6200096
    dataset_statement = selected['statement']
    source_normal = normalize(source_statement)
    selected_normal = normalize(dataset_statement)
    assert source_normal == selected_normal
    sha = lambda s: hashlib.sha256(s.encode('utf-8')).hexdigest()
    assert sha(dataset_statement) == '8602f7430f7159f04b3b4ce4f6d7ef710dd623648f2d137689a107ebe22c5768'
    assert sha(source_normal) == '1a1b790520689277eebdd2e31d4f88c23c1f219f6bfc1d7b237bd77f4f3172ac'
    return {
        'target_id': 6200096,
        'exact_normalized_equality': True,
        'raw_selected_statement_sha256_utf8': sha(dataset_statement),
        'author_normalized_statement_sha256_utf8': sha(source_normal),
        'author_digest_reproduced': True,
        'source_contents_redistributed': False,
        'normalization_difference': "The original author normal form uses literal X PRIME; the audit uses a prime glyph. Different normal forms have different digests."
    }


if __name__ == '__main__':
    if len(sys.argv) != 3:
        raise SystemExit(__doc__)
    print(json.dumps(check(Path(sys.argv[1]).read_text(),
                           json.loads(Path(sys.argv[2]).read_text())),
                     indent=2, sort_keys=True))
