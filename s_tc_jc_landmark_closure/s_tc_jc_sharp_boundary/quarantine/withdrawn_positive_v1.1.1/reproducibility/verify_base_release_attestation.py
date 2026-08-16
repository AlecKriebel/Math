#!/usr/bin/env python3
"""Verify the unchanged hash-locked base statistical release and its clean replay.

The publication strengthening adds only the automatic-triangle graph theorem.
The expensive base full-adversarial replay is preserved byte-for-byte from the
previous author-ready release; this verifier checks its transcript and every
file listed by the base release's internal manifest.
"""
from __future__ import annotations
from hashlib import sha256
from pathlib import Path

ROOT=Path(__file__).resolve().parents[1]
BASE=ROOT/'reproducibility'/'exact_release'
TRANSCRIPT=ROOT/'transcripts'/'base_release_full_adversarial_verification.txt'
PUBLICATION_MANIFEST=ROOT/'reproducibility'/'publication_base_manifest.sha256'
EXPECTED_TRANSCRIPT='92a5788165b71fb5cb3c2fd6482cb0641b51568840e3fc0a85a2627abe184ada'
EXPECTED_MANIFEST='4192dcf0c7c7207188114bde3018a2abb8a4ce8d6e2f58ef97b5b7af459ee520'

def digest(path: Path) -> str:
    h=sha256()
    with path.open('rb') as stream:
        for block in iter(lambda:stream.read(1<<20),b''):
            h.update(block)
    return h.hexdigest()

def main() -> None:
    manifest=BASE/'MANIFEST.sha256'
    assert digest(manifest)==EXPECTED_MANIFEST
    for line in manifest.read_text().splitlines():
        expected,relative=line.split('  ',1)
        path=BASE/relative
        assert path.is_file(),relative
        assert digest(path)==expected,(relative,expected,digest(path))
    assert digest(TRANSCRIPT)==EXPECTED_TRANSCRIPT

    for line in PUBLICATION_MANIFEST.read_text().splitlines():
        expected,relative=line.split('  ',1)
        path=ROOT/relative
        assert path.is_file(),relative
        assert digest(path)==expected,(relative,expected,digest(path))
    text=TRANSCRIPT.read_text(errors='replace')
    assert 'AUTHOR-READY FULL INDEPENDENT VERIFICATION PASSED' in text
    full=(BASE/'full_adversarial_verification_output.txt').read_text(errors='replace')
    assert '"full_adversarial_replay": true' in full
    assert '"status": "ALL EXACT CHECKS PASSED"' in full
    print('HASH-LOCKED BASE STATISTICAL AND PUBLICATION FULL-ADVERSARIAL ATTESTATION PASSED')

if __name__=='__main__': main()
