from pathlib import Path
import urllib.request, datetime, json, hashlib, os

D = Path(__file__).resolve().parent
(D / 'private_sources').mkdir(exist_ok=True)
records = []
for name in ['result-j.pdf', 'plan-j.pdf', 'list.pdf']:
    url = 'https://www.omu.ac.jp/orp/ocami/people/researchers/pdf/researcher/2011/Kuriya/' + name
    row = {'URL': url, 'UTC_start': datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'operator_PID': os.getpid(), 'locator': 'Actual institution-linked URL'}
    try:
        with urllib.request.urlopen(url, timeout=15) as response:
            data = response.read()
            row.update({'HTTP_status': response.status, 'final_URL': response.url,
                        'true_content_type': response.headers.get('Content-Type'),
                        'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest(),
                        'PDF_magic': data.startswith(b'%PDF-')})
            (D / 'private_sources' / name).write_bytes(data)
    except Exception as error:
        row.update({'retrieval_failed': True, 'error_type': type(error).__name__,
                    'error': str(error), 'source_read': False})
    row['UTC_end'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    records.append(row)
(D / 'OSAKA_NATIVE_RETRIEVAL.json').write_text(json.dumps(records, indent=2) + '\n')
print(json.dumps(records))
