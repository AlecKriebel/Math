"""Pin the supplied article and extract a private read-only research copy."""
import datetime
import hashlib
import json
import os
from pathlib import Path
import subprocess
import tempfile

source = Path('/Users/alec/Downloads/Some-New-Results-on-Geometric-Transversals.pdf')
raw = source.read_bytes()
if not raw.startswith(b'%PDF-'):
    raise SystemExit('supplied file is not a PDF')
directory = Path(tempfile.mkdtemp(prefix='math-pr18-root-priority-', dir='/private/tmp'))
pdf = directory / 'supplied-article.pdf'
pdf.write_bytes(raw)
pdf.chmod(0o400)
info = subprocess.run(['/opt/homebrew/bin/pdfinfo', str(pdf)], capture_output=True, text=True, check=True)
text_path = directory / 'supplied-article.txt'
subprocess.run(['/opt/homebrew/bin/pdftotext', '-layout', str(pdf), str(text_path)], check=True)
text_path.chmod(0o400)
body = text_path.read_bytes()
receipt = {
    'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
    'pid': os.getpid(),
    'source_path': str(source),
    'pdf_bytes': len(raw),
    'pdf_sha256': hashlib.sha256(raw).hexdigest(),
    'private_pdf': str(pdf),
    'private_text': str(text_path),
    'text_bytes': len(body),
    'text_sha256': hashlib.sha256(body).hexdigest(),
    'pdfinfo': info.stdout,
    'redistribution': 'Private supplied article and text are outside the repository. No license or permission to redistribute is inferred.'
}
receipt_path = Path(__file__).parent / 'SUPPLIED_ARTICLE_RECEIPT.json'
if receipt_path.exists():
    raise SystemExit('receipt already exists; do not replace the historical observation')
receipt_path.write_text(json.dumps(receipt, indent=2) + '\n')
receipt_path.chmod(0o444)
print(json.dumps(receipt, indent=2))
