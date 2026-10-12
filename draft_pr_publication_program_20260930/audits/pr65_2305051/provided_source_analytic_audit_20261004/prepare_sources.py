import datetime, hashlib, json, pathlib, shutil, uuid

root = pathlib.Path(__file__).resolve().parent
cache = pathlib.Path('/Users/alec/.cache/codex-pr65-priority-20261004') / ('analytic_' + uuid.uuid4().hex)
cache.mkdir(parents=True)
input_root = pathlib.Path('/Users/alec/.cache/codex-pr65-priority-20261004/provided_primary_sources_20261004')
records = []
for name in ('duren1966.pdf', 'piranian1966.pdf'):
    src = input_root / name
    dst = cache / name
    shutil.copy2(src, dst)
    txt = input_root / (name + '.txt')
    if txt.exists():
        shutil.copy2(txt, cache / txt.name)
    records.append({'name': name, 'input_path': str(src), 'private_copy': str(dst),
                    'sha256': hashlib.sha256(src.read_bytes()).hexdigest()})
info = {'created_utc': datetime.datetime.now(datetime.timezone.utc).isoformat(),
        'private_cache': str(cache), 'sources': records,
        'tools': {x: shutil.which(x) for x in ('python3','pdftoppm','pdftotext','pdfinfo','mutool')}}
(root / 'source_pins.json').write_text(json.dumps(info, indent=2)+'\n')
print(json.dumps(info, indent=2))
