"""Read-only public-source retrieval for the bounded PR1205 priority audit."""
from pathlib import Path
import hashlib, json, urllib.request, subprocess
from datetime import datetime, timezone

ROOT = Path(__file__).parent
SOURCES = {
    'owr20.pdf': 'https://ems.press/content/serial-article-files/46898',
    'owr52.pdf': 'https://ems.press/content/serial-article-files/46930',
    'ks2022.html': 'https://link.springer.com/article/10.1007/s10801-022-01144-z',
    'ks2022.pdf': 'https://link.springer.com/content/pdf/10.1007/s10801-022-01144-z.pdf',
    'ks_arxiv.html': 'https://arxiv.org/abs/2109.14439',
    'ks_arxiv_v1.pdf': 'https://arxiv.org/pdf/2109.14439v1',
    'author_schumann.html': 'https://www.mi.uni-koeln.de/~bschuman/',
    'lg_arxiv.html': 'https://arxiv.org/abs/2208.00028',
    'lg_v2.pdf': 'https://arxiv.org/pdf/2208.00028v2',
    'km2024_slides.pdf': 'https://pca-pdmi.ru/2024/files/30/coefficients-pre2.pdf',
    'km2023_slides.pdf': 'https://pca-pdmi.ru/2023/files/51/F-poly-Newton%283%29.pdf',
    'km2023_abstracts.pdf': 'https://pca-pdmi.ru/2023/pca2023_book.pdf',
    'km2022_preprint.pdf': 'https://easychair.org/publications/preprint/z55N/open',
    'openalex_ks.json': 'https://api.openalex.org/works/https://doi.org/10.1007/s10801-022-01144-z',
    'crossref_ks.json': 'https://api.crossref.org/works/10.1007/s10801-022-01144-z',
    'semantic_ks.json': 'https://api.semanticscholar.org/graph/v1/paper/DOI:10.1007/s10801-022-01144-z?fields=title,year,citationCount,citations.title,citations.externalIds,citations.year',
    'zenodo_author.json': 'https://zenodo.org/api/records?q=creators.name:%22Kriebel,%20Alec%22&size=100',
}

records = []
for name, url in SOURCES.items():
    record = {'name': name, 'requested_url': url, 'retrieved_utc': datetime.now(timezone.utc).isoformat()}
    try:
        req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0 (independent mathematical literature audit)'})
        with urllib.request.urlopen(req, timeout=45) as response:
            body = response.read()
            record.update(final_url=response.url, status=response.status, content_type=response.headers.get('content-type'))
        (ROOT/'sources'/name).write_bytes(body)
        record.update(bytes=len(body), sha256=hashlib.sha256(body).hexdigest())
        if body.startswith(b'%PDF'):
            result = subprocess.run(['pdftotext','-layout',str(ROOT/'sources'/name),str(ROOT/'sources'/name.replace('.pdf','.txt'))],capture_output=True,text=True)
            record['text_extraction_returncode'] = result.returncode
        elif name.endswith('.pdf'):
            record['warning'] = 'Response is not a PDF; inspect response before relying on it.'
    except Exception as exc:
        record['error'] = str(exc)
    records.append(record)
    (ROOT/'RETRIEVALS.json').write_text(json.dumps(records, indent=2)+'\n')
    print(name, record.get('bytes', record.get('error')))
