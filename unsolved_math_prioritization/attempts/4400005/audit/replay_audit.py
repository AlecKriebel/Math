#!/usr/bin/env python3
"""Offline replay: exact frozen input binding and independent finite controls.

Usage: python3 replay_audit.py /path/to/AUTHOR_PACKET.zip
No network, imports from the packet, repository writes, or source PDFs needed.
The frozen verifier is executed in a temporary directory only after its digest,
all packet file digests, and the whole ZIP digest have been checked.
"""
import argparse
import hashlib
import itertools
import json
from fractions import Fraction
from pathlib import Path
import subprocess
import sys
import tempfile
import zipfile

EXPECTED_ZIP_SHA256 = '66c2af685b3e86b88f78659db26aa60698415e7cab966bc3fa737d4794879bcf'
EXPECTED_ZIP_BYTES = 16393
EXPECTED_FILES = {
    'README.md': (1157, '52ed5a0bfffd8d66fdabbff9037cd5809c054854ce8348fde014e4591acdc903'),
    'analysis.md': (12426, '6e1e90162c8a7286d6f40a3b21fc369782f16df5565e844948540e22b1ec1a90'),
    'controls.json': (1919, '7f207b7128c63642d995ddafc8504223167d089cc9568b8a09c92ed965eef229'),
    'research_log.md': (2131, '319e8364a71b4b6d9001a58a9522b437b17911db59305390bf33a0f5e1b6f4e8'),
    'result.json': (4045, '9f366f185faf91b5e26ed2af275903a2c14ff29c06a6bf05b10ef44af170a286'),
    'source_map.md': (5034, 'a6f9c8f567e40a4c3db3a1736243bddaf632a5f9b8d0761cb0db61cf905f94ec'),
    'verification_metadata.json': (7116, 'd9a50fe3f3c8f5210e4f05c23c7332128193c27910d998484feaa0130d144914'),
    'verify.py': (3339, '433b7f2317c5d43e67ed837e62e576f6314e5319fbb32915c945610f27d9dea8'),
}

