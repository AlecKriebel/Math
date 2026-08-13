#!/usr/bin/env python3
from __future__ import annotations
from hashlib import sha256
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
MAN=ROOT/'MANIFEST.sha256'
EXCLUDED={'MANIFEST.sha256','AUTHOR_READY_RELEASE.zip','AUTHOR_READY_RELEASE.sha256'}
AUX={'.pyc','.aux','.bcf','.blg','.fdb_latexmk','.fls','.log','.out'}
TRANSIENT_BINARIES={'regenerate_directed_pair_universe','regenerate_signature_relation','review_directed_pair_universe','review_multitriangle_exclusion'}
def tracked(p: Path) -> bool:
    rel=p.relative_to(ROOT)
    return (p.is_file() and str(rel) not in EXCLUDED
            and (not rel.parts or rel.parts[0] != 'transcripts')
            and '__pycache__' not in rel.parts
            and p.suffix not in AUX and not p.name.endswith('.run.xml')
            and p.name not in TRANSIENT_BINARIES)
def digest(p: Path) -> str:
    h=sha256()
    with p.open('rb') as f:
        for block in iter(lambda:f.read(1<<20),b''): h.update(block)
    return h.hexdigest()
def main() -> None:
    expected={}
    for line in MAN.read_text().splitlines():
        d,r=line.split('  ',1); assert r not in expected; expected[r]=d
    actual={str(p.relative_to(ROOT)):digest(p) for p in ROOT.rglob('*') if tracked(p)}
    assert actual==expected,(
        sorted(set(actual)-set(expected)),sorted(set(expected)-set(actual)),
        [(k,expected[k],actual[k]) for k in expected.keys()&actual.keys() if expected[k]!=actual[k]][:5])
    print(f'ALL OUTER ARCHIVE INTEGRITY CHECKS PASSED ({len(actual)} files)')
if __name__=='__main__': main()
