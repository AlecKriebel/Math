"""Build this note's deterministic source/verification archive and file pins."""
import hashlib
import json
import pathlib
import zipfile

ROOT = pathlib.Path(__file__).resolve().parent / 'publication'
ARCHIVE = ROOT / 'full_stress_stratifications_source_verification_v1.zip'


def main():
    files = [ROOT / name for name in (
        'research_note.tex', 'research_note.pdf', 'README.md', 'SUPPLEMENT.md',
        'run_checks.py', 'metadata.json')]
    for directory in ('checks', 'expected', 'evidence'):
        files.extend(path for path in (ROOT / directory).rglob('*') if path.is_file())
    files.sort(key=lambda p: p.relative_to(ROOT).as_posix())
    records = []
    for path in files:
        data = path.read_bytes()
        records.append({'path': path.relative_to(ROOT).as_posix(),
                        'bytes': len(data), 'sha256': hashlib.sha256(data).hexdigest()})
    manifest = ROOT / 'PACKAGE_MANIFEST.json'
    manifest.write_text(json.dumps({
        'version': '1.0',
        'claim': 'Literal equality of full fixed-labelled connected coordinate-sign stress partitions determines a simple graph, for n,d>=1, with collisions retained.',
        'license': 'CC-BY-4.0',
        'third_party_papers_redistributed': False,
        'manifest_self_hash_excluded': True,
        'files': records,
    }, indent=2) + '\n')
    files.append(manifest)
    with zipfile.ZipFile(ARCHIVE, 'w', compression=zipfile.ZIP_DEFLATED,
                         compresslevel=9) as archive:
        for path in sorted(files, key=lambda p: p.relative_to(ROOT).as_posix()):
            info = zipfile.ZipInfo('full_stress_stratifications_v1/' +
                                  path.relative_to(ROOT).as_posix(),
                                  date_time=(2026, 10, 12, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, path.read_bytes())
    metadata = json.loads((ROOT / 'metadata.json').read_text())
    (ROOT / 'zenodo-deposit.json').write_text(json.dumps({
        'metadata': metadata,
        'files': [
            {'path': 'research_note.pdf',
             'name': 'full_stress_stratifications_determine_a_labelled_graph.pdf'},
            {'path': ARCHIVE.name},
        ]}, indent=2) + '\n')
    print(json.dumps({'archive': ARCHIVE.name, 'files': len(files),
                      'bytes': ARCHIVE.stat().st_size,
                      'sha256': hashlib.sha256(ARCHIVE.read_bytes()).hexdigest()}))


if __name__ == '__main__':
    main()
