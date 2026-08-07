#!/usr/bin/env python3
"""Regenerate the deterministic outer SHA-256 integrity manifest."""
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
    rows=[f'{digest(p)}  {p.relative_to(ROOT)}' for p in sorted(ROOT.rglob('*')) if tracked(p)]
    MAN.write_text('\n'.join(rows)+'\n')
    print(f'OUTER MANIFEST REGENERATED ({len(rows)} files)')
if __name__=='__main__': main()
