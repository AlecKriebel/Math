#!/usr/bin/env python3
"""Independent frozen-package checks. Read-only; standard library; no network."""
import hashlib
import json
from pathlib import Path
import subprocess
import sys

BASE = Path(__file__).resolve().parent.parent
PUB = BASE / 'public'
EXPECTED_MANIFEST = 'f9a155e07ffa4391de564c59d147c26071b0dfb7de5b37ee127c27e8b99fa0ed'
EXPECTED_PROOF = 'd020ba52a186b8384c651311e86c5860eb77c39256c25be87cced7759f503272'

def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()

def main():
    assert digest(PUB / 'SHA256SUMS.json') == EXPECTED_MANIFEST
    assert digest(PUB / 'PROOF.md') == EXPECTED_PROOF
    manifest = json.loads((PUB / 'SHA256SUMS.json').read_text())
    actual = {p.relative_to(PUB).as_posix() for p in PUB.rglob('*') if p.is_file()}
    assert actual == set(manifest['files']) | {'SHA256SUMS.json'}
    assert len(actual) == 12
    for name, expected in manifest['files'].items():
        data = (PUB / name).read_bytes()
        assert len(data) == expected['bytes'], name
        assert hashlib.sha256(data).hexdigest() == expected['sha256'], name
    m = subprocess.check_output([sys.executable, str(PUB / 'verify_manifest.py')])
    assert json.loads(m)['status'] == 'PASS'
    output = subprocess.check_output([sys.executable, str(PUB / 'verify.py')])
    controls = json.loads(output)
    assert output == (PUB / 'CHECKS.json').read_bytes()
    assert controls['assertions'] == 1718
    assert sum(controls['counts'].values()) == 1718
    assert controls['status'] == 'PASS'
    status = json.loads((PUB / 'STATUS.json').read_text())
    assert status['status'] == 'unsolved'
    assert status['turns_used'] == status['turn_budget'] == 5
    assert not status['full_solution_claimed'] and not status['formal_verification']
    sources = json.loads((PUB / 'SOURCE_MANIFEST.json').read_text())
    names = ['hayman-lingham-2018.pdf','jenkins-1959.pdf','huber-1986.pdf',
             'vainio-1989.pdf','vainio-1995.pdf','bishop-2007.pdf']
    verified = []
    for record, name in zip(sources['sources'], names):
        file = BASE / 'private' / name
        assert file.stat().st_size == record['observed_bytes'], name
        assert digest(file) == record['observed_sha256'], name
        assert not record['included_in_public_package'], name
        verified.append({'name': name, 'bytes': file.stat().st_size, 'sha256': digest(file)})
    selected = json.loads((BASE / 'private' / 'selected-problem.json').read_text())[0]
    old = json.loads((BASE / 'private' / 'selected-research_results.json').read_text())['AMR-022-6063']
    assert selected['id'] == 2306063
    assert 'positive continuous function' in selected['statement']
    assert '\\varepsilon(x)' in selected['statement']
    assert '\\varepsilon>0' in old['problem']
    # The six downloaded sources remain private. Public inventory is prose/JSON/Python only.
    assert all(Path(name).suffix in {'.md','.json','.py'} for name in actual)
    assert digest(PUB / 'SHA256SUMS.json') == EXPECTED_MANIFEST
    assert digest(PUB / 'PROOF.md') == EXPECTED_PROOF
    print(json.dumps({
        'mechanical_status':'PASS',
        'mathematical_verdict':'PASS_AS_UNSOLVED_RESTRICTED_RESULTS',
        'problem_id':2306063,'rank':585,
        'public_file_count':len(actual),
        'manifest_sha256':EXPECTED_MANIFEST,'proof_sha256':EXPECTED_PROOF,
        'author_controls_reproduced':1718,'checks_json_reproduced_byte_for_byte':True,
        'private_source_files_verified':verified,
        'source_tolerance_correction_confirmed':True,
        'frozen_public_files_modified':False,
        'mandatory_corrections':[],
        'limitations':[
            'Mechanical checks are supplementary, not formal mathematical verification.',
            'Source-byte checks establish consistency with the manifest, not independent provenance of each download.',
            'No new live repository publication gate is performed by this script.',
            'Global current literature status and completeness of historical searches are not certified.'
        ]
    },indent=2,sort_keys=True))

if __name__ == '__main__':
    main()
