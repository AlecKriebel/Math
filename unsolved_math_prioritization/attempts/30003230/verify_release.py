#!/usr/bin/env python3
"""Read-only byte-bound replay of the corrected composite, not a general proof."""
from pathlib import Path
import hashlib
import json
import subprocess
import sys
import zipfile

ROOT = Path(__file__).resolve().parent
AUTHOR_MANIFEST = '5d6dfeea07270a9a307fc7e21a623cd427826c0f9eb638ffcb389ea9c6e324f2'
AUDIT_MANIFEST = 'bce51a0b41f5712d524189d2da4ed1c799d305c2eb8e2d90d0a3990585a02128'
AUTHOR_ZIP = 'STRINGY_DIVISORIAL_30003230_SAFE_PACKET.zip'
AUDIT_ZIP = 'STRINGY_DIVISORIAL_30003230_INDEPENDENT_AUDIT_SAFE.zip'

def require(ok, message):
    if not ok:
        raise RuntimeError(message)

def digest(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()

def load(name):
    return json.loads((ROOT / name).read_text(encoding='utf-8'))

def main():
    manifest = load('PUBLICATION_MANIFEST.json')
    expected = set(manifest['files']) | {'PUBLICATION_MANIFEST.json'}
    nodes = list(ROOT.rglob('*'))
    require(not any(p.is_symlink() for p in nodes), 'Symlinks are not allowed')
    require({p.relative_to(ROOT).as_posix() for p in nodes if p.is_file()} == expected, 'Publication allowlist differs')
    require({p.relative_to(ROOT).as_posix() for p in nodes if p.is_dir()} == {'author', 'audit'}, 'Publication directory set differs')
    for name, meta in manifest['files'].items():
        p = ROOT / name
        require(len(p.read_bytes()) == meta['bytes'] and digest(p) == meta['sha256'], 'Publication member mismatch: ' + name)
    for folder, mh, archive, zh, size in [
        ('author', AUTHOR_MANIFEST, AUTHOR_ZIP, 'b6c69b1639fd31f5a8ed675fa7ddaac6e097cf669419ff8222315af9dba86710', 17356),
        ('audit', AUDIT_MANIFEST, AUDIT_ZIP, '1b227a011882ae8bfd418794a24fa075e61664a9676c944a237bcbfbc6345150', 18920),
    ]:
        require(digest(ROOT / folder / 'MANIFEST.json') == mh, 'Frozen manifest changed: ' + folder)
        require(digest(ROOT / archive) == zh and (ROOT / archive).stat().st_size == size, 'Frozen archive changed: ' + folder)
        frozen = load(folder + '/MANIFEST.json')
        members = set(frozen['files']) | {'MANIFEST.json'}
        require({p.name for p in (ROOT / folder).iterdir()} == members, 'Frozen member set changed')
        for name, meta in frozen['files'].items():
            p = ROOT / folder / name
            require(p.stat().st_size == meta['bytes'] and digest(p) == meta['sha256'], 'Frozen member changed: ' + name)
        with zipfile.ZipFile(ROOT / archive) as z:
            require(len(z.namelist()) == len(members) and set(z.namelist()) == members, 'Archive member set differs')
            for name in members:
                require(z.read(name) == (ROOT / folder / name).read_bytes(), 'Archive member bytes differ')
    status = load('release_status.json')
    require(status['status'] == 'unsolved' and status['turns'] == '5/5' and not status['general_conjecture_resolved'], 'Current scope changed')
    require(status['original_provenance_verdict'] == 'REVISE_REQUIRED' and status['composite_verdict'] == 'SCOPED_PASS_WITH_CONTROLLING_C1', 'Verdict distinction lost')
    require(status['controlling_overlay'] == 'audit/SOURCE_METADATA_CORRECTION.json', 'Controlling overlay missing')
    correction = load(status['controlling_overlay'])
    require(correction['controlling'] is True and correction['correction_id'] == 'C1', 'Correction authority changed')
    require(correction['corrected_fields']['url'] == 'https://ems.press/content/serial-article-files/46651?nt=1', 'EMS identity changed')
    require(correction['corrected_fields']['pdf_bytes'] == 661526 and correction['separately_bound_MFO_copy']['bytes'] == 626588, 'Source byte identities conflated')
    require(correction['mathematical_revision_required'] is False, 'Correction scope changed')
    p = subprocess.run([sys.executable, *(['-O'] if sys.flags.optimize else []), str(ROOT / 'audit/check_audit.py'), str(ROOT / 'author'), str(ROOT / AUTHOR_ZIP)], capture_output=True)
    require(p.returncode == 0 and not p.stderr, 'Frozen audit replay failed: ' + p.stderr.decode(errors='replace'))
    replay = json.loads(p.stdout)
    require(replay['original_packet_verdict'] == 'REVISE_REQUIRED' and replay['corrected_composite_verdict'] == 'PASS' and replay['independent_checks'] == 53895, 'Replay verdict changed')
    print(json.dumps({'publication_verified': True, 'problem_id': '30003230', 'status': 'unsolved', 'turns': '5/5', 'original_provenance_verdict': 'REVISE_REQUIRED', 'composite_verdict': 'SCOPED_PASS_WITH_CONTROLLING_C1', 'author_checks': 2427, 'independent_checks': 53895, 'publication_file_count': len(expected), 'geometric_realization_certified_by_numerics': False}, sort_keys=True, indent=2))

if __name__ == '__main__':
    main()
