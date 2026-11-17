#!/usr/bin/env python3
"""Acquisition only: treats downloaded and archived sources as inert data."""
import concurrent.futures
import datetime
import hashlib
import json
import pathlib
import shutil
import subprocess

HERE = pathlib.Path(__file__).resolve().parent
NATIVE = pathlib.Path('/Users/alec/Documents/Math/research_website_catalogue_20261024/papers/23202994/sources/archives/01-source-and-verification.zip.extracted')
SOURCES = [
    dict(id='KS1998_author', url='https://math.vanderbilt.edu/saffeb/texts/159.pdf', archive='kuijlaars_saff_159.pdf', sha256='98e0eb5006404d85ed2a1d3bc67de830c0e029b077ad7a99aaab4e845e4ffbdc', bytes=273455, edition='Author-hosted journal copy; Trans. AMS 350(2) (1998), 523–538; historically pinned in sources/classical/SOURCE_MANIFEST.json.'),
    dict(id='BHS2012_arxiv_v1', url='https://arxiv.org/pdf/1202.4037v1', archive='brauchart_hardin_saff_1202.4037v1.pdf', sha256='1a1f545e0634693d82d5ebe4a5564ca640e35f1a47d436695c65da1c764fad5b', bytes=983916, edition='Explicit version-qualified arXiv:1202.4037v1; historically pinned in sources/classical/SOURCE_MANIFEST.json.'),
    dict(id='BHS2012_author', url='https://math.vanderbilt.edu/saffeb/texts/235.pdf', archive='brauchart_hardin_saff_235.pdf', sha256='9216e0feca0dd4be9714af9bdc494d6be8d3a17a78a75aab6486d2722120773f', bytes=733099, edition='Author-hosted 235.pdf; historical manifest describes retrieval on 2026-10-06; independently retained from arXiv v1.'),
    dict(id='HSS2014_arxiv_v2', url='https://arxiv.org/pdf/1403.7505v2', archive='hardin_saff_simanek1403.7505v2-priority.pdf', sha256='20f9d795746e3430c642c9555b5685bd557a52e5cc055c393a4bae8fce86346b', bytes=398801, edition='Explicit version-qualified arXiv:1403.7505v2; historical bytes/hash in sources/priority/EVIDENCE_MANIFEST.json.'),
    dict(id='HLSS2018_arxiv_v2', url='https://arxiv.org/pdf/1702.02894v2', archive='hardin_leble_saff_serfaty1702.02894v2-priority.pdf', sha256='54c2686fafb93d810b8de9f685642e48321409422b3fbeb164709eb626fb64ab', bytes=397420, edition='Explicit version-qualified arXiv:1702.02894v2; historical bytes/hash in sources/priority/EVIDENCE_MANIFEST.json; separate from published author copy.'),
    dict(id='HLSS2018_published_author', url='https://www.math.vanderbilt.edu/saffeb/texts/266.pdf', archive=None, sha256=None, bytes=None, edition='Author-hosted published personal copy; discovery from official author research list and primary PDF URL. No historical native pin found; must be qualified by current bytes and PDF front matter.'),
    dict(id='HLSS2018_published_author_fallback', url='https://math.vanderbilt.edu/saffeb/texts/266.pdf', archive=None, sha256=None, bytes=None, edition='Same official author-hosted path on the non-www primary math.vanderbilt.edu hostname already documented in native SOURCE_MANIFEST.json. Explicit fallback after the www host certificate SAN mismatch; failure attempt retained separately. Current edition must be identified from front matter, without claiming byte identity to any unpinned historical copy.'),
]

def now():
    return datetime.datetime.now(datetime.timezone.utc).isoformat()

def pins(path):
    b = path.read_bytes()
    return dict(bytes=len(b), sha256=hashlib.sha256(b).hexdigest(), md5=hashlib.md5(b).hexdigest())

def inspect_pdf(path, prefix):
    info = subprocess.run(['pdfinfo', str(path)], capture_output=True)
    prefix.with_suffix('.pdfinfo.txt').write_bytes(info.stdout)
    prefix.with_suffix('.pdfinfo.stderr.txt').write_bytes(info.stderr)
    txt = prefix.with_suffix('.pdf.txt')
    proc = subprocess.run(['pdftotext', '-layout', str(path), str(txt)], capture_output=True)
    prefix.with_suffix('.pdftotext.stderr.txt').write_bytes(proc.stderr)
    return dict(pdfinfo_exit=info.returncode, pdftotext_exit=proc.returncode,
                text_path=str(txt.relative_to(HERE)) if txt.exists() else None,
                text_integrity=pins(txt) if txt.exists() else None)

