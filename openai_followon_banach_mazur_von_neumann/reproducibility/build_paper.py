#!/usr/bin/env python3
"""Build the standalone paper from a fresh directory without editing its source."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import shutil
import subprocess
import tempfile

def sha(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path(__file__).resolve().parents[1])
    parser.add_argument('--receipt', type=Path)
    parser.add_argument('--render', action='store_true', help='render every page with Poppler')
    args = parser.parse_args()
    root = args.root.resolve()
    source = root / 'manuscript/main.tex'
    before = sha(source)
    scratch = root / 'tmp'
    scratch.mkdir(exist_ok=True)
    work = Path(tempfile.mkdtemp(prefix='clean-publication-build-', dir=scratch))
    shutil.copyfile(source, work / 'main.tex')
    version = subprocess.run(['tectonic', '--version'], check=True, capture_output=True, text=True).stdout.strip()
    build = subprocess.run(['tectonic', '--chatter', 'minimal', '--outdir', str(work), str(work / 'main.tex')], capture_output=True, text=True)
    if build.returncode or 'Overfull' in build.stderr:
        raise RuntimeError('Build or layout failure: ' + build.stderr)
    if sha(source) != before:
        raise RuntimeError('Source changed while building')
    pdf = work / 'main.pdf'
    info = subprocess.run(['pdfinfo', str(pdf)], check=True, capture_output=True, text=True).stdout
    subprocess.run(['pdftotext', '-layout', str(pdf), str(work / 'paper.txt')], check=True)
    output = root / 'output/pdf/paper.pdf'
    output.parent.mkdir(parents=True, exist_ok=True)
    shutil.copyfile(pdf, output)
    rendered = []
    if args.render:
        subprocess.run(['pdftoppm', '-png', '-r', '105', str(output), str(work / 'page')], check=True, capture_output=True)
        rendered = sorted(str(p.relative_to(root)) for p in work.glob('page-*.png'))
    receipt = {
        'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'source_path': 'manuscript/main.tex', 'source_sha256': before,
        'pdf_path': 'output/pdf/paper.pdf', 'pdf_sha256': sha(output),
        'pdf_bytes': output.stat().st_size, 'build_runtime': version,
        'clean_build_exit': build.returncode, 'diagnostics': build.stderr,
        'pdfinfo': info, 'temporary_directory': str(work.relative_to(root)),
        'rendered_pages': rendered,
        'visual_inspection': 'not performed by this script; required separately',
        'formal_verification': False,
    }
    if args.receipt:
        args.receipt.parent.mkdir(parents=True, exist_ok=True)
        args.receipt.write_text(json.dumps(receipt, indent=2) + '\n')
    print(json.dumps(receipt, indent=2))

if __name__ == '__main__':
    main()
