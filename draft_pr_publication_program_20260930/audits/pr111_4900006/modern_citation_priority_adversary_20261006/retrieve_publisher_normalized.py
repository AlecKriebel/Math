import datetime, hashlib, json, pathlib, subprocess, urllib.request

ROOT = pathlib.Path(__file__).resolve().parent
URLS = [
    ('zelik2008_normalized_data', 'https://data.aimsciences.org/aimsmath-upload/cpaa/2008/4/PDF/1534-0392_2008_4_971.pdf'),
    ('zelik2008_normalized_www', 'https://www.aimsciences.org/aimsmath-upload/cpaa/2008/4/PDF/1534-0392_2008_4_971.pdf'),
]
receipts = []
for name, url in URLS:
    item = {'name': name, 'url': url, 'started_UTC': datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        request = urllib.request.Request(url, headers={'User-Agent': 'IndependentMathAudit/1.0'})
        with urllib.request.urlopen(request, timeout=30) as response:
            body = response.read(30*1024*1024+1)
            if len(body) > 30*1024*1024:
                raise RuntimeError('body cap exceeded')
            item.update(http_status=response.status, final_url=response.url, bytes=len(body), sha256=hashlib.sha256(body).hexdigest())
        if not body.startswith(b'%PDF'):
            raise RuntimeError('not PDF')
        pdf = ROOT/'private_sources'/(name+'.pdf')
        txt = ROOT/'private_sources'/(name+'.txt')
        pdf.write_bytes(body)
        result = subprocess.run(['/opt/homebrew/bin/pdftotext','-layout',str(pdf),str(txt)], capture_output=True, timeout=30)
        if result.returncode:
            raise RuntimeError('PDF extraction failed')
        item.update(success=True, extracted_text_bytes=txt.stat().st_size, extracted_text_sha256=hashlib.sha256(txt.read_bytes()).hexdigest())
    except Exception as error:
        item.update(success=False, error=str(error))
    item['completed_UTC'] = datetime.datetime.now(datetime.timezone.utc).isoformat()
    receipts.append(item)
    print(json.dumps(item), flush=True)
    (ROOT/'NORMALIZED_PUBLISHER_RECEIPTS.json').write_text(json.dumps(receipts, indent=2, sort_keys=True)+'\n')
