"""Match deposited PDF checksums to local manuscripts and extract exact content."""
from pathlib import Path
import json
import hashlib
import subprocess
from urllib.request import Request, urlopen
from urllib.parse import quote
from concurrent.futures import ThreadPoolExecutor

HERE = Path(__file__).resolve().parent
ROOT = HERE.parent
records = json.loads((HERE / 'INVENTORY.json').read_text())['records']

def md5(path):
    h = hashlib.md5()
    with path.open('rb') as stream:
        for block in iter(lambda: stream.read(1024 * 1024), b''):
            h.update(block)
    return h.hexdigest()

def main():
    paths = subprocess.check_output(['rg', '--files', '--hidden', '-g', '*.pdf', '-g', '!.git', '-g', '!zenodo_discoverability_20261010'], cwd=ROOT, text=True).splitlines()
    index = {}
    def hash_one(name):
        p = ROOT / name
        return md5(p), str(p)
    with ThreadPoolExecutor(max_workers=4) as pool:
        for checksum, p in pool.map(hash_one, paths):
            index.setdefault(checksum, []).append(p)
    catalog = []
    for r in records:
        md = r.get('metadata', {})
        pdfs = [f for f in r.get('files', []) if f.get('filename', '').lower().endswith('.pdf')]
        is_paper = r.get('submitted') and bool(pdfs) and (
            md.get('upload_type') == 'publication' or r['id'] == 22929556)
        if not is_paper:
            reason = 'unpublished draft' if not r.get('submitted') else 'supporting dataset/software/source/manifest or no manuscript files'
            catalog.append({'id': r['id'], 'status': 'excluded', 'reason': reason, 'title': md.get('title')})
            continue
        sources = []
        dest = HERE / 'papers' / str(r['id'])
        dest.mkdir(parents=True, exist_ok=True)
        for f in pdfs:
            checksum = f['checksum'].removeprefix('md5:')
            matches = index.get(checksum, [])
            if matches:
                path = Path(matches[0])
            else:
                path = dest / Path(f['filename']).name
                url = f"https://zenodo.org/records/{r['id']}/files/{quote(f['filename'], safe='')}?download=1"
                request = Request(url, headers={'User-Agent': 'Math-Zenodo-Deposit-Tool/1.0'})
                with urlopen(request, timeout=60) as response:
                    data = response.read(30 * 1024 * 1024 + 1)
                if len(data) != f['filesize'] or hashlib.md5(data).hexdigest() != checksum:
                    raise RuntimeError(f"Downloaded PDF integrity failed for {r['id']}")
                path.write_bytes(data)
            out = dest / (Path(f['filename']).stem + '.txt')
            subprocess.run(['pdftotext', '-layout', str(path), str(out)], check=True)
            sources.append({'filename': f['filename'], 'md5': checksum, 'size': f['filesize'],
                            'pdf_path': str(path), 'text_path': str(out), 'origin': 'local checksum match' if matches else 'verified public download'})
        catalog.append({'id': r['id'], 'status': 'paper', 'title': md.get('title'), 'sources': sources})
        print(f"Prepared {r['id']}: {md.get('title')}", flush=True)
    (HERE / 'SOURCE_CATALOG.json').write_text(json.dumps(catalog, indent=2, ensure_ascii=False) + '\n')
    print(f"Papers: {sum(c['status'] == 'paper' for c in catalog)}; excluded: {sum(c['status'] == 'excluded' for c in catalog)}")

if __name__ == '__main__':
    main()
