from pathlib import Path
from datetime import datetime, timezone
import concurrent.futures
import hashlib
import json
import re
import urllib.request

ROOT = Path(__file__).resolve().parent
PRIVATE = ROOT / 'private_reading'
now = lambda: datetime.now(timezone.utc).isoformat()
sha = lambda data: hashlib.sha256(data).hexdigest()

# The complete web excerpts remain private reading material.  The public ledger
# records the queries, discovery URLs, and bounded screening decisions only.
raw = json.loads((PRIVATE / 'RAW_WEB_QUERY_RESULTS.json').read_text())
queries = []
for group in raw:
    result = group['result']
    content = str(result.get('value', result))
    found = []
    for line in content.splitlines():
        match = re.match(r'^(.+?) \((https?://[^)]+)\)$', line)
        if match:
            title, url = match.groups()
            entry = {'title': title[:240], 'url': url}
            if entry not in found:
                found.append(entry)
    members = group.get('queries', [{'q': group.get('query')}])
    for member in members:
        q = member['q']
        if 'Empty search results' in content:
            outcome = 'No results returned by this bounded search call.'
        elif 'left_Hamm.html' in content:
            outcome = 'Exact Aldous page was among results; no closure inferred from that page.'
        elif any(x in content for x in ['arxiv.org', 'Hammersley', 'stationarity']):
            outcome = 'Discovery leads screened; primary follow-up checks are in SOURCE_COVERAGE.md.'
        else:
            outcome = 'No exact-model closure identified in returned discovery results.'
        queries.append({'id': f'Q{len(queries)+1:03}', 'utc': group['utc'],
                        'query': q, 'batched_result': len(members) > 1,
                        'outcome': outcome, 'discovery_results': found})
(ROOT / 'QUERY_LEDGER.json').write_text(json.dumps({
    'generated_utc': now(), 'query_count': len(queries),
    'limitations': [
        'Web searches are bounded and ranking dependent; dates are query filters, not reliable bibliographic publication dates.',
        'A batched-result list is the union returned for that search batch and is not attributed individually to one query.',
        'No-result calls do not prove absence of prior work.',
        'Raw returned third-party text is private reading material and excluded from authored publication manifests.'
    ], 'queries': queries}, indent=2, ensure_ascii=False) + '\n')

retrievals = json.loads((PRIVATE / 'PRIMARY_RETRIEVAL.json').read_text())
version_checks = []
jobs = []
for path in sorted(PRIVATE.glob('*_abs.html')):
    html = path.read_text()
    match = re.search(r'\[Submitted on.*?</div>', html, re.S)
    dateline = re.sub('<[^>]+>', '', match.group(0)) if match else ''
    versions = re.findall(r'\bv([0-9]+)\b', dateline)
    version = 'v' + (versions[-1] if versions else '1')
    arxiv_id = re.search(r'([0-9]{4}\.[0-9]{4,5})_abs', path.name).group(1)
    pdf = PRIVATE / path.name.replace('_abs.html', '.pdf')
    jobs.append((pdf, 'https://arxiv.org/pdf/' + arxiv_id + version, dateline))

def check_version(job):
    pdf, url, dateline = job
    check = {'local_pdf': pdf.name, 'version_url': url, 'dateline_from_primary_abs': dateline,
             'local_sha256': sha(pdf.read_bytes()), 'checked_utc': now()}
    try:
        with urllib.request.urlopen(url, timeout=40) as response:
            data = response.read()
            check.update({'retrieved_sha256': sha(data), 'bytes': len(data),
                          'matches_latest_download': data == pdf.read_bytes()})
    except Exception as error:
        check['error'] = str(error)
    return check

with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
    version_checks = list(pool.map(check_version, jobs))
