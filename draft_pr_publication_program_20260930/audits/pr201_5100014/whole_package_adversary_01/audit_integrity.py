"""Read-only audit of the frozen publication package; outputs only own receipt."""
from pathlib import Path, PurePosixPath
from datetime import datetime, timezone
import hashlib, json, zipfile, stat

HERE = Path(__file__).resolve().parent
PACKAGE = HERE.parent / 'publication_package_v1'
MATERIALS = PACKAGE / 'materials'

def pin(data):
    return {'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()}

def require(condition, message):
    if not condition:
        raise RuntimeError(message)

def verify_map(base, mapping, label):
    checked = []
    for rel, expected in mapping.items():
        p = PurePosixPath(rel)
        require(not p.is_absolute() and '..' not in p.parts, label + ': unsafe path ' + rel)
        path = base / rel
        require(path.is_file() and not path.is_symlink(), label + ': absent/symlink ' + rel)
        actual = pin(path.read_bytes())
        want = {k: expected[k] for k in ('bytes', 'sha256')}
        require(actual == want, label + ': pin mismatch ' + rel)
        checked.append(rel)
    return len(checked)

def main():
    seal_bytes = (PACKAGE / 'PACKAGE_SEAL.json').read_bytes()
    require(pin(seal_bytes) == {'bytes': 81493, 'sha256': 'c4a151a0129b6ad4aab7a7ee60bc506fbd498e40ef87938f9bf4ef5f7b7ca3e6'}, 'Wrong frozen seal')
    seal = json.loads(seal_bytes)
    upload_count = verify_map(PACKAGE, seal['upload_files'], 'uploads')
    safe_count = verify_map(PACKAGE, seal['package_safe_files'], 'sealed materials')
    actual = {str(p.relative_to(MATERIALS)): pin(p.read_bytes()) for p in MATERIALS.rglob('*') if p.is_file()}
    require(all(not p.is_symlink() for p in MATERIALS.rglob('*')), 'symlink in materials')
    manifest = json.loads((MATERIALS / 'MANIFEST.json').read_text())
    root_count = verify_map(MATERIALS, manifest['files'], 'root manifest')
    require(set(manifest['files']) == set(actual) - {'MANIFEST.json'}, 'Root manifest coverage')
    require(set(seal['package_safe_files']) == {'materials/' + p for p in actual} | {'outer_pedal_flag.pdf', 'outer_pedal_flag.tex', 'verification-package.zip', 'zenodo-deposit.json'}, 'Seal coverage')
    require(seal['zip_entries'] == actual, 'Sealed ZIP inventory differs')
    with zipfile.ZipFile(PACKAGE / 'verification-package.zip') as archive:
        infos = archive.infolist()
        require(len(set(x.filename for x in infos)) == len(infos), 'Duplicate ZIP entries')
        require(set(archive.namelist()) == set(actual), 'ZIP membership differs')
        for item in infos:
            rel = PurePosixPath(item.filename)
            require(not rel.is_absolute() and '..' not in rel.parts, 'Unsafe ZIP path')
            require(not stat.S_ISLNK(item.external_attr >> 16), 'ZIP symlink')
            require(pin(archive.read(item.filename)) == actual[item.filename], 'ZIP bytes differ ' + item.filename)
        require(archive.testzip() is None, 'ZIP CRC failure')
        zip_count = len(infos)
    require((PACKAGE / 'outer_pedal_flag.tex').read_bytes() == (MATERIALS / 'outer_pedal_flag.tex').read_bytes(), 'LaTeX copies differ')
    metadata = json.loads((MATERIALS / 'metadata.json').read_text())
    deposit = json.loads((PACKAGE / 'zenodo-deposit.json').read_text())
    require(metadata == deposit['metadata'] == seal['metadata_exact'], 'Metadata inconsistency')
    require([v['path'] for v in deposit['files']] == list(seal['upload_files']), 'Deposit upload list differs')
    nested = []
    for path in sorted(MATERIALS.rglob('*.json')):
        d = json.loads(path.read_text())
        if 'manifest' not in path.name.lower() or path == MATERIALS/'MANIFEST.json' or not isinstance(d, dict):
            continue
        mapping = d.get('files', d.get('safe_allowlist'))
        if isinstance(mapping, list):
            mapping = {v['path']: v for v in mapping}
        if isinstance(mapping, dict):
            n = verify_map(path.parent, mapping, str(path.relative_to(MATERIALS)))
            nested.append({'manifest': str(path.relative_to(MATERIALS)), 'entries': n})
    for rel in ['audit/ROOT_MATHEMATICAL_GATE_01.json', 'audit/ROOT_PRIORITY_AND_EDITORIAL_GATE_01.json', 'audit/root_reproduction_01/ROOT_INPUT_CUSTODY.json']:
        d = json.loads((MATERIALS/rel).read_text())
        n = verify_map(MATERIALS/'audit', d['safe_files'], rel)
        nested.append({'manifest': rel, 'entries': n})
    provenance = json.loads((MATERIALS/'verification/PORTABILITY_PROVENANCE.json').read_text())
    for v in provenance:
        original = (MATERIALS/'audit'/v['source']).read_bytes()
        portable = (MATERIALS/v['portable']).read_bytes()
        require(pin(original) == v['source_pin'] and pin(portable) == v['portable_pin'], 'Provenance pin mismatch')
        transformed = original.decode()
        for line in v['removed_lines']:
            require(transformed.count(line) == 1, 'Provenance removal occurrence')
            transformed = transformed.replace(line, '')
        require(transformed.encode() == portable, 'Unstated portable code change')
        require(pin((MATERIALS/'audit'/v['expected_result_source']).read_bytes()) == v['expected_result_pin'], 'Expected-source pin')
    custody = json.loads((MATERIALS/'audit/ORIGINAL_SUBMISSION_CUSTODY.json').read_text())
    missing_originals = [name for name in custody['files'] if not any(p.name == Path(name).name and pin(p.read_bytes()) == {k:v[k] for k in ('bytes','sha256')} for p in MATERIALS.rglob('*') if p.is_file() for v in [custody['files'][name]])]
    result = {'UTC': datetime.now(timezone.utc).isoformat(), 'seal': pin(seal_bytes), 'all_supplied_pins_pass': True,
              'uploads_verified': upload_count, 'sealed_all_package_files': safe_count, 'material_files': len(actual), 'root_manifest_entries': root_count,
              'zip_entries': zip_count, 'zip_all_bytes_equal_materials': True, 'source_copies_equal': True,
              'metadata_consistent': True, 'nested_manifests': nested, 'portable_provenance_scripts': len(provenance),
              'promised_original24_absent': missing_originals,
              'scope': 'All supplied hashes/coverage passed; this does not cure absent original24 promised by README.'}
    (HERE/'INTEGRITY_RECEIPT.json').write_text(json.dumps(result, indent=2)+'\n')
    print(json.dumps(result, indent=2))

if __name__ == '__main__':
    main()
