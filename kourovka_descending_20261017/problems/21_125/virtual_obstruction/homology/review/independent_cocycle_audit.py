#!/usr/bin/env python3
"""Independent rank-five audit; no imports from any author program.

Run from any directory.  Inputs are read only; output is written only when
explicitly requested.  Graph and target definitions come from the mathematical
claim, rather than the certificate's computed permutation/word fields.
"""
import argparse
import datetime
import hashlib
import json
from collections import deque
from pathlib import Path


def require(condition, message):
    if not condition:
        raise ValueError(message)


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def inverse(word):
    return [-letter for letter in reversed(word)]


def substitute(word):
    answer = []
    for letter in word:
        i = abs(letter)
        image = [i] if i == 1 else [i, i - 1]
        answer.extend(image if letter > 0 else inverse(image))
    return answer


def commutator(first, second):
    return first + second + inverse(first) + inverse(second)


def audit(certificate_path, check_manifest=True):
    root = Path(__file__).resolve().parent.parent
    certificate = json.loads(certificate_path.read_text())
    manifest = json.loads((root / 'FROZEN_INPUTS.json').read_text())
    frozen_receipt = []
    for item in manifest['files']:
        path = root / item['file']
        actual_hash = digest(path)
        actual_size = path.stat().st_size
        matches = actual_hash == item['sha256'] and actual_size == item['bytes']
        if check_manifest:
            require(matches, 'Frozen input changed: ' + item['file'])
        frozen_receipt.append(dict(file=item['file'], sha256=actual_hash,
                                   bytes=actual_size, matches_manifest=matches))

    # Literal graph from the compact mathematical specification.  Encoding is
    # vertex = v + 32*s, independently checked against the certificate.
    epsilon = {(2, 1), (3, 1), (5, 2), (6, 2), (10, 3), (12, 3)}
    permutations = []
    for i in range(5):
        permutation = []
        for vertex in range(64):
            v, s = vertex % 32, vertex // 32
            permutation.append((v ^ (1 << i)) + 32 * (s ^ int((v, i) in epsilon)))
        require(sorted(permutation) == list(range(64)), 'Graph is not a cover')
        permutations.append(permutation)
    require(certificate['permutations'] == permutations,
            'Certificate does not encode the six-entry epsilon graph')
    period = certificate['stable_letter_power']
    require(period in (8, 16), 'This audit supports the explicit r=8 and r=16 claims')
    subgroup_index = 64 * period
    require((certificate['m'], certificate['fiber_cover_degree'], certificate['index']) == (5, 64, subgroup_index),
            'Incorrect advertised rank, degree, power, or index')
    inverses = []
    for permutation in permutations:
        inv = [None] * 64
        for source, target in enumerate(permutation):
            inv[target] = source
        inverses.append(inv)

    def walk(word, start=0, weights=None):
        position, value = start, 0
        for letter in word:
            require(type(letter) is int and 1 <= abs(letter) <= 5,
                    'Illegal free-generator letter')
            generator = abs(letter) - 1
            if letter > 0:
                if weights is not None:
                    value += weights.get((position, generator), 0)
                position = permutations[generator][position]
            else:
                position = inverses[generator][position]
                if weights is not None:
                    value -= weights.get((position, generator), 0)
        return position, value

    reached, queue, tree_words = {0}, deque([0]), {0: []}
    while queue:
        vertex = queue.popleft()
        for signed in list(range(1, 6)) + list(range(-5, 0)):
            target, _ = walk([signed], vertex)
            if target not in reached:
                reached.add(target)
                tree_words[target] = tree_words[vertex] + [signed]
                queue.append(target)
    require(len(reached) == 64, 'Disconnected graph')

    theta_powers = [[[i] for i in range(1, 6)]]
    for _ in range(16):
        theta_powers.append([substitute(word) for word in theta_powers[-1]])
    theta_r = theta_powers[period]
    def substitute_power(word, exponent):
        transformed = []
        for letter in word:
            image = theta_powers[exponent][abs(letter) - 1]
            transformed.extend(image if letter > 0 else inverse(image))
        return transformed
    identity_lift_exponents = []
    for exponent, images in enumerate(theta_powers[1:], 1):
        if all(walk(images[i], vertex)[0] == permutations[i][vertex]
               for i in range(5) for vertex in range(64)):
            identity_lift_exponents.append(exponent)
    require(period in identity_lift_exponents, 'theta^r does not lift fixing vertices')

    # A theta^k lift may permute vertices while fixing the root.  Merely
    # failing the identity lift is insufficient to exclude subgroup invariance.
    # Test the unique possible rooted lift and retain explicit closed-loop
    # counterexamples for the disputed smaller exponents.
    rooted_lift_checks = []
    for exponent in (1, 2, 4, 8, 16):
        vertex_map = [walk(substitute_power(tree_words[v], exponent))[0] for v in range(64)]
        failures = []
        for vertex in range(64):
            for i in range(5):
                target = permutations[i][vertex]
                actual = walk(theta_powers[exponent][i], vertex_map[vertex])[0]
                if actual != vertex_map[target]:
                    loop = tree_words[vertex] + [i + 1] + inverse(tree_words[target])
                    require(walk(loop)[0] == 0, 'Proposed counterexample is not a loop')
                    transformed_endpoint = walk(substitute_power(loop, exponent))[0]
                    require(transformed_endpoint != 0, 'Proposed counterexample fails to obstruct')
                    failures.append(dict(word=loop, image_endpoint=transformed_endpoint))
        item = dict(exponent=exponent, rooted_edge_failures=len(failures),
                    preserves_based_subgroup=not failures)
        if failures:
            item['closed_loop_counterexample'] = min(failures, key=lambda item: len(item['word']))
        else:
            require(sorted(vertex_map) == list(range(64)), 'Rooted lift fails bijectivity')
        rooted_lift_checks.append(item)

    # A distinct cross-check of index and conjugation convention: build a
    # transitive right action of G5 on (q, vertex), q in Z/r.  Here ai acts by
    # theta^q(ai) and t decrements q.  It satisfies t^-1 ai t = ai*a(i-1).
    actions = []
    for i in range(5):
        action = []
        for q in range(period):
            action.extend(q * 64 + walk(theta_powers[q][i], v)[0] for v in range(64))
        require(sorted(action) == list(range(subgroup_index)), 'Invalid full ai action')
        actions.append(action)
    t_action = [((point // 64 - 1) % period) * 64 + point % 64 for point in range(subgroup_index)]
    t_inverse = [((point // 64 + 1) % period) * 64 + point % 64 for point in range(subgroup_index)]
    relator_checks = 0
    for i in range(5):
        for point in range(subgroup_index):
            lhs = t_action[actions[i][t_inverse[point]]]
            rhs = actions[i][point]
            if i:
                rhs = actions[i - 1][rhs]
            require(lhs == rhs, 'Full Hydra conjugation relation failed')
            relator_checks += 1
    all_reached, queue = {0}, deque([0])
    while queue:
        point = queue.popleft()
        for action in actions + [t_action]:
            target = action[point]
            if target not in all_reached:
                all_reached.add(target)
                queue.append(target)
    require(len(all_reached) == subgroup_index, 'Full Hydra action is not transitive')

    characters = {}
    edge_cell_checks = 0
    for record in certificate['characters']:
        index = record['index']
        require(type(index) is int and index not in characters, 'Duplicate character index')
        weights = {}
        for key, value in record['positive_edge_weights'].items():
            coordinates = key.split(',')
            require(len(coordinates) == 2, 'Malformed edge key')
            edge = tuple(map(int, coordinates))
            require(0 <= edge[0] < 64 and 0 <= edge[1] < 5 and type(value) is int,
                    'Nonintegral or out-of-range edge weight')
            weights[edge] = value
        potentials = record['vertex_potentials']
        require(len(potentials) == 64 and all(type(x) is int for x in potentials),
                'Nonintegral or wrong-sized vertex potential')
        for vertex in range(64):
            for i in range(5):
                endpoint, image_weight = walk(theta_r[i], vertex, weights)
                target = permutations[i][vertex]
                require(endpoint == target, 'Lift endpoint mismatch')
                difference = image_weight - weights.get((vertex, i), 0)
                require(difference == potentials[target] - potentials[vertex],
                        f'Cell identity failed for character {index}, vertex {vertex}, generator {i+1}')
                edge_cell_checks += 1
        characters[index] = weights
    require(len(characters) == 9 and edge_cell_checks == 2880, 'Incorrect character/cell count')

    expected_targets = [(f'a{i}', [i]) for i in range(1, 6)]
    expected_targets.extend((f'[a{i},a{j}]', commutator([i], [j]))
                            for i in range(1, 6) for j in range(i + 1, 6))
    nested = [1]
    for i in range(2, 6):
        nested = commutator(nested, [i])
        expected_targets.append((f'left_nested_through_a{i}', nested))
    require(len(certificate['targets']) == len(expected_targets), 'Missing or extra target')
    target_receipt = []
    for record, (label, word) in zip(certificate['targets'], expected_targets):
        require(record['label'] == label and record['word'] == word,
                'Target is not the declared generator or left-nested commutator')
        orbit, position = [], 0
        while position not in orbit:
            orbit.append(position)
            position, _ = walk(word, position)
        require(position == 0, 'Word permutation is not invertible')
        power = len(orbit)
        require(record['power_closing_in_fiber_cover'] == power,
                'Recorded power is not the exact first closed lift')
        weights = characters[record['character_index']]
        endpoint, value = walk(word * power, weights=weights)
        require(endpoint == 0, 'Target power not in L')
        require(value != 0 and record['visible'] is True,
                'Target has zero character evaluation')
        require(str(value) == record['character_value'], 'Incorrect recorded target value')
        # Evaluate the substituted signed target directly as an additional
        # nonlocal check, independent of its individual cell checks.
        substituted = substitute_power(word * power, period)
        transformed_endpoint, transformed_value = walk(substituted, weights=weights)
        require(transformed_endpoint == 0 and transformed_value == value,
                'Invariant character failed on actual target loop')
        target_receipt.append(dict(label=label, power=power, character_index=record['character_index'],
                                   value=value, substituted_length=len(substituted)))
    require(target_receipt[0]['power'] == 2 and target_receipt[0]['value'] == 1,
            'Central a1^2 -> 1 claim failed')
    unique_words = len({tuple(word) for _, word in expected_targets})
    require(unique_words == 18, 'Wrong number of distinct target words')

    return dict(status='PASS', audit_scope='Explicit rank-five integral-cocycle claim only',
                timestamp_utc=datetime.datetime.now(datetime.timezone.utc).isoformat(),
                independent_verifier_sha256=digest(Path(__file__)),
                frozen_manifest_sha256=digest(root / 'FROZEN_INPUTS.json'),
                certificate_sha256=digest(certificate_path), frozen_inputs=frozen_receipt,
                graph_vertices=len(reached), full_action_orbit=len(all_reached),
                full_hydra_relator_checks=relator_checks,
                stable_letter_power=period, index=subgroup_index,
                identity_lift_exponents_through_16=identity_lift_exponents,
                rooted_lift_checks=rooted_lift_checks,
                theta_r_positive_word_lengths=[len(word) for word in theta_r],
                characters=len(characters), edge_cell_checks=edge_cell_checks,
                target_entries=len(target_receipt), distinct_target_words=unique_words,
                targets=target_receipt)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--certificate', type=Path,
                        default=Path(__file__).resolve().parent.parent / 'rank5_cocycle_certificate.json')
    parser.add_argument('--output', type=Path)
    parser.add_argument('--skip-manifest-check', action='store_true',
                        help='Only for adversarial synthetic copies; original input hashes still recorded.')
    args = parser.parse_args()
    result = audit(args.certificate, not args.skip_manifest_check)
    encoded = json.dumps(result, indent=2) + '\n'
    if args.output:
        args.output.write_text(encoded)
    else:
        print(encoded, end='')