(PRIVATE / 'PINNED_VERSION_VERIFICATION.json').write_text(json.dumps(version_checks, indent=2) + '\n')
by_pdf = {x['local_pdf']: x for x in version_checks}
sources = []
for item in retrievals:
    name = item['path']
    if 'error' in item or 'openalex' in name:
        continue
    if not (name.endswith('.pdf') or name in ['aldous_problem.html', 'aldous_op_index.html']):
        continue
    source = {k: item[k] for k in ['path', 'url', 'final_url', 'retrieved_utc', 'sha256', 'bytes']}
    source['private_copy'] = 'private_reading/' + name
    if name in by_pdf:
        source['pinned_version'] = by_pdf[name]
    txt = PRIVATE / name.replace('.pdf', '.txt')
    if name.endswith('.pdf') and txt.exists():
        source['pdf_page_count'] = len(txt.read_text().split('\f')) - 1
    sources.append(source)
(ROOT / 'SOURCE_PINS.json').write_text(json.dumps({
    'generated_utc': now(), 'note': 'This manifest contains references and byte pins only; private reading copies are excluded from the authored-file manifest.',
    'sources': sources}, indent=2, ensure_ascii=False) + '\n')

reviews = {
 '10.47443/dml.2021.0049': 'Primary model definitions checked: multilayer and planar particle insertions, no deterministic coordinate drift.',
 '10.1090/bull/1623': 'Primary arXiv commentary retrieved and screened: KPZ progress, no fixed-left-pile stationary joint law identified.',
 '10.48550/arxiv.1806.10542': 'Same primary commentary as the journal version; arXiv v1 checked.',
 '10.70675/97744e22z0e8az45d5za59eze8eef5cef58b': 'Full thesis retrieved; stationary sources/sinks and weighted-line definitions checked.',
 '10.1007/978-3-319-92402-1_4': 'Primary arXiv definitions checked: lives/heap process, not the fixed-prefix coordinate-drift process.',
 '10.1214/22-aihp1343': 'Primary t-PNG Burke/stationarity definitions checked: independent boundary PPPs and bulk asymptotics.',
 '10.1093/imrn/rnae168': 'Primary definitions and Poisson LPP sections checked: whole-line fluid model and Busemann/bulk scaling.',
 '10.1016/j.aam.2022.102478': 'Primary Corollary 1.4 and Section 1.10 checked: sqrt(n) bulk scale at w>0, excluding w=0 target boundary.',
 '10.1007/s00440-021-01074-0': 'Primary backwards TASEP definitions and extensions checked: lattice state space and index-dependent rates.',
 '10.24033/bsmf.2863': 'Primary PKS definitions and reversibility section checked: translation-invariant weighted horizontal/vertical lines.',
}
screen = {}
counts = {}
for name in ['openalex_1999_citations_since2018.json', 'openalex_1995_citations_since2018.json']:
    data = json.loads((PRIVATE / name).read_text())
    counts[name] = {'reported_count': data['meta']['count'], 'returned_count': len(data['results'])}
    for item in data['results']:
        key = item.get('doi') or item['id']
        if key not in screen:
            doi = (item.get('doi') or '').replace('https://doi.org/', '').lower()
            inv = item.get('abstract_inverted_index')
            screen[key] = {'id': item['id'], 'doi': item.get('doi'), 'title': item['title'],
                'publication_date_as_indexed': item['publication_date'],
                'screening_depth': 'title; primary source reviewed' if doi in reviews else 'title only in this bounded pass',
                'indexed_abstract_available': bool(inv),
                'decision': reviews.get(doi, 'Not advanced for exact-model full-text review in this lane; no content-level exclusion is claimed from title screening alone.'),
                'appears_in': []}
        screen[key]['appears_in'].append(name)
(ROOT / 'CITATION_SCREEN.json').write_text(json.dumps({
    'generated_utc': now(), 'counts': counts, 'unique_indexed_records': len(screen),
    'limitations': 'Discovery index is incomplete, may duplicate publications/preprints, and is not proof of priority or exhaustive coverage. Publication dates are index metadata. Claims about primary documents use SOURCE_COVERAGE.md and byte-pinned copies.',
    'records': list(screen.values())}, indent=2, ensure_ascii=False) + '\n')
print(json.dumps({'queries': len(queries), 'sources': len(sources), 'pinned_version_matches': sum(x.get('matches_latest_download', False) for x in version_checks), 'pinned_version_checks': len(version_checks), 'citation_counts': counts, 'unique_records': len(screen)}, indent=2))
