import datetime
import hashlib
import json
import os
import pathlib
import subprocess
import urllib.request

D = pathlib.Path(__file__).resolve().parent
D.mkdir(parents=True, exist_ok=True)
url = 'https://arxiv.org/pdf/hep-th/0006169v4'
start = datetime.datetime.now(datetime.timezone.utc).isoformat()
request = urllib.request.Request(url, headers={'User-Agent': 'Independent mathematical literature audit'})
with urllib.request.urlopen(request, timeout=45) as response:
    body = response.read()
    record = {'requested_url': url, 'resolved_url': response.url,
              'HTTP_status': response.status, 'content_type': response.headers.get('Content-Type')}
if not body.startswith(b'%PDF-'):
    raise RuntimeError('Retrieved body is not an authenticated PDF')
pdf = D / 'zois2000v4.pdf'
pdf.write_bytes(body)
text_file = D / 'zois2000v4.txt'
process = subprocess.Popen(['/opt/homebrew/bin/pdftotext', '-layout', str(pdf), str(text_file)],
                           stdout=subprocess.PIPE, stderr=subprocess.PIPE)
out, err = process.communicate(timeout=45)
record.update({'start_UTC': start, 'end_UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(),
               'operator_PID': os.getpid(), 'extractor_PID': process.pid, 'extractor_exit': process.returncode,
               'PDF_bytes': len(body), 'PDF_sha256': hashlib.sha256(body).hexdigest(),
               'extracted_text_sha256': hashlib.sha256(text_file.read_bytes()).hexdigest(),
               'extractor_stdout': out.decode(), 'extractor_stderr': err.decode(),
               'third_party_full_text_private_only': True,
               'purpose': 'Check pre-2002 Godbillon-Vey/contact discussion for an exact covering tightness claim; do not infer priority from title or abstract.'})
(D / 'RETRIEVAL.json').write_text(json.dumps(record, indent=2) + '\n')
if process.returncode:
    raise RuntimeError('PDF extraction failed')
print(json.dumps(record, indent=2))
