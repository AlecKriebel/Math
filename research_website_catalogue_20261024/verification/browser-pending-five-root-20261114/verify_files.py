"""Bind actual browser downloads to unchanged originals, site files and current HTTP."""
from pathlib import Path
from hashlib import sha256, md5
from urllib.request import urlopen
import datetime, json

OUT = Path(__file__).resolve().parent
PROGRAMME = OUT.parents[1]
SITE = Path('/Users/alec/Desktop/alec-dev/aleckriebel.com/public')
FIELDS = {
    '23333353': ('all_actual_assets', 'api_file_object'),
    '23416806': ('all_assets', 'original_api_file_object'),
    '23441617': ('all_assets', 'original_api_file_object'),
    '23576280': ('all_assets', 'original_api_file_object'),
    '23331258': ('all_assets', 'original_api_file_object'),
}

def need(condition, message):
    if not condition:
        raise RuntimeError(message)

def write(name, value):
    target = OUT / name
    need(not target.exists(), 'Existing receipt: ' + name)
    target.write_text(json.dumps(value, indent=2, ensure_ascii=False) + '\n')

observations = json.loads((OUT / 'observations.json').read_text())
need([r['record'] for r in observations] == list(FIELDS), 'Exact five observed records')
downloads, targets = [], []
for row in observations:
    paper = PROGRAMME / 'papers' / row['record']
    ready = json.loads((paper / 'sources/SOURCE_READY.json').read_text())
    publication = json.loads((paper / 'publication.json').read_text())
    asset_field, native_field = FIELDS[row['record']]
    for kind in ['pdfDownload', 'zipDownload']:
        actual = Path(row[kind])
        data = actual.read_bytes()
        digest = sha256(data).hexdigest()
        matches = [a for a in ready[asset_field] if a['sha256'] == digest and a['bytes'] == len(data)]
        need(len(matches) == 1, 'One exact source asset: ' + row['record'] + kind)
        asset = matches[0]
        native = asset[native_field]
        local = SITE / 'research' / publication['slug'] / native['key']
        need(data == Path(asset['path']).read_bytes() == local.read_bytes(), 'Three-way byte identity')
        need('md5:' + md5(data).hexdigest() == native['checksum'], 'Native MD5')
        downloads.append({'record_id': row['record'], 'kind': kind,
                          'actual_browser_saved_path': str(actual), 'bytes': len(data),
                          'sha256': digest, 'local_site_path': str(local), 'whole_native_asset': asset})
    targets.append((row['url'], SITE / 'research' / publication['slug'] / 'index.html'))
write('DOWNLOAD_CUSTODY.json', {'status': 'PASS_TEN_ACTUAL_BROWSER_DOWNLOADS_MATCH_ORIGINAL_AND_SITE_BYTES',
                                'downloads': downloads})
targets += [('https://aleckriebel.com/research/', SITE / 'research/index.html'),
            ('https://aleckriebel.com/research/sitemap.xml', SITE / 'research/sitemap.xml')]
http = []
for url, local in targets:
    with urlopen(url, timeout=30) as response:
        body = response.read()
        event = {'url': url, 'status': response.status, 'final_url': response.url,
                 'ordered_response_headers': list(response.headers.raw_items()), 'bytes': len(body),
                 'sha256': sha256(body).hexdigest(), 'local_path': str(local),
                 'ordinary_GET_no_cache_bypass': True}
    need(event['status'] == 200 and body == local.read_bytes(), 'Current live exact bytes: ' + url)
    http.append(event)
write('LIVE_HTTP.json', {'utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
                         'status': 'PASS_SEVEN_ORDINARY_LIVE_GETS_EXACT', 'requests': http})
print(json.dumps({'status': 'PASS', 'actual_browser_downloads': len(downloads), 'live_exact_GETs': len(http)}))
