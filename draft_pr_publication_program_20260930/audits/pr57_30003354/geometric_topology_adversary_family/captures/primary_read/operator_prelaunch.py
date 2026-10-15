"""Read exact source topologies; whole papers/images stay in private A57 cache."""
import hashlib
import json
import os
import stat
import subprocess
import urllib.request
from datetime import datetime, timezone
from pathlib import Path
from pypdf import PdfReader

ROOT = Path(__file__).resolve().parent
PRIVATE = ROOT.parent / 'private_primary_reading_cache' / ROOT.name
ORIGINAL = ROOT.parent / 'original_preparation_family' / 'original'
INPUTS = (
    ('owr_2017', 'https://ems.press/doi/pdf/10.4171/OWR/2017/3', [17]),
    ('banakh_belegradek', 'https://arxiv.org/pdf/1510.07269', [3, 4, 17, 19]),
    ('belegradek_hu_erratum', 'https://link.springer.com/content/pdf/10.1007/s00208-015-1354-1.pdf', [1]),
)


def utc(): return datetime.now(timezone.utc).isoformat()
def sha(data): return hashlib.sha256(data).hexdigest()


def main():
    PRIVATE.mkdir(parents=True, exist_ok=False)
    captures = ROOT / 'primary_child_captures'; captures.mkdir()
    rows = []; runs = []
    for name, url, pages in INPUTS:
        started = utc()
        try:
            request = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
            with urllib.request.urlopen(request, timeout=60) as response:
                body = response.read(); final_url = response.url
            assert body.startswith(b'%PDF')
            pdf = PRIVATE / (name + '.pdf'); pdf.write_bytes(body)
            reader = PdfReader(pdf)
            row = {'name': name, 'requested_url': url, 'final_url': final_url, 'acquired': True,
                   'bytes': len(body), 'sha256': sha(body), 'pages': len(reader.pages),
                   'private_pdf_absolute_path': str(pdf), 'started_utc': started, 'ended_utc': utc(),
                   'whole_body_redistributed': False}
            commands = [['/opt/homebrew/bin/pdftotext', '-layout', str(pdf), str(PRIVATE / (name + '.layout.txt'))]]
            commands += [['/opt/homebrew/bin/pdftoppm', '-f', str(page), '-l', str(page), '-scale-to', '1500',
                          '-png', '-singlefile', str(pdf), str(PRIVATE / (name + '_page_' + str(page)))] for page in pages]
            for number, argv in enumerate(commands):
                tag = name + '_' + str(number); run_start = utc()
                with (captures / (tag + '.stdout.bin')).open('wb') as stdout, (captures / (tag + '.stderr.bin')).open('wb') as stderr:
                    child = subprocess.Popen(argv, stdout=stdout, stderr=stderr, cwd=ROOT)
                    entry = {'owner_pid': os.getpid(), 'owned_child_pid': child.pid, 'started_utc': run_start,
                             'argv': argv, 'source_pdf_sha256': sha(body)}
                    (captures / (tag + '.PRELAUNCH.json')).write_text(json.dumps(entry, indent=2) + '\n')
                    code = child.wait()
                entry.update(ended_utc=utc(), exit_code=code)
                for stream in ('stdout', 'stderr'):
                    filename = tag + '.' + stream + '.bin'; data = (captures / filename).read_bytes()
                    entry[stream] = filename; entry[stream + '_bytes'] = len(data); entry[stream + '_sha256'] = sha(data)
                runs.append(entry); assert code == 0
            rows.append(row)
        except Exception as error:
            rows.append({'name': name, 'requested_url': url, 'acquired': False, 'started_utc': started,
                         'ended_utc': utc(), 'limitation': str(error), 'whole_body_redistributed': False})
    private_rows = []
    for path in sorted(PRIVATE.rglob('*')):
        if path.is_file():
            path.chmod(0o444); data = path.read_bytes()
            private_rows.append({'absolute_path': str(path), 'bytes': len(data), 'sha256': sha(data),
                                 'full_mode_07777': f'{stat.S_IMODE(path.lstat().st_mode):04o}'})
    PRIVATE.chmod(0o755)
    bindings = []
    for name in ('source_record.json', 'CANDIDATE.md'):
        path = ORIGINAL / name; data = path.read_bytes()
        bindings.append({'absolute_path': str(path), 'bytes': len(data), 'sha256': sha(data),
                         'full_mode_07777': f'{stat.S_IMODE(path.lstat().st_mode):04o}'})
    assert next(x['sha256'] for x in bindings if x['absolute_path'].endswith('/CANDIDATE.md')) == '7f358fb1aaa73dc3cfd06c798c10f6afed65ee430b622b84b90f0554dd440e62'
    record = json.loads((ORIGINAL / 'source_record.json').read_text())
    assert record['id'] == 30003354 and record['problem_number'] == 'OWR-15208-008'
    result = {'schema': 'pr57-geometric-primary-source-receipts/v1', 'operator_pid': os.getpid(),
              'utc': utc(), 'sources': rows, 'private_reading_inputs': private_rows,
              'original_source_bindings': bindings, 'private_cache_required_by_ROOT_close': False,
              'whole_PDF_fulltext_PNG_bodies_in_public_handoff': False,
              'scope': 'Exact primary topology/normalization passages; not a full literature or priority audit'}
    (ROOT / 'PRIMARY_SOURCE_RECEIPTS.json').write_text(json.dumps(result, indent=2, sort_keys=True) + '\n')
    (captures / 'OWNED_RUNS.json').write_text(json.dumps(runs, indent=2, sort_keys=True) + '\n')
    print(json.dumps({'operator_pid': os.getpid(), 'utc': utc(), 'sources': rows,
                      'private_reading_input_count': len(private_rows), 'recorded_owned_children': len(runs),
                      'whole_bodies_redistributed': False}, indent=2, sort_keys=True))


if __name__ == '__main__': main()