def require(predicate, message):
    if not predicate:
        raise AssertionError(message)


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('packet', type=Path)
    args = parser.parse_args()
    data = args.packet.read_bytes()
    require(len(data) == EXPECTED_ZIP_BYTES, 'Archive byte count changed')
    require(hashlib.sha256(data).hexdigest() == EXPECTED_ZIP_SHA256, 'Archive hash changed')
    with zipfile.ZipFile(args.packet) as archive:
        names = archive.namelist()
        require(len(names) == len(set(names)) == len(EXPECTED_FILES), 'Unexpected or duplicate archive entries')
        require(set(names) == set(EXPECTED_FILES), 'Archive file set changed')
        packet = {}
        inputs = []
        for name, (size, digest) in EXPECTED_FILES.items():
            payload = archive.read(name)
            actual_digest = hashlib.sha256(payload).hexdigest()
            require(len(payload) == size, 'File size changed: ' + name)
            require(actual_digest == digest, 'File hash changed: ' + name)
            packet[name] = payload
            inputs.append({'path': name, 'bytes': size, 'sha256': digest})
    with tempfile.TemporaryDirectory(prefix='geodesic-audit-') as folder:
        verifier = Path(folder) / 'verify.py'
        verifier.write_bytes(packet['verify.py'])
        completed = subprocess.run([sys.executable, '-I', str(verifier)], cwd=folder, text=True,
                                   capture_output=True, timeout=60, check=True)
        frozen_output = json.loads(completed.stdout)
    expected_controls = json.loads(packet['controls.json'])
    authored_result = json.loads(packet['result.json'])
    require(frozen_output == expected_controls, 'Frozen verifier and controls.json disagree')
    require(frozen_output == authored_result['controls'], 'Frozen verifier and result.json disagree')
    require(frozen_output['all_passed'] and frozen_output['assertions'] == 754, 'Frozen controls fail')

    checks = 0
    def test(value, context):
        nonlocal checks
        require(value, context)
        checks += 1

    roots = []
    enumerated = 0
    for n in range(1, 10):
        rotation = tuple((j+1) % n for j in range(n))
        count = 0
        for permutation in itertools.permutations(range(n)):
            enumerated += 1
            if all(permutation[permutation[j]] == rotation[j] for j in range(n)):
                count += 1
                test(all(permutation[rotation[j]] == rotation[permutation[j]] for j in range(n)),
                     'A permutation root must commute with its square')
                test(all(permutation[j] == (j+permutation[0]) % n for j in range(n)),
                     'A map commuting with a single cycle must be a power of that cycle')
        test(count == int(n % 2 == 1), 'Cycle square-root count differs from independent modular criterion')
        roots.append({'cycle_length': n, 'permutation_square_roots': count})

    # Explicit independent inverse-limit controls: odd roots are compatible;
    # even roots fail modulo 2, and the parity eigenfunction is real-valued.
    odd_root_rows = []
    for odd in (1, 3, 5, 7, 9, 11, 13, 15):
        prev = None
        for k in range(1, 19):
            modulus = 1 << k
            inverse = pow(odd, -1, modulus)
            test((odd * inverse) % modulus == 1, 'Odd root modular identity')
            if prev is not None:
                test(inverse % (modulus // 2) == prev, 'Odd roots must be inverse-limit compatible')
            prev = inverse
        odd_root_rows.append({'root_order': odd, 'maximum_modulus': 1 << 18, 'compatible': True})
    for even in range(2, 34, 2):
        test(not any((even * r) % 2 == 1 for r in range(2)), 'Even root obstruction modulo 2')
    for k in range(1, 14):
        modulus = 1 << k
        test(all((1 if ((j+1) % modulus) % 2 == 0 else -1) ==
                 -(1 if j % 2 == 0 else -1) for j in range(modulus)), 'Parity eigenfunction identity')

    # Nonergodic control: a four-cycle roots the product of two flips.
    r = (1, 2, 3, 0)
    r_squared = tuple(r[r[j]] for j in range(4))
    test(r_squared == (2, 3, 0, 1), 'Nonergodic two-flip root control')
    test(r_squared[0] == 2 and r_squared[2] == 0, 'First invariant component')
    test(r_squared[1] == 3 and r_squared[3] == 1, 'Second invariant component')

    # Probability measures supported on rational flow circles. This control
    # does not assume that the given manifold has a rational closed orbit.
    circle_cases = 0
    for numerator in range(1, 21):
        for denominator in range(1, 21):
            length = Fraction(numerator, denominator)
            p, q = length.numerator, length.denominator
            support = {(Fraction(j) % length) for j in range(p)}
            test(len(support) == p, 'Time-one rational circle orbit cardinality')
            test({(x+1) % length for x in support} == support, 'Time-one invariance')
            test(not support.intersection({(x+Fraction(1, 2*q)) % length for x in support}),
                 'A nonzero real flow shift moves support off itself')
            circle_cases += 1

    # A manuscript arithmetic slip need not spoil Borel-Cantelli: the bound
    # 6/2**(k+1) is still summable although it is not less than 1/2**k.
    test(Fraction(6, 2**3) > Fraction(1, 2**2), 'Identify the factor-three comparison slip')
    partial = sum((Fraction(6, 2**(k+1)) for k in range(1, 40)), Fraction())
    test(partial < 3, 'Corrected summable bound remains sufficient')

    output = {
        'archive': {'name': 'AUTHOR_PACKET.zip', 'bytes': len(data), 'sha256': EXPECTED_ZIP_SHA256},
        'bound_files': inputs,
        'input_binding_passed': True,
        'frozen_controls_replay': {'matches_controls_json': True, 'matches_result_json': True,
                                   'assertions': frozen_output['assertions'],
                                   'permutations_enumerated': frozen_output['permutations_enumerated']},
        'independent_controls': {'all_passed': True, 'assertions': checks,
                                 'permutations_enumerated': enumerated, 'cycle_root_counts': roots,
                                 'compatible_odd_roots': odd_root_rows, 'rational_circle_cases': circle_cases,
                                 'nonergodic_countercontrol_passed': True},
        'limitations': ['Finite controls are not a proof of specification or universality.',
                        'Mathematical applicability is assessed in AUDIT.md.'],
    }
    print(json.dumps(output, indent=2, sort_keys=True))

if __name__ == '__main__':
    main()
