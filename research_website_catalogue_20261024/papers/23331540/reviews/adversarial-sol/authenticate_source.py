"""Fixed source-custody data reader; never loads scientific code or opinion bodies."""
from pathlib import Path
import hashlib, json, stat, datetime

R = Path(__file__).resolve().parent
S = R.parents[1] / 'sources'

def pin(p, root):
    st = p.lstat()
    if not stat.S_ISREG(st.st_mode):
        raise RuntimeError('not a regular file: ' + str(p))
    data = p.read_bytes()
    return {'path': p.relative_to(root).as_posix(), 'bytes': len(data),
            'SHA256': hashlib.sha256(data).hexdigest(), 'mode': stat.S_IMODE(st.st_mode)}

def inventory(root):
    files, dirs = [], []
    for p in sorted(root.rglob('*')):
        st = p.lstat()
        if stat.S_ISREG(st.st_mode):
            files.append(pin(p, root))
        elif stat.S_ISDIR(st.st_mode):
            dirs.append({'path': p.relative_to(root).as_posix(), 'mode': stat.S_IMODE(st.st_mode)})
        else:
            raise RuntimeError('nonregular topology: ' + str(p))
    return files, dirs

fixed = {
    'SOURCE_FINAL.json': '40247a4dc07e93b1148109187d032faa0ff76e318b801967109ba097c600fc07',
    'SOURCE_MANIFEST.json': '3a31e184c158203cd9f93b24004621b5af7b9cc4fe0e86820337a7852ee16944',
    'assets/full_stress_stratifications_determine_a_labelled_graph.pdf': 'd1820035901020691f091c92a6cf0f78bc8a270413f72727a68b2abb341cf475',
    'published-source/container-001/tree/full_stress_stratifications_v1/research_note.tex': '6827d5e72216e8b67a3324a7f0bf9492163091e322a39b0b983c0fec909a1d89',
}
for name, digest in fixed.items():
    if pin(S / name, S)['SHA256'] != digest:
        raise RuntimeError('fixed identity mismatch: ' + name)
manifest = json.loads((S / 'SOURCE_MANIFEST.json').read_text())
files, dirs = inventory(S)
excluded = ['SOURCE_FINAL.json', 'SOURCE_MANIFEST.json']
if manifest['exact_terminal_exclusions'] != excluded:
    raise RuntimeError('unexpected exclusions')
if [q for q in files if q['path'] not in excluded] != manifest['files']:
    raise RuntimeError('source payload drift')
if dirs != manifest['directories'] or stat.S_IMODE(S.lstat().st_mode) != manifest['root_mode']:
    raise RuntimeError('source mode/topology drift')
if len(files) != 133 or len(dirs) != 14:
    raise RuntimeError('unexpected finite source extent')
embedded = S / 'published-source/container-001/tree/full_stress_stratifications_v1/research_note.pdf'
if embedded.read_bytes() != (S / 'assets/full_stress_stratifications_determine_a_labelled_graph.pdf').read_bytes():
    raise RuntimeError('standalone/embedded PDF differs')
record = json.loads((S / 'record.response.body').read_text())
file_response = json.loads((S / 'files-23331540.response.body').read_text())
md5 = []
for f in record['files']:
    data = (S / 'assets' / f['key']).read_bytes()
    if len(data) != f['size'] or 'md5:' + hashlib.md5(data).hexdigest() != f['checksum']:
        raise RuntimeError('native asset mismatch: ' + f['key'])
    md5.append({'name': f['key'], 'bytes': len(data), 'native_checksum': f['checksum']})
receipt = {'UTC': datetime.datetime.now(datetime.timezone.utc).isoformat(),
           'status': 'PASS_DATA_CUSTODY_ONLY', 'source_files': len(files), 'source_child_directories': len(dirs),
           'root_mode': stat.S_IMODE(S.lstat().st_mode), 'files': files, 'directories': dirs,
           'native_asset_order_and_checksums': md5, 'embedded_PDF_identical': True,
           'is_published_present': 'is_published' in record, 'native_status': record.get('status'),
           'native_state': record.get('state'), 'native_submitted': record.get('submitted'),
           'file_wrapper_order': file_response.get('order'), 'file_wrapper_default_preview': file_response.get('default_preview'),
           'scientific_programs_or_opinion_bodies_opened': False,
           'hashing_does_not_count_as_semantic_reading': True}
with (R / 'SOURCE_CUSTODY.json').open('x') as f:
    json.dump(receipt, f, ensure_ascii=False, indent=2)
    f.write('\n')
print(json.dumps({'status': receipt['status'], 'files': len(files), 'dirs': len(dirs),
                  'native_assets': md5, 'embedded_PDF_identical': True}, indent=2))
