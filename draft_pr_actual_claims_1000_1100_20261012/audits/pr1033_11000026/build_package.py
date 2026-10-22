"""Build the deterministic source and written-verification archive."""
import hashlib
import json
from pathlib import Path
import zipfile

ROOT = Path(__file__).resolve().parent / 'publication'
ARCHIVE = ROOT / 'teichmuller_original_ball_paths_source_audits_v1.zip'


def main():
    files = [ROOT / n for n in ('research_note.tex', 'research_note.pdf', 'README.md',
                               'SUPPLEMENT.md', 'metadata.json')]
    files += [p for p in (ROOT / 'evidence').rglob('*') if p.is_file()]
    files.sort(key=lambda p: p.relative_to(ROOT).as_posix())
    rows = [{'path': p.relative_to(ROOT).as_posix(), 'bytes': p.stat().st_size,
             'sha256': hashlib.sha256(p.read_bytes()).hexdigest()} for p in files]
    manifest = ROOT / 'PACKAGE_MANIFEST.json'
    manifest.write_text(json.dumps({'version': '1.0', 'license': 'CC-BY-4.0',
        'claim': 'Expository corollary of LR: original closed half-log Teichmuller ball paths of length at most ambient distance plus 4c_g for all fixed closed genus g>=2.',
        'third_party_papers_redistributed': False, 'executable_verification_claimed': False,
        'manifest_self_hash_excluded': True, 'files': rows}, indent=2) + '\n')
    files.append(manifest)
    with zipfile.ZipFile(ARCHIVE, 'w', compression=zipfile.ZIP_DEFLATED, compresslevel=9) as z:
        for p in sorted(files, key=lambda p: p.relative_to(ROOT).as_posix()):
            info = zipfile.ZipInfo('teichmuller_original_ball_paths_v1/' + p.relative_to(ROOT).as_posix(),
                                   date_time=(2026, 10, 13, 0, 0, 0))
            info.create_system = 3
            info.external_attr = 0o100644 << 16
            info.compress_type = zipfile.ZIP_DEFLATED
            z.writestr(info, p.read_bytes())
    metadata = json.loads((ROOT / 'metadata.json').read_text())
    (ROOT / 'zenodo-deposit.json').write_text(json.dumps({'metadata': metadata, 'files': [
        {'path': 'research_note.pdf', 'name': 'teichmuller_original_ball_paths_expository_corollary.pdf'},
        {'path': ARCHIVE.name}]}, indent=2) + '\n')
    print(json.dumps({'entries': len(files), 'archive_bytes': ARCHIVE.stat().st_size,
                      'archive_sha256': hashlib.sha256(ARCHIVE.read_bytes()).hexdigest()}))


if __name__ == '__main__':
    main()
