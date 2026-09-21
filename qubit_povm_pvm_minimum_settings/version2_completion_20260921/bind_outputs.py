#!/usr/bin/env python3
"""Bind the reviewed PDFs, LaTeX archive, proof snapshot and final source ZIP.

Run only after a complete successful clean-extraction reproduction. This does
not publish a release and does not itself check a Lean proof.
"""
from __future__ import annotations
import argparse
import gzip
import hashlib
import io
import json
from pathlib import Path
import shutil
import tarfile


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('stage', type=Path)
    parser.add_argument('reproduction', type=Path, help='successful wrapper receipt.json')
    parser.add_argument('output', type=Path)
    args = parser.parse_args()
    stage, out = args.stage.resolve(), args.output.resolve()
    receipt = json.loads(args.reproduction.read_text())
    if receipt.get('status') != 'passed':
        raise ValueError('A complete successful reproduction is required')
    kernel = receipt['lean_receipt']['kernel_report']
    if kernel['status'] != 'passed' or not kernel['all_project_source_kernel_checked']:
        raise ValueError('The complete project was not checked')
    out.mkdir(parents=True, exist_ok=True)
    for source, name in [('main.pdf', 'Minimum_Bell_Setting_Complexity_v2.0.0.pdf'),
                         ('review.pdf', 'Minimum_Bell_Setting_Complexity_review_v2.0.0.pdf')]:
        shutil.copy2(stage/'paper'/source, out/name)
    source_tar = out/'qubit-povm-pvm-latex-v2.0.0.tar.gz'
    with source_tar.open('wb') as stream, gzip.GzipFile(fileobj=stream, mode='wb', mtime=0) as gz:
        with tarfile.open(fileobj=gz, mode='w') as tar:
            inputs = sorted(p for p in (stage/'paper').rglob('*')
                            if p.is_file() and p.suffix in {'.tex', '.bib', '.sty', '.sh'})
            for path in inputs + [stage/'LICENSE']:
                name = path.relative_to(stage/'paper').as_posix() if path.parent != stage else path.name
                data = path.read_bytes()
                info = tarfile.TarInfo('qubit-povm-pvm-latex-v2.0.0/'+name)
                info.size = len(data)
                info.mode = path.stat().st_mode & 0o777
                info.mtime = 0
                tar.addfile(info, io.BytesIO(data))
    snapshot = out/'proof_source_snapshot.json'
    verified_root = args.reproduction.resolve().parents[2]
    snapshot_source = verified_root/'bell_lean'/kernel['logs_directory']/'source_snapshot.json'
    if json.loads(snapshot_source.read_text()) != kernel['source_snapshot']:
        raise ValueError('Run-specific proof snapshot differs from the kernel receipt')
    shutil.copy2(snapshot_source, snapshot)
    shutil.copy2(args.reproduction, out/'final_reproduction_receipt.json')
    archive = out/'qubit-povm-pvm-v2.0.0.zip'
    if not archive.is_file():
        raise ValueError('Final source ZIP is missing')
    protected = kernel['source_snapshot']
    for name, expected in protected.items():
        if sha(stage/'bell_lean'/name) != expected:
            raise ValueError(f'Stage differs from verified proof input: {name}')
    binding = {'version': '2.0.0', 'published': False, 'new_doi': None,
               'verified_run_id': kernel['run_id'], 'protected_inputs': len(protected),
               'shipment_manifest_sha256': sha(stage/'SHA256SUMS.txt'),
               'reproduction_shipment_manifest_sha256': receipt['shipment_manifest_sha256'],
               'files': {p.name: {'sha256': sha(p), 'bytes': p.stat().st_size}
                         for p in sorted(out.iterdir()) if p.is_file()
                         and p.name not in {'BINDINGS.json', 'SHA256SUMS.txt'}},
               'trust_boundary': receipt['trust_boundary']}
    if binding['shipment_manifest_sha256'] != binding['reproduction_shipment_manifest_sha256']:
        raise ValueError('Reproduction did not consume this exact final shipment')
    (out/'BINDINGS.json').write_text(json.dumps(binding, indent=2)+'\n')
    (out/'SHA256SUMS.txt').write_text(''.join(sha(p)+'  '+p.name+'\n' for p in sorted(out.iterdir())
                                           if p.is_file() and p.name != 'SHA256SUMS.txt'))
    print(json.dumps(binding, indent=2))


if __name__ == '__main__':
    main()
