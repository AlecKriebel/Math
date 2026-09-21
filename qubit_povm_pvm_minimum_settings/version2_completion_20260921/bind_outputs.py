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
import subprocess
import tarfile
import tempfile
import zipfile


def sha(path: Path) -> str:
    return hashlib.sha256(path.read_bytes()).hexdigest()


def verify_archive(stage: Path, archive: Path) -> None:
    prefix = 'qubit-povm-pvm-v2.0.0/'
    files = {prefix+p.relative_to(stage).as_posix(): p for p in stage.rglob('*') if p.is_file()}
    with zipfile.ZipFile(archive) as z:
        if z.testzip() is not None or len(z.namelist()) != len(set(z.namelist())):
            raise ValueError('ZIP CRC failure or duplicate member')
        if set(z.namelist()) != set(files):
            raise ValueError('ZIP membership differs from the verified stage')
        for name, path in files.items():
            if path.is_symlink() or z.read(name) != path.read_bytes():
                raise ValueError(f'ZIP content differs from stage: {name}')
        expected = {}
        for line in z.read(prefix+'SHA256SUMS.txt').decode().splitlines():
            digest, name = line.split('  ', 1)
            if name in expected or Path(name).is_absolute() or '..' in Path(name).parts:
                raise ValueError('Unsafe or duplicate shipment manifest entry')
            expected[name] = digest
        if set(files) != {prefix+n for n in expected} | {prefix+'SHA256SUMS.txt'}:
            raise ValueError('Embedded manifest has different membership')
        for name, digest in expected.items():
            if hashlib.sha256(z.read(prefix+name)).hexdigest() != digest:
                raise ValueError(f'Embedded manifest hash differs: {name}')


def rendered_pages(path: Path) -> list[str]:
    with tempfile.TemporaryDirectory(prefix='bell-pdf-binding-') as temporary:
        prefix = Path(temporary)/'page'
        subprocess.run(['pdftoppm', '-scale-to', '850', '-png', str(path), str(prefix)],
                       check=True, capture_output=True)
        pages = sorted(Path(temporary).glob('page-*.png'))
        if not pages:
            raise ValueError('No PDF pages rendered')
        return [sha(p) for p in pages]


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
    if sha(stage/'SHA256SUMS.txt') != receipt['shipment_manifest_sha256']:
        raise ValueError('Reproduction did not consume this exact final shipment')
    archive = out/'qubit-povm-pvm-v2.0.0.zip'
    verify_archive(stage, archive)
    verified_root = args.reproduction.resolve().parents[2]
    pdf_evidence = {}
    for name in ('main.pdf', 'review.pdf'):
        shipped, rebuilt = stage/'paper'/name, verified_root/'paper'/name
        if sha(rebuilt) != receipt['pdf_sha256'][name]:
            raise ValueError(f'Rebuilt PDF differs from reproduction receipt: {name}')
        shipped_pages, rebuilt_pages = rendered_pages(shipped), rendered_pages(rebuilt)
        if shipped_pages != rebuilt_pages:
            raise ValueError(f'Shipped and rebuilt PDF renderings differ: {name}')
        pdf_evidence[name] = {'shipped_sha256': sha(shipped), 'rebuilt_sha256': sha(rebuilt),
                              'byte_identical': sha(shipped) == sha(rebuilt),
                              'rendered_pages_identical': True, 'page_count': len(shipped_pages),
                              'png_page_sha256_at_850px': shipped_pages}
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
    snapshot_source = verified_root/'bell_lean'/kernel['logs_directory']/'source_snapshot.json'
    if json.loads(snapshot_source.read_text()) != kernel['source_snapshot']:
        raise ValueError('Run-specific proof snapshot differs from the kernel receipt')
    shutil.copy2(snapshot_source, snapshot)
    shutil.copy2(args.reproduction, out/'final_reproduction_receipt.json')
    protected = kernel['source_snapshot']
    for name, expected in protected.items():
        if sha(stage/'bell_lean'/name) != expected:
            raise ValueError(f'Stage differs from verified proof input: {name}')
    binding = {'version': '2.0.0', 'published': False, 'new_doi': None,
               'verified_run_id': kernel['run_id'], 'protected_inputs': len(protected),
               'shipment_manifest_sha256': sha(stage/'SHA256SUMS.txt'),
               'reproduction_shipment_manifest_sha256': receipt['shipment_manifest_sha256'],
               'archive_bytes_match_verified_stage': True,
               'pdf_rebuild_comparison': pdf_evidence,
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