def acquire(s):
    directory = HERE/'sources'/s['id']
    directory.mkdir(parents=True, exist_ok=True)
    if (directory/'acquisition.json').exists():
        return json.loads((directory/'acquisition.json').read_text())
    result = dict(s)
    if s['archive']:
        old = NATIVE/'sources/classical'/s['archive']
        result['native_referenced_payload_path'] = str(old)
        result['native_referenced_payload_present'] = old.is_file()
        if old.is_file():
            copied = directory/'historical.pdf'
            shutil.copyfile(old, copied)
            result['historical_path'] = str(copied.relative_to(HERE))
            result['historical_integrity'] = pins(copied)
            result['historical_matches_pin'] = result['historical_integrity']['sha256'] == s['sha256'] and result['historical_integrity']['bytes'] == s['bytes']
            result['historical_extract'] = inspect_pdf(copied, directory/'historical')
    if s['id'] in {'KS1998_author', 'BHS2012_arxiv_v1', 'BHS2012_author'}:
        reuse_names = {'KS1998_author': 'kuijlaars-saff-159.pdf', 'BHS2012_arxiv_v1': 'brauchart-hardin-saff-1202.4037v1.pdf', 'BHS2012_author': 'brauchart-hardin-saff-235.pdf'}
        reuse = NATIVE.parents[2]/'reviews/adversarial-sol-continuation-20261117/primary'/reuse_names[s['id']]
        result['reuse_source'] = str(reuse)
        result['reuse_integrity'] = pins(reuse)
        result['reuse_matches_historical_pin'] = result['reuse_integrity']['sha256'] == s['sha256'] and result['reuse_integrity']['bytes'] == s['bytes']
        copied = directory/'historical.pdf'
        shutil.copyfile(reuse, copied)
        result['historical_path'] = str(copied.relative_to(HERE))
        result['historical_integrity'] = pins(copied)
        result['historical_matches_pin'] = result['reuse_matches_historical_pin']
        result['historical_extract'] = inspect_pdf(copied, directory/'historical')
        result['acquisition_status'] = 'Historical primary copy retained; independent prior continuation copy directly validated against native pin; no redundant network request.'
        result['retrieval_metadata_qualification'] = 'Native manifest records URL and historical retrieval date; historical final URL, HTTP status, headers, MD5 and precise retrieval time were not recorded there. Current local bytes, SHA-256 and MD5 recorded here; no claim of a new remote retrieval.'
        (directory/'acquisition.json').write_text(json.dumps(result, indent=2)+'\n')
        return result
    body = directory/'response-body.bin'
    headers = directory/'http-headers.txt'
    result['retrieval_start_utc'] = now()
    cmd = ['curl', '-q', '--location', '--silent', '--show-error', '--max-time', '75', '--retry', '0', '--dump-header', str(headers), '--output', str(body), '--write-out', '%{json}', s['url']]
    proc = subprocess.run(cmd, capture_output=True)
    result['retrieval_end_utc'] = now()
    result['curl_exit'] = proc.returncode
    (directory/'curl-metadata.json').write_bytes(proc.stdout)
    (directory/'curl-stderr.txt').write_bytes(proc.stderr)
    try:
        response = json.loads(proc.stdout)
    except Exception:
        response = {}
    result['requested_url'] = s['url']
    result['final_url'] = response.get('url_effective')
    result['http_status'] = response.get('http_code')
    result['headers_path'] = str(headers.relative_to(HERE))
    if body.exists():
        result['response_integrity'] = pins(body)
        result['response_has_pdf_signature'] = body.read_bytes().startswith(b'%PDF-')
        result['remote_matches_historical_sha256'] = result['response_integrity']['sha256'] == s['sha256'] if s['sha256'] else None
        if result['response_has_pdf_signature'] and proc.returncode == 0 and 200 <= result['http_status'] < 300:
            pdf = directory/'retrieved.pdf'
            body.rename(pdf)
            result['retrieved_pdf_path'] = str(pdf.relative_to(HERE))
            result['retrieved_extract'] = inspect_pdf(pdf, directory/'retrieved')
        else:
            result['failure_body_path'] = str(body.relative_to(HERE))
    (directory/'acquisition.json').write_text(json.dumps(result, indent=2)+'\n')
    return result

if __name__ == '__main__':
    (HERE/'native-reference-manifests').mkdir(exist_ok=True)
    for relative in ['sources/classical/SOURCE_MANIFEST.json', 'sources/priority/EVIDENCE_MANIFEST.json']:
        shutil.copyfile(NATIVE/relative, HERE/'native-reference-manifests'/pathlib.Path(relative).name)
    with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
        results = list(pool.map(acquire, SOURCES))
    (HERE/'ACQUISITION_MANIFEST.json').write_text(json.dumps(dict(created_utc=now(), scope='source acquisition and edition integrity only; no mathematical assessment', sources=results), indent=2)+'\n')
    for r in results:
        print(json.dumps({k:r.get(k) for k in ['id','curl_exit','http_status','historical_matches_pin','response_has_pdf_signature','remote_matches_historical_sha256','retrieved_pdf_path']}))
