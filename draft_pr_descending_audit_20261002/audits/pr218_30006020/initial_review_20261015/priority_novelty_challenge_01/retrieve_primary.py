"""Fetch only public primary sources; retain complete reading material privately."""
import concurrent.futures, datetime, hashlib, json, pathlib, subprocess, urllib.request

BASE = pathlib.Path(__file__).resolve().parent
PRIVATE = BASE / 'private'
SOURCES = {
    'owr2024': 'https://publications.mfo.de/bitstream/handle/mfo/4255/OWR_2024_41.pdf?sequence=1',
    'dl_final': 'https://ems.press/content/serial-article-files/51451?nt=1',
    'dl_arxiv_page': 'https://arxiv.org/abs/2202.10255',
    'dgzz_final': 'https://webusers.imj-prg.fr/~anton.zorich/Papers/Large_Genus_Asymptotic_Geometry_2022_Inventiones_published.pdf',
    'dgzz_arxiv_page': 'https://arxiv.org/abs/2007.04740',
}

def fetch(item):
    name, url = item
    entry = {'id': name, 'requested_url': url, 'retrieved_at_utc': datetime.datetime.now(datetime.timezone.utc).isoformat()}
    try:
        request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 Independent mathematical literature audit'})
        with urllib.request.urlopen(request, timeout=90) as response:
            data = response.read()
            entry.update(final_url=response.url, content_type=response.headers.get('Content-Type'), response_headers=dict(response.headers))
        ext = '.pdf' if data.startswith(b'%PDF') else '.html'
        destination = PRIVATE / (name + ext)
        destination.write_bytes(data)
        entry.update(path=str(destination.relative_to(BASE)), sha256=hashlib.sha256(data).hexdigest(), bytes=len(data))
        if ext == '.pdf':
            subprocess.run(['pdftotext', '-layout', str(destination), str(PRIVATE / (name + '.txt'))], check=True)
        return entry
    except Exception as error:
        entry['error'] = repr(error)
        return entry

if __name__ == '__main__':
    PRIVATE.mkdir(exist_ok=True)
    with concurrent.futures.ThreadPoolExecutor(max_workers=5) as pool:
        entries = list(pool.map(fetch, SOURCES.items()))
    (PRIVATE / 'primary_retrieval_raw.json').write_text(json.dumps(entries, indent=2) + '\n')
    safe = [{k: v for k, v in entry.items() if k != 'response_headers'} for entry in entries]
    (BASE / 'SOURCE_PINS.json').write_text(json.dumps(safe, indent=2) + '\n')
    print(json.dumps(safe, indent=2))
