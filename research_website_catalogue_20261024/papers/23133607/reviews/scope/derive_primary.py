#!/usr/bin/env python3
"""Explicit document-only derivatives; never imports/executes scientific code."""
from pathlib import Path
import datetime
import hashlib
import json
import subprocess
import sys

A = Path(__file__).resolve().parent

def pin(path):
    body = path.read_bytes()
    return {'path': str(path.relative_to(A)), 'bytes': len(body), 'SHA256': hashlib.sha256(body).hexdigest()}

def main():
    if sys.argv[1:] != ['--derive']:
        print('Inert default; --derive explicitly creates document-only derivatives.')
        return
    D = A / 'primary-derived'
    D.mkdir(exist_ok=False)
    receipts = []
    def run(label, argv, inputs, outputs):
        start = datetime.datetime.now(datetime.timezone.utc).isoformat()
        process = subprocess.run(argv, cwd=A, capture_output=True)
        stdout = D / (label + '.stdout')
        stderr = D / (label + '.stderr')
        stdout.write_bytes(process.stdout)
        stderr.write_bytes(process.stderr)
        receipts.append({'started_UTC': start, 'completed_UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                         'argv': argv, 'exit': process.returncode, 'stdout': pin(stdout), 'stderr': pin(stderr),
                         'inputs': [pin(p) for p in inputs], 'outputs': [pin(p) for p in outputs if p.exists()]})
        (D / 'DERIVATION_RECEIPTS.json').write_text(json.dumps(receipts, indent=2) + '\n')
        if process.returncode:
            raise RuntimeError('document derivative failed; exact streams preserved')
    ps = A / 'primary/Oort-author-PS-hop0.body'
    pdf = D / 'Oort-author.pdf'
    run('Oort-PS-render', ['gs', '-dSAFER', '-dBATCH', '-dNOPAUSE', '-sDEVICE=pdfwrite', '-sOutputFile=' + str(pdf), '-f', str(ps)], [ps], [pdf])
    pairs = [('Hoshi', A/'primary/Hoshi-revised2021-hop0.body'),
             ('Fontaine-Laffaille', A/'primary/Fontaine-Laffaille-PDF-hop0.body'),
             ('Takao-report', A/'primary/Takao-OWR42-PDF-hop0.body'),
             ('Pries-Ulmer', A/'primary/Pries-Ulmer-hop0.body'), ('Oort', pdf)]
    for label, source in pairs:
        run(label+'-pdfinfo', ['pdfinfo', str(source)], [source], [])
        text = D / (label + '-all.txt')
        run(label+'-text', ['pdftotext', '-layout', str(source), str(text)], [source], [text])
    print(json.dumps({'document_derivatives_only': True, 'scientific_programmes_executed': [], 'receipts': len(receipts)}))

if __name__ == '__main__':
    main()
