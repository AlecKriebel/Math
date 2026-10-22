"""Read-only verification of prior own closed audits, with no shared writes."""
import hashlib
import json
from pathlib import Path

ROOT = Path('/Users/alec/Documents/Math/final_full_solution_sweep_20261020_01a15be7')
PINS = [
    ("pr1346_30000215/independent_original_prior_review01", "3f3b946ddddce4061996fd277b195627a5eccd8942fad25ce943a619d9387009"),
    ("pr1337_30004534/independent_original_prior_review01", "75e8c43616471802659d0fc140030633ebb49af733320bb654086f7d614a7989"),
    ("pr1312_3109/independent_original_prior_review01", "d2a4c7440e3ef63fd4a6e3d0ea8a5ae7f3292c7b727ff4955916b2823b572195"),
    ('pr1311_3100082/independent_original_prior_review01', 'd025774e252a04fbe192540fb5dfc37fa51f007ba1752116417fb88a68737c21'),
    ('pr1314_2800905/independent_original_prior_review01', 'f7ee0e9e7cacfbd50431b742cdd7072fa3213e87f5d33d69a300388d8ccb1725'),
    ('pr1297_30002198/independent_original_scope_review01', '01318ecd77a1c0abb7e0d735f81b2dcdb546a5971ae04ea93dcabb2abbcf0cb0'),
    ('pr1235_30000107/independent_correctness_scope_review01', 'b3a4c8c288a2b5bc948ec14cc587eabd516f046841cac339fc70d917a2710fcd'),
    ('pr1239_20001003/independent_correctness_scope_review01', '4cd3f45e08d1357412d7c73197020d500c516b13d5917716803ca234d755ee1d'),
    ('pr1253_30001703/independent_original_prior_review01', '75c42a859d4b34978fe5668c26c5462a7d780b5b9809076879b25332f6dddc3a'),
    ('pr1260_30000663/independent_original_prior_review01', '070af027d855d3084c40f6779596d50c266ea5939f7fac91ca62b00e4dc79c15'),
    ('pr1263_30002470/independent_original_prior_review01', '6cd9d07c4088068eeb4195b5874bac59289d26cf79281e5309d6f0b47cd4ce81'),
    ('pr1270_2200014/independent_original_prior_review01', 'bc0c67e9c270c43c317189e187fe4ce61ed35db9f46c159420ead4613ecd3407'),
    ('pr1279_3223/independent_original_prior_review01', '22db38138f75019b258c32e8603daf7452532cb39573b7f288cf25bc28743d01'),
    ('pr1294_10400226/independent_original_prior_review01', 'ce6837d19a0273f75d7a2ceee777cbecfcf256fc3ba6e89b8de101d0c51b55ba'),
    ('pr1296_20000125/independent_original_prior_review01', '44795bafafca4c971f4f6957a967c8811535733959a3445cc8121f12814c9fde'),
]


def sha(p):
    return hashlib.sha256(p.read_bytes()).hexdigest()


def main():
    out = []
    for rel, seal_digest in PINS:
        folder = ROOT / 'audits' / rel
        seal_path = folder / 'CLOSED_DIRECTORY_SEAL.json'
        if sha(seal_path) != seal_digest:
            raise RuntimeError('earlier seal digest changed: ' + rel)
        seal = json.loads(seal_path.read_text())
        exclusions = seal['exclusion_exact_relative_paths']
        if exclusions != ['CLOSED_DIRECTORY_SEAL.json']:
            raise RuntimeError('unexpected prior exclusions')
        physical = {str(p.relative_to(folder)) for p in folder.rglob('*') if p.is_file()}
        expected = {r['path'] for r in seal['members']}
        if physical - set(exclusions) != expected:
            raise RuntimeError('prior physical membership changed: ' + rel)
        for member in seal['members']:
            path = folder / member['path']
            if path.stat().st_size != member['bytes'] or sha(path) != member['sha256']:
                raise RuntimeError('prior payload changed: ' + rel + '/' + member['path'])
        out.append({'prior_audit': rel, 'seal_sha256': seal_digest,
                    'member_count': len(expected), 'all_members_pass': True})
    print(json.dumps({'schema': 'read-only-prior-own-seal-recheck-v1',
                      'status': 'PASS', 'audits': out}, indent=2))


if __name__ == '__main__':
    main()
